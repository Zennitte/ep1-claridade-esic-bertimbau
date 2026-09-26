# Etapa 5c.1 — Protocolo da ablação de conflitos de rótulo

**Estado:** subdivisão 5c.1 **Concluída em 25/09/2026**. A variante A reutiliza a corrida compatível da 5c; B e C foram treinadas no fold 1. O holdout não foi avaliado. A política que segue para confirmação em 5d é **Original**.

## Pergunta e variável experimental

**Hipótese:** grupos de textos equivalentes associados a classes diferentes podem introduzir ruído de supervisão. Remover esse ruído pode melhorar a generalização, embora também reduza o conjunto de treino.

No fold 1, comparar exatamente três políticas aplicadas apenas aos **índices de treino**. Os exemplos de validação, inclusive os difíceis e conflitantes, permanecem idênticos nas três avaliações. Não recalcular folds, normalizar o texto usado pelo BERT, usar similaridade aproximada ou alterar rótulos.

| Variante | Regra no treino |
| --- | --- |
| A — Original | Conservar cada índice e rótulo do treino original do fold. É o controle. |
| B — Remoção completa | Se um grupo de treino tiver mais de uma classe, remover todas as suas instâncias. |
| C — Maioria conservadora | Se houver maioria única, manter somente as instâncias que já têm esse rótulo; remover as minoritárias. Em empate, remover o grupo inteiro. Nunca relabelar. |

Um grupo só é considerado conflitante pelas classes **presentes no treino daquele fold**. A chave continua congelada desde a Etapa 1: `group_sha256` em `data/row_manifest.csv`, calculada por SHA-256 sobre texto em Unicode NFC, `casefold()` e sequências de espaços colapsadas. O texto original da planilha continua sendo o texto de entrada do modelo; a única célula numérica continua convertida por `str()`.

## Compatibilidade verificada antes de alterar o plano

Foram inspecionados `reports/etapa1_audit.md`/`.json`, `data/splits_grouped_v1.json`, `data/row_manifest.csv`, as configurações, relatórios e registros das Etapas 2–5 e os checkpoints existentes. `train.xlsx` corresponde ao SHA-256 `0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818`. A divisão preservada é `grouped_v1_seed_20260924`, SHA-256 `aa9c99a79ccccc3655399761c53098f5fd3d770c9aa6c8b68be29c49eba3586b`; o manifesto tem 20.092 índices únicos. O fold 1 tem 11.488 índices de treino e 5.580 de validação, sem grupos compartilhados entre eles. Nenhuma linha ou rótulo da validação foi usado para construir as políticas abaixo.

Contagens dos manifests reproduzíveis, construídos somente a partir dos índices de treino persistidos:

| Variante | N treino | Removidos | Percentual | `c1` | `c234` | `c5` | Grupos conflitantes afetados | Grupos totalmente removidos | Grupos tratados por maioria | Empates removidos |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A — Original | 11.488 | 0 | 0% | 3.637 | 3.927 | 3.924 | 0 | 0 | 0 | 0 |
| B — Remoção completa | 10.265 | 1.223 | 10,65% | 3.141 | 3.537 | 3.587 | 169 | 169 | 0 | 77 identificados entre os 169 |
| C — Maioria conservadora | 10.806 | 682 | 5,94% | 3.447 | 3.645 | 3.714 | 169 | 77 | 92 | 77 |

Esses números se referem apenas ao **treino do fold 1**. O fato de a variante B remover mais exemplos pode, por si, afetar desempenho. O teste medirá o efeito da política completa, e não provará sozinho que a causa de eventual melhora foi apenas o ruído dos rótulos.

## Manifests e verificações prévias

Os manifests A/B/C foram criados em `data/stage5_conflict_ablation/`; cada um preserva a ordem original dos índices do fold e inclui índices mantidos/removidos, decisão por grupo, contagens de rótulos, hashes da fonte/divisão/manifesto de linhas, a validação original e o hash dos índices do holdout. Nenhum dataset editado foi criado e os arquivos originais ficaram intactos. Não há repositório Git neste diretório; o campo de commit está vazio.

