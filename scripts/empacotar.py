"""Cria pacote por lista explícita, sem dados de uso, segredos ou histórico Git."""

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, urlparse
import zipfile

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVOS = ("codigo_fonte.py", "dados_colonia.json", "registros_colonia.txt",
            "regras_logicas.pdf", "prompts_utilizados.pdf", "README.md", "CONTRIBUTING.md",
            "requirements-docs.txt", ".gitignore", ".gitattributes")


def validar_video(url):
    partes = urlparse(url)
    if partes.scheme != "https" or partes.username or partes.password:
        raise ValueError("Informe uma URL HTTPS de vídeo no YouTube.")
    if partes.netloc in ("youtube.com", "www.youtube.com") and partes.path == "/watch":
        identificador = parse_qs(partes.query).get("v", [""])[0]
    elif partes.netloc == "youtu.be":
        identificador = partes.path.removeprefix("/")
    else:
        raise ValueError("Use youtube.com/watch?v=... ou youtu.be/...")
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", identificador):
        raise ValueError("Identificador de vídeo inválido.")
    return url


def criar_pacote(destino, video_url=None):
    if video_url is not None:
        validar_video(video_url)
    arquivos = [RAIZ / nome for nome in ARQUIVOS]
    for pasta, extensao in (("src", "*.py"), ("tests", "*.py"), ("scripts", "*.py"), ("docs", "*.md")):
        arquivos.extend(sorted((RAIZ / pasta).glob(extensao)))
    for arquivo in arquivos:
        if not arquivo.is_file() or arquivo.is_symlink() or RAIZ not in arquivo.resolve().parents:
            raise ValueError(f"Arquivo ausente ou inválido: {arquivo.name}")
        if arquivo.suffix == ".pdf" and not arquivo.read_bytes().startswith(b"%PDF-"):
            raise ValueError(f"PDF inválido: {arquivo.name}")
    destino = Path(destino)
    if destino.suffix.lower() != ".zip" or destino.is_symlink():
        raise ValueError("O destino deve ser um arquivo .zip regular.")
    if destino.resolve() in [arquivo.resolve() for arquivo in arquivos]:
        raise ValueError("O destino não pode substituir um arquivo do projeto.")
    destino.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destino, "w", compression=zipfile.ZIP_DEFLATED) as pacote:
        for arquivo in arquivos:
            pacote.write(arquivo, arquivo.relative_to(RAIZ).as_posix())
        if video_url:
            pacote.writestr("link_video.txt", video_url + "\n")
    with zipfile.ZipFile(destino) as pacote:
        if pacote.testzip() is not None:
            raise ValueError("Falha na integridade do ZIP.")
    return destino


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video-url", help="URL verdadeira; acesso e duração devem ser conferidos pela equipe")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    destino = args.output or RAIZ / "dist" / ("ncas-entrega.zip" if args.video_url else "ncas-testes.zip")
    try:
        print(criar_pacote(destino, args.video_url))
    except (OSError, ValueError) as exc:
        print(f"Não foi possível gerar o pacote: {exc}", file=sys.stderr)
        return 1
    print("Pacote gerado. " + ("Confira o vídeo antes da submissão." if args.video_url else "Versão para testes, sem vídeo."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
