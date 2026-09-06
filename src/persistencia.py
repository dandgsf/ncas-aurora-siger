"""JSON é a fonte de verdade; TXT é a trilha auxiliar em append."""

from contextlib import contextmanager
from datetime import datetime
import json
import os
from pathlib import Path
import tempfile
import warnings

from .modelos import texto, validar_ocorrencia
from .analise import ESTRATEGIAS, analisar, construir_prompt, validar_analise
from uuid import uuid4


def vazio():
    return {"versao": 1, "ocorrencias": [], "analises": []}


def pares_unicos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError("JSON contém chaves repetidas.")
        objeto[chave] = valor
    return objeto


def validar_base(base):
    if not isinstance(base, dict) or set(base) != {"versao", "ocorrencias", "analises"}:
        raise ValueError("Estrutura do arquivo de dados inválida.")
    if type(base["versao"]) is not int or base["versao"] != 1:
        raise ValueError("Versão do arquivo de dados não suportada.")
    if not isinstance(base["ocorrencias"], list) or not isinstance(base["analises"], list):
        raise ValueError("Ocorrências e análises devem ser listas.")
    ids = set()
    for registro in base["ocorrencias"]:
        validar_ocorrencia(registro)
        if registro["id"] in ids:
            raise ValueError("Identificador de ocorrência duplicado.")
        ids.add(registro["id"])
    ocorrencias = {o["id"]: o for o in base["ocorrencias"]}
    analise_ids = set()
    for item in base["analises"]:
        campos = {"id", "data_hora", "estrategia", "prompt", "resposta", "revisao"}
        if not isinstance(item, dict) or set(item) != campos:
            raise ValueError("Histórico de análise inválido.")
        for campo in ("id", "data_hora", "prompt"):
            if not isinstance(item[campo], str) or not item[campo].strip():
                raise ValueError("Histórico com campos vazios.")
        if item["id"] in analise_ids or item["estrategia"] not in ESTRATEGIAS:
            raise ValueError("Análise repetida ou estratégia desconhecida.")
        analise_ids.add(item["id"])
        resposta = item["resposta"]
        if not isinstance(resposta, dict) or resposta.get("ocorrencia_id") not in ocorrencias:
            raise ValueError("Análise órfã.")
        validar_analise(resposta, ocorrencias[resposta["ocorrencia_id"]])
        if item["revisao"] is not None:
            revisao = item["revisao"]
            if not isinstance(revisao, dict) or set(revisao) != {"data_hora", "observacao", "decisao"}:
                raise ValueError("Revisão inválida.")
            texto(revisao["observacao"], "observação")
            texto(revisao["data_hora"], "data")
            if revisao["decisao"] != "resolvida":
                raise ValueError("Decisão de revisão inválida.")
    return base


