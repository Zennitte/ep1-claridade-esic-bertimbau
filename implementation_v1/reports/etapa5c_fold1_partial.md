# Etapa 5c — Fold 1 (resultado parcial)

**Data:** 25/09/2026. **Status:** parcial; falta executar `headtail256_lr2e5` amanhã de manhã, conforme orientação do usuário. **Holdout:** preservado.

## Escopo executado

Executado apenas o finalista início, 512 tokens, taxa `2e-5` (`start512_lr2e5`), no fold agrupado 1 completo: 11.488 linhas de treino e 5.580 de validação. Semente `20260924`, lote efetivo 8, máximo de duas épocas, validação integral a cada 384 passos e no limite de época. A corrida completou as duas épocas (2.872 passos); early stopping não foi acionado.

| Passo | Época | Acurácia | Macro-F1 | Loss de validação |
| ---: | ---: | ---: | ---: | ---: |
| 384 | 1 | 39,25% | 36,45% | 1,0934 |
| 768 | 1 | 42,15% | 41,52% | 1,0656 |
| 1.152 | 1 | 41,43% | 37,88% | 1,0783 |
| 1.436 (fim da época 1) | 1 | 44,16% | 43,84% | 1,0516 |
| 1.536 | 2 | 44,70% | 42,82% | 1,0502 |
| 1.920 | 2 | 43,46% | 39,30% | 1,0803 |
| 2.304 | 2 | 43,51% | 41,73% | 1,0681 |
| **2.688 (melhor)** | 2 | **45,14%** | **44,51%** | 1,0655 |
| 2.872 (fim da época 2) | 2 | 44,18% | 42,22% | 1,0661 |

## Comparação com o baseline do mesmo fold

TF-IDF + regressão logística, `C=0,5`, no mesmo fold: 44,61% de acurácia e 44,35% de macro-F1. No melhor checkpoint BERT, a diferença é **+0,54 ponto percentual** em acurácia e **+0,16 ponto** em macro-F1. A margem é pequena e vem de um fold; não permite concluir ainda que o BERT é superior de forma estável.

No melhor checkpoint, recalls: `c1` 48,92%, `c234` 30,21%, `c5` 56,31%. O baseline teve 40,16%, 38,10% e 55,02%, respectivamente. O BERT melhorou em `c1` e `c5`, mas ficou abaixo em `c234`; observar esse padrão nos outros folds.

## Custo e arquivos

- Duração total de parede: **4.241,518 s (70,69 min)**; treino reportado: 2.168,791 s; avaliações: 2.042,172 s.
- Pico de memória alocada na RX 7600: **3.247.774.720 bytes (3,25 GB)**; pico reservado: 3,76 GB.
- Melhor checkpoint no passo 2.688; recarga conferida, logits finitos com forma `[5,3]`.
- Métricas completas e histórico: `runs/etapa5/etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed/metrics.json`.
- Configuração efetiva: `runs/etapa5/etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed/config.json`.
- Checkpoint: `models/bert_stage5/etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed/best/`.
- Curvas: `reports/etapa5/etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed_accuracy.svg` e `_loss.svg`.

## Incidente de execução e retomada

A primeira tentativa no ambiente isolado falhou antes de um passo de treino por `hipErrorInvalidImage`; ela está registrada em `runs/etapa5/etapa5c_start512_lr2e5_fold1_20260924_2359/failure.json`. A repetição fora do isolamento completou sem falhas, usando o comando:

```powershell
python src/bert_stage4.py start512_lr2e5 --run-id etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed --fold 1 --full-fold --eval-every 384 --stage 5
```

Conforme pedido do usuário, `headtail256_lr2e5` não foi iniciado e fica para amanhã de manhã. A subdivisão 5c continua em andamento; fold 2/3 e holdout não foram executados.
