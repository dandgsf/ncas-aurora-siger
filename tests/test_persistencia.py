import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from src.modelos import criar_ocorrencia, validar_ocorrencia
from src.persistencia import Repositorio


def exemplo():
    return criar_ocorrencia("alerta_operacional", "suporte_de_vida", "Oscilação na ventilação.",
                            "critica", {"falha": True, "critico": True})


class PersistenciaTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Repositorio(self.temp.name)

    def test_arquivo_ausente_inicia_vazio_sem_gravar(self):
        self.assertEqual(self.repo.listar(), [])
        self.assertFalse(self.repo.json.exists())

    def test_cadastro_sobrevive_nova_instancia_e_log_append(self):
        a, b = exemplo(), exemplo()
        self.repo.cadastrar(a)
        primeira_linha = self.repo.txt.read_text(encoding="utf-8")
        self.repo.cadastrar(b)
        self.assertEqual(Repositorio(self.temp.name).listar(), [a, b])
        self.assertTrue(self.repo.txt.read_text(encoding="utf-8").startswith(primeira_linha))
        self.assertEqual(len(self.repo.txt.read_text(encoding="utf-8").splitlines()), 2)

    def test_json_corrompido_nao_e_sobrescrito(self):
        for conteudo in ("{", '{"versao": 1, "versao": 1}', '[]', '\ufeff{}'):
            with self.subTest(conteudo=conteudo):
                self.repo.json.write_text(conteudo, encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.repo.cadastrar(exemplo())
                self.assertEqual(self.repo.json.read_text(encoding="utf-8"), conteudo)

    def test_entrada_invalida_rejeitada_sem_criar_json(self):
        alteracoes = [{"prioridade": "enorme"}, {"descricao": " "}, {"tipo": "invalido"},
                      {"status": "fechada"}, {"data_hora": "2026-09-06"},
                      {"descricao": "linha\nforjada"}, {"condicoes_operacionais": {"falha": 1, "critico": True}},
                      {"condicoes_operacionais": {"falha": True}}, {"extra": "x"}]
        for alteracao in alteracoes:
            with self.subTest(alteracao=alteracao):
                registro = exemplo() | alteracao
                with self.assertRaises(ValueError):
                    self.repo.cadastrar(registro)
        self.assertFalse(self.repo.json.exists())

    def test_id_duplicado_preserva_base(self):
        registro = exemplo()
        self.repo.cadastrar(registro)
        with self.assertRaises(ValueError):
            self.repo.cadastrar(registro)
        self.assertEqual(len(self.repo.listar()), 1)

    def test_falha_de_substituicao_preserva_json_anterior(self):
        self.repo.cadastrar(exemplo())
        anterior = self.repo.json.read_bytes()
        with patch("src.persistencia.os.replace", side_effect=OSError("disco indisponível")):
            with self.assertRaises(OSError):
                self.repo.cadastrar(exemplo())
        self.assertEqual(self.repo.json.read_bytes(), anterior)
        self.assertEqual(list(Path(self.temp.name).glob("*.tmp")), [])

    def test_trava_impede_escrita_concorrente(self):
        with self.repo.bloqueio():
            with self.assertRaises(ValueError):
                self.repo.cadastrar(exemplo())
        self.assertFalse(self.repo.json.exists())

    def test_falha_no_log_informa_que_json_foi_salvo(self):
        self.repo.txt.mkdir()
        with self.assertWarnsRegex(RuntimeWarning, "Dados salvos"):
            self.repo.cadastrar(exemplo())
        self.assertEqual(len(self.repo.listar()), 1)

    def test_filtros_e_id_inexistente(self):
        self.repo.cadastrar(exemplo())
        self.assertEqual(len(self.repo.listar(prioridade="critica")), 1)
        self.assertEqual(self.repo.listar(status="resolvida"), [])
        with self.assertRaises(ValueError):
            self.repo.listar(campo="x")
        with self.assertRaises(ValueError):
            self.repo.obter("inexistente")

    def test_validacao_de_base_rejeita_ids_repetidos_e_versao(self):
        self.repo.cadastrar(exemplo())
        base = self.repo.carregar()
        for nova in (base | {"versao": True}, base | {"ocorrencias": base["ocorrencias"] * 2}):
            self.repo.json.write_text(json.dumps(nova), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.repo.carregar()

    def test_segredo_na_descricao_e_rejeitado(self):
        with self.assertRaises(ValueError):
            validar_ocorrencia(exemplo() | {"descricao": "sk-" + "z" * 20})
