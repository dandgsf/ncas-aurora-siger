"""JSON é a fonte de verdade; TXT é a trilha auxiliar em append."""

from contextlib import contextmanager
from datetime import datetime
import json
import os
from pathlib import Path
import tempfile
import warnings

from .modelos import validar_ocorrencia


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
