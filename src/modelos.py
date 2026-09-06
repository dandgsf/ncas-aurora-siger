"""Contratos de entrada: rejeitam dados ambíguos antes da persistência."""

from datetime import datetime
import re
from uuid import uuid4

TIPOS = {"alerta_operacional": ("falha", "critico"),
         "solicitacao_tripulacao": ("urgente", "setor_essencial"),
         "evento_energetico": ("falha", "consumo_elevado")}
PRIORIDADES = ("baixa", "media", "alta", "critica")
STATUS = ("aberta", "em_analise", "resolvida")
CAMPOS = {"id", "tipo", "modulo_origem", "descricao", "prioridade", "status",
          "data_hora", "condicoes_operacionais"}


def texto(valor, campo, limite=500):
    if not isinstance(valor, str) or not valor.strip() or len(valor) > limite:
        raise ValueError(f"{campo}: informe um texto de 1 a {limite} caracteres.")
    if any(ord(c) < 32 or ord(c) == 127 for c in valor):
        raise ValueError(f"{campo}: caracteres de controle não são permitidos.")
    if re.search(r"sk-[A-Za-z0-9_-]{12,}", valor):
        raise ValueError(f"{campo}: não insira credenciais nos registros.")
    return valor.strip()


def validar_ocorrencia(registro):
    if not isinstance(registro, dict) or set(registro) != CAMPOS:
        raise ValueError("Ocorrência com campos ausentes ou desconhecidos.")
    for campo in ("id", "tipo", "modulo_origem", "descricao", "prioridade", "status", "data_hora"):
        texto(registro[campo], campo)
    texto(registro["modulo_origem"], "módulo", 80)
    if registro["tipo"] not in TIPOS:
        raise ValueError("Tipo de ocorrência inválido.")
    if registro["prioridade"] not in PRIORIDADES or registro["status"] not in STATUS:
        raise ValueError("Prioridade ou status inválido.")
    validar_instante(registro["data_hora"])
    sinais = registro["condicoes_operacionais"]
    if not isinstance(sinais, dict) or set(sinais) != set(TIPOS[registro["tipo"]]):
        raise ValueError("Informe exatamente as condições do tipo selecionado.")
    if any(type(v) is not bool for v in sinais.values()):
        raise ValueError("Condições devem ser booleanas, não números ou textos.")
    return registro


def validar_instante(valor):
    texto(valor, "data")
    try:
        instante = datetime.fromisoformat(valor)
    except ValueError as exc:
        raise ValueError("Data deve estar em ISO 8601.") from exc
    if instante.utcoffset() is None:
        raise ValueError("Data deve informar o fuso horário.")
    return instante


def criar_ocorrencia(tipo, modulo, descricao, prioridade, condicoes):
    return validar_ocorrencia({
        "id": "OCR-" + uuid4().hex[:12],
        "tipo": texto(tipo, "tipo"),
        "modulo_origem": texto(modulo, "módulo", 80),
        "descricao": texto(descricao, "descrição"),
        "prioridade": texto(prioridade, "prioridade"),
        "status": "aberta",
        "data_hora": datetime.now().astimezone().isoformat(timespec="seconds"),
        "condicoes_operacionais": dict(condicoes),
    })
