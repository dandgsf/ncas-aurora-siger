"""Gera os dois documentos autorais a partir das regras e prompts implementados."""

import json
from pathlib import Path
import sys
import textwrap
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (PageBreak, Paragraph, Preformatted, SimpleDocTemplate,
                               Spacer, Table, TableStyle)

from src.analise import analisar, construir_prompt, tabela_verdade
from src.persistencia import Repositorio

RAIZ = Path(__file__).resolve().parents[1]
AZUL = colors.HexColor("#153B50")
VERDE = colors.HexColor("#087F8C")
ESTILOS = getSampleStyleSheet()
ESTILOS.add(ParagraphStyle(name="TituloNCAS", fontName="Helvetica-Bold", fontSize=24,
                          leading=29, textColor=AZUL, spaceAfter=20))
ESTILOS.add(ParagraphStyle(name="SubtituloNCAS", fontName="Helvetica-Bold", fontSize=13,
                          leading=18, textColor=VERDE, spaceBefore=13, spaceAfter=8))
ESTILOS.add(ParagraphStyle(name="CorpoNCAS", fontName="Helvetica", fontSize=10,
                          leading=15, textColor=colors.HexColor("#243746"), spaceAfter=10))
ESTILOS.add(ParagraphStyle(name="CodigoNCAS", fontName="Courier", fontSize=9,
                          leading=12, spaceAfter=10))


def p(texto):
    return Paragraph(escape(texto), ESTILOS["CorpoNCAS"])


def h(texto):
    return Paragraph(escape(texto), ESTILOS["SubtituloNCAS"])


def codigo(texto):
    linhas = []
    for linha in texto.splitlines():
        linhas.extend(textwrap.wrap(linha, width=85, break_long_words=False,
                                   break_on_hyphens=False, replace_whitespace=False) or [""])
    return Preformatted("\n".join(linhas), ESTILOS["CodigoNCAS"])


def tabela(linhas, larguras):
    resultado = Table(linhas, colWidths=larguras, repeatRows=1, hAlign="LEFT")
    resultado.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#EDF5F6"), colors.white]),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, VERDE),
    ]))
    return resultado


def pagina(canvas, doc):
    largura, altura = A4
    canvas.saveState()
    canvas.setTitle(doc.title)
    canvas.setAuthor("Equipe NCAS")
    canvas.setCreator("NCAS")
    canvas.setProducer("NCAS")
    canvas.setFillColor(AZUL)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(54, altura - 32, "NCAS / AURORA SIGER")
    canvas.setStrokeColor(VERDE)
    canvas.line(54, altura - 42, largura - 54, altura - 42)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(54, 28, "Protótipo acadêmico | Dados fictícios | Revisão humana")
    canvas.drawRightString(largura - 54, 28, str(doc.page))
    canvas.restoreState()


def construir(nome, titulo, elementos):
    destino = RAIZ / nome
    doc = SimpleDocTemplate(str(destino), pagesize=A4, leftMargin=54, rightMargin=54,
                            topMargin=62, bottomMargin=48, title=titulo,
                            author="Equipe NCAS")
    doc.build(elementos, onFirstPage=pagina, onLaterPages=pagina,
              canvasmaker=lambda *a, **k: Canvas(*a, **(k | {"invariant": 1})))
    print(destino.name)


