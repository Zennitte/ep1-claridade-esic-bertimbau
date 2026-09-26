# Etapa 5f — Auditoria única do holdout

**Conclusão:** 26/09/2026, 09:29 BRT. O holdout foi consultado uma vez, após o treino e o salvamento do modelo de auditoria. Os resultados não foram usados para alterar a configuração congelada na 5e.

## Protocolo e integridade

- Configuração da 5e: `configs/bert_stage5_final.json` (SHA-256 `4377c55014be7f6f3de1b89b9dfb9c64785561b3df1a4b96b4eeef7e9a8b0953`); modelo BERTimbau Base na revisão congelada `94d69c95f98f7d5b2a8700c420230ae10def0baa`, cabeça de classificação nova, representação inicial de 512 tokens.
- Fonte `train.xlsx`, divisão agrupada e manifesto de linhas conferidos contra os hashes persistidos. Desenvolvimento: 17.068 linhas (`c1=5.395`, `c234=5.817`, `c5=5.856`); holdout: 3.024. Sobreposição de índices: zero; sobreposição de grupos: zero.
- Treino exclusivamente nos índices de desenvolvimento, sem validação, parada antecipada ou seleção de checkpoint. AdamW, LR `2e-5`, `weight_decay=0,01`, batch efetivo 8, seed `20260924`, 3.842 updates (1,8012 épocas equivalentes). O checkpoint de auditoria foi salvo após o update final.
- Ambiente: Windows 11, Python 3.14.7, PyTorch 2.13.0+rocm10.0.0, Transformers 4.56.2, AMD Radeon RX 7600. Tempo de treino: 2.834,67 s (47,24 min); pico de memória alocada: 3,03 GiB. Inferência do holdout: 124,42 s.

## Resultado da única avaliação

| Métrica | Resultado |
|---|---:|
| Acurácia | 45,966% |
| Macro-F1 | 44,523% |
| Loss média | 1,0429 |

| Classe | Suporte | Recall |
|---|---:|---:|
| `c1` | 952 | 51,261% |
| `c234` | 1.036 | 24,131% |
| `c5` | 1.036 | 62,934% |

Matriz de confusão (linhas = classe verdadeira; colunas = classe prevista; ordem `c1`, `c234`, `c5`):

```text
[[488, 188, 276],
 [353, 250, 433],
 [194, 190, 652]]
```

O recall baixo de `c234` e as confusões com as duas classes adjacentes continuam sendo a principal limitação observada. A acurácia é descritivamente próxima da média de validação agrupada dos folds internos (45,007%); os conjuntos e a execução não permitem alegar ganho. Como definido antes da consulta, este resultado serve à auditoria e não justifica retuning. A regra congelada da 5e permanece inalterada.

## Artefatos

- Runner: `src/run_stage5f_holdout_audit.py`.
- Execução e integridade: `runs/etapa5f/etapa5f_start512_lr2e5_audit_20260926/audit.json`.
- Métricas: `runs/etapa5f/etapa5f_start512_lr2e5_audit_20260926/metrics.json`.
- Previsões por índice, rótulo verdadeiro, previsão e probabilidades: `runs/etapa5f/etapa5f_start512_lr2e5_audit_20260926/holdout_predictions.csv`.
- Log de treino: `runs/etapa5f/etapa5f_start512_lr2e5_audit_20260926/training.jsonl`.
- Checkpoint da auditoria: `models/bert_stage5f/etapa5f_start512_lr2e5_audit_20260926/final/`.

A Etapa 5 está concluída. A Etapa 6, que treinará o modelo integral com os 20.092 exemplos segundo a especificação congelada, ainda requer autorização própria.
