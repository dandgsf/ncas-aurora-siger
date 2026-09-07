# Guia operacional de gravação — NCAS em até cinco minutos

Este documento é um roteiro de execução e fala para gravar a demonstração acadêmica
do NCAS. A tomada recomendada dura **4min45s**, deixando cerca de 15 segundos de
margem para pausas, transições e variações de fala. O limite oficial é de cinco
minutos; não acelere o vídeo depois de gravado para caber no prazo.

## Resultado que o vídeo precisa comprovar

Ao final, quem avalia deve ter visto e ouvido, sem depender do README:

- o propósito do NCAS e seu limite como apoio a especialistas;
- dados fictícios estruturados em JSON e eventos incrementais em TXT;
- leitura, gravação e recuperação dos dados após reiniciar o programa;
- a regra booleana principal, sua simplificação e as quatro combinações;
- zero-shot, few-shot, saída estruturada e a simulação local de análise;
- uma proposta objetiva para medir melhoria das respostas;
- memória, armazenamento e fluxo de entrada e saída;
- diversidade, risco de vieses, responsabilidade e confirmação humana;
- execução prática do menu em Python.

Não é necessário demonstrar todos os menus nem ler todo o conteúdo dos PDFs. O
objetivo é apresentar evidências suficientes de cada critério da rubrica.

## Formato recomendado

- Grave em **1920 × 1080**, 30 fps e com áudio de voz claro.
- Capture uma janela ou uma tela preparada, não a área de trabalho inteira.
- Use Windows Terminal maximizado, fonte entre **18 e 22**, tema com contraste alto
  e zoom que permita ler JSON em 1080p.
- Deixe o terminal com aproximadamente 100 colunas. Linhas muito largas tornam os
  campos ilegíveis; linhas muito estreitas quebram o JSON em excesso.
- Use o roteiro em um segundo monitor, tablet ou papel. Ele não precisa aparecer.
- Webcam é opcional. Se usada, mantenha-a pequena e sem cobrir terminal ou PDFs.
- Prefira uma tomada contínua. Cortes são aceitáveis apenas para remover silêncio ou
  erro; não corte entre uma ação e seu resultado, pois isso enfraquece a evidência.
- Fale em ritmo normal, aproximadamente 125 a 140 palavras por minuto.

## Preparação obrigatória — antes de iniciar a captura

### 1. Ambiente e privacidade

1. Ative **Não perturbe** no Windows.
2. Feche e-mail, mensageiros, gerenciadores de senha, configurações do sistema e
   terminais que contenham histórico pessoal.
3. Não abra `.env`, variáveis de ambiente, tokens, chaves, perfis do navegador ou
   configurações da OpenAI. Esta versão não usa API nem chave.
4. Não use dados reais. Os nomes, eventos e medições exibidos devem permanecer
   fictícios.
5. Feche abas do portal acadêmico que exibam nome completo, matrícula, turma ou nota.
6. Desative autocomplete ou extensões que possam sugerir segredos no terminal.

### 2. Materiais que ficarão abertos

Prepare somente três superfícies:

1. **Terminal**, já posicionado na raiz do projeto;
2. `regras_logicas.pdf`, aberto na página 1 e com zoom legível;
3. `prompts_utilizados.pdf`, aberto na página 2, que mostra o few-shot.

Deixe as páginas prontas antes de gravar. Use `Alt+Tab` para alternar entre o
terminal e os PDFs. Não procure arquivos durante a tomada.

### 3. Conferência técnica

Na raiz do projeto, execute antes da gravação:

```powershell
python --version
python -m unittest discover -s tests -v
python scripts/demonstrar.py
```

Resultado esperado: Python 3.10 ou superior, **30 testes com `OK`** e a mensagem
`DEMONSTRAÇÃO CONCLUÍDA`. Esses comandos são ensaio e validação prévia; não precisam
aparecer no vídeo, porque o tempo deve ser usado no funcionamento do produto.

Faça uma gravação de dez segundos e confira voz, ausência de eco, foco, cursor e
legibilidade. Assista ao teste antes da tomada final.

### 4. Pasta exclusiva da tomada

Use uma pasta de dados com nome novo em cada tentativa. Para a tomada final, o
roteiro usa:

```text
runtime/video-final-01
```

Se repetir a gravação, troque apenas o número para `video-final-02`, `03` e assim
por diante. Não reutilize a pasta de uma tentativa anterior: a ocorrência pode já
estar resolvida e comprometer a sequência. Não é necessário apagar pastas antigas.