`src/prepare_stage5_conflict_ablation.py` executou as asserções antes da GPU e novamente depois da geração. Todas passaram: A é idêntica ao treino original; B não retém exemplos dos grupos conflitantes; C não tem conflitos restantes e remove todos os empates; os rótulos não foram alterados; as três classes continuam presentes; nenhum índice migrou de partição; treino e validação continuam sem grupos compartilhados; validação e holdout mantêm os índices originais. Hashes verificados: `train.xlsx` `0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818`, divisão `aa9c99a79ccccc3655399761c53098f5fd3d770c9aa6c8b68be29c49eba3586b`, manifesto de linhas `e07917a05f89f9940d6194d118fed7ebce9b9342acfc956eb38cadfd4dc2a2c4`.

## Congelamento do BERT de referência após 5c

Na 5c concluída, `start512_lr2e5` foi selecionado pela acurácia do fold 1 com treino Original: 45,143% contra 44,803% de `headtail256_lr2e5`. O macro-F1 de 256 tokens foi ligeiramente maior, mas era apenas desempate. A representação de referência é `start`, `max_length=512`, taxa `2e-5`, modelo pré-treinado `neuralmind/bert-base-portuguese-cased`, tokenizer correspondente e seed `20260924`. As versões efetivas estão no `metrics.json` da corrida de referência. A decisão foi tomada antes de qualquer geração ou treino B/C; não usar resultados da ablação para trocar o BERT de referência. Ver `reports/etapa5c_fold1_final.md`.

O controle A reutilizou a corrida completa de 5c: `runs/etapa5/etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed/metrics.json` (11.488 treinos, 5.580 validações, duas épocas, melhor passo 2.688). Foi confirmada equivalência de fold completo e ordem dos índices, fonte/divisão por hash, candidato (início/512, `2e-5`), modelo/tokenizer, seed, AdamW/`weight_decay`, batch/acumulação, avaliações, early stopping, critério de checkpoint e versões. A extensão em `src/bert_stage4.py` apenas seleciona os índices do manifesto antes da codificação; o loop de otimização/avaliação não mudou. O checkpoint A existe e foi recarregado com logits finitos `[5,3]`. A corrida 5a de 896 passos e as da Etapa 4 em subconjunto não foram usadas como controle.

## Protocolo fixo de treino e validação

As três variantes usaram o mesmo `src/bert_stage4.py` e protocolo 5b: fold 1, seed `20260924`, modelo inicial/tokenizer congelados, início/512, AdamW, taxa `2e-5`, `weight_decay=0,01`, microbatch 2, acumulação 4, lote efetivo 8, sem scheduler/warmup, até duas épocas, validação integral a cada 384 passos e no fim de época, early stopping (mínimo 512, paciência 3), descarte da acumulação incompleta, seleção por acurácia (macro-F1 desempata) e mesmas versões. B/C selecionaram índices pelos manifests; texto e rótulos nunca foram alterados.

Como o número de exemplos muda, os passos possíveis por época e o número de avaliações no limite da época também mudam **como consequência da política**, mantendo a mesma regra de duas épocas e cadência de 384 passos. Pela implementação atual, a projeção antes de early stopping é A: 1.436 passos/época e 0 exemplo residual descartado; B: 1.283 passos e 1 exemplo residual; C: 1.350 passos e 6 exemplos residuais. Esses resíduos são distintos dos 1.223/682 exemplos removidos pelas políticas de dados. Registrar tamanho usado, linhas realmente percorridas, passos e resíduos por época. Não ajustar épocas, lote ou taxa para compensar a remoção; essa diferença limita uma interpretação causal estrita sobre “ruído” isoladamente.

## Manifests e barreira antes da GPU

Foram criados `data/stage5_conflict_ablation/fold1_original.json`, `fold1_remove_conflicts.json` e `fold1_majority_conflicts.json`. Cada arquivo contém `row_index` base zero, listas ordenadas de índices mantidos/removidos, grupos/frequências/decisões, distribuição de classes, seed, horário, versão da regra e hashes da fonte, divisão e `row_manifest.csv`. O hash SHA-256 de cada arquivo está no `.sha256` correspondente e nos registros da corrida em `configs/bert_stage5_conflict_ablation.json`. Os manifests referenciam a validação original e registram o hash do holdout; validação alguma foi filtrada. Para folds 2 e 3, os manifests serão gerados somente sob autorização da subdivisão 5d.

Antes de iniciar GPU, foram implementadas em `src/prepare_stage5_conflict_ablation.py` e executadas verificações que falhariam imediatamente se:

