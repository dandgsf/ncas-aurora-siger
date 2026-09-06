# Preparação do repositório no GitHub

O projeto tem Git independente e branches locais por marco funcional. Não depende
de submódulos, servidores ou arquivos externos. Publicação remota não foi executada.

## Antes de publicar

1. Execute os testes e experimente o menu em uma pasta de dados nova.
2. Revise `git status --short` e `git diff --check`. Dados de uso em `runtime/`,
   `.env` e chaves devem continuar ignorados.
3. Acorde com os integrantes a autoria, a licença e a visibilidade. Um repositório
   público sem licença não concede automaticamente permissão de reutilização.
4. Crie um repositório vazio chamado `ncas-aurora-siger`, sem README ou licença
   gerados automaticamente, para preservar o histórico local existente.
5. Configure `origin` com a URL exata do novo repositório e publique `main` e as
   branches de tarefa com comandos explícitos. Não use force-push.

Os comandos abaixo são modelos; substitua `SUA-CONTA` pelo destino aprovado:

```text
git remote add origin https://github.com/SUA-CONTA/ncas-aurora-siger.git
git push -u origin main
git push origin chore/estrutura-independente feat/cadastro-persistencia feat/analise-assistida feat/extensoes-operacionais docs/validacao-entrega
```

Se `origin` já existir, confira-o antes de qualquer alteração. As branches estão
integradas localmente com commits de merge, preservando seus limites para revisão.
PRs devem ser usados para próximas mudanças; não há necessidade de simular PRs de
branches que já foram integradas.

## Validação contínua

O workflow do projeto executa os testes em Windows e Linux, com Python 3.10 e 3.12,
e confere espaços inválidos no diff. A validação remota só estará confirmada após
a primeira execução no GitHub; validação local não implica CI publicada.

## O que pode ser compartilhado

Código, testes, dados fictícios, síntese autoral, roteiro, PDFs produzidos pela
equipe e instruções. Não incluir material didático original, identificadores
acadêmicos, credenciais ou dados reais da tripulação. O pacote de testes é gerado
por lista explícita de arquivos e exclui estado de execução e histórico Git.
