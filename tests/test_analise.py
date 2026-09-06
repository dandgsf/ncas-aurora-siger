import copy
import json
import tempfile
import unittest

from src.analise import (ESTRATEGIAS, analisar, avaliar_alerta, construir_prompt,
                        tabela_verdade, validar_analise)
from src.persistencia import Repositorio
from test_persistencia import exemplo


class AnaliseTest(unittest.TestCase):
    def test_status_fabricado_e_historico_malformado_sao_rejeitados(self):
        with tempfile.TemporaryDirectory() as pasta:
            repo = Repositorio(pasta)
            registro = repo.cadastrar(exemplo())
            repo.analisar(registro["id"])
            original = repo.carregar()
            for campo, valor in (("data_hora", "ontem"), ("resposta", {"ocorrencia_id": []})):
                base = copy.deepcopy(original)
                base["analises"][0][campo] = valor
                repo.json.write_text(json.dumps(base), encoding="utf-8")
                with self.subTest(campo=campo), self.assertRaises(ValueError):
                    repo.carregar()
            for status in ("aberta", "resolvida"):
                base = copy.deepcopy(original)
                base["ocorrencias"][0]["status"] = status
                repo.json.write_text(json.dumps(base), encoding="utf-8")
                with self.subTest(status=status), self.assertRaises(ValueError):
                    repo.carregar()

    def test_quatro_combinacoes_equivalentes(self):
        linhas = tabela_verdade()
        self.assertEqual(len(linhas), 4)
        for linha in linhas:
            self.assertEqual(linha["original"], linha["simplificada"])
            self.assertEqual(linha["simplificada"], linha["falha"])

    def test_regra_rejeita_booleanos_ambiguos(self):
        for valor in (1, "false", None):
            with self.assertRaises(ValueError):
                avaliar_alerta(valor, True)

    def test_resultado_deterministico_e_sem_mutacao_da_entrada(self):
        registro = exemplo()
        anterior = copy.deepcopy(registro)
        self.assertEqual(analisar(registro), analisar(registro))
        self.assertEqual(registro, anterior)
        self.assertIs(analisar(registro)["necessita_revisao_humana"], True)
        self.assertEqual(analisar(registro)["modo_execucao"], "fallback_local")

    def test_tres_prompts_distintos_e_dois_exemplos_few_shot(self):
        registro = exemplo()
        prompts = [construir_prompt(registro, e) for e in ESTRATEGIAS]
        self.assertEqual(len(set(prompts)), 3)
        self.assertNotIn("Exemplo de entrada:", prompts[0])
        self.assertEqual(prompts[1].count("Exemplo de entrada:"), 2)
        for prompt in prompts:
            self.assertIn(registro["id"], prompt)
            self.assertIn("necessita_revisao_humana=true", prompt)
        with self.assertRaises(ValueError):
            construir_prompt(registro, "desconhecido")

    def test_contrato_rejeita_contradicoes_e_campos_invalidos(self):
        registro = exemplo()
        resposta = analisar(registro)
        for alteracao in ({"necessita_revisao_humana": False}, {"ocorrencia_id": "outra"},
                          {"classificacao": "sem_alerta_por_falha"}, {"fatos_confirmados": []},
                          {"modelo": "modelo-inexistente"}, {"extra": True}):
            with self.subTest(alteracao=alteracao), self.assertRaises(ValueError):
                validar_analise(resposta | alteracao, registro)

    def test_analise_e_revisao_persistem_com_confirmacao(self):
        with tempfile.TemporaryDirectory() as pasta:
            repo = Repositorio(pasta)
            registro = repo.cadastrar(exemplo())
            with self.assertRaises(ValueError):
                repo.revisar(registro["id"], "CONFIRMAR", "Verificação concluída.")
            item = repo.analisar(registro["id"])
            self.assertEqual(repo.obter(registro["id"])["status"], "em_analise")
            self.assertEqual(Repositorio(pasta).carregar()["analises"], [item])
            with self.assertRaises(ValueError):
                repo.revisar(registro["id"], "nao", "Não resolvido.")
            self.assertEqual(repo.obter(registro["id"])["status"], "em_analise")
            repo.revisar(registro["id"], "CONFIRMAR", "Verificação fictícia concluída.")
            self.assertEqual(Repositorio(pasta).obter(registro["id"])["status"], "resolvida")
            self.assertIs(repo.carregar()["analises"][0]["resposta"]["necessita_revisao_humana"], True)
            with self.assertRaises(ValueError):
                repo.analisar(registro["id"])

    def test_historico_corrompido_nao_e_sobrescrito(self):
        with tempfile.TemporaryDirectory() as pasta:
            repo = Repositorio(pasta)
            registro = repo.cadastrar(exemplo())
            repo.analisar(registro["id"])
            base = repo.carregar()
            base["analises"][0]["resposta"]["ocorrencia_id"] = "orfao"
            repo.json.write_text(json.dumps(base), encoding="utf-8")
            original = repo.json.read_bytes()
            with self.assertRaises(ValueError):
                repo.cadastrar(exemplo())
            self.assertEqual(repo.json.read_bytes(), original)
