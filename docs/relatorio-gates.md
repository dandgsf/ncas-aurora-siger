# Relatório de implementação dos gates 2 a 5

## Resultado

Versão local do NCAS implementada para avaliação funcional. Contém três tipos de
ocorrência, persistência, regras, prompts, simulação, revisão humana, histórico,
demonstração, documentação e empacotamento. O Git tem histórico próprio e integração
local em `main`. Publicação remota, vídeo e API real não são apresentados como concluídos.

## Branches e motivo de cada separação

| Branch | Motivo | Entrega e verificação do marco |
|---|---|---|
| `chore/estrutura-independente` | Separar a base do repositório e o escopo do código funcional; evitar dependência do arquivo acadêmico original. | Estrutura, regras de contribuição, ignorados e escopo; commit `dbd36ae`. |
| `feat/cadastro-persistencia` | Isolar o componente que grava dados, permitindo revisar integridade antes de acrescentar análise. | Cadastro, JSON atômico, TXT incremental e trava; 11 testes; commit `fc98dfa`. |
| `feat/analise-assistida` | Regras e interpretação mudam o comportamento do produto e precisam de revisão própria. | Equivalência, três prompts, análise local e confirmação humana; 18 testes acumulados; commit `2b54378`. |
| `feat/extensoes-operacionais` | Acrescentar dois tipos sem misturar suas regras com a validação inicial da persistência. | Tripulação, energia e demonstração idempotente; 22 testes acumulados; commit `f470ddd`. |
| `fix/integridade-historico` | A revisão identificou a necessidade de rejeitar status sem revisão compatível e referências malformadas no histórico. | Validação cruzada e datas; 23 testes acumulados; commit `87e4989`. |
| `docs/validacao-entrega` | Reunir os materiais e as verificações que permitem a outra pessoa reproduzir o projeto fora do ambiente de desenvolvimento. | README, roteiro, PDFs autorais, ZIP por lista explícita, workflow e testes por subprocesso. |
| `docs/roteiro-gravacao-5min` | Isolar a reformulação do roteiro, pois ela muda a estratégia de apresentação e a evidência acadêmica, mas não o comportamento do programa. A separação permite revisar tempo, falas e comandos sem misturar alterações funcionais. | Guia operacional cronometrado, inputs literais, enquadramento, privacidade, contingência e checklist de submissão; fluxo validado em dois processos. |
| `docs/ajusta-video-final-02` | Atualizar a pasta da segunda tomada sem reutilizar o estado persistido da gravação anterior, evitando iniciar a demonstração com uma ocorrência já resolvida. | Todos os comandos do roteiro passam a usar `runtime/video-final-02`; novas tentativas começam em `video-final-03`. |

As branches funcionais foram criadas sequencialmente sobre a base integrada.
Cada marco foi preservado em sua branch e integrado com merge local, sem squash
ou reescrita. A branch documental incorporou a correção antes da validação final.
A melhoria posterior do roteiro também recebeu branch própria por ser uma revisão
extensa da apresentação, independente do código já validado. Não foram criadas
branches vazias por arquivo ou usadas alterações de exercícios
externos a este projeto. Os hashes finais podem ser consultados com
`git log --all --graph --oneline --decorate`.

## Evidências de validação

Validação final: **30 testes aprovados em Windows, Python 3.12.10**. A demonstração
automatizada também concluiu o fluxo dos três tipos. Os dois PDFs possuem duas e
quatro páginas A4, respectivamente; texto e metadados foram conferidos, com revisão
visual das seis páginas. A geração usa data interna fixa para ser reproduzível.

- Suíte padrão: `python -m unittest discover -s tests -v`.
- Recuperação de registros entre dois processos, não apenas entre objetos Python.
- Fluxo real de terminal com pasta contendo espaços e acentos.
- JSON inválido, chaves repetidas, entrada ambígua, ID duplicado e falha de gravação.
- Tabela-verdade e todas as combinações das regras adicionais.
- Análise determinística, contrato, histórico e confirmação de revisão.
- ZIP extraído em pasta temporária, executado com `python -S`, sem pacotes externos.
- Dados de uso e credenciais excluídos do pacote; link de vídeo ausente no pacote de testes.
- PDFs gerados a partir das funções implementadas e revisados após renderização.

Os testes são locais. O workflow preparado para Windows/Linux e Python 3.10/3.12
ainda depende de publicação para executar no GitHub. Isso não constitui evidência
de execução remota ou de integração com API.

## Limites e pendências externas

O adaptador de API real não foi implementado e não é necessário para esta versão.
Nenhuma chave é utilizada. A simulação não verifica sensores, não autentica o
operador e não filtra todo conteúdo ofensivo. JSON e TXT não são transacionados
conjuntamente: falha no log posterior à persistência é comunicada explicitamente.

Para a entrega acadêmica final, faltam a gravação e publicação do vídeo, conferência
do link e inclusão dos integrantes. Para publicação do repositório, faltam destino,
visibilidade e acordo de licença. O programa está preparado para testes locais
independentemente dessas decisões.
