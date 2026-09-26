# Classificação de clareza de respostas e-SIC

Código do EP1 de ACH2118. O objetivo é classificar respostas em `c1`, `c234` e `c5`. O modelo final usa BERTimbau Base com até 512 tokens. O código e as configurações estão aqui; planilhas de entrada, predições, relatórios de execução e pesos do modelo não são publicados.

## Estrutura

- `src/audit_and_split.py`: auditoria e divisão por grupos de textos normalizados.
- `src/run_baseline.py`: referência TF-IDF com regressão logística.
- `src/bert_stage4.py` e scripts `src/run_stage5*.py`: busca, confirmação e auditoria no holdout.
- `configs/bert_stage5_final.json`: especificação congelada antes do holdout.
- `src/run_stage6_final.py`: treinamento final com todas as 20.092 linhas.
- `src/predict_final.py`: inferência em textos informados na linha de comando.
- `src/predict_test_xlsx.py`: predição em planilha com `resp_text` e `clarity`.

## Reproduzir

O ambiente usado está descrito em [ENVIRONMENT.md](ENVIRONMENT.md). O arquivo `requirements.lock.txt` registra as versões; os pacotes ROCm da AMD dependem de uma instalação compatível com o sistema. Use Python 3.14 e uma GPU compatível com ROCm para repetir o treinamento final. Obtenha `train.xlsx` e `test1.xlsx` pelo canal autorizado da disciplina; eles não estão neste repositório.

1. Instale as dependências listadas em `requirements.lock.txt`, observando as instruções ROCm da AMD para PyTorch.
2. Coloque `train.xlsx` na raiz e execute `python src/audit_and_split.py`. O script verifica o SHA-256 da planilha original usado no EP1 (`0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818`). Uma versão diferente exige nova auditoria e novo protocolo.
3. Execute `python src/run_stage6_final.py --run-id reproducao_01`. O script verifica os hashes da configuração e da divisão, exige GPU ROCm e grava o checkpoint em `models/bert_final/`. Execute em uma cópia sem esse diretório, pois o script preserva checkpoints existentes.
4. Execute `python src/predict_test_xlsx.py test1.xlsx test1_predito.xlsx --sheet test1 --device cuda`. O comando preserva a planilha de entrada e preenche `clarity` na cópia.

O protocolo de avaliação usa holdout externo por grupos de textos normalizados e três divisões internas com `StratifiedGroupKFold`. A acurácia do BERTimbau no holdout foi 45,966%; a regressão logística com TF-IDF obteve 45,437% nas mesmas linhas. A diferença de 0,529 ponto percentual foi pequena (McNemar exato, `p = 0,590`). O checkpoint final foi treinado em todas as linhas após essa auditoria; como `test1.xlsx` não contém rótulos, sua acurácia não é conhecida.
