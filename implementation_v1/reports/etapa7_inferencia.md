# Etapa 7 — Inferência no conjunto de teste

**Data:** 26/09/2026 11:05 BRT  
**Run:** `etapa7_20260926_105326_ca987906`

## Protocolo

Aplicado o modelo final validado da Etapa 6 (`models/bert_final/`) às 900 respostas da aba `test1` de `test1.xlsx`. Inferência em lotes de 8, truncamento em até 512 tokens e classes `c1`, `c234` e `c5`. Nenhum rótulo do conjunto de teste foi usado para seleção ou avaliação; a coluna `clarity` estava vazia antes da execução.

A primeira tentativa de inferência na GPU dentro do sandbox falhou com erro de kernel ROCm. Após a solicitação do usuário, a inferência foi executada fora do sandbox na AMD Radeon RX 7600 e concluiu com sucesso em 43,45 segundos. A distribuição predita foi `c1`: 319, `c234`: 176, `c5`: 405. Essas contagens descrevem as previsões; não são métricas de acurácia.

## Verificação da saída

- Arquivo final: `outputs/etapa7_20260926_105326_ca987906/test1_predito.xlsx`.
- Aba `test1`, 900 linhas de dados e cabeçalhos `resp_text`, `clarity` preservados.
- As 900 células de predição foram preenchidas; todas pertencem às três classes esperadas.
- A coluna `resp_text` permaneceu idêntica à original. O arquivo de entrada permaneceu intacto (SHA-256 `e626f030d4bf2be889fc41dd1fe9b81fb31f1f50f3ace50530d658683260449f`).
- O `.xlsx` exportado foi reaberto com Artifact Tool e validado; a amostra visual confirmou o cabeçalho e valores na posição existente, sem criar aba ou coluna.
- SHA-256 da saída: `4e6e149ad9f9407b51890ee0c4e31a09589568d090e765293864945ee7e24a8c`.

Evidências e metadados: `runs/etapa7/etapa7_20260926_105326_ca987906/`.

**Limite:** como o arquivo é conjunto de teste sem rótulos, nenhuma métrica de desempenho no teste pode ser calculada nesta etapa.
