# Etapa 5c.2 — Diagnóstico de separabilidade e limite informacional

**Data:** 25/09/2026. **Status:** concluída. **Escopo:** fold 1 de desenvolvimento. **Holdout:** não consultado nem avaliado.

## Objetivo e protocolo

Investigar se a faixa de desempenho observada decorre de ajuste insuficiente, generalização, confusão entre classes ou informação limitada na entrada. Não houve novo treinamento, busca de hiperparâmetros, fold ou alteração de rótulo. O checkpoint `start512_lr2e5`, selecionado na 5c e reutilizado como A na 5c.1, foi avaliado sem gradientes no treino e na validação completos do fold 1. A inferência leu somente as linhas dessas duas partições. Nenhuma linha de holdout foi usada.

## Artefatos e resultados do checkpoint

Entradas: `train.xlsx` (SHA-256 `0e9219…e46818`), divisão `grouped_v1_seed_20260924` (SHA-256 `aa9c99…3586b`), `data/row_manifest.csv`, métricas/checkpoint da corrida A em `runs/etapa5/etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed/` e configuração `configs/bert_stage5_protocol.json`. O código de inferência e amostragem está em `src/diagnose_stage5_dataset_limit.py`; resultados em `runs/etapa5/diagnose_fold1_dataset_limit_20260925/metrics.json` e previsões por linha em `validation_predictions.jsonl`.

| Partição | N | Loss CE | Accuracy | Macro-F1 | Weighted-F1 | Gap accuracy treino−val | Gap macro-F1 treino−val |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Treino | 11.488 | 0,8842 | 59,03% | 58,39% | 58,29% |  |  |
| Validação | 5.580 | 1,0655 | 45,14% | 44,51% | 44,48% | **13,88 p.p.** | **13,88 p.p.** |

O melhor checkpoint foi salvo no passo 2.688 pela acurácia de validação, com macro-F1 de desempate. A curva registrada teve loss de treino decrescente (1,097 no passo 384 para cerca de 0,997 no passo 2.688); a accuracy de treino nas janelas subiu até 50,07% no passo 1.920. No passo 2.688 a validação atingiu 45,14%/44,51%; no último passo 2.872 caiu para 44,18%/42,22%. A menor loss de validação da série, 1,0502, ocorreu no passo 1.536, diferente do checkpoint escolhido por accuracy. Há aprendizado e gap de generalização, sem evidência de falha de convergência ou bug objetivo. A accuracy completa de treino de 59,03% foi medida agora, sem novo treino.

| Classe | Treino precision | Treino recall | Treino F1 | Validação precision | Validação recall | Validação F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `c1` | 59,50% | 65,27% | 62,25% | 46,89% | 48,92% | 47,88% |
| `c234` | 53,28% | 40,90% | 46,28% | 39,68% | **30,21%** | **34,30%** |
| `c5` | 62,47% | 71,38% | 66,63% | 47,16% | 56,31% | 51,33% |

## Matriz de confusão e direção dos erros

Linhas = classe verdadeira; colunas = predição; ordem `c1`, `c234`, `c5`.

| Contagens | Predito `c1` | Predito `c234` | Predito `c5` | Suporte |
| --- | ---: | ---: | ---: | ---: |
| Verdadeiro `c1` | **860** | 404 | 494 | 1.758 |
| Verdadeiro `c234` | 594 | **571** | 725 | 1.890 |
| Verdadeiro `c5` | 380 | 464 | **1.088** | 1.932 |

| Normalizada pela classe verdadeira | Predito `c1` | Predito `c234` | Predito `c5` |
| --- | ---: | ---: | ---: |
| `c1` | **48,92%** | 22,98% | 28,10% |
| `c234` | 31,43% | **30,21%** | 38,36% |
| `c5` | 19,67% | 24,02% | **56,31%** |

- `c234` tem o menor recall, precision e F1.
- Há 3.061 erros. A coluna `c5` absorve mais previsões incorretas: 1.219 (39,8%); `c1` recebe 974 e `c234`, 868.
- `c234` é a classe mais frequentemente confundida: 1.319 exemplos verdadeiros de `c234` foram enviados às classes extremas.
- Confusões entre classes adjacentes somam 2.187 erros (71,4%): `c1↔c234` 998 e `c234↔c5` 1.189. Confusões extremas `c1↔c5` somam 874 (28,6%), também substanciais.
- O modelo prediz `c234` 1.439 vezes contra suporte verdadeiro de 1.890 (subpredição); prediz `c5` 2.307 vezes contra suporte de 1.932.

