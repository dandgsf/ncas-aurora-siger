# Gravação da demonstração - até cinco minutos

## Preparação

Execute os testes e ensaie `python scripts/demonstrar.py`. Para gravar o menu real,
abra um terminal limpo, aumente a fonte para leitura confortável e use uma pasta
nova: `python codigo_fonte.py --demo --data-dir runtime/gravacao-01`.
Em outra tentativa, troque o sufixo da pasta. Não apague seus dados de teste.

Capture somente a janela do terminal e, quando necessário, os PDFs. Feche janelas
com dados pessoais; desative notificações; teste voz e áudio em um trecho curto.
Os registros são fictícios. Não mostre configurações de ambiente ou credenciais.
O script de demonstração não grava tela; use seu gravador habitual.

## Roteiro com ações e falas sugeridas

| Tempo | Ação visível | Fala sugerida |
|---|---|---|
| 00:00-00:25 | Mostrar título e menu | O NCAS organiza ocorrências da Aurora Siger e apoia especialistas. Esta versão usa Python e simulação local, com revisão humana. |
| 00:25-01:10 | Opção 1: cadastrar alerta; depois opção 2 | Registramos módulo, descrição, prioridade e sinais booleanos. O JSON guarda a estrutura e o TXT recebe o evento sem apagar o histórico. |
| 01:10-01:40 | Sair com 0, reabrir o mesmo comando e listar | Os dados continuam disponíveis após encerrar o programa. A leitura reconstrói os objetos em memória a partir do armazenamento. |
| 01:40-02:20 | Opção 5 e PDF de regras | Fatoramos a falha. Crítico ou não crítico é verdadeiro; por isso a expressão se reduz a falha. As quatro combinações confirmam a equivalência. |
| 02:20-03:15 | Opção 4: zero-shot e few-shot de OCR-DEMO-001 | Zero-shot fornece instruções; few-shot inclui dois pares de exemplo. Pedimos fatos, recomendações e pendências separados, sem inventar medições. |
| 03:15-03:55 | Opção 3, OCR-DEMO-001, estruturado; opção 7 | A análise retorna campos definidos e registra modo local. Não há chamada a LLM: regras e textos predefinidos simulam a resposta. |
| 03:55-04:25 | Opção 6: revisar OCR-DEMO-001 | Resolver exige observação e confirmação explícita. A recomendação não atua sobre equipamentos. Uma futura comparação de prompts mediria formato, classificação, fatos e revisão. |
| 04:25-04:50 | Mostrar registros de tripulação e energia | Os outros tipos reutilizam o fluxo. Priorização e descrições podem incorporar vieses; diversidade na equipe e revisão especializada são necessárias. |
| 04:50-05:00 | Encerrar | Demonstramos persistência, lógica, prompts e responsabilidade humana. O projeto acompanha testes e instruções reproduzíveis. |

Cadastro ensaiado: tipo `alerta_operacional`, módulo `ventilacao`, descrição
`Oscilacao ficticia na ventilacao.`, prioridade `alta`, falha `s`, critico `n`.
Use o ID exibido se quiser analisar o novo cadastro. Os IDs `OCR-DEMO-001` a `003`
são estáveis e facilitam a gravação. Na revisão, use `Verificacao ficticia concluida.`
e confirme com `CONFIRMAR`.

## Conferência antes da submissão

Confira duração de até cinco minutos, legibilidade, volume de voz, nomes dos
integrantes e cobertura do roteiro. Publique como Não listado, teste o link sem
depender da sessão de edição e gere o ZIP final com a URL verdadeira.
Não apresente simulação como integração real, nem testes aprovados como garantia
de nota. A data de entrega deve ser confirmada no ambiente acadêmico.
