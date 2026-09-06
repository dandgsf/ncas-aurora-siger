# Arquitetura e decisões

## Caminho de uma ocorrência

Terminal -> validação -> JSON -> trilha TXT -> regra -> prompt -> resposta local
validada -> revisão humana explícita -> persistência do resultado.

`src/modelos.py` valida contratos; `src/persistencia.py` centraliza leitura e gravação;
`src/analise.py` reúne regras, prompts e simulação; `src/terminal.py` contém o menu.
O ponto de entrada é `codigo_fonte.py`. Todos os caminhos padrão são relativos à
localização do programa. `--data-dir` relativo é resolvido a partir da pasta atual.

## Formato dos dados

O objeto JSON possui `versao: 1`, `ocorrencias` e `analises`. Cada ocorrência contém
ID estável, tipo, módulo, descrição, prioridade, status, instante ISO 8601 com fuso
e condições booleanas próprias do tipo. Campos ausentes, adicionais, enums inválidos,
IDs repetidos e chaves JSON duplicadas são rejeitados.

Cada análise guarda ID, instante, estratégia, prompt, resposta e revisão opcional.
A resposta contém identificação da ocorrência, resumo, classificação, fatos,
recomendações, pendências, revisão humana obrigatória, modo local e modelo nulo.
O histórico permite consultar a análise após reiniciar. Recomendações nunca mudam
o status para resolvida: isso exige a opção de revisão, uma observação e `CONFIRMAR`.

| Tipo | Condições | Regra adotada |
|---|---|---|
| Alerta operacional | falha, critico | Alerta = falha |
| Solicitação da tripulação | urgente, setor_essencial | Priorizar = urgente AND setor_essencial |
| Evento energético | falha, consumo_elevado | Atenção = falha OR consumo_elevado |

As duas extensões são decisões do projeto. A criticidade continua registrada e
visível, mas não altera a existência do alerta na regra principal escolhida.
Prioridade é um dado informado, não uma medição nem uma decisão gerada pela análise.

## Memória e armazenamento

As entradas e os registros lidos tornam-se dicionários/listas em memória RAM.
Serialização converte a estrutura em JSON UTF-8. O sistema escreve em arquivo
temporário na mesma pasta, descarrega o buffer e usa substituição atômica do JSON.
Uma nova execução lê os bytes do armazenamento e reconstrói os objetos em memória.
O sistema operacional intermedeia essas operações de entrada e saída e o transporte
entre memória e dispositivos; o programa não acessa barramentos diretamente.

Uma trava exclusiva serializa as gravações para a mesma pasta. Leitores recebem
um JSON completo. A trava deixada após queda abrupta requer inspeção do operador.
O TXT é aberto em append e registra eventos e IDs, sem copiar descrições ou prompts.
Se o append falhar após salvar o JSON, o programa avisa que os dados foram salvos.
Essa limitação é explícita: a trilha auxiliar pode ficar incompleta. Não há banco,
transação entre os dois arquivos, autenticação ou suporte a operação distribuída.

## Prompts, melhoria e limites

Zero-shot fornece instruções sem exemplos. Few-shot acrescenta dois pares completos,
um com falha e outro sem falha. A opção estruturada reforça campos, tipos e restrições.
O simulador usa a mesma função de análise nos três casos; diferenças de texto do
prompt não demonstram ganho de um modelo. Não há treinamento, inferência de LLM,
RAG nem validação de API nesta versão.

Para avaliar melhoria de respostas em uma integração futura, manter um conjunto
fictício fixo e comparar: aderência ao contrato, classificação correta, ausência
de fatos inventados e presença de revisão humana. Uma pontuação de quatro critérios
pode orientar revisão dos prompts. Não se promete melhora sem medir resultados.

## Ética, diversidade e responsabilidade

O sistema classifica sinais operacionais, não pessoas. Origem, etnia, gênero e
outros atributos pessoais não participam das regras. Ainda assim, descrições e
prioridades informadas podem refletir vieses humanos. Uma equipe diversa deve
revisar linguagem, exemplos e critérios para evitar exclusão ou tratamento desigual.

A simulação repete a descrição fornecida; não verifica a veracidade de sensores,
não identifica causas e não filtra integralmente linguagem ofensiva. Use apenas
dados fictícios. A revisão exige ação humana, mas não comprova a identidade do
operador nem autoriza intervenções físicas. Automatizar recomendações sem análise
especializada pode atrasar atendimento ou distribuir recursos de forma injusta.

## Integração real futura

A API é opcional para a atividade. Sua configuração permanece pendente; esta versão
não lê credenciais nem tenta usar chaves disponíveis no computador. A evolução deve
preservar o contrato da análise, a validação, o funcionamento local em caso de falha
e a decisão humana. Falhas de rede e respostas remotas não foram testadas aqui,
porque o adaptador remoto ainda não existe.