## Confiança e entropia

Probabilidades softmax, top-1, margem top-1−top-2 e entropia em nats foram calculadas em cada previsão da validação. Quartis da confiança top-1: Q25 0,4320; mediana 0,4955; Q75 0,5995.

| Grupo | N | Confiança média / mediana | Margem média | Entropia média (nats) |
| --- | ---: | ---: | ---: | ---: |
| Acertos | 2.519 | 0,5444 / 0,5204 | 0,2413 | 0,9377 |
| Erros | 3.061 | 0,5054 / 0,4796 | 0,1852 | 0,9819 |
| Verdadeiro `c1` | 1.758 | 0,5236 / 0,4958 | 0,2133 | 0,9628 |
| Verdadeiro `c234` | 1.890 | **0,5089 / 0,4850** | **0,1892** | **0,9774** |
| Verdadeiro `c5` | 1.932 | 0,5362 / 0,5085 | 0,2288 | 0,9460 |

31 erros têm confiança ≥0,80 (1,01% dos erros); apenas dois têm confiança ≥0,90. A maioria dos erros não é de confiança extrema: em média os erros são menos confiantes, têm menor margem e maior entropia que os acertos. `c234` apresenta menor margem e maior entropia entre classes, compatível com fronteiras menos claras. Há sobreposição nas distribuições; probabilidades não provam ambiguidade semântica nem identificam rótulos incorretos.

### Similaridade textual exploratória para `c234`

Como `c234` teve desempenho menor, ajustamos somente o vocabulário TF-IDF nas 11.488 respostas de treino do fold e comparamos as 1.890 respostas `c234` da validação com exemplos de treino de cada classe por cosseno. A similaridade top-5 média foi 0,3579 para `c1`, 0,3747 para `c234` e 0,3615 para `c5`; maior similaridade individual média foi 0,4551/0,4778/0,4593, respectivamente. A classe do vizinho textual mais próximo foi `c1` em 630 casos, `c234` em 654 e `c5` em 606. O padrão mostra vizinhos das três classes quase igualmente frequentes; não mostra que os exemplos intermediários sejam lexicalmente mais próximos das duas extremas do que da própria classe. É compatível com sobreposição de vocabulário, mas TF-IDF não mede semântica nem determinabilidade humana. Detalhes em `runs/etapa5/diagnose_fold1_dataset_limit_20260925/tfidf_similarity.json`.

## Inspeção qualitativa controlada

Foi criada amostra determinística de 60 exemplos da validação: acertos/erros de confiança alta/baixa e exemplos nas seis direções de confusão (`c1↔c234`, `c234↔c5`, `c1↔c5`). Alta/baixa usa os quartis 75/25 da validação. O apêndice [etapa5_dataset_limit_diagnosis_examples.md](etapa5_dataset_limit_diagnosis_examples.md) inclui texto integral, linha Excel, rótulo, predição, probabilidades, grupo normalizado, confiança, entropia e truncamento. É uma amostra intencionalmente enriquecida para revisão, não aleatória: 48/60 divergem do rótulo e isso não estima a taxa global de erro.

### Leitura dos exemplos

- **Erro de modelo em relação ao rótulo observado:** todos os itens em que predição e rótulo divergem (48 nesta amostra selecionada) contam como erros preditivos para a avaliação. Há erros de alta confiança em respostas longas de encaminhamento/recusa com fundamentação legal, por exemplo linhas Excel 1396 e 2779 (`c234→c1`), e respostas curtas que apenas apontam a um site ou dizem que não há contrato/projeto, por exemplo linhas 11525 e 15206 (`c1→c5`). Isso mostra que tamanho e presença de linguagem formal não explicam sozinhos a decisão. **Não** permite concluir que o rótulo esteja incorreto.
- **Acertos do modelo também variam em forma:** há acertos `c1` em textos longos de negativa fundamentada (linha 478) e em notificações curtas sobre uma planilha anexada (linha 9458); acertos `c234` incluem orientações de contato e consulta presencial (linhas 698 e 4793). Portanto, comprimento, estrutura em itens ou presença de links isoladamente não definem a classe.
- **Possível ambiguidade ou dependência de critério:** respostas com informação organizada em itens, restrições legais, encaminhamento para outro órgão e respostas negativas aparecem em rótulos diferentes. A clareza formal pode ser julgada separadamente da completude, utilidade ou satisfação com o conteúdo; o material não fornece rubrica detalhada para saber qual aspecto orientou cada avaliação.
- **Possível inconsistência de anotação:** nenhum dos 60 selecionados repete a mesma chave de texto normalizado, portanto a amostra não contém um par direto para comparar rótulos do mesmo texto. No conjunto completo de validação do fold 1, a chave de grupo identifica 93 grupos com rótulos conflitantes (423 linhas). São contradições observáveis entre avaliações, mas não dizem por si qual avaliação está errada.
- **Possivelmente impossível avaliar só com o campo atual:** linhas como 15667 (“segue em anexo, resposta para conhecimento”), 3832 (“questionário respondido” em anexo) e 9439 (resposta elaborada pela unidade em arquivo anexo) não incluem o conteúdo referido. É possível avaliar a frase de encaminhamento, mas não a clareza do documento anexado. Links, pedidos e documentos externos também não são fornecidos ao modelo.