class Repositorio:
    def __init__(self, pasta):
        self.pasta = Path(pasta).resolve()
        self.json = self.pasta / "dados_colonia.json"
        self.txt = self.pasta / "registros_colonia.txt"

    def carregar(self):
        if not self.json.exists():
            return vazio()
        try:
            with self.json.open(encoding="utf-8") as arquivo:
                return validar_base(json.load(arquivo, object_pairs_hook=pares_unicos))
        except (ValueError, UnicodeError) as exc:
            raise ValueError("Dados inválidos: arquivo preservado. Corrija ou restaure uma cópia.") from exc

    @contextmanager
    def bloqueio(self):
        self.pasta.mkdir(parents=True, exist_ok=True)
        trava = self.pasta / ".ncas.lock"
        try:
            arquivo = trava.open("x", encoding="utf-8")
        except FileExistsError as exc:
            raise ValueError("Outra gravação está em curso. Confira a trava .ncas.lock.") from exc
        try:
            with arquivo:
                arquivo.write(str(os.getpid()))
            yield
        finally:
            trava.unlink()

    def _salvar(self, base):
        validar_base(base)
        temporario = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.pasta,
                                             suffix=".tmp", delete=False) as arquivo:
                temporario = Path(arquivo.name)
                json.dump(base, arquivo, ensure_ascii=False, indent=2, allow_nan=False)
                arquivo.write("\n")
                arquivo.flush()
                os.fsync(arquivo.fileno())
            os.replace(temporario, self.json)
        finally:
            if temporario is not None and temporario.exists():
                temporario.unlink()

    def _log(self, evento, ocorrencia_id):
        registro = {"data_hora": datetime.now().astimezone().isoformat(timespec="seconds"),
                    "evento": evento, "ocorrencia_id": ocorrencia_id}
        try:
            with self.txt.open("a", encoding="utf-8") as arquivo:
                arquivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
        except OSError:
            warnings.warn("Dados salvos em JSON, mas o log TXT falhou. Não repita o cadastro; confira permissões.",
                          RuntimeWarning, stacklevel=2)

    def cadastrar(self, registro):
        validar_ocorrencia(registro)
        if registro["status"] != "aberta":
            raise ValueError("Uma nova ocorrência deve iniciar aberta.")
        with self.bloqueio():
            base = self.carregar()
            if any(o["id"] == registro["id"] for o in base["ocorrencias"]):
                raise ValueError("Identificador já cadastrado.")
            base["ocorrencias"].append(registro)
            self._salvar(base)
            self._log("cadastro", registro["id"])
        return registro

    def inicializar_demo(self, base):
        validar_base(base)
        with self.bloqueio():
            if self.json.exists():
                self.carregar()  # Confere integridade, sem substituir dados existentes.
                return False
            self._salvar(base)
            for ocorrencia in base["ocorrencias"]:
                self._log("exemplo_ficticio", ocorrencia["id"])
        return True

    def listar(self, **filtros):
        if set(filtros) - {"tipo", "prioridade", "status"}:
            raise ValueError("Filtro desconhecido.")
        return [o for o in self.carregar()["ocorrencias"]
                if all(o[campo] == valor for campo, valor in filtros.items() if valor)]

    def obter(self, identificador):
        for registro in self.listar():
            if registro["id"] == identificador:
                return registro
        raise ValueError("Ocorrência não encontrada.")

    def analisar(self, identificador, estrategia="estruturado"):
        with self.bloqueio():
            base = self.carregar()
            ocorrencia = next((o for o in base["ocorrencias"] if o["id"] == identificador), None)
            if ocorrencia is None:
                raise ValueError("Ocorrência não encontrada.")
            if ocorrencia["status"] == "resolvida":
                raise ValueError("Ocorrência resolvida; cadastre uma nova ocorrência se necessário.")
            item = {"id": "ANA-" + uuid4().hex[:12],
                    "data_hora": datetime.now().astimezone().isoformat(timespec="seconds"),
                    "estrategia": estrategia,
                    "prompt": construir_prompt(ocorrencia, estrategia),
                    "resposta": analisar(ocorrencia), "revisao": None}
            base["analises"].append(item)
            ocorrencia["status"] = "em_analise"
            self._salvar(base)
            self._log("analise:fallback_local", identificador)
        return item

    def revisar(self, identificador, confirmacao, observacao):
        if confirmacao != "CONFIRMAR":
            raise ValueError("Revisão cancelada: é necessário digitar CONFIRMAR.")
        observacao = texto(observacao, "observação")
        with self.bloqueio():
            base = self.carregar()
            ocorrencia = next((o for o in base["ocorrencias"] if o["id"] == identificador), None)
            historico = [a for a in base["analises"] if a["resposta"]["ocorrencia_id"] == identificador]
            if ocorrencia is None or ocorrencia["status"] != "em_analise" or not historico:
                raise ValueError("A revisão exige uma ocorrência em análise e uma análise registrada.")
            historico[-1]["revisao"] = {
                "data_hora": datetime.now().astimezone().isoformat(timespec="seconds"),
                "observacao": observacao, "decisao": "resolvida"}
            ocorrencia["status"] = "resolvida"
            self._salvar(base)
            self._log("revisao_humana:resolvida", identificador)
        return ocorrencia
