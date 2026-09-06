import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from scripts.empacotar import criar_pacote, validar_video
from src.persistencia import Repositorio

RAIZ = Path(__file__).resolve().parents[1]


def executar(raiz, pasta, entradas, demo=False):
    comando = [sys.executable, "-S", str(raiz / "codigo_fonte.py"), "--data-dir", str(pasta)]
    if demo:
        comando.append("--demo")
    return subprocess.run(comando, input=entradas, text=True, encoding="utf-8",
                          capture_output=True, cwd=pasta.parent,
                          env=os.environ | {"PYTHONIOENCODING": "utf-8"}, timeout=15)


class TerminalPacoteTest(unittest.TestCase):
    def test_cadastro_e_consulta_em_processos_separados(self):
        with tempfile.TemporaryDirectory() as pasta:
            dados = Path(pasta) / "sessão com espaços"
            primeiro = executar(RAIZ, dados,
                "1\nalerta_operacional\nventilacao\nOscilacao ficticia.\nalta\ns\nn\n0\n")
            self.assertEqual(primeiro.returncode, 0, primeiro.stderr)
            self.assertIn("Cadastrado:", primeiro.stdout)
            segundo = executar(RAIZ, dados, "2\n0\n")
            self.assertIn("Oscilacao ficticia.", segundo.stdout)
            self.assertEqual(len(Repositorio(dados).listar()), 1)

    def test_menu_completo_demo_e_revisao(self):
        with tempfile.TemporaryDirectory() as pasta:
            dados = Path(pasta) / "dados"
            roteiro = ("5\n4\nOCR-DEMO-001\nfew-shot\n3\nOCR-DEMO-001\nestruturado\n"
                       "6\nOCR-DEMO-001\nVerificacao ficticia.\nCONFIRMAR\n7\n8\nstatus\nresolvida\n0\n")
            resultado = executar(RAIZ, dados, roteiro, demo=True)
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertNotIn("Não foi possível", resultado.stdout)
            self.assertIn("SIMULAÇÃO LOCAL", resultado.stdout)
            self.assertEqual(Repositorio(dados).obter("OCR-DEMO-001")["status"], "resolvida")

    def test_eof_e_entrada_invalida_encerram_sem_traceback(self):
        with tempfile.TemporaryDirectory() as pasta:
            resultado = executar(RAIZ, Path(pasta) / "dados", "invalido\n1\ntipo_inexistente\n")
            self.assertEqual(resultado.returncode, 0)
            self.assertNotIn("Traceback", resultado.stderr)
            self.assertIn("Opção inválida", resultado.stdout)

    def test_demo_recusa_json_corrompido(self):
        with tempfile.TemporaryDirectory() as pasta:
            dados = Path(pasta) / "dados"
            dados.mkdir()
            arquivo = dados / "dados_colonia.json"
            arquivo.write_text("{", encoding="utf-8")
            resultado = executar(RAIZ, dados, "0\n", demo=True)
            self.assertEqual(resultado.returncode, 1)
            self.assertEqual(arquivo.read_text(encoding="utf-8"), "{")

    def test_zip_extraido_executa_sem_dependencias_externas(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            pacote = criar_pacote(raiz / "teste.zip")
            destino = raiz / "projeto extraído"
            with zipfile.ZipFile(pacote) as arquivo:
                nomes = arquivo.namelist()
                self.assertNotIn("link_video.txt", nomes)
                self.assertFalse(any(n.startswith((".git/", "runtime/", "tmp/")) for n in nomes))
                self.assertFalse(any(Path(n).name.startswith(".env") for n in nomes))
                arquivo.extractall(destino)
            resultado = executar(destino, raiz / "dados", "2\n3\nOCR-DEMO-002\nzero-shot\n0\n", demo=True)
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertIn("atendimento_prioritario", resultado.stdout)
            self.assertNotIn("Não foi possível", resultado.stdout)

    def test_url_final_validada_sem_acesso_remoto(self):
        # ID fictício apenas para validar sintaxe; nunca publicado como vídeo real.
        valido = "https://youtu.be/abcdefghijk"
        self.assertEqual(validar_video(valido), valido)
        for invalido in ("", "http://youtu.be/abcdefghijk", "https://evil.test/abcdefghijk",
                         "https://youtube.com.evil.test/watch?v=abcdefghijk", "https://youtu.be/curto"):
            with self.subTest(url=invalido), self.assertRaises(ValueError):
                validar_video(invalido)
        with tempfile.TemporaryDirectory() as pasta:
            pacote = criar_pacote(Path(pasta) / "entrega.zip", valido)
            with zipfile.ZipFile(pacote) as arquivo:
                self.assertEqual(arquivo.read("link_video.txt").decode().strip(), valido)

    def test_pacote_nao_sobrescreve_fonte(self):
        with self.assertRaises(ValueError):
            criar_pacote(RAIZ / "codigo_fonte.py")
