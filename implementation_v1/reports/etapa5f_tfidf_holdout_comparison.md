# Comparação no holdout: TF-IDF + regressão logística versus BERT

**Data:** 26/09/2026 11:14 BRT  
**Run:** `etapa5f_tfidf_holdout_20260926_1115`

## Protocolo

A pedido do usuário, ajustei o baseline TF-IDF + regressão logística nos mesmos 17.068 índices de desenvolvimento usados pelo BERT da auditoria 5f e avaliei ambos nos mesmos 3.024 índices do holdout. O hiperparâmetro foi fixado antes de consultar o holdout: `C=0,5`, escolhido pela validação agrupada da Etapa 2. Mantive unigramas e bigramas, `min_df=3`, até 100.000 termos, normalização L2, `sublinear_tf=True`, `lowercase=True`, `lbfgs` e até 400 iterações. O ajuste terminou em 44 iterações. Nenhum ajuste de parâmetros foi feito com base no holdout.

Hashes da fonte e da divisão foram conferidos. Os índices, rótulos verdadeiros e previsões BERT foram alinhados linha a linha; as métricas BERT recalculadas reproduziram o `audit.json` da 5f.

## Resultados no mesmo holdout

| Modelo | Acurácia | Macro-F1 |
|---|---:|---:|
| TF-IDF + regressão logística (`C=0,5`) | **45,437%** | **45,056%** |
| BERT `start512_lr2e5` | 45,966% | 44,523% |
| Diferença BERT − TF-IDF | +0,529 p.p. | −0,533 p.p. |

Em acurácia, o BERT acertou 16 das 3.024 respostas a mais. O TF-IDF teve macro-F1 maior, principalmente por recall melhor em `c234` (33,69%, contra 24,13% do BERT); o BERT teve recall maior em `c1` (51,26% contra 45,06%) e `c5` (62,93% contra 57,53%).

Como as previsões são pareadas nos mesmos exemplos, apliquei o teste exato de McNemar: o BERT acertou exclusivamente 395 casos e o TF-IDF acertou exclusivamente 379; `p=0,590`. A diferença observada não fornece evidência de vantagem estatisticamente clara de acurácia para um dos modelos.

## Conclusão e artefatos

Os resultados no holdout são muito próximos. A vantagem de 0,53 ponto do BERT em acurácia é pequena e vem acompanhada de macro-F1 inferior; portanto, não sustenta afirmar superioridade geral. Esse resultado é uma comparação retrospectiva no holdout solicitado, não altera parâmetros nem a decisão congelada do protocolo.

- Métricas, hashes, configuração e versões: `runs/etapa5f/etapa5f_tfidf_holdout_20260926_1115/comparison.json`.
- Previsões pareadas por linha: `runs/etapa5f/etapa5f_tfidf_holdout_20260926_1115/predictions.csv`.
- Modelo ajustado: `models/baseline/etapa5f_tfidf_holdout_20260926_1115/tfidf_logreg_C_0_5.joblib`.
- Runner reproduzível: `src/run_stage5f_tfidf_holdout.py`.