Na amostra há respostas padronizadas, encaminhamentos para links/contatos, referências legais e menções a anexos ou dados tabulares em diferentes classes; formalidade/boilerplate, por si, não separa nitidamente as classes. Isso sugere sobreposição de estilos, não que um rótulo específico esteja errado. A amostra serve para revisão humana; discordância do modelo, por si, não indica erro de anotação.

## Relação entre target, entrada e truncamento

- **Target:** clareza da resposta fornecida ao usuário; o enunciado diz que usuários a anotaram numa escala de 1–5, agregada nas classes `c1`, `c234` (escores intermediários) e `c5` (página 2 de `ep1-enunciado.pdf`).
- **Entrada atual:** somente `resp_text`; `clarity` é o target. A aba de treino não contém pedido original, nota individual, avaliador, justificativa ou outro campo adicional. Arquivos `test*.xlsx` não foram abertos, pois podem conter dados reservados.
- Não há campo textual adicional claramente relacionado no treino para o teste de contexto da Parte 7; não houve novo treino. A ausência de `request_text` impede medir seu benefício. Para clareza linguística, a resposta pode conter sinal suficiente; o contexto do pedido pode ajudar a interpretação, mas o material disponível não diz que ele seja necessário.
- No corte usado pelo candidato, foram truncadas 1.259/11.488 respostas de treino (10,96%) e 584/5.580 da validação (10,47%); média tokenizada de 220,35 e 217,96 tokens. O candidato `headtail256_lr2e5` da 5c ficou 0,34 p.p. abaixo em accuracy de `start512_lr2e5`; isso não isola truncamento, pois representação e comprimento também mudam. Não há evidência de que a porção removida contenha informação decisiva.

## Revisão da ablação de conflitos (5c.1)

A política alterou somente o treino; a validação de 5.580 exemplos foi idêntica.

| Variante | N | Removidos | `c1` | `c234` | `c5` | Predições na validação (`c1`, `c234`, `c5`) |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| A — original | 11.488 | 0 | 31,65% | 34,18% | 34,16% | 1.834, 1.439, 2.307 |
| B — remover conflitos | 10.265 | 1.223 (10,65%) | 30,61% | 34,46% | 34,95% | 2.412, 1.302, 1.866 |
| C — maioria conservadora | 10.806 | 682 (5,94%) | 31,90% | 33,73% | 34,37% | 2.047, 1.593, 1.940 |

| Variante | Accuracy | Macro-F1 | Weighted-F1 | F1 `c1` | F1 `c234` | F1 `c5` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A — original | **45,14%** | 44,51% | 44,48% | 47,88% | 34,30% | 51,33% |
| B — remoção | 45,09% | 44,25% | 44,14% | 50,79% | 32,89% | 49,08% |
| C — maioria | 44,95% | **44,67%** | **44,61%** | 48,57% | 35,95% | 49,48% |

As matrizes mudam e as políticas redistribuem previsões/recall entre classes. B aumenta recall de `c1` em 11,32 p.p., mas reduz `c5` em 8,07 p.p.; C aumenta um pouco `c1`/`c234` e reduz `c5` em 6,73 p.p. vs. A. Nenhuma alternativa supera A em accuracy (critério principal). C vence A em macro-F1 por 0,159 p.p., mas perde 0,197 p.p. em accuracy. Sem réplicas em outras seeds/folds nesta ablação, não é possível estimar se as diferenças excedem a variação normal nem atribuir causalidade à remoção. Os conflitos exatos não parecem ser o fator dominante limitando a generalização neste fold.

