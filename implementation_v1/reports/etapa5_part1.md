# Etapa 5 — parte 1: confirmação inicial no fold 1

**Data:** 24/09/2026. **Escopo de hoje:** um candidato em um fold completo. A Etapa 5 continua pendente para os demais folds e para o segundo finalista.

## Protocolo executado

- Finalista: BERTimbau Base, representação início, 512 tokens, taxa `2e-5`, seed `20260924`.
- Fold agrupado 1: loader de treino baseado nas 11.488 linhas do fold e validação completa com 5.580 linhas. Sem interseção com o holdout; a validação final não foi consultada.
- O checkpoint de triagem teve melhor acurácia no passo 896. No fold 1, treinamos até esse passo e avaliamos toda a validação nos passos 384, 768 e 896 para controlar o custo. Isso corresponde a 0,624 época: 7.168 exemplos passaram pelo treino, não todas as 11.488 linhas.
- Baseline reproduzido na Etapa 2 para o mesmo fold, TF-IDF + logística `C=0,5`: 44,61% de acurácia e 44,35% de macro-F1.

## Resultado

| Passo | Acurácia | Macro-F1 | Loss de validação |
| ---: | ---: | ---: | ---: |
| 384 | 39,25% | 36,45% | 1,0934 |
| 768 | 42,15% | 41,52% | 1,0656 |
| 896 (melhor) | **43,85%** | **43,23%** | 1,0616 |

No passo 896, recalls por classe: `c1` 44,43%, `c234` 30,74%, `c5` 56,16%. Em relação ao baseline do fold, este BERT ficou **0,76 ponto percentual abaixo em acurácia** e **1,12 ponto abaixo em macro-F1**. A comparação ainda é preliminar: o TF-IDF foi ajustado em todas as 11.488 linhas de treino, enquanto o BERT, parado em 0,624 época, processou 7.168 delas. É uma única confirmação de fold, com treino parcial, e não basta para descartar os outros finalistas nem para concluir o resultado final. Na continuação, precisamos definir uma duração comparável e aplicá-la de forma consistente entre folds.

## Custo e artefatos

- Tempo de parede: **1.376,361 s (22,94 min)**; pico de memória GPU alocada: **3.247.774.720 bytes (3,25 GB)**.
- O checkpoint foi recarregado; gerou logits finitos com forma `[5,3]` e rótulos válidos.
- Métricas: `runs/etapa5/etapa5_start512_lr2e5_fold1_full_20260924_2300/metrics.json`.
- Configuração congelada para esta corrida: `configs/bert_stage5.json`; código de treino generalizado: `src/bert_stage4.py`.
- Checkpoint: `models/bert_stage5/etapa5_start512_lr2e5_fold1_full_20260924_2300/best/`.
- Curvas: `reports/etapa5/etapa5_start512_lr2e5_fold1_full_20260924_2300_accuracy.svg` e `reports/etapa5/etapa5_start512_lr2e5_fold1_full_20260924_2300_loss.svg`.

## Retomada

O usuário reservou mais quatro horas amanhã para a Etapa 5 e autorizou continuar além dessa janela se necessário para concluir a confirmação dos dois finalistas nos folds 2 e 3. Retomar definindo uma duração comum e aplicando-a consistentemente aos candidatos/folds. Registrar a média e a variação somente quando houver folds suficientes. Não consultar o holdout até fixar família, representação, hiperparâmetros e duração de treino.
