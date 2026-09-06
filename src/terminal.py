"""Interação textual, independente de serviços externos."""

import argparse
import json
from pathlib import Path

from .modelos import PRIORIDADES, TIPOS, criar_ocorrencia
from .persistencia import Repositorio
from .analise import ESTRATEGIAS, construir_prompt, tabela_verdade

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
            print("\n1 Cadastrar | 2 Listar | 3 Analisar | 4 Ver prompts | 5 Tabela-verdade")
            print("6 Revisar e resolver | 7 Histórico | 8 Filtrar | 0 Sair")
            opcao = input("> ").strip()
            if opcao == "0":
                print("Sessão encerrada. Dados preservados.")
                return 0
            if opcao == "1":
                cadastrar(repo)
            elif opcao == "2":
                mostrar(repo.listar())
            elif opcao == "3":
                identificador = input("ID da ocorrência: ").strip()
                estrategia = escolher("Estratégia", ESTRATEGIAS)
                print("SIMULAÇÃO LOCAL: regras e textos predefinidos, sem chamada a LLM.")
                mostrar(repo.analisar(identificador, estrategia))
            elif opcao == "4":
                ocorrencia = repo.obter(input("ID da ocorrência: ").strip())
                estrategia = escolher("Estratégia", ESTRATEGIAS)
                print(construir_prompt(ocorrencia, estrategia))
            elif opcao == "5":
                print("(FALHA AND CRITICO) OR (FALHA AND NOT CRITICO) = FALHA")
                mostrar(tabela_verdade())
            elif opcao == "6":
                identificador = input("ID da ocorrência: ").strip()
                observacao = input("Resultado da verificação humana: ")
                confirmacao = input("Digite CONFIRMAR para resolver: ").strip()
                mostrar(repo.revisar(identificador, confirmacao, observacao))
            elif opcao == "7":
                mostrar(repo.carregar()["analises"])
            elif opcao == "8":
                campo = escolher("Filtrar por", ("tipo", "prioridade", "status"))
                valor = input("Valor exato: ").strip()
                mostrar(repo.listar(**{campo: valor}))
            else:
                print("Opção inválida.")
        except (ValueError, OSError) as exc:
            print(f"Não foi possível concluir: {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\nSessão encerrada. Dados já gravados foram preservados.")
            return 0