1. A não for exatamente o treino original do fold (mesmos índices e rótulos).
2. B ainda contiver qualquer índice de grupo conflitante do treino.
3. C contiver dois rótulos no mesmo grupo, mantiver um grupo empatado ou alterar o rótulo de qualquer índice.
4. Qualquer variante contiver índice fora do treino original, duplicar índice, perder uma das três classes válidas ou alterar índice de validação.
5. O hash da fonte, da divisão ou do manifesto de linhas divergir, ou houver grupo comum entre treino e validação.
6. O holdout ou os índices persistidos da Etapa 1 tiverem sido modificados. A checagem de hash não consulta suas métricas.

Todas passaram; se qualquer uma tivesse falhado, o script teria parado antes do treino. `train.xlsx`, `data/splits_grouped_v1.json` e `data/row_manifest.csv` permanecem originais.

## Métricas, análise e decisão no fold 1

Para cada variante registrar N original/final, remoção absoluta/percentual, distribuição de classes antes/depois, grupos afetados/removidos/tratados por maioria/empatados, acurácia, macro-F1, weighted-F1, precisão/recall/F1 por `c1`, `c234`, `c5`, matriz de confusão, loss de treino e validação por avaliação, melhor passo e checkpoint, épocas efetivas, motivo de parada, tempo, throughput quando disponível e memória GPU. Todos os valores de classificação devem usar a **mesma validação integral** e o checkpoint escolhido por acurácia. As métricas adicionais de A podem ser derivadas da sua matriz de confusão já salva, sem novo treino: `precision=TP/coluna`, `recall=TP/linha`, `F1=2PR/(P+R)` com zero quando denominador é zero, `weighted-F1=Σ(suporte×F1)/N`. Verificar que acurácia e macro-F1 derivados reproduzem os registrados. Aplicar exatamente a mesma derivação a B/C.

Resultados selecionados pelos checkpoints de maior acurácia na mesma validação:

| Variante | N treino | Removidos | Accuracy | Macro-F1 | Weighted-F1 | Recall `c1` | Recall `c234` | Recall `c5` | Melhor checkpoint | Tempo |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A — Original | 11.488 | 0 (0%) | 45,14% | 44,51% | 44,48% | 48,92% | 30,21% | 56,31% | 2.688 | 70,69 min |
| B — Remoção completa | 10.265 | 1.223 (10,65%) | 45,09% | 44,25% | 44,14% | 60,24% | 27,78% | 48,24% | 2.304 | 62,96 min |
| C — Maioria conservadora | 10.806 | 682 (5,94%) | 44,95% | **44,67%** | **44,61%** | 52,56% | 33,12% | 49,59% | 1.536 | 64,20 min |

`Weighted-F1` e precision/F1 por classe foram derivados da matriz de confusão do checkpoint. Recall e acurácia reproduzem os valores salvos. As três variantes usaram a mesma validação de 5.580 linhas. Os checkpoints B/C foram recarregados e geraram logits finitos `[5,3]`.

### Métricas por classe

| Variante | Classe | Precision | Recall | F1 |
| --- | --- | ---: | ---: | ---: |
| A | c1 | 46,89% | 48,92% | 47,88% |
| A | c234 | 39,68% | 30,21% | 34,30% |
| A | c5 | 47,16% | 56,31% | 51,33% |
| B | c1 | 43,91% | 60,24% | 50,79% |
| B | c234 | 40,32% | 27,78% | 32,89% |
| B | c5 | 49,95% | 48,24% | 49,08% |
| C | c1 | 45,14% | 52,56% | 48,57% |
| C | c234 | 39,30% | 33,12% | 35,95% |
| C | c5 | 49,38% | 49,59% | 49,48% |

### Matrizes de confusão

Linhas são rótulos verdadeiros; colunas são predições, na ordem `c1`, `c234`, `c5`.

- A: `[[860, 404, 494], [594, 571, 725], [380, 464, 1088]]`
- B: `[[1059, 322, 377], [808, 525, 557], [545, 455, 932]]`
- C: `[[924, 427, 407], [689, 626, 575], [434, 540, 958]]`

| Comparação | Δ Accuracy | Δ Macro-F1 | Δ Weighted-F1 |
| --- | ---: | ---: | ---: |
| B − A | −0,054 pp | −0,252 pp | −0,342 pp |
| C − A | −0,197 pp | +0,159 pp | +0,131 pp |

### Interpretação e decisão