## Baseline versus BERT

Os três resultados abaixo são da mesma validação do fold 1 (5.580 exemplos); TF-IDF usa `C=0,5`.

| Modelo | Accuracy | Macro-F1 | Weighted-F1 | F1 `c1` | F1 `c234` | F1 `c5` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Classe majoritária (`c234`) | 33,87% | 16,87% | 17,14% | 0,00% | 50,60% | 0,00% |
| TF-IDF + regressão (`C=0,5`) | 44,61% | 44,35% | 44,41% | 44,03% | 38,21% | 50,81% |
| BERTimbau `start512_lr2e5` | **45,14%** | **44,51%** | **44,48%** | **47,88%** | 34,30% | **51,33%** |

Δ BERT−TF-IDF: **+0,54 p.p.** accuracy, **+0,16 p.p.** macro-F1 e **+0,07 p.p.** weighted-F1. O ganho global é marginal; BERT melhora F1 de `c1`/`c5`, mas fica 3,90 p.p. abaixo no F1 de `c234`. Um fold não mostra se o ganho se repetirá.

## Hipóteses e força da evidência

| Hipótese | Força | Evidência e limite |
| --- | --- | --- |
| H1 — Overfitting/generalização | **Moderada** | Gap de 13,88 p.p.; métricas de validação oscilam. Gap é menor que o do TF-IDF e treino/validação agrupados têm distribuição diferente. |
| H2 — Underfitting/capacidade insuficiente | **Fraca/inconclusiva** | Accuracy de treino ainda modesta, mas o gap também é claro; os dados não distinguem subajuste de ruído/ambiguidade. |
| H3 — Ruído de rótulo | **Moderada para contradições exatas; fraca no geral** | Há grupos repetidos conflitantes, mas removê-los/tratá-los não melhora accuracy. Outros ruídos e confiabilidade dos avaliadores não foram medidos. |
| H4 — Baixa separabilidade textual | **Moderada** | TF-IDF e BERT ficam próximos; há confusão em ambas direções e erros extremos. Um fold não estima limite informacional. |
| H5 — Classe intermediária ambígua | **Moderada** | `c234` tem menor F1/recall, erros para ambas as extremas, maior entropia e menor margem. Revisão humana ainda é necessária. |
| H6 — Informação necessária ausente | **Fraca/inconclusiva** | Treino tem apenas resposta e target. Nenhum texto adicional pode ser testado; não se sabe se o pedido ajudaria a avaliar clareza. |
| H7 — Truncamento destrutivo | **Fraca/inconclusiva** | Cerca de 10,5% excedem 512 tokens; não foi demonstrado que os tokens removidos tenham sinal. `headtail256` não supera `start512`. |
| H8 — Desbalanceamento | **Fraca como causa dominante** | Classes do treino completo variam de 31,59% a 34,30%. Há subpredição de `c234`, mas não forte desequilíbrio no dataset. |
| H9 — Subjetividade do target | **Moderada** | Rótulos vêm de avaliações dos usuários numa escala agregada, sem notas individuais, rubrica ou concordância disponíveis. |

## Recomendação para 5d

**Fatos observados:** o checkpoint aprende, mas mantém gap de generalização; `c234` é difícil no fold 1; o ganho de BERT sobre TF-IDF é marginal; o tratamento de conflitos exatos não ajudou accuracy; pouco mais de 10% da validação é truncada em 512; e o treino não oferece outros campos textuais.

**Interpretação:** há evidência moderada de sobreposição entre classes, sobretudo em `c234`, e da contribuição possível da natureza subjetiva do target. Há também gap de generalização. Os fatores podem coexistir. Não se demonstrou teto absoluto nem necessidade de contexto externo.

**Hipóteses em aberto:** variação entre folds/seeds; ambiguidade semântica versus ruído de anotação; benefício do pedido original; impacto informacional do truncamento; julgamento humano dos exemplos amostrados.

**Decisão recomendada:** a configuração atual é plausível para a confirmação cross-fold. Na 5d, manter BERT, representação, política Original e protocolo congelados e verificar se desempenho e dificuldade de `c234` se repetem nos folds 2 e 3. Esta recomendação não inicia a 5d; parar e aguardar autorização explícita do usuário.
