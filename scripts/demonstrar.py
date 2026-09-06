"""Demonstra o ciclo completo em diretório temporário, sem alterar runtime."""

from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.analise import tabela_verdade
from src.persistencia import Repositorio
from src.terminal import RAIZ, mostrar


def main():
    with tempfile.TemporaryDirectory(prefix="ncas-demo-") as pasta:
        repo = Repositorio(pasta)
        repo.inicializar_demo(Repositorio(RAIZ).carregar())
        print("1. TRÊS OCORRÊNCIAS FICTÍCIAS")
        mostrar(repo.listar())
        print("2. EQUIVALÊNCIA DA REGRA")
        mostrar(tabela_verdade())
        print("3. ANÁLISE LOCAL E REVISÃO SIMULADA")
        for ocorrencia in repo.listar():
            item = repo.analisar(ocorrencia["id"])
            mostrar(item["resposta"])
            repo.revisar(ocorrencia["id"], "CONFIRMAR", "Revisão fictícia do roteiro automatizado.")
        print("4. RECUPERAÇÃO EM NOVA INSTÂNCIA")
        mostrar(Repositorio(pasta).listar(status="resolvida"))
        assert len(Repositorio(pasta).listar(status="resolvida")) == 3
        print("DEMONSTRAÇÃO CONCLUÍDA: dados de uso preservados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
