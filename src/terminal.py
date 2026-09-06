"""Interação textual, independente de serviços externos."""

import argparse
import json
from pathlib import Path

from .modelos import PRIORIDADES, TIPOS, criar_ocorrencia
from .persistencia import Repositorio

RAIZ = Path(__file__).resolve().parents[1]


def mostrar(objeto):
    print(json.dumps(objeto, ensure_ascii=False, indent=2))


def escolher(rotulo, opcoes):
    print(f"{rotulo}: {', '.join(opcoes)}")
    resposta = input("> ").strip()
    if resposta not in opcoes:
        raise ValueError("Opção inválida; use um dos valores apresentados.")
    return resposta


def perguntar_bool(rotulo):
    resposta = input(f"{rotulo}? (s/n): ").strip().lower()
    if resposta not in ("s", "n"):
        raise ValueError("Responda s ou n.")
    return resposta == "s"


def cadastrar(repo):
    tipo = escolher("Tipo", TIPOS)
    modulo = input("Módulo de origem: ")
    descricao = input("Descrição (use dados fictícios): ")
    prioridade = escolher("Prioridade", PRIORIDADES)
    sinais = {campo: perguntar_bool(campo) for campo in TIPOS[tipo]}
    registro = repo.cadastrar(criar_ocorrencia(tipo, modulo, descricao, prioridade, sinais))
    print(f"Cadastrado: {registro['id']}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="NCAS - central de ocorrências da Aurora Siger")
    parser.add_argument("--data-dir", type=Path, default=RAIZ / "runtime",
                        help="pasta de dados persistentes (padrão: runtime junto ao programa)")
    args = parser.parse_args(argv)
    repo = Repositorio(args.data_dir)
    print("NCAS | Aurora Siger | Protótipo acadêmico")
    print(f"Dados: {repo.pasta}")
    while True:
        try:
            print("\n1 Cadastrar | 2 Listar | 0 Sair")
            opcao = input("> ").strip()
            if opcao == "0":
                print("Sessão encerrada. Dados preservados.")
                return 0
            if opcao == "1":
                cadastrar(repo)
            elif opcao == "2":
                mostrar(repo.listar())
            else:
                print("Opção inválida.")
        except (ValueError, OSError) as exc:
            print(f"Não foi possível concluir: {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\nSessão encerrada. Dados já gravados foram preservados.")
            return 0
