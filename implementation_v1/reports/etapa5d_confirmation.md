# Etapa 5d — Confirmação dos finalistas nos folds 2 e 3

**Status:** concluída. Política de dados: Original. O holdout não foi consultado.

## Protocolo

Foram reutilizadas as corridas completas do fold 1 (5c) e reunidas às quatro corridas novas dos folds 2 e 3. Cada corrida usa até duas épocas, lote efetivo 8, validação completa a cada 384 passos e no fim de cada época, acurácia para selecionar checkpoint e macro-F1 como desempate. TF-IDF `C=0,5` vem da avaliação pareada da Etapa 2. Os folds são agrupados por texto e não compartilham grupos entre treino e validação.

## Resultados por fold

| Candidato | Fold | Acurácia | Macro-F1 | Baseline TF-IDF acc. | Δ acc. | Tempo (min) | Passo melhor |
|---|---:|---:|---:|---:|---:|---:|---:|
| `start512_lr2e5` | 1 | 45.143% | 44.507% | 44.606% | +0.538 pp | 70.69 | 2688 |
| `start512_lr2e5` | 2 | 45.540% | 45.471% | 44.134% | +1.406 pp | 69.48 | 2304 |
| `start512_lr2e5` | 3 | 44.337% | 44.093% | 45.376% | -1.039 pp | 70.10 | 2688 |
| `headtail256_lr2e5` | 1 | 44.803% | 44.644% | 44.606% | +0.197 pp | 35.64 | 1436 |
| `headtail256_lr2e5` | 2 | 45.042% | 44.818% | 44.134% | +0.908 pp | 44.93 | 2304 |
| `headtail256_lr2e5` | 3 | 44.882% | 44.914% | 45.376% | -0.494 pp | 45.02 | 2688 |

## Média entre os três folds

| Modelo | Acurácia média ± DP amostral | Macro-F1 média ± DP amostral | Tempo médio por corrida |
|---|---:|---:|---:|
| TF-IDF `C=0,5` | 44.705% ± 0.627% | 44.453% ± 0.631% | — |
| `start512_lr2e5` | 45.007% ± 0.613% | 44.690% ± 0.707% | 70.09 min |
| `headtail256_lr2e5` | 44.909% ± 0.122% | 44.792% ± 0.137% | 41.86 min |

## Decisão da 5d

Pelo critério primário congelado, `start512_lr2e5` fica como referência: sua acurácia média é maior por +0.098 pp. `headtail256_lr2e5` tem macro-F1 médio maior por +0.102 pp e tempo médio menor. As diferenças são pequenas frente à variação observada entre folds; a escolha do checkpoint principal segue a acurácia, sem inferência de superioridade estatística.

Ambos os candidatos superam o TF-IDF em acurácia média por +0.302 pp (`start512_lr2e5`) e +0.204 pp (`headtail256_lr2e5`). A 5d confirma apenas o protocolo/folds observados; ainda não fixa a política final nem autoriza consulta ao holdout.

## Artefatos e integridade

Resumo de máquina: `runs/etapa5/stage5d_confirmation_summary.json`. O script `src/summarize_stage5d.py` carrega IDs e métricas persistidos, confirma candidato/fold e recarga de checkpoint, e exige que o holdout esteja marcado como não avaliado. Hashes da fonte e divisão: `0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818` e `aa9c99a79ccccc3655399761c53098f5fd3d770c9aa6c8b68be29c49eba3586b`. Nenhum rótulo, split ou conjunto de holdout foi alterado.
