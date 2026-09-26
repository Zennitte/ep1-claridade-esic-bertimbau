# Ambiente do EP1

Ambiente verificado em 24/09/2026 no Windows 11 com Python 3.14.7 em `.venv` e AMD Radeon RX 7600 (8 GiB). O snapshot exato das bibliotecas instaladas está em `requirements.lock.txt`. O PyTorch 2.13.0+rocm10.0.0 e seus pacotes AMD vieram da instalação ROCm já existente; uma instalação nova desses pacotes pode exigir o índice e as instruções da AMD. Não substituir essa instalação por uma versão de PyTorch sem ROCm.

**Nota da Etapa 3:** no ambiente isolado de comandos do Codex, operações ROCm falharam com `hipErrorInvalidImage`. O mesmo código de fine-tuning funcionou quando executado fora desse isolamento. Isso é uma limitação observada na execução por agente, não uma falha de memória da RX 7600.

## Verificação única

Na raiz do projeto, execute:

```powershell
.\.venv\Scripts\python.exe src\verify_environment.py
```

O comando lê `train.xlsx` e `ep1-enunciado.pdf`, carrega o tokenizer de `neuralmind/bert-base-portuguese-cased` e executa um passo de treino na GPU (forward, backward e atualização de pesos). A primeira execução pode baixar o tokenizer. O resultado é gravado em `runs/etapa0/verification.json`. O script falha se a GPU não for detectada ou se os pesos não mudarem.

## Convenção para as próximas etapas

- `src/`: código executável.
- `configs/`: parâmetros fixados por experimento.
- `data/`: índices de divisões e manifestos; os arquivos de entrada originais permanecem intactos.
- `runs/<id>/`: configuração, log, métricas, duração de parede e de GPU, uso de memória e ID do checkpoint.
- `models/<id>/`: checkpoints, tokenizer e manifesto do modelo.
- `reports/`: tabelas, figuras e relatório.

Cada execução futura deve usar um ID único, registrar semente, hash das entradas e versões do ambiente. Os arquivos originais e checkpoints grandes não devem entrar no Git.
