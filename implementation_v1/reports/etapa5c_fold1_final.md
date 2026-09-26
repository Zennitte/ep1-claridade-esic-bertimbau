# Etapa 5c — Comparação dos dois finalistas no fold 1

**Data:** 25/09/2026. **Status:** concluída. **Holdout:** não consultado. O treino Original do fold 1 contém 11.488 linhas e a validação integral contém 5.580 linhas em ambas as corridas.

## Protocolo

Ambos os candidatos usaram BERTimbau `neuralmind/bert-base-portuguese-cased`, seed `20260924`, taxa `2e-5`, microbatch 2, acumulação 4, lote efetivo 8, até duas épocas, validação a cada 384 passos e no fim de época, e a regra de early stopping da 5b. O checkpoint é escolhido por acurácia de validação, com macro-F1 como desempate. A única diferença planejada entre os candidatos é a representação/comprimento: início com 512 tokens versus início + fim com 256 tokens.

| Candidato | Melhor passo | Épocas percorridas | Acurácia | Macro-F1 | Recall `c1` | Recall `c234` | Recall `c5` | Tempo | Pico GPU alocada |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `start512_lr2e5` | 2.688 | 2,000 | **45,14%** | 44,51% | 48,92% | 30,21% | 56,31% | 70,69 min | 3,25 GB |
| `headtail256_lr2e5` | 1.436 | 1,604 | 44,80% | **44,64%** | 51,19% | 34,50% | 49,07% | 35,64 min | 2,37 GB |

O candidato de 256 tokens parou por early stopping no passo 2.304 após três avaliações sem melhora elegíveis; seu melhor checkpoint foi salvo no fim da primeira época. O candidato de 512 tokens completou as duas épocas, com melhor checkpoint no passo 2.688. Ambos tiveram checkpoint recarregado, logits finitos `[5,3]` e zero linhas descartadas por acumulação incompleta em cada época.

No mesmo fold, o baseline TF-IDF `C=0,5` obteve 44,61% de acurácia e 44,35% de macro-F1. O modelo de 512 tokens ficou aproximadamente **+0,54 pp / +0,16 pp** acima; o de 256 tokens, **+0,20 pp / +0,29 pp**. São diferenças pequenas em um único fold.

## Decisão da 5c

`start512_lr2e5` vence pela acurácia, 45,143% contra 44,803% (**+0,341 pp**). O `headtail256_lr2e5` tem macro-F1 **+0,137 pp** maior, mas essa métrica é apenas desempate quando a acurácia é igual. Assim, **`start512_lr2e5` é o BERT de referência congelado para a futura ablação 5c.1**. Isso não é a escolha definitiva do modelo ou da política de dados: ambos os finalistas ainda serão considerados em 5d sob a política de dados escolhida.

O padrão por classe difere: 256 tokens teve recalls maiores em `c1` e `c234`, enquanto 512 tokens teve recall maior em `c5`. Matrizes de confusão, losses por avaliação e demais detalhes estão nos `metrics.json` abaixo. Nenhum ganho causal da janela ou da representação pode ser isolado nesta comparação, porque as duas propriedades mudaram juntas.

## Artefatos

- 512 tokens: `runs/etapa5/etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed/metrics.json` e `models/bert_stage5/etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed/best/`.
- 256 tokens: `runs/etapa5/etapa5c_headtail256_lr2e5_fold1_20260925_resume/metrics.json` e `models/bert_stage5/etapa5c_headtail256_lr2e5_fold1_20260925_resume/best/`.
- Curvas de ambos: `reports/etapa5/`.
- Registro da primeira sessão: `reports/etapa5c_fold1_partial.md`, preservado como histórico.

A 5c.1 permanece pendente e requer autorização específica. Nenhuma variante B/C foi gerada ou treinada nesta sessão.
