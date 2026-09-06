# NCAS - Núcleo Cognitivo da Aurora Siger

Central de ocorrências fictícias da Aurora Siger, desenvolvida como protótipo
acadêmico da Fase 5. Permite registrar alertas, solicitações da tripulação e eventos
energéticos, consultar dados, aplicar regras, apresentar prompts e registrar revisão humana.

**Versão local pronta para testes.** A análise é uma simulação determinística,
feita por regras e textos predefinidos. Não há chamadas a APIs, uso de chave,
treinamento de modelo ou controle de equipamentos.

## Executar

Requisito: Python 3.10 ou superior. O programa e os testes usam somente a biblioteca
padrão; não é necessário instalar pacotes, configurar servidor ou criar conta.

Na pasta do projeto:

```powershell
python codigo_fonte.py --demo
```

No Windows, se `python` não estiver disponível, use `py -3 codigo_fonte.py --demo`.
Para começar sem exemplos, execute `python codigo_fonte.py` em uma pasta de dados nova.

O modo `--demo` inclui três ocorrências fictícias na primeira execução. Os dados
de uso ficam em `runtime/dados_colonia.json` e `runtime/registros_colonia.txt`.
Fechar e reabrir preserva os registros. Repetir `--demo` não apaga nem duplica dados.
Os arquivos de mesmo nome na raiz são exemplos distribuídos, mantidos intactos.

Para uma sessão separada, use uma pasta ainda não utilizada:

```powershell
python codigo_fonte.py --demo --data-dir runtime/meu-teste-01
```

## Primeiro teste manual

1. Escolha **2** para listar `OCR-DEMO-001`, `OCR-DEMO-002` e `OCR-DEMO-003`.
2. Escolha **5** e confira as quatro linhas da tabela-verdade.
3. Escolha **4**, informe `OCR-DEMO-001` e `few-shot` para ver dois exemplos completos.
4. Escolha **3**, informe `OCR-DEMO-001` e `estruturado`. Confira a resposta com
   `modo_execucao: fallback_local` e `necessita_revisao_humana: true`.
5. Escolha **6**, informe o mesmo ID, descreva a verificação fictícia e digite
   `CONFIRMAR`. Essa ação registra a revisão e muda o status para `resolvida`.
6. Saia com **0**, execute novamente e confirme o status pela opção **2** e o histórico pela **7**.
7. Experimente cadastrar pela opção **1**, informar prioridade inválida e filtrar pela **8**.

As estratégias aceitas são `zero-shot`, `few-shot` e `estruturado`. Use os nomes
exatamente como apresentados. Uma ocorrência resolvida não é reaberta; crie outro
registro para um novo evento. Cancelar a confirmação mantém o status anterior.

## Testes automatizados e demonstração guiada

```powershell
python -m unittest discover -s tests -v
python scripts/demonstrar.py
```

O segundo comando executa uma demonstração automatizada em pasta temporária:
carrega os três exemplos, mostra a tabela-verdade, analisa, revisa e relê os dados.
Não grava vídeo nem altera seus registros de uso. O material para gravação humana
está em [docs/roteiro-gravacao.md](docs/roteiro-gravacao.md).

## Documentação e pacote

- [Escopo e rubrica](docs/escopo.md).
- [Arquitetura, limites e responsabilidade](docs/arquitetura.md).
- [Relatório dos gates e motivos das branches](docs/relatorio-gates.md).
- [Preparação para GitHub](docs/publicacao.md).
- [Regras lógicas](regras_logicas.pdf) e [prompts utilizados](prompts_utilizados.pdf).

```powershell
python scripts/empacotar.py
```

Gera `dist/ncas-testes.zip` com código, exemplos, testes, documentação e PDFs.
O pacote exclui Git, credenciais, dados de uso e material didático de terceiros.
Extraia em uma pasta nova e execute `python codigo_fonte.py --demo`.

O pacote de testes não é a entrega acadêmica final: falta o vídeo. Após gravá-lo,
execute o empacotador com `--video-url` seguido da URL real do YouTube para gerar
`dist/ncas-entrega.zip`, incluindo `link_video.txt`. O script confere apenas o
formato da URL; a equipe precisa verificar acesso, duração e publicação Não listada.

Para regenerar os PDFs, instale as dependências opcionais de documentação:

```powershell
python -m pip install -r requirements-docs.txt
python scripts/gerar_pdfs.py
```

Isso não é necessário para executar ou testar a aplicação: os PDFs já acompanham o projeto.

## Problemas comuns

- **JSON inválido:** o programa preserva o arquivo. Corrija uma cópia ou restaure um backup;
  para testar sem interferir nele, use outra pasta em `--data-dir`.
- **Trava `.ncas.lock`:** uma gravação pode estar em andamento. Se houve encerramento abrupto,
  confirme que não há processo do NCAS usando a pasta antes de remover somente essa trava.
- **Falha no TXT:** um aviso informa que o JSON foi salvo. Não repita o cadastro;
  confira permissões e espaço. JSON e TXT não constituem uma transação conjunta.
- **Acentos no terminal:** use um terminal UTF-8, como Windows Terminal. Os arquivos são UTF-8.

## Pendências externas

Gravação e submissão do vídeo, definição dos integrantes e da licença de distribuição,
criação/publicação do repositório remoto e eventual integração real com API.
Nenhuma dessas etapas é necessária para testar esta versão local.