- **Observação:** B descartou 10,65% do treino e ficou 0,054 pp abaixo de A em acurácia; teve menor macro-F1 e weighted-F1. Aumentou recall de `c1` em 11,32 pp, ao custo de reduzir recall de `c5` em 8,07 pp e `c234` em 2,43 pp. B gerou mais previsões `c1` (2.412 contra 1.834 em A) e menos `c5` (1.866 contra 2.307).
- **Observação:** C descartou 5,94% do treino. Teve acurácia 0,197 pp abaixo de A, mas macro-F1 0,159 pp e weighted-F1 0,131 pp acima. Recall de `c1` e `c234` cresceu 3,64 pp e 2,91 pp; recall de `c5` caiu 6,73 pp. C previu mais `c1`/`c234` e menos `c5` que A.
- **Observação:** C ficou 0,143 pp abaixo de B em acurácia, mas 0,411 pp acima em macro-F1 e 0,473 pp acima em weighted-F1, mantendo 541 exemplos a mais. Porém, C não superou o controle A na métrica principal.
- **Hipótese:** a diferença entre C e B é compatível com a hipótese de que manter exemplos da classe majoritária conserva sinal útil. Um fold e uma seed não isolam o efeito de ruído da redução de dados nem provam causalidade.
- **Conclusão sustentada:** nenhuma alternativa superou A em acurácia, que era o critério principal fixado antes do treino; macro-F1 só desempata igualdade de acurácia. Portanto, **Original é a política que segue para confirmação na 5d**. A decisão também evita escolher uma política que reduziu recall de `c5` em 6,73–8,07 pp neste fold. Isso não prova que os conflitos sejam inofensivos; o efeito precisa ser observado nos demais folds.

### Perdas, paradas e custos

- A e B completaram duas épocas; early stopping não foi acionado. C parou por paciência após 2.688 passos, com melhor checkpoint no passo 1.536, cobrindo 1,991 das duas épocas planejadas.
- A descartou zero linhas por época na acumulação incompleta; B descartou uma; C descartou seis. Esse descarte decorre da regra fixa do carregador e não deve ser confundido com a política de conflitos.
- Losses no melhor checkpoint (treino/validação): A `0,9968/1,0655`; B `0,9775/1,0942`; C `1,0010/1,0807`.
- Tempo total: A 70,69 min; B 62,96 min; C 64,20 min. Pico de memória alocada: A 3,25 GB; B 3,26 GB; C 3,27 GB. Throughput não fazia parte da instrumentação existente.

### Arquivos de execução

- A reutilizado: `runs/etapa5/etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed/metrics.json`; checkpoint em `models/bert_stage5/etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed/best/`.
- B: `runs/etapa5/etapa5c1_B_remove_conflicts_fold1_20260925/metrics.json`; checkpoint em `models/bert_stage5/etapa5c1_B_remove_conflicts_fold1_20260925/best/`.
- C: `runs/etapa5/etapa5c1_C_majority_conflicts_fold1_20260925/metrics.json`; checkpoint em `models/bert_stage5/etapa5c1_C_majority_conflicts_fold1_20260925/best/`.
- Manifests e hashes: `data/stage5_conflict_ablation/`; configuração com protocolo e execuções em `configs/bert_stage5_conflict_ablation.json`.

A decisão foi feita pela acurácia, com macro-F1 como desempate, sem criar limiar depois dos resultados. Como B e C ficaram abaixo de A na acurácia, Original segue para 5d. A regra de desempate entre B/C não foi necessária. Recalls e matrizes foram examinados para identificar perdas por classe.

## Continuação e treino definitivo

Na 5d, confirmar Original para o BERT de referência nos folds 2 e 3 e depois comparar os dois finalistas BERT sob **essa mesma política**, reutilizando os resultados de 5c no fold 1. Agregar médias, variação e diferenças por fold. Nenhuma política alternativa será carregada para os folds restantes.

Em 5e, congelar modelo, política de dados e protocolo de treino. O número esperado para o conjunto de desenvolvimento pode ser calculado sem consultar o holdout; uma futura contagem para treino com todos os rótulos disponíveis será consequência mecânica da regra já congelada e não poderá alterar a escolha. Em 5f, consultar o holdout uma única vez. A Etapa 6 recebe apenas a configuração final e não executa A/B/C nem tuning.

**Custo realizado:** A foi reutilizado. B levou 62,96 min e C 64,20 min, total de 127,16 min nas duas corridas novas. Os tempos incluem treino, validações e gravação/recarga do checkpoint.
