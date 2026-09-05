# NCAS: escopo de implementação

O Núcleo Cognitivo da Aurora Siger organiza ocorrências de uma colônia fictícia
e apoia a revisão de especialistas. A aplicação funciona em terminal com Python
3.10 ou superior e sua biblioteca padrão. Os dados de demonstração são fictícios.

## Origem e independência

Projeto acadêmico da Fase 5 de Ciência da Computação. Referência: FIAP,
Capítulo 1, *Inteligência Artificial no Comando*, seções 5 a 7, páginas físicas
10 a 19. Este documento é uma síntese autoral de requisitos e decisões técnicas.
O material didático original não integra este repositório.

Este Git possui histórico próprio, sem submódulos, caminhos para outro projeto,
serviços compartilhados, banco externo ou infraestrutura de hospedagem.
Execução, testes e documentação partem da raiz deste projeto. A criação do
repositório remoto, sua visibilidade e publicação constituem uma etapa posterior.

## Requisitos acadêmicos

- Cadastro e consulta com persistência em JSON e registros incrementais em TXT.
- Uma regra booleana implementada, simplificada e demonstrada por equivalência.
- Exemplos zero-shot, few-shot e saída estruturada, com simulação de assistente.
- Menu no terminal, código organizado e execução demonstrável.
- Explicação de memória, armazenamento, fluxo de dados, melhoria de respostas,
  diversidade, vieses e responsabilidade humana.
- Pacote final: `codigo_fonte.py`, `dados_colonia.json`, `registros_colonia.txt`,
  `regras_logicas.pdf`, `prompts_utilizados.pdf` e `link_video.txt`.
- Vídeo de até cinco minutos no YouTube como Não listado; a gravação e a
  submissão pertencem ao gate 6, fora desta implementação.

## Decisões do produto

Fluxo: cadastrar, validar, persistir, consultar, avaliar regras, mostrar prompt,
simular análise e registrar revisão humana. O fluxo principal é
`alerta_operacional`; `solicitacao_tripulacao` e `evento_energetico` são extensões
da equipe. Um registro só é resolvido por confirmação explícita do operador.

JSON é a fonte estruturada: versão do formato, ocorrências e análises.
TXT oferece uma trilha cronológica de eventos, acrescentada sem apagar o passado.
O protótipo é local, sem identidade autenticada: a confirmação humana é uma
ação registrada, não uma assinatura digital nem autorização para atuar fisicamente.

A simulação é determinística e utiliza regras e textos predefinidos. Os prompts
são apresentados como material didático; não se afirma que o simulador seja um
LLM ou que execute inferência generativa. Uma API real é opcional para a atividade
e depende de decisão de configuração específica. O funcionamento local é completo.

Não fazem parte desta fase: interface web, autenticação, banco de dados,
treinamento de modelo, controle de equipamentos ou decisões críticas autônomas.

## Gates e evidências

| Gate | Resultado esperado | Evidência |
|---|---|---|
| 2 | Cadastro, validação, consulta e recuperação após reinício | Testes de persistência e terminal |
| 3 | Regra, tabela-verdade, prompts, análise local e revisão | Testes de lógica e análise |
| 4 | Três tipos com condições próprias e mesmos contratos | Testes das extensões |
| 5 | Testes integrados, dois PDFs e instruções executáveis | Testes, PDFs e README |

## Rubrica e cobertura

| Critério | Pontos | Evidência planejada |
|---|---:|---|
| Integração das disciplinas | 2,0 | Fluxo completo e explicação técnica |
| Arquivos e JSON | 2,0 | Cadastro, recuperação e trilha TXT |
| Lógica booleana | 1,5 | Implementação, PDF e quatro combinações |
| Prompts e LLMs | 2,0 | Prompts, saída estruturada e limites da simulação |
| Organização | 1,5 | Menu, módulos, testes e README |
| Ética e responsabilidade | 1,0 | Revisão humana e reflexão contextualizada |

Os testes demonstram comportamento técnico; não substituem a avaliação acadêmica
nem a apresentação. Autoria dos integrantes, divisão de responsabilidades, vídeo,
conferência do prazo no portal e submissão permanecem pendências da equipe.