def regras():
    linhas = [["FALHA", "CRITICO", "Original", "Simplificada", "Equivalentes"]]
    for linha in tabela_verdade():
        linhas.append([str(int(linha[k])) for k in ("falha", "critico", "original", "simplificada")] + ["Sim"])
    elementos = [Paragraph("Regras lógicas", ESTILOS["TituloNCAS"]),
        p("Demonstração da regra principal implementada no NCAS e das extensões operacionais da equipe."),
        h("1. Regra original e simplificação"),
        codigo("A = (F AND C) OR (F AND NOT C)\nA = F AND (C OR NOT C)     [distributividade]\nA = F AND TRUE             [complemento]\nA = F                     [identidade]"),
        p("F representa falha e C representa criticidade. A existência do alerta depende somente de F. "
          "Criticidade e prioridade continuam visíveis no registro, mas não alteram o resultado desta regra."),
        h("2. Verificação pelas quatro combinações"), tabela(linhas, [70, 80, 90, 100, 110]),
        Spacer(1, 16), p("As colunas original e simplificada coincidem em todas as entradas possíveis. "
          "As funções alerta_original e avaliar_alerta reproduzem essas duas formas; os testes verificam sua equivalência."),
        h("3. Exemplo operacional"),
        p("Uma falha não crítica também gera alerta: F=true, C=false produz A=true. "
          "Não registrar falha produz A=false, mas não comprova segurança do módulo. A regra depende da qualidade dos dados."),
        PageBreak(), Paragraph("Extensões e interpretação", ESTILOS["TituloNCAS"]),
        h("4. Regras adicionais do projeto"),
        codigo("PRIORIDADE_ATENDIMENTO = URGENTE AND SETOR_ESSENCIAL\nATENCAO_ENERGETICA = FALHA OR CONSUMO_ELEVADO"),
        p("Uma solicitação exige as duas condições para atendimento prioritário. Um evento energético recebe "
          "atenção quando pelo menos um sinal está ativo. As quatro combinações de cada extensão são testadas. "
          "Essas regras são escolhas da equipe, não obrigações adicionais do enunciado."),
        h("5. Relação com De Morgan"),
        codigo("NOT (F OR E) = (NOT F) AND (NOT E)"),
        p("A ausência de atenção energética equivale a não haver falha e não haver sinal de consumo elevado. "
          "O teorema troca OR por AND ao negar as duas entradas. A simplificação principal usa distributividade, "
          "complemento e identidade; De Morgan é apresentado aqui como relação complementar."),
        h("6. Memória, arquivos e responsabilidade"),
        p("O programa lê JSON do armazenamento e cria objetos em memória; avalia os sinais e grava a análise. "
          "O TXT recebe um evento por append. Encerrar o processo libera a memória, mas preserva os arquivos."),
        p("Nenhuma regra opera equipamentos. A resolução exige uma observação humana e confirmação explícita. "
          "O sistema não autentica o operador e não substitui especialistas."),
        h("Referências e evidências"),
        p("FIAP, Fase 5, Capítulo 1: Inteligência Artificial no Comando, seções 5.4, 5.6 e 7. "
          "Síntese autoral. Código: src/analise.py. Evidências: tests/test_analise.py e tests/test_extensoes.py.")]
    construir("regras_logicas.pdf", "NCAS - Regras lógicas", elementos)


def prompts():
    ocorrencia = Repositorio(RAIZ).obter("OCR-DEMO-001")
    elementos = []
    descricoes = {
        "zero-shot": "Instruções e contrato sem exemplos anteriores. O contexto delimita a tarefa e exige revisão humana.",
        "few-shot": "Dois pares completos mostram falha ausente e presente. São exemplos fictícios, não resultados de uma API.",
        "estruturado": "O contrato explicita campos, tipos e limites. O programa valida a resposta local antes de armazená-la.",
    }
    for i, estrategia in enumerate(("zero-shot", "few-shot", "estruturado")):
        if i:
            elementos.append(PageBreak())
        elementos.extend([Paragraph(f"Prompts / {estrategia}", ESTILOS["TituloNCAS"]),
                          p(descricoes[estrategia]),
                          p("Texto produzido pela função construir_prompt para OCR-DEMO-001:"),
                          codigo(construir_prompt(ocorrencia, estrategia))])
    elementos.extend([PageBreak(), Paragraph("Saída e avaliação", ESTILOS["TituloNCAS"]),
        h("Exemplo completo de resposta local"),
        codigo(json.dumps(analisar(ocorrencia), ensure_ascii=False, indent=2)),
        h("Melhoria de resposta e limites"),
        p("Avaliar quatro critérios em exemplos fixos: formato válido, classificação correta, ausência de fatos "
          "inventados e revisão humana presente. Na versão atual, a resposta vem de regras locais; mudar o prompt "
          "não altera a simulação nem demonstra ganho de um modelo generativo."),
        p("Prompts e exemplos são materiais de engenharia de prompts. Um LLM trabalha com tokens e previsão de "
          "continuações; esse processo não é executado aqui. Uma futura integração precisará validar formato, "
          "conteúdo, falhas e recusas, preservando o modo local."),
        h("Ética e evidência"),
        p("Não inferir atributos pessoais. Revisar descrições, exemplos e prioridades para reduzir vieses. "
          "Diversidade na equipe e supervisão especializada continuam necessárias. A análise não autoriza ações críticas."),
        p("Referência: FIAP, Fase 5, Capítulo 1, seções 5.5 e 5.7. "
          "Código: src/analise.py. Testes: tests/test_analise.py. Conteúdo autoral e dados fictícios.")])
    construir("prompts_utilizados.pdf", "NCAS - Prompts utilizados", elementos)


if __name__ == "__main__":
    regras()
    prompts()
