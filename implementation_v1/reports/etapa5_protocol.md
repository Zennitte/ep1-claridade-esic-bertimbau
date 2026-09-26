# Etapa 5b — Protocolo comum de duração e avaliação

**Status:** concluída.  
**Configuração de referência:** `configs/bert_stage5_protocol.json`.  
**Holdout:** não consultado.

## Regra definida

Os dois finalistas (`start512_lr2e5` e `headtail256_lr2e5`) serão avaliados nos folds 1, 2 e 3 com o conjunto completo de treino e validação de cada fold. Cada execução terá no máximo duas épocas. A execução pode terminar antes se a acurácia de validação deixar de melhorar em três avaliações consecutivas, contadas a partir de avaliações feitas no passo 512 ou depois.

A acurácia de validação seleciona o checkpoint; macro-F1 desempata. A comparação com TF-IDF usa `C=0.5` e o resultado da validação do mesmo fold já registrado em `runs/etapa2/baseline_20260924_1724/metrics.json`.

## Cadência e duração em passos

- Lote físico de 2 exemplos, acumulação de 4 lotes e lote efetivo de 8 exemplos, iguais à configuração da Etapa 4.
- Avaliação da validação completa a cada 384 passos do otimizador e no fim de cada época. Se os eventos coincidirem, conta uma única avaliação.
- O número máximo previsto é de 2.872 passos no fold 1, 2.862 no fold 2 e 2.798 no fold 3. Os folds têm tamanhos diferentes, portanto a regra comum é em épocas, não um número idêntico de passos.
- Um grupo incompleto de acumulação é descartado no fim da época. Ele não atravessa a fronteira para a época seguinte. Isso evita misturar gradientes de épocas distintas. O número máximo de exemplos omitidos por época é pequeno e fica registrado nas métricas da execução.
- Mesma semente (`20260924`), mesmo checkpoint pré-treinado, mesmos hiperparâmetros de otimização e mesmas divisões para os dois finalistas. O holdout não participa.

## Justificativa e relação com 5a

A Etapa 4 já limitava as corridas a duas épocas e usava parada antecipada com mínimo de 512 passos e paciência de três avaliações. O intervalo de 384 passos mantém avaliações frequentes o bastante para observar a evolução, reduzindo o custo de percorrer a validação completa dos folds, que é bem maior que a amostra de desenvolvimento usada na Etapa 4. A avaliação extra nos limites das épocas garante que cada época seja medida mesmo quando seu número de passos não é múltiplo de 384.

A corrida preliminar `start512_lr2e5` da subdivisão 5a parou no passo 896, equivalente a 0,624 época, e ainda não percorreu o conjunto de treino do fold. Ela fica preservada como exploração e não entra como comparação equivalente. Em 5c, esse candidato será reexecutado junto com `headtail256_lr2e5` sob este protocolo.

## Ajuste de implementação

`src/bert_stage4.py` agora encerra a acumulação dentro de cada época, avalia no limite da época e conta a paciência de early stopping somente nas avaliações a partir do passo mínimo. As corridas históricas e seus arquivos não foram alterados. A implementação passa a descartar, por época, os poucos exemplos que não completam um grupo de acumulação; essa contagem será registrada em cada execução.

## Próxima subdivisão

A subdivisão 5c comparará os dois finalistas no fold 1 e repetirá `start512_lr2e5` com validação completa. Nenhuma corrida de 5c foi iniciada nesta sessão.