## Mapa rápido da tomada

| Tempo-alvo | Tela | Evidência principal |
|---|---|---|
| 00:00–00:25 | Terminal limpo | problema, objetivo e limites |
| 00:25–01:05 | Menu e opção 2 | Python, JSON, tipos e dados fictícios |
| 01:05–01:40 | Opção 5 + PDF de regras | expressão, simplificação e equivalência |
| 01:40–02:20 | PDF de prompts | zero-shot, few-shot e estrutura |
| 02:20–03:10 | Opção 3 | simulação e resposta estruturada |
| 03:10–03:45 | Opção 6 | revisão humana e responsabilidade |
| 03:45–04:15 | Reinício + opção 8 | persistência entre execuções |
| 04:15–04:35 | PowerShell | evidência do TXT em append |
| 04:35–04:55 | Terminal | melhoria, memória, ética e encerramento |

O encerramento em **4min55s é o limite de ensaio**. A fala principal abaixo foi
escrita para terminar perto de 4min45s; se o ensaio passar de 4min50s, encurte as
pausas, não remova requisitos.

## Roteiro literal — ações, inputs e fala

### 00:00–00:25 — abertura

**Tela:** terminal limpo, maximizado e já na raiz do projeto. Inicie a captura e
aguarde um segundo antes de falar.

**Fala sugerida:**

> Nós somos [NOMES DOS INTEGRANTES] e este é o NCAS, Núcleo Cognitivo da Aurora
> Siger. O protótipo em Python registra ocorrências, aplica regras e apoia
> especialistas. Não controla equipamentos nem substitui decisões humanas. Os dados
> são fictícios e a análise é uma simulação local, sem API de inteligência artificial.

### 00:25–01:05 — iniciar, carregar e consultar dados

**Digite e pressione Enter:**

```powershell
python codigo_fonte.py --demo --data-dir runtime/video-final-01
```

Quando o menu aparecer, digite:

```text
2
```

**Tela:** deixe visíveis por alguns segundos `id`, `tipo`, `modulo_origem`,
`prioridade`, `status` e `condicoes_operacionais`. Não tente ler todo o JSON.

**Fala sugerida enquanto a listagem aparece:**

> O modo de demonstração gravou três ocorrências: alerta operacional, solicitação
> da tripulação e evento energético. O JSON guarda versão, ocorrências e análises,
> com ID, tipo, módulo, descrição, prioridade, status, data e sinais booleanos. Na
> execução, esses dados são reconstruídos como dicionários e listas na memória.

**Se a tela mostrar `Dados existentes preservados`:** interrompa a tomada e use
outro sufixo. Para a primeira execução correta, deve aparecer `Três exemplos
fictícios carregados.`

### 01:05–01:40 — regra booleana e simplificação

Quando o menu reaparecer, digite:

```text
5
```

**Tela:** mostre a expressão e as quatro linhas da tabela. Em seguida, use
`Alt+Tab` e mostre a página 1 de `regras_logicas.pdf`, já aberta.

**Fala sugerida:**

> A regra é: falha e crítico, ou falha e não crítico. Fatorando falha, crítico ou
> não crítico é verdadeiro pelo complemento; pela identidade, resta somente falha.
> As quatro combinações confirmam a equivalência. A criticidade orienta prioridade,
> mas não decide se a falha gera alerta.

Não permaneça na segunda página do PDF; as extensões são úteis, mas não valem o
tempo da demonstração principal.

### 01:40–02:20 — prompts e melhoria mensurável

Use `Alt+Tab` para mostrar `prompts_utilizados.pdf` na página 2. Role brevemente ou
aponte visualmente os títulos e os blocos de entrada/saída. Depois, avance para a
página 3 e, por fim, para a página 4.

**Fala sugerida:**

> Há três estratégias: zero-shot instrui sem exemplos; few-shot acrescenta dois
> pares de entrada e saída; e o estruturado exige campos definidos. A resposta
> separa fatos, recomendações e pendências, sempre com revisão humana. Uma evolução
> seria medida nos mesmos casos fictícios por formato válido, classificação correta,
> ausência de invenções e presença da revisão. Aqui, mudar o prompt não prova melhora
> de um modelo porque a resposta é local.

**Importante:** não diga que o sistema está usando ChatGPT, GPT ou a OpenAI API.
Os prompts são materiais de engenharia e a resposta atual é gerada por regras e
textos predefinidos.

