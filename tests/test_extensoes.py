from pathlib import Path
import tempfile
import unittest

from src.analise import analisar
from src.modelos import TIPOS, criar_ocorrencia
from src.persistencia import Repositorio

RAIZ = Path(__file__).resolve().parents[1]


class ExtensoesTest(unittest.TestCase):
    def test_todas_combinacoes_das_extensoes(self):
        for tipo, resultado_positivo, resultado_negativo in (
            ("solicitacao_tripulacao", "atendimento_prioritario", "atendimento_regular"),
            ("evento_energetico", "atencao_energetica", "sem_alerta_energetico"),
        ):
            for a in (False, True):
                for b in (False, True):
                    with self.subTest(tipo=tipo, a=a, b=b):
                        registro = criar_ocorrencia(tipo, "modulo", "Evento fictício.", "media",
                                                    dict(zip(TIPOS[tipo], (a, b))))
                        ativo = a and b if tipo == "solicitacao_tripulacao" else a or b
                        self.assertEqual(analisar(registro)["classificacao"],
                                         resultado_positivo if ativo else resultado_negativo)

    def test_tres_tipos_completam_cadastro_analise_e_revisao(self):
        with tempfile.TemporaryDirectory() as pasta:
            repo = Repositorio(pasta)
            for registro in Repositorio(RAIZ).listar():
                repo.cadastrar(registro)
                repo.analisar(registro["id"], "few-shot")
                repo.revisar(registro["id"], "CONFIRMAR", "Verificação simulada concluída.")
            self.assertEqual(len(repo.listar(status="resolvida")), 3)
            self.assertEqual(len(Repositorio(pasta).carregar()["analises"]), 3)

    def test_sinais_de_outro_tipo_sao_rejeitados(self):
        with self.assertRaises(ValueError):
            criar_ocorrencia("evento_energetico", "energia", "Evento fictício.", "alta",
                              {"falha": True, "critico": True})

    def test_demo_idempotente_preserva_revisoes(self):
        with tempfile.TemporaryDirectory() as pasta:
            repo = Repositorio(pasta)
            amostras = Repositorio(RAIZ).carregar()
            self.assertTrue(repo.inicializar_demo(amostras))
            repo.analisar("OCR-DEMO-001")
            antes = repo.json.read_bytes()
            self.assertFalse(repo.inicializar_demo(amostras))
            self.assertEqual(repo.json.read_bytes(), antes)
            self.assertEqual(len(repo.listar()), 3)
