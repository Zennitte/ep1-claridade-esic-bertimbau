# Etapa 5e — Especificação congelada do treinamento final

**Status:** concluída em 25/09/2026. **Configuração:** `configs/bert_stage5_final.json`. **Holdout:** não consultado; a configuração foi congelada antes da 5f. Nenhuma GPU ou treino foi executado nesta etapa.

## Evidências consideradas

Foram lidas as métricas completas dos seis runs BERT da 5c/5d e as métricas pareadas do TF-IDF `C=0,5`. A síntese da 5d reporta as médias e desvios amostrais entre folds. As matrizes abaixo somam as previsões dos checkpoints escolhidos pela acurácia nos três folds internos; cada linha é classe verdadeira e cada coluna, classe prevista, na ordem `c1`, `c234`, `c5`.

| Modelo | Acurácia média ± DP | Macro-F1 média ± DP | Weighted-F1 médio | Tempo médio/run |
|---|---:|---:|---:|---:|
| TF-IDF `C=0,5` | 44,705% ± 0,627 p.p. | 44,453% ± 0,631 p.p. | — | — |
| `start512_lr2e5` | **45,007% ± 0,613 p.p.** | 44,690% ± 0,707 p.p. | 44,677% | 70,09 min |
| `headtail256_lr2e5` | 44,909% ± 0,122 p.p. | **44,792% ± 0,137 p.p.** | **44,820%** | 41,86 min |

`start512_lr2e5` excede o TF-IDF em média por 0,302 p.p. de acurácia, mas fica abaixo do baseline no fold 3. Sua vantagem média sobre o outro finalista é somente 0,098 p.p.; ela é menor que a variação observada entre folds e não demonstra superioridade estatística. Acurácia continua sendo a métrica primária congelada na 5b, então `start512_lr2e5` é selecionado. `headtail256_lr2e5` tem +0,102 p.p. de macro-F1 e custa cerca de 40% menos por execução.

## Desempenho por classe

Média de recall por classe nos três folds:

| Candidato | `c1` | `c234` | `c5` |
|---|---:|---:|---:|
| `start512_lr2e5` | 45,11% | 35,76% | 54,06% |
| `headtail256_lr2e5` | 41,67% | 41,54% | 51,24% |

`headtail256_lr2e5` tem recall médio `c234` 5,77 p.p. maior; `start512_lr2e5` tem recall médio `c1` 3,44 p.p. e `c5` 2,83 p.p. maior. Este é um tradeoff entre classes que a pequena diferença de acurácia média não resolve. A escolha permanece baseada na regra primária de seleção já fixada, sem esconder esse limite.

Matrizes agregadas das previsões out-of-fold:

```text
start512_lr2e5
[[2436, 1588, 1371],
 [1673, 2079, 2065],
 [1014, 1677, 3165]]

headtail256_lr2e5
[[2244, 1987, 1164],
 [1498, 2420, 1899],
 [ 889, 1966, 3001]]
```

Os suportes agregados são `c1=5.395`, `c234=5.817` e `c5=5.856`, total de 17.068 exemplos de desenvolvimento. Fold 3 contém 5.871 itens de validação e 11.197 de treino; os `metrics.json` e a divisão persistida confirmam esses números. Corrigiu-se no plano um erro de transcrição anterior (`5.595`/`11.193`); não houve mudança de dados, métrica ou checkpoint.

## Especificação de dados congelada

- Aplicar política **Original**: manter todas as linhas e os rótulos originais; não remover duplicatas, não excluir grupos conflitantes e nunca relabelar.
- O dataset contém 20.092 exemplos: `c1=6.347`, `c234=6.853`, `c5=6.892`. Os 316 grupos normalizados conflitantes, com 1.975 linhas, também permanecem integralmente.
- Depois da auditoria única 5f, o ajuste final usará as 20.092 linhas de `train.xlsx`, incluindo as linhas da validação reservada agora para a auditoria. A métrica do holdout não servirá para tuning; somente um erro objetivo de implementação ou vazamento poderá reabrir a especificação, com a perda de independência documentada conforme o plano.
- A chave de grupo é SHA-256 do texto após Unicode NFC, `casefold()` e colapso de espaços; sem agrupamento por similaridade aproximada. Ela documenta a política e auditorias; não transforma nem remove exemplos no treino final.

## Especificação do modelo e treino congelada

- BERTimbau Base `neuralmind/bert-base-portuguese-cased`, com cabeça de classificação de três classes inicializada novamente a partir do checkpoint pré-treinado; não continuar de um checkpoint de fold.
- Revisão de base/tokenizer congelada em `94d69c95f98f7d5b2a8700c420230ae10def0baa`, observada como `refs/main` e como snapshot local com pesos e vocabulário completos. Os registros históricos de 5c/5d guardam o ID do modelo, mas não persistiram `_commit_hash`; no treino final será passada a revisão explicitamente e usada a cópia local. Esta limitação de proveniência histórica fica registrada.
- Tokenizer correspondente, entrada `resp_text`, representação somente do início, `max_length=512` incluindo tokens especiais, truncamento à direita e padding dinâmico por lote. Sem limpeza de texto adicional ou aumento de dados.
- Mapeamento estável: `c1 → 0`, `c234 → 1`, `c5 → 2`.
- Seed `20260924`; AdamW; taxa `2e-5`; `weight_decay=0,01`; norma de clipping de gradiente 1,0; sem scheduler e sem warmup. Microbatch 2, acumulação 4, lote efetivo 8; shuffle com gerador semeado.
- **Duração fixa: 4.523 updates do otimizador.** Os melhores checkpoints de `start512_lr2e5` foram selecionados em 1,872, 1,610 e 1,921 épocas equivalentes nos folds 1–3; a média é 1,8011. Com todos os dados, há 2.511 updates por época, portanto `round(1,8011 × 2.511)=4.523` updates. Isso representa aproximadamente 1,80 passagens pelo conjunto, não um `early stopping`.
- No treino final não haverá validação interna, seleção por métrica ou parada antecipada; após 5f, treinar com todos os rótulos retidos e salvar o modelo no passo 4.523. Assim, a auditoria do holdout acontece antes do ajuste final e só uma vez.

A etapa 6 implementará o treino final conforme `configs/bert_stage5_final.json`, registrando passos, duração, pico de memória, manifesto e verificação de recarga. A 5f permanece pendente e requer autorização própria.