### 02:20–03:10 — executar a análise estruturada

Volte ao terminal com `Alt+Tab`. Quando o menu estiver visível, digite exatamente,
um valor por vez:

```text
3
OCR-DEMO-001
estruturado
```

**Não digite `3` ou `6` no campo de estratégia.** Os únicos valores aceitos são
`zero-shot`, `few-shot` e `estruturado`, com letras minúsculas e hífen quando houver.

**Tela:** deixe a saída parada na região que exibe `classificacao`,
`fatos_confirmados`, `acoes_recomendadas`, `pendencias`,
`necessita_revisao_humana`, `modo_execucao` e `modelo`. Se necessário, role devagar
uma única vez; não faça movimentos rápidos.

**Fala sugerida:**

> O programa carrega a ocorrência, aplica a regra e registra uma análise. A saída
> separa fatos, recomendações e pendências e exige revisão humana. Fallback local e
> modelo nulo comprovam que não houve chamada a LLM. Para os mesmos dados e regras,
> o resultado é reproduzível.

### 03:10–03:45 — revisão humana e resolução

Quando o menu reaparecer, digite exatamente:

```text
6
OCR-DEMO-001
Verificação fictícia concluída; sensores serão avaliados pelo especialista.
CONFIRMAR
```

Cada linha corresponde a uma pergunta diferente. `CONFIRMAR` deve ser digitado
somente no último campo e em letras maiúsculas.

**Fala sugerida:**

> A recomendação não muda o estado sozinha. Um operador registra a verificação e
> confirma explicitamente; só então o status se torna resolvida. Isso demonstra
> supervisão, mas não autentica o operador nem autoriza intervenção física.

### 03:45–04:15 — provar persistência após reinício

Quando o menu reaparecer, digite:

```text
0
```

Depois de voltar ao PowerShell, execute **o mesmo comando e a mesma pasta**:

```powershell
python codigo_fonte.py --demo --data-dir runtime/video-final-01
```

Quando o menu aparecer, digite:

```text
8
status
resolvida
```

**Tela:** deixe visíveis `OCR-DEMO-001` e `"status": "resolvida"`.

**Fala sugerida:**

> Ao encerrar, os objetos saem da memória. Reabrindo a mesma pasta, o filtro recupera
> do JSON a ocorrência resolvida, comprovando persistência entre execuções.

### 04:15–04:35 — mostrar a trilha TXT em append

Saia novamente:

```text
0
```

No PowerShell, digite:

```powershell
Get-Content runtime/video-final-01/registros_colonia.txt | Select-Object -Last 5
```

**Tela:** deixe as últimas linhas visíveis, especialmente eventos de análise e
revisão. Não é necessário abrir o Explorador de Arquivos.

**Fala sugerida:**

> O TXT mantém uma trilha cronológica em append, acrescentando eventos sem apagar o
> histórico. O JSON usa gravação atômica; o TXT é auxiliar e não forma uma transação
> conjunta com ele.

### 04:35–04:55 — ética, diversidade e encerramento

**Tela:** mantenha o terminal com a trilha TXT visível. Não abra novos arquivos.

**Fala sugerida:**

> O NCAS classifica sinais, não pessoas, mas descrições e prioridades podem carregar
> vieses. Diversidade, revisão da linguagem e validação especializada são essenciais.
> Assim integramos Python, arquivos, lógica, prompts e responsabilidade humana,
> mantendo a decisão final com especialistas.

Pare de falar, aguarde um segundo e encerre a captura. Não continue improvisando.

## Cola de inputs — ordem exata

Use este bloco no segundo monitor. Ele contém tudo o que será digitado na tomada:

```text
python codigo_fonte.py --demo --data-dir runtime/video-final-01
2
5

[mostrar regras_logicas.pdf p. 1]
[mostrar prompts_utilizados.pdf pp. 2, 3 e 4]

3
OCR-DEMO-001
estruturado

6
OCR-DEMO-001
Verificação fictícia concluída; sensores serão avaliados pelo especialista.
CONFIRMAR

0
python codigo_fonte.py --demo --data-dir runtime/video-final-01
8
status
resolvida
0

Get-Content runtime/video-final-01/registros_colonia.txt | Select-Object -Last 5
```

## O que mostrar

