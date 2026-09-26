# Etapa 6 — Treinamento integral e empacotamento

**Status:** concluída em 26/09/2026, 10:40 BRT. O modelo final foi ajustado conforme a especificação congelada na 5e e passou pela checagem de recarga. A auditoria de holdout não foi repetida.

## Execução

- Fonte: `train.xlsx`, SHA-256 conferido; 20.092 linhas usadas, com `c1=6.347`, `c234=6.853` e `c5=6.892`. Os índices efetivamente utilizados estão no manifesto CSV do run.
- Modelo: BERTimbau Base `neuralmind/bert-base-portuguese-cased`, revisão `94d69c95f98f7d5b2a8700c420230ae10def0baa`, cabeça nova de três classes, início de texto, limite de 512 tokens.
- Treino: seed `20260924`; AdamW; learning rate `2e-5`; `weight_decay=0,01`; batch efetivo 8; sem scheduler, warmup, validação ou early stopping; **4.523 updates** (1,8013 épocas equivalentes conforme os passos efetivos por época).
- Ambiente: Windows 11, Python 3.14.7, PyTorch 2.13.0+rocm10.0.0, Transformers 4.56.2, AMD Radeon RX 7600.
- Duração do treino: 3.401,84 s (56,70 min). Pico de memória GPU alocada: 3.266.404.352 bytes (3,04 GiB).

O resultado 5f indicou limitações de generalização, principalmente recall baixo de `c234`. A configuração foi mantida como congelada; o resultado do holdout não foi usado para retuning. Conforme o protocolo decidido antes da auditoria, os exemplos do holdout agora fazem parte do treino final. Portanto, o modelo final não deve ser reavaliado nesse mesmo holdout; a avaliação posterior usa `test1.xlsx`, arquivo de teste confirmado pelo usuário depois da conclusão desta etapa.

## Validação do artefato

O modelo e tokenizer foram salvos em `models/bert_final/` e recarregados localmente. Em cinco linhas de treino conhecidas, as previsões repetidas foram idênticas; logits e probabilidades tiveram forma `[5, 3]`; as probabilidades foram finitas e somaram 1 por linha; todas as classes previstas pertencem ao mapeamento congelado `c1/c234/c5`. A validação passou.

## Uso

Classifique um texto no PowerShell:

```powershell
.\.venv\Scripts\python.exe src\predict_final.py --text "Texto da resposta a classificar" --device cpu
```

Pode-se repetir `--text` para classificar um lote pequeno. `--device auto` (padrão) usa a GPU disponível; `--device cpu` força a CPU.

## Artefatos

- Modelo e tokenizer: `models/bert_final/`.
- Execução, configuração, log e hashes: `runs/etapa6/etapa6_final_20260926/`.
- Manifesto de índices usados: `runs/etapa6/etapa6_final_20260926/train_indices.csv`.
- Resumo estruturado: `reports/etapa6/etapa6_final_20260926_summary.json`.
- Runner de treino: `src/run_stage6_final.py`.
- Comando de inferência: `src/predict_final.py`.

A Etapa 6 terminou. A Etapa 7 permanece pendente; `test1.xlsx` não foi aberto nem usado nesta etapa.
