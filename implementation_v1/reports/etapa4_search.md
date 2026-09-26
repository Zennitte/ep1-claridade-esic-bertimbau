# Etapa 4 — triagem do BERTimbau e curvas de aprendizado

**Data:** 24/09/2026. **Status:** concluída após complemento autorizado. Foram avaliadas oito configurações BERT em um único subconjunto fixo de desenvolvimento; a seleção ainda precisa de confirmação por folds.

## Protocolo

- Fonte: `train.xlsx`, SHA-256 `0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818`.
- Divisão: `data/splits_grouped_v1.json`, SHA-256 `aa9c99a79ccccc3655399761c53098f5fd3d770c9aa6c8b68be29c49eba3586b`. Holdout final de 3.024 linhas preservado, sem avaliação.
- Subconjunto fixo do fold 1: `data/stage4_subset.json`, ID `stage4_fold1_stratified_4096_1024_seed_20260924`, com 4.096 linhas de treino e 1.024 de validação. As mesmas linhas foram usadas nas oito variantes e no TF-IDF.
- BERTimbau Base (`neuralmind/bert-base-portuguese-cased`), semente `20260924`, duas épocas máximas, microbatch 2, acumulação 4 (lote efetivo 8), AdamW, `weight_decay=0,01`, avaliação a cada 128 passos. Parada antecipada a partir do passo 512, com paciência de três avaliações. Melhor checkpoint escolhido pela acurácia de validação; macro-F1 secundário.
- TF-IDF + regressão logística `C=0,5`, ajustado nas mesmas 4.096 linhas: **44,24%** de acurácia e **43,90%** de macro-F1 nas mesmas 1.024 linhas. A média de **44,71%** da Etapa 2 vem de três folds completos e não é comparação direta desta triagem.

## Resultados ordenados por acurácia

| Representação | Tokens | Taxa | Melhor passo | Acurácia | Macro-F1 | Diferença para TF-IDF | Tempo | Pico GPU | Validação acima da janela |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Início | 512 | `2e-5` | 896 | **45,80%** | **45,35%** | **+1,56 pp** | 18,68 min | 3,26 GB | 99 (9,7%) |
| Início + fim | 256 | `2e-5` | 896 | **45,21%** | **44,13%** | **+0,98 pp** | 12,38 min | 2,37 GB | 357 (34,9%) |
| Início + fim | 512 | `2e-5` | 896 | **45,21%** | 43,48% | **+0,98 pp** | 18,86 min | 3,26 GB | 99 (9,7%) |
| Início + fim | 512 | `3e-5` | 1.024 | 44,82% | 43,90% | +0,59 pp | 18,80 min | 3,26 GB | 99 (9,7%) |
| Início | 512 | `3e-5` | 896 | 44,04% | 43,11% | −0,20 pp | 18,81 min | 3,26 GB | 99 (9,7%) |
| Início + fim | 256 | `3e-5` | 896 | 43,07% | 41,38% | −1,17 pp | 12,42 min | 2,37 GB | 357 (34,9%) |
| Início | 256 | `2e-5` | 128 | 41,60% | 41,37% | −2,64 pp | 6,22 min | 2,37 GB | 357 (34,9%) |
| Início | 256 | `3e-5` | 128 | 40,72% | 40,25% | −3,52 pp | 6,24 min | 2,37 GB | 357 (34,9%) |

“Acima da janela” conta textos com mais tokens que o limite. A seleção início + fim retém as duas extremidades e descarta parte do meio quando necessário; não perde todo o fim. O lote efetivo e `weight_decay` ficaram fixos.

## Curvas e interpretação

Os gráficos comparam candidatos de cada comprimento à linha do TF-IDF: [256 tokens](etapa4/comparison_accuracy_256.svg) e [512 tokens](etapa4/comparison_accuracy_512.svg). As curvas individuais de acurácia e loss e o [resumo numérico](etapa4/comparison_summary.json) também estão em `reports/etapa4/`.

Na janela de 512, início com `2e-5` foi o melhor. Início + fim com `2e-5` teve a mesma acurácia arredondada que início + fim com 256, mas macro-F1 inferior e custo maior. Elevar a taxa para `3e-5` não melhorou o início; para início + fim com 512, ficou 0,39 pp abaixo de `2e-5`. Na janela de 256, início + fim com `3e-5` superou início com `3e-5`, mas não o TF-IDF. No geral, a taxa maior não mostrou ganho consistente.

As métricas oscilaram entre avaliações. Dois melhores pontos ocorreram no passo 896, e início + fim com 512 e `3e-5` ainda melhorava no passo 1.024; não há evidência suficiente para localizar uma saturação comum. Acurácias dos melhores candidatos incluem escolha entre várias avaliações e pertencem a uma única validação; não indicam superioridade estável.

## Finalistas provisórios para a Etapa 5

1. **Início, 512 tokens, `2e-5`:** maior acurácia e macro-F1 observados; priorizar a confirmação por folds.
2. **Início + fim, 256 tokens, `2e-5`:** acurácia 0,59 pp abaixo do primeiro, macro-F1 de 44,13%, com 6,30 minutos a menos e aproximadamente 0,88 GB a menos de pico. Mantém uma opção mais econômica.

Início + fim com 512 e `2e-5` empatou em acurácia com o candidato de 256, mas não melhorou o macro-F1 e custou 6,48 minutos a mais. Portanto, não entra entre os dois finalistas. Os números não estabelecem que qualquer BERT supera o baseline fora deste subconjunto. A Etapa 5 deve confirmar os dois finalistas nos folds agrupados e consultar o holdout uma única vez depois de fixar a escolha.

## Custo e reprodutibilidade

As quatro corridas iniciais consumiram 2.610,998 s (43,52 min). O complemento autorizado consumiu **4.133,263 s (68,89 min)**; a Etapa 4 inteira consumiu **6.744,261 s (112,40 min)**. Somados cerca de 126,417 s da Etapa 3 e 9,44 s de comando da Etapa 0, o total experimental é aproximadamente **114,67 min**. Restam aproximadamente **5–125 min** de um orçamento total de 2–4 horas. O custo real ficou maior que a estimativa inicial para as variantes de 512 tokens; cada corrida levou cerca de 18,7–18,9 min. A Etapa 5 deverá priorizar a confirmação de um finalista se o limite efetivo estiver perto de duas horas.

Comandos usados: `python src/bert_stage4.py <id> --run-id <id_de_execucao>` para cada candidato; `python src/baseline_stage4_subset.py`; `python src/summarize_stage4.py`. As corridas BERT usaram a RX 7600 fora do isolamento de comandos do Codex, necessário devido ao erro ROCm `hipErrorInvalidImage` dentro dele. Métricas por execução estão em `runs/etapa4/stage4_*/metrics.json`; checkpoints em `models/bert_stage4/stage4_*/best/`. Todos os oito checkpoints foram recarregados com logits finitos `[5,3]` e rótulos válidos. Configuração: `configs/bert_stage4.json`; código de treino: `src/bert_stage4.py`.