- o comando real iniciando `codigo_fonte.py`;
- o menu e pelo menos uma consulta de ocorrência;
- os três tipos de ocorrência, ainda que sem ler todos os campos;
- a expressão booleana, sua forma simplificada e a tabela com quatro casos;
- os títulos e diferenças entre zero-shot, few-shot e estruturado;
- uma saída completa o bastante para identificar contrato, fallback e revisão;
- a confirmação humana e a mudança para `resolvida`;
- o fechamento, a nova execução e o registro recuperado;
- linhas finais do TXT comprovando o append;
- dados sempre identificados como fictícios.

## O que não mostrar ou afirmar

- não mostre chaves, `.env`, variáveis de ambiente, credenciais ou histórico de
  comandos que possa conter segredos;
- não mostre notificações, e-mail, matrícula, portal acadêmico ou dados pessoais;
- não diga que existe integração real com OpenAI, ChatGPT ou qualquer LLM;
- não diga que o sistema treinou, ajustou ou executou um modelo;
- não apresente o fallback local como inteligência artificial generativa real;
- não afirme que os testes garantem nota ou que substituem a avaliação;
- não sugira que o NCAS controla módulos, sensores ou decisões críticas;
- não use a opção 6 antes da opção 3: a revisão exige análise registrada;
- não reutilize uma pasta cuja ocorrência já esteja resolvida;
- não demonstre erros de digitação, cadastro inválido ou recursos secundários na
  tomada final; eles consomem tempo e não aumentam a cobertura da rubrica;
- não mostre código-fonte linha por linha. O vídeo deve provar comportamento e
  explicar decisões, não realizar uma revisão de código;
- não mostre os 30 testes durante a tomada final; cite-os somente se sobrar tempo.

## Recuperação de erros durante a tomada

| Problema | Ação recomendada |
|---|---|
| Apareceu `Ocorrência não encontrada` | Pare e regrave usando `OCR-DEMO-001` exatamente em maiúsculas. |
| Apareceu `Opção inválida` na estratégia | Pare e regrave; use `estruturado` em minúsculas. |
| A revisão diz que exige análise | A opção 3 não foi concluída nessa pasta; recomece com outro sufixo. |
| Apareceu `Dados existentes preservados` logo no início | A pasta já foi usada; troque o sufixo e recomece. |
| Notificação ou dado pessoal apareceu | Interrompa e descarte a tomada; não tente ocultar apenas com um corte impreciso. |
| O ensaio passou de 5 minutos | Regrave; não aumente a velocidade. Use a fala sugerida sem comentários extras. |
| O terminal ficou ilegível | Regrave com fonte maior e captura em 1080p. |
| Houve silêncio curto ou troca lenta de tela | Corte somente o intervalo, preservando ação e resultado na mesma sequência. |

## Plano B seguro

Se o menu falhar imediatamente antes da gravação, execute:

```powershell
python scripts/demonstrar.py
```

Esse comando percorre ocorrências, tabela-verdade, análise, revisão e recuperação em
uma pasta temporária. Ele é uma contingência, não a primeira escolha: o fluxo
principal acima evidencia melhor os inputs do usuário, o menu e a confirmação
humana. Não afirme que o script grava o vídeo; ele apenas executa a demonstração.

## Checklist depois de gravar

Assista ao vídeo inteiro antes de publicar e confirme:

- [ ] duração igual ou inferior a 5:00;
- [ ] fala compreensível e sem música competindo com a voz;
- [ ] terminal e PDFs legíveis em 1080p;
- [ ] nomes dos integrantes apresentados na abertura, cartela ou descrição;
- [ ] `fallback_local`, `modelo: null` e revisão humana visíveis ou explicados;
- [ ] nenhum segredo, notificação ou dado pessoal aparece;
- [ ] nenhuma integração opcional foi apresentada como implementada;
- [ ] o link do YouTube está como **Não listado**, não Privado;
- [ ] o link abre em janela anônima/desconectada;
- [ ] a versão publicada é a tomada correta e possui até cinco minutos;
- [ ] uma cópia local do vídeo foi preservada fora do repositório Git.

Depois de obter a URL real do YouTube, gere o pacote final:

```powershell
python scripts/empacotar.py --video-url "https://youtu.be/ID_REAL_11_CARACTERES"
```

O resultado esperado é `dist/ncas-entrega.zip`, contendo `link_video.txt`. Substitua
o endereço de exemplo pela URL verdadeira e teste novamente o vídeo antes da
submissão. Não adicione o arquivo bruto da gravação ao Git.
