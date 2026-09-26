# Plano de implementação — EP1 de PLN: clareza de respostas do e-SIC

**Versão inicial:** 23/09/2026  
**Prazo oficial:** 04/10/2026  
**Objetivo:** obter e entregar um classificador de três classes que supere o baseline oficial de TF-IDF + regressão logística, com experimento reproduzível, modelo treinado, relatório, apresentação em PDF e planilha de teste rotulada.

## 1. Contexto e decisões já estabelecidas

- Fontes: `ep1-enunciado.pdf`, `train.xlsx` e `test1.xlsx` (arquivo do conjunto de teste, confirmado pelo usuário em 26/09/2026). Não ler nem inferir sobre o teste antes da autorização para a Etapa 7.
- `train.xlsx`: 20.092 respostas, colunas `resp_text` e `clarity`; classes observadas `c1` (6.347), `c234` (6.853), `c5` (6.892). A classe majoritária é cerca de 34,3%.
- **Correção da anotação inicial (24/09/2026):** a página 2 de `ep1-enunciado.pdf` menciona `{c1, c234, c5}`, em acordo com a planilha. A afirmação anterior de que o enunciado mencionava `c6` estava incorreta. Usar `c5`; confirmar o formato de saída quando o arquivo de teste definitivo estiver disponível.
- Há 18.143 textos distintos após normalização simples de caixa e espaços; 2.449 linhas pertencem a grupos repetidos, e 316 desses grupos apresentam rótulos conflitantes (1.975 linhas). Isso motiva divisão por grupos e análise de ruído, sem apagar ou arbitrar rótulos contraditórios por padrão.
- Tamanho mediano da resposta: 101 palavras; percentil 90: 309 palavras. Comparar a seleção de trechos sob limite de tokens.
- Modelo principal proposto: **BERTimbau Base com fine-tuning para classificação em três classes**. Referência obrigatória: TF-IDF + regressão logística. Alternativa de menor custo: embeddings de BERTimbau congelado + classificador, se o benchmark inviabilizar a busca com fine-tuning. Uma estratégia início + fim ou por trechos só entra se houver tempo e evidência de ganho.
- Orçamento inicial de GPU para **busca experimental** nas Etapas 0–4: 2–4 horas na RX 7600; o treinamento final é uma etapa adicional. O usuário concedeu à Etapa 5 uma janela própria de quatro horas amanhã, sem prendê-la ao saldo desse orçamento inicial. Disponibilidade e desempenho reais da GPU devem ser medidos, nunca presumidos. O resultado anterior de cerca de 46% com TF-IDF é histórico e não comparável até reproduzir a mesma avaliação.
- Meta de calendário: escolher configuração até 27/09; treinar o modelo final entre 28 e 30/09; concluir inferência, relatório, apresentação e conferência até 03/10, reservando 04/10 para a entrega.

## 2. Contrato de execução por etapas

**Instrução ao agente executor:** este arquivo é a fonte de verdade do progresso. Em cada sessão, leia-o integralmente, identifique a primeira etapa `Pendente` ou `Em andamento`, leia os artefatos e o registro da etapa anterior e execute **somente essa etapa**. A autorização do usuário para iniciar uma etapa não autoriza começar a seguinte.

1. No início, mude o status da etapa autorizada para `Em andamento` e registre data/hora, ambiente e objetivo da sessão. Pode fazer todos os subtarefas necessários **dentro da etapa autorizada**.
2. Ao terminar, salve código, configurações, modelos e métricas nos caminhos estáveis do projeto; preencha o registro da etapa com resultados reais, comandos, duração, decisões, limitações e evidências. Marque `Concluída` apenas depois de cumprir seus critérios de saída e de persistir os arquivos. Se não cumprir, deixe `Em andamento` ou `Bloqueada`, explique a causa e proponha a correção ainda nessa etapa.
3. Mostre ao usuário um resumo do que foi feito e os arquivos produzidos. **Pare e peça autorização explícita para iniciar a próxima etapa.** Não avance por inferência, silêncio ou passagem de tempo. Se houver várias sessões, retome a mesma etapa até concluí-la.
4. Se o tempo de GPU acabar, registre consumo acumulado, resultados parciais e uma decisão de redução de escopo para aprovação do usuário. Não apresente uma busca incompleta como prova de hiperparâmetros ideais.
5. Uma correção necessária em etapa concluída deve ser anotada como revisão, com motivo, impacto nas métricas posteriores e nova validação. Não apague resultados antigos. Salve o plano atualizado ao fim de **cada** sessão, inclusive quando estiver bloqueada, para que a janela do agente possa ser fechada com segurança.

### Convenções de registro e arquivos

Estrutura sugerida, ajustável ao repositório existente: `src/` para código, `configs/` para configurações, `data/` para entradas e índices de divisão, `runs/` para métricas e logs por execução, `models/` para checkpoints e artefatos finais, `reports/` para tabelas e figuras. Não versionar dados privados ou checkpoints grandes em Git sem uma decisão explícita; manter um manifesto dos caminhos e identificadores. Usar nomes estáveis, semente fixa, versões de dependências, hash ou identificador dos arquivos de entrada e ID único por execução. Todo experimento deve registrar configuração, divisão, tempo de GPU/parede, métricas e checkpoint correspondente.

Na seção **Diário de execução**, preencher uma entrada por sessão, mesmo que a etapa não termine. Não substituir valores `A medir` por números estimados. Salvar o plano e os artefatos em armazenamento persistente entre sessões; se estiver em um repositório, fazer commit das mudanças de código e documentação ao fim da etapa quando apropriado.

## 3. Métricas e protocolo de decisão

- **Métrica primária:** acurácia, como no EP. Secundárias: macro-F1, acurácia/recall por classe, matriz de confusão, média e desvio entre folds, tempo de treino e memória de GPU. Registrar métricas de treino e validação para identificar overfitting.
- **Divisão:** guardar uma validação final agrupada por texto normalizado (proposta inicial: aproximadamente 15%; ajustar caso a estratificação fique ruim). Dentro do restante, usar folds estratificados por classe e agrupados por texto para comparar finalistas. Fixar índices e semente. Qualquer limpeza aprendida, vetorização e ajuste de classificadores devem ocorrer **dentro do treino de cada fold**; a validação final não participa da busca.
- **Grupos:** agrupar respostas com caixa/espaços normalizados; manter as linhas com rótulos conflitantes e seus rótulos originais. Verificar interseção zero de grupos entre lados das divisões. Se a distribuição das classes ficar inadequada, documentar e ajustar a divisão antes dos experimentos.
- **Seleção:** preferir maior acurácia média de validação; usar macro-F1, estabilidade, desempenho por classe e custo conforme o protocolo declarado antes dos resultados. A ablação 5c.1 compara políticas de conflito sem trocar o BERT de referência; 5d confirma o efeito nos folds restantes antes de congelar a política de dados. Reportar sempre a diferença frente ao TF-IDF reproduzido no mesmo protocolo. Não afirmar superioridade baseada apenas no treino ou em uma única execução ruidosa.
- **Validação final:** consultar **uma vez**, após fixar família, representação, hiperparâmetros, duração e política de dados com os folds; usá-la como auditoria de generalização. Não escolher política de conflitos a partir desse resultado. Se ela revelar erro objetivo ou vazamento que exija revisão, registrar que deixou de ser uma estimativa independente e criar nova estratégia de avaliação.
- **Treino final:** após a seleção, aplicar mecanicamente a política de dados congelada e treinar com os rótulos disponíveis que ela retiver, usando hiperparâmetros e número de passos/épocas escolhidos a partir das curvas dos folds. Sem conjunto de validação, não alegar `early stopping` nessa execução. Alternativamente, preservar um conjunto de validação para monitorar e salvar o melhor checkpoint, explicitando que o modelo não foi ajustado com 100% das linhas retidas. Escolher e registrar uma dessas duas opções em 5e, antes de 5f e do treino final.

## 4. Etapas e pontos de parada

### Etapa 0 — Preparação do projeto e ambiente

**Status:** Concluída  
**Janela-alvo:** 24/09  
**GPU prevista:** teste curto; consumo medido entra no orçamento total.

**Executar:** identificar repositório/estrutura disponível; preparar ambiente reproduzível com versões fixadas; confirmar leitura dos dois arquivos; verificar PyTorch, tokenizer, armazenamento livre e operação real da RX 7600 com forward, backward e atualização de pesos em um lote pequeno. Evitar instalação ou migração de ambiente sem necessidade; registrar limitações do Windows/ROCm observadas na máquina. Criar comando único de verificação e convenção de logs/checkpoints.

**Saída:** projeto executável, dependências registradas, teste de treino na GPU com tempo/memória observados ou diagnóstico concreto de bloqueio e alternativa viável. **Parar e pedir autorização para a Etapa 1.**

### Etapa 1 — Auditoria dos dados e definição das divisões

**Status:** Concluída  
**Janela-alvo:** 24/09  
**GPU prevista:** nenhuma.

**Executar:** conferir esquema, nulos, classes, duplicatas exatas/normalizadas, conflitos, comprimentos e qualidade textual; examinar casos representativos sem alterar rótulos. Definir normalização conservadora para agrupamento (não presumir que remoção agressiva melhora o modelo). Gerar índices persistidos de validação final e folds, com testes de ausência de vazamento por grupos e contagens por classe. Conferir a alegada discrepância `c6`/`c5` (resolvida: enunciado e planilha usam `c5`).

**Saída:** relatório de auditoria, índices reproduzíveis e protocolo congelado. **Parar e pedir autorização para a Etapa 2.**

### Etapa 2 — Referências e instrumentação de experimentos

**Status:** Concluída  
**Janela-alvo:** 24–25/09  
**GPU prevista:** nenhuma ou mínima.

**Executar:** medir classe majoritária e reproduzir TF-IDF + regressão logística com texto de entrada idêntico e mesma divisão; ajustar apenas uma busca pequena, encapsulada no treino. Calcular acurácia, macro-F1, matriz de confusão e tempo. Implementar registro por execução e gráficos de curvas que também servirão ao BERT. Não usar a validação final para escolher os parâmetros do baseline.

**Saída:** baseline reproduzível com números reais e artefatos de avaliação. Comparar com os ~46% históricos só após verificar protocolo equivalente. **Parar e pedir autorização para a Etapa 3.**

### Etapa 3 — BERTimbau mínimo e benchmark de custo

**Status:** Concluída  
**Janela-alvo:** 25/09  
**GPU prevista:** até 45–75 minutos, condicionado ao benchmark inicial.

**Executar:** montar `AutoTokenizer` e classificador de três classes com mapeamento fixo; começar com BERTimbau Base e janela inicial de texto. Fazer tokenização e batches com padding dinâmico, escolher tamanho de sequência inicial (por exemplo 256) conforme distribuição **real de tokens** e memória disponível. Treinar um pequeno número de batches, depois uma execução curta completa; registrar throughput, memória, tempo por época, loss, acurácia e falhas. Usar semente, checkpoint, `weight_decay` e avaliação periódica. Habilitar early stopping e carregamento do melhor checkpoint nas execuções com validação. Testar se o modelo salvo volta a produzir previsões.

**Decisão de contingência:** se o fine-tuning não rodar de forma estável ou o custo inviabilizar a busca, medir extração de embeddings em inferência e classificadores simples como trilha alternativa; registrar o impacto no critério de inovação antes de trocar a abordagem principal.

**Saída:** implementação mínima funcional e estimativa empírica de custo por candidato. **Parar e pedir autorização para a Etapa 4.**

### Etapa 4 — Busca enxuta e curva de aprendizado

**Status:** Concluída (complemento concluído)  
**Janela-alvo:** 25–26/09  
**GPU prevista:** até 60–90 minutos; ajustar ao total acumulado de 2–4 horas.

**Executar:** variar poucos fatores com hipótese definida, sem produto cartesiano amplo: representação do documento (início versus início + fim), comprimento de sequência que couber na GPU, taxa de aprendizado em pequena faixa, tamanho efetivo de lote e `weight_decay`. Definir épocas máximas com margem para a parada antecipada; observar a curva por passo ou época para estimar o ponto de saturação e detectar overfitting. Fazer triagem em uma divisão de desenvolvimento, não na validação final. Se couber no orçamento e o método inicial falhar por truncamento, testar uma estratégia por trechos; não implementá-la só por aparência de inovação.

**Saída:** tabela ordenada de candidatos, curvas e custo; selecionar 1–2 finalistas com justificativa mensurável. **Parar e pedir autorização para a Etapa 5.**

### Etapa 5 — Confirmação por folds e escolha final

**Status:** Concluída — (a), (b), (c), (c.1), 5c.2, (d), (e) e (f) concluídas  
**Janela-alvo:** até 27/09  
**GPU prevista:** janela de quatro horas concedida pelo usuário para a continuação original; confirmar os folds 2 e 3 mesmo que seja necessário ultrapassá-la, retomando em outra sessão. A 5c.1 consumiu 127,16 min de GPU em duas novas corridas; A foi reutilizada.

**Subdivisões da Etapa 5:**

- **a) Primeira corrida no fold 1 — Concluída, preliminar.** Início, 512 tokens, `2e-5`, até o passo 896. Acurácia 43,85%, macro-F1 43,23%; treino cobriu 0,624 época. Como não passou por todas as linhas de treino do fold, o resultado serve como primeira medição e precisa ser interpretado com essa limitação.
- **b) Definir duração e protocolo comuns — Concluída (24/09/2026).** Até duas épocas por execução, validação completa a cada 384 passos e no fim de cada época; early stopping após três avaliações consecutivas sem melhora, contando apenas avaliações a partir do passo 512. Acurácia seleciona o checkpoint e macro-F1 desempata. Lote efetivo 8; acumulação incompleta descartada no limite de cada época. Protocolo detalhado em `configs/bert_stage5_protocol.json` e `reports/etapa5_protocol.md`. A corrida preliminar (a), limitada a 0,624 época, será refeita em (c) para comparação justa.
- **c) Comparar os dois finalistas no fold 1 — Concluída (25/09/2026).** Sob o protocolo de (b), `start512_lr2e5` atingiu 45,14% de acurácia e 44,51% de macro-F1; `headtail256_lr2e5` atingiu 44,80% e 44,64%. A acurácia seleciona `start512_lr2e5` como BERT de referência da 5c.1. Diferenças por classe e custo em `reports/etapa5c_fold1_final.md`; o registro parcial anterior foi preservado.
- **5c.1 — Ablação controlada de conflitos de rótulo — Concluída (25/09/2026).** Foram comparadas A Original (reuso exato do controle), B remoção completa e C maioria conservadora no fold 1. A obteve 45,14% de acurácia; B 45,09%; C 44,95%. C teve macro-F1 ligeiramente maior que A, mas acurácia menor. Pelo critério congelado, nenhuma alternativa supera A; a política **Original** segue para 5d. Pré-flight, contagens, métricas por classe e interpretação em `reports/etapa5_conflict_ablation.md`; manifests persistidos em `data/stage5_conflict_ablation/`.
- **5c.2 — Diagnóstico de separabilidade e limite informacional do dataset — Concluída (25/09/2026).** Foram reavaliados sem gradientes o checkpoint A em todo o treino/validação do fold 1, confiança e entropia na validação, amostra humana de 60 exemplos, similaridade TF-IDF da classe `c234`, truncamento, schema/target, ablação e baseline. Treino: 59,03% accuracy/58,39% macro-F1; validação: 45,14%/44,51%; gaps de 13,88 p.p. em ambas. `c234` tem recall 30,21% e F1 34,30%; 71,4% dos erros são entre classes adjacentes, 28,6% entre extremos. Erros raramente têm confiança ≥0,80 (1,01%). BERT melhora o TF-IDF do mesmo fold em somente +0,54/+0,16/+0,07 p.p. para accuracy/macro-F1/weighted-F1. Similaridade léxica de c234 não a aproxima mais das classes extremas do que dela própria; vizinho mais próximo reparte-se quase igualmente entre c1/c234/c5. Schema de treino contém apenas `resp_text` e `clarity`; sem campo textual adicional disponível, não se fez teste de contexto nem treino novo. Evidências, limites e recomendação constam em `reports/etapa5_dataset_limit_diagnosis.md`; amostra em `reports/etapa5_dataset_limit_diagnosis_examples.md`; métricas/previsões em `runs/etapa5/diagnose_fold1_dataset_limit_20260925/`. Holdout não consultado.
- **d) Confirmar política e finalistas nos folds 2 e 3 — Concluída (25/09/2026).** Como B e C não superaram A na acurácia do fold 1, a política Original foi confirmada nos dois folds para ambos os finalistas. Reutilizando o fold 1, `start512_lr2e5` alcançou média de 45,007% de acurácia (DP amostral 0,613 p.p.) e 44,690% macro-F1; `headtail256_lr2e5`, 44,909% (0,122 p.p.) e 44,792%. TF-IDF `C=0,5`: 44,705% e 44,453%. Pelo critério primário, início 512 segue como referência por +0,098 p.p. de acurácia média; início + fim obteve +0,102 p.p. em macro-F1 e custou menos tempo. Diferenças pequenas, sem inferência de superioridade estatística. Relatório e resumo reproduzível em `reports/etapa5d_confirmation.md`, `runs/etapa5/stage5d_confirmation_summary.json` e `src/summarize_stage5d.py`. Holdout preservado.
- **e) Consolidar e congelar — Concluída (25/09/2026).** Comparados acurácia, macro-F1, recalls por classe e matrizes agregadas dos três folds, além do TF-IDF pareado. Congelados modelo `start512_lr2e5`, BERTimbau Base, tokenizer e representação inicial de 512 tokens; política Original preservando todos os rótulos; normalização/chave de grupos; e treino final com todos os 20.092 rótulos, taxa `2e-5`, AdamW, batch efetivo 8 e duração fixa de 4.523 updates (1,8011 equivalentes de época), sem validação ou early stopping na execução final. A duração deriva da média dos melhores pontos por época nos três folds do finalista selecionado. Especificação reproduzível em `configs/bert_stage5_final.json`; evidências, recalls e matrizes em `reports/etapa5e_final_spec.md`. Holdout intacto. Solicitar autorização específica antes de 5f.
- **f) Auditar o holdout uma única vez — Pendente.** Só após 5e congelar modelo, dados e protocolo, avaliar uma vez a validação final reservada. Não escolher entre Original, remoção e maioria a partir dela. Uma revisão após essa auditoria só cabe diante de erro objetivo de implementação ou vazamento, com a perda da independência do holdout documentada.

#### 5c.1 — Protocolo da ablação de conflitos

**Status:** Concluída (25/09/2026). **Dependência:** 5c concluída; referência congelada `start512_lr2e5`. **GPU realizada:** duas novas corridas (B 62,96 min; C 64,20 min), total 127,16 min; A foi reutilizada após a equivalência de protocolo e índices ser conferida.

**Variável única:** política aplicada a grupos conflitantes **somente no treino** do fold 1. A usa os 11.488 índices originais. B elimina todos os índices dos grupos que contêm mais de uma classe. C conta classes por grupo, conserva somente instâncias com a classe majoritária única e elimina grupos empatados; nenhuma instância é relabelada. A chave de grupo continua sendo a da Etapa 1: SHA-256 do texto após Unicode NFC, `casefold()` e colapso de espaços. Não introduzir similaridade aproximada, novos grupos ou novos folds.

**Controles:** manter o mesmo fold, validação, seed, modelo, tokenizer, representação, `max_length`, taxa, lote, acumulação, `weight_decay`, ausência de scheduler/warmup, duas épocas máximas, avaliação a cada 384 passos e no fim de época, early stopping e seleção de checkpoint por acurácia com macro-F1 como desempate. O lote incompleto no fim de cada época continua sendo descartado; como os datasets terão tamanhos diferentes, os passos por época e o número de exemplos vistos podem diferir como consequência da própria política. Registrar ambos, sem ajustar outro parâmetro para compensar.

**Persistência e barreira pré-treino:** manifests A/B/C criados em `data/stage5_conflict_ablation/`, com índices originais, mantidos/removidos, grupos e decisões, hashes, seed, classes e data/hora. As verificações de sanidade passaram antes dos treinos; o script também valida a reprodução. A, B e C preservaram a mesma validação e holdout. Arquivos originais e folds não foram modificados.

**Métricas e decisão:** registrar acurácia, macro-F1, weighted-F1, precisão/recall/F1 por classe, matriz de confusão, losses de treino/validação, passo e motivo de parada, épocas percorridas, tempo e memória. Calcular diferenças B−A e C−A. Se B ou C superar A no fold 1 pelo critério já fixado, levar somente a melhor alternativa a 5d; em empate exato de acurácia e macro-F1 com A, preferir Original. O efeito sobre cada classe e a perda de exemplos devem ser analisados antes de congelar a política, sem concluir causalidade apenas por uma métrica de um fold.

**Saída:** decisão congelada sobre modelo, hiperparâmetros, duração, política de dados e procedimento de treino final; relatório de comparação honesto. Caso nenhuma configuração supere o baseline, tratar como bloqueio de desempenho e propor correções prioritárias antes do treino final. Pedir autorização antes de cada nova subdivisão da Etapa 5 e, ao concluí-la, antes da Etapa 6.

### Etapa 6 — Treinamento integral e empacotamento do modelo

**Status:** Concluída (26/09/2026)  
**Janela-alvo:** 28–30/09  
**GPU prevista:** adicional às 2–4 horas de experimentos; estimar com os tempos medidos.

**Entrada obrigatória:** uma única especificação congelada em 5e e auditada em 5f: arquitetura, modelo pré-treinado, tokenizer, representação, `max_length`, hiperparâmetros, número de épocas/passos, scheduler e warmup (inclusive sua ausência), regra de early stopping ou duração final equivalente, política de conflitos, normalização/chave para identificar grupos e mapeamento das três classes. A contagem efetiva do treino final deve resultar mecanicamente dessa política, sem nova decisão após 5f.

**Executar:** treinar o modelo definitivo do zero a partir do checkpoint pré-treinado ou conforme a política congelada, usando somente a variante de dados escolhida. Não comparar A/B/C, não fazer tuning e não trocar a política após observar métricas do treinamento integral. Salvar pesos, tokenizer, mapeamento de classes, pré-processamento, configuração, versões, índices utilizados e log. Se treinar em todos os rótulos disponíveis, usar duração fixa definida em 5e e não alegar early stopping; se preservar validação para monitorar, registrar que nem todas as linhas foram usadas no ajuste. Validar recarga do artefato, previsões determinísticas em amostra conhecida, forma do vetor de probabilidades e ausência de classes fora do conjunto.

**Saída:** modelo final **já treinado e pronto para inferência**, comando de uso e manifesto; registrar duração, consumo de memória e evidência de recarga. **Parar e pedir autorização para a Etapa 7.**

### Etapa 7 — Inferência no conjunto de teste e verificação da planilha

**Status:** Concluída — 26/09/2026 11:05 BRT  
**Janela-alvo:** assim que o arquivo chegar; idealmente até 01–02/10.

**Executar:** inspecionar `test1.xlsx` antes de escrever; preservar número e ordem das linhas, colunas existentes, tipo de arquivo e convenções de rótulos do conjunto recebido. Não usar rótulos de teste para seleção do modelo, se vierem a existir. Executar inferência em lotes, verificar contagens e classes válidas, abrir novamente o `.xlsx` exportado e conferir uma amostra de linhas e a posição exata da coluna de predição. Manter o original intacto. Se a especificação de saída for ambígua, obter confirmação do usuário antes de produzir a versão definitiva.

**Saída:** planilha final válida e relatório de checagem estrutural. Se `test1.xlsx` deixar de estar disponível, registrar `Bloqueada` e retomar esta etapa quando estiver acessível, sem afirmar entrega concluída. **Parar e pedir autorização para a Etapa 8.**

### Etapa 8 — Relatório, apresentação e pacote de entrega

**Status:** Artefatos preparados e conferidos — aguardando nomes e números USP e inclusão do relatório pelo usuário no ZIP final  
**Janela-alvo:** até 03/10.

**Modelo e destinos:** usar `C:\Users\KABUM\Downloads\ep1-modelo-relatorio.pdf` como modelo de conteúdo do relatório. Criar o relatório como documento nativo editável no Google Docs do usuário e a apresentação como apresentação nativa no Google Presentations/Google Slides do usuário. Preservar os links das versões nativas no registro do projeto. O conteúdo do modelo PDF define requisitos do trabalho; não autoriza compartilhamento, publicação ou submissão.

**Executar:** no relatório do Google Docs, seguir os nove itens do modelo: (1) nomes e números USP dos integrantes efetivos; (2) introdução breve da estratégia principal e representação/classificador, indicando claramente o modelo final; (3) pré-processamento; (4) tabela dos parâmetros e faixas avaliadas; (5) valores ótimos; (6) divisão treino/teste e passos de reprodução; (7) tabela da métrica solicitada somente para o modelo final; (8) link do repositório de código; (9) instruções passo a passo, bibliotecas e dependências para reproduzir. Registrar evidências e limitações sem alegar acurácia no teste externo sem rótulos. Usar placeholders visíveis para nomes e números USP, conforme pedido do usuário. Criar um repositório GitHub público com o código do projeto e publicar diretamente na branch `main`; incluir seu URL no relatório. A Etapa 5f e sua comparação posterior de holdout podem ser descritas com clareza como auditoria comparativa; não as apresentar como métrica do conjunto externo `test1.xlsx` nem como resultado de um modelo escolhido após ajuste pelo holdout.

Criar no Google Presentations/Slides uma apresentação de até dez minutos, consistente com o relatório. Exportar a apresentação para PDF. O modelo informa que o ZIP deve conter o relatório e os outros dois itens solicitados: o PDF da apresentação e a planilha Excel com os rótulos previstos. O usuário adicionará a exportação do relatório ao ZIP depois; entregar o Google Doc nativo e deixar um ZIP preparado com o PDF da apresentação e a planilha, sinalizando que o relatório ainda precisa ser incluído. Incluir também link do repositório e instruções de reprodução no relatório conforme exigido pelo modelo.

Antes de fechar o pacote, conferir integridade do ZIP, nomes e conteúdos dos três itens, links das versões nativas, reprodução mínima da inferência e abertura da planilha e dos PDFs/exportações. Não compartilhar nem submeter nada externamente sem autorização específica do usuário.

**Saída:** Google Doc editável, Google Presentation editável, repositório GitHub público na `main` e ZIP preparado com PDF da apresentação e planilha; o usuário acrescentará o relatório ao ZIP. **Parar e apresentar os links e o pacote ao usuário.**
## 5. Controle de progresso

| Etapa | Status | Início | Conclusão | Evidência principal | Autorização para iniciar |
| --- | --- | --- | --- | --- | --- |
| 0. Ambiente | Concluída | 24/09/2026 16:23 BRT | 24/09/2026 16:27 BRT | `runs/etapa0/verification.json` | Autorizada pelo pedido de iniciar a implementação |
| 1. Auditoria e divisões | Concluída | 24/09/2026 16:29 BRT | 24/09/2026 16:34 BRT | `reports/etapa1_audit.md`; `data/splits_grouped_v1.json` | Autorizada explicitamente pelo usuário |
| 2. Baselines | Concluída | 24/09/2026 17:20 BRT | 24/09/2026 17:25 BRT | `reports/etapa2_baseline.md`; `runs/etapa2/baseline_20260924_1724/metrics.json` | Autorizada explicitamente pelo usuário |
| 3. BERT mínimo | Concluída | 24/09/2026 17:38 BRT | 24/09/2026 17:58 BRT | `reports/etapa3_benchmark.md`; `runs/etapa3/bert_stage3_short_20260924_1753/metrics.json` | Autorizada explicitamente pelo usuário |
| 4. Busca e curvas | Concluída após complemento | 24/09/2026 18:02 BRT | 24/09/2026 20:42 BRT | `reports/etapa4_search.md`; oito candidatos, curvas e checkpoints | Quatro execuções adicionais autorizadas explicitamente pelo usuário |
| 5. Confirmação e escolha | Concluída | 24/09/2026 22:56 BRT | 26/09/2026 09:29 BRT | `reports/etapa5f_holdout_audit.md`; configuração congelada em `configs/bert_stage5_final.json` | Subdivisões autorizadas pelo usuário |
| 5c.1 Ablação de conflitos | Concluída | 25/09/2026 11:48 BRT | 25/09/2026 15:11 BRT | Relatório da ablação; corridas B/C; manifests e configuração | Próxima subdivisão 5d exige autorização |
| 5c.2 Diagnóstico de separabilidade | Concluída | 25/09/2026 16:56 BRT | 25/09/2026 17:28 BRT | `reports/etapa5_dataset_limit_diagnosis.md`; amostra de 60 itens e inferência no fold 1 | 5d requer autorização explícita |
| 5d Confirmação folds 2 e 3 | Concluída | 25/09/2026 17:44 BRT | 25/09/2026 23:00 BRT | `reports/etapa5d_confirmation.md`; seis métricas BERT e baseline pareados | Autorizada explicitamente pelo usuário |
| 5e Congelar especificação | Concluída | 25/09/2026 23:15 BRT | 25/09/2026 23:27 BRT | `configs/bert_stage5_final.json`; `reports/etapa5e_final_spec.md` | Autorizada explicitamente pelo usuário |
| 5f Auditoria do holdout | Concluída | 26/09/2026 | 26/09/2026 09:29 BRT | `reports/etapa5f_holdout_audit.md` | Autorizada explicitamente pelo usuário |
| 6. Treino final | Concluída | 26/09/2026 | 26/09/2026 | `reports/etapa6_final.md`; `models/bert_final/` | Autorizada explicitamente pelo usuário |
| 7. Inferência e planilha | Concluída | 26/09/2026 | 26/09/2026 11:05 BRT | `reports/etapa7_inferencia.md`; `outputs/etapa7_20260926_105326_ca987906/test1_predito.xlsx` | Autorizada explicitamente pelo usuário |
| 8. Entrega | Artefatos preparados; ZIP final pendente | 26/09/2026 19:00 BRT | — | Google Docs, Google Slides, GitHub público e `outputs/etapa8/EP1_ACH2118_parcial_sem_relatorio.zip` | Autorizada explicitamente pelo usuário |

## 6. Diário de execução

Adicionar ao final de cada sessão, mantendo as entradas anteriores:

```text
Data/hora e etapa:
Autorização recebida:
Estado ao iniciar:
Arquivos e versões de entrada:
Ambiente e comando(s) executado(s):
Trabalho realizado:
Resultados (métricas, tempo, memória, número de folds, seed):
Artefatos salvos e localização persistente:
Problemas, limitações e correções:
Decisão e justificativa:
GPU experimental acumulada / orçamento restante:
Critérios de saída verificados:
Novo estado da etapa:
Próxima etapa proposta (não iniciar sem autorização):
```

**Registro inicial — 23/09/2026:** planejamento criado a partir do enunciado, inspeção da planilha e discussão do prazo/orçamento. Nenhum modelo novo foi treinado neste plano; métricas experimentais e tempos de GPU permanecem **A medir**. Primeira ação autorizável: **Etapa 0**.

**Sessão — 24/09/2026 16:23–16:27 BRT, Etapa 0**

- **Autorização recebida:** pedido do usuário para ler o plano e iniciar sua implementação; pelo contrato deste plano, autorização aplicada somente à Etapa 0.
- **Estado ao iniciar:** Etapa 0 pendente; pasta sem repositório Git, `.venv` já instalado com PyTorch ROCm; `train.xlsx`, `ep1-enunciado.pdf` e `test1.xlsx` presentes. `test1.xlsx` não foi analisado nesta etapa e não equivale automaticamente ao `test.xlsx` citado para a Etapa 7.
- **Arquivos e versões de entrada:** `train.xlsx` SHA-256 `0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818` (7.616.781 bytes); `ep1-enunciado.pdf` SHA-256 `d269889e3c3275790e38af23a2c9436ad0b8d404da13ff9d5ace933d6432fe7b` (154.989 bytes). A planilha abriu com 20.093 linhas incluindo cabeçalho e colunas `resp_text`, `clarity`; o PDF abriu com 14 páginas e texto extraível.
- **Ambiente e comandos executados:** Windows 11, Python 3.14.7, PyTorch 2.13.0+rocm10.0.0, transformers 4.56.2, tokenizers 0.22.1, openpyxl 3.1.5, pypdf 6.1.1, scikit-learn 1.7.2. Dependências adicionais instaladas com `python -m pip install transformers==4.56.2 tokenizers==0.22.1 safetensors==0.6.2 huggingface-hub==0.35.3 openpyxl==3.1.5 pypdf==6.1.1 scikit-learn==1.7.2`; snapshot completo em `requirements.lock.txt`. Verificação reproduzível: `python src/verify_environment.py`. Espaço livre medido na unidade C: 332.999.860.224 bytes.
- **Trabalho realizado:** criado verificador único para hashes, leitura das entradas, carregamento do tokenizer BERTimbau Base e um lote sintético de treino na GPU; documentadas convenções de logs, checkpoints e proteção de dados para eventual Git em `ENVIRONMENT.md` e `.gitignore`.
- **Resultados:** tokenizer `neuralmind/bert-base-portuguese-cased` carregou; PyTorch detectou AMD Radeon RX 7600 com 8.573.157.376 bytes de memória total. Forward, backward e `optimizer.step()` concluíram, com pesos alterados. Tempo do passo sincronizado: 0,944166 s; pico alocado: 86.220.288 bytes; pico reservado: 90.177.536 bytes; tempo de parede do comando final: cerca de 9,44 s. Semente do teste: 20260924. Estes valores são apenas do modelo sintético pequeno, não estimam o custo de fine-tuning BERTimbau.
- **Artefatos salvos:** `src/verify_environment.py`, `runs/etapa0/verification.json`, `requirements.lock.txt`, `ENVIRONMENT.md`, `.gitignore` e este registro em `plan.md`.
- **Problemas, limitações e correções:** acesso à rede pelo ambiente isolado bloqueou PyPI e Hugging Face; a instalação e o download do tokenizer foram repetidos com acesso externo autorizado e concluídos. Consulta WMI da placa retornou acesso negado; a identificação e a memória foram obtidas diretamente do PyTorch. A primeira tentativa de imprimir todo o texto do PDF encontrou limitação de codificação do terminal, mas a leitura e extração do texto pelo script foram bem-sucedidas. Não foi executado um benchmark do modelo BERT completo, reservado à Etapa 3.
- **Decisão e justificativa:** manter o `.venv` com ROCm existente, sem migração de ambiente; a GPU e as entradas estão operacionais. Pacotes AMD ROCm podem exigir fonte de instalação específica ao recriar o ambiente em outra máquina.
- **GPU experimental acumulada / orçamento restante:** 0,944166 s de passo medido, aproximadamente 9,44 s de comando incluindo inicialização e leituras; orçamento de 2–4 horas de experimentação praticamente intacto.
- **Critérios de saída verificados:** projeto executável; dependências fixadas; duas entradas lidas; armazenamento medido; GPU real executou forward, backward e atualização de pesos, com tempo e memória registrados.
- **Novo estado da etapa:** Concluída.
- **Próxima etapa proposta:** Etapa 1, auditoria de dados e divisões; **não iniciar sem autorização explícita do usuário**.

**Sessão — 24/09/2026 16:29–16:34 BRT, Etapa 1**

- **Autorização recebida:** usuário autorizou explicitamente iniciar a Etapa 1 após a conclusão da Etapa 0.
- **Estado ao iniciar:** Etapa 1 pendente; ambiente e verificação de GPU da Etapa 0 concluídos em `runs/etapa0/verification.json`.
- **Arquivos e versões de entrada:** `train.xlsx` SHA-256 `0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818`; `ep1-enunciado.pdf` SHA-256 `d269889e3c3275790e38af23a2c9436ad0b8d404da13ff9d5ace933d6432fe7b`; Python 3.14.7, openpyxl 3.1.5, scikit-learn 1.7.2, transformers 4.56.2.
- **Ambiente e comandos executados:** Windows 11, `.venv`; `python src/audit_and_split.py` (execução final 16,51 s de parede; tempo interno de auditoria 8,544 s); verificação independente por releitura de `data/splits_grouped_v1.json` e `data/row_manifest.csv`.
- **Trabalho realizado:** auditados esquema, tipos, nulos, rótulos, duplicatas, conflitos, comprimentos em palavras, caracteres e tokens, indicadores de qualidade e casos representativos. Criada normalização conservadora apenas para chave de agrupamento, com Unicode NFC, `casefold()` e colapso de espaços. Gerados holdout de cerca de 15% e três folds estratificados por classe e agrupados por texto. Índices base zero e hash da fonte persistidos.
- **Resultados:** 20.092 linhas; `c1` 6.347, `c234` 6.853 e `c5` 6.892; nenhum nulo. Uma célula de texto numérica (linha Excel 5028) exige conversão explícita por `str()`. Foram encontrados 18.143 grupos normalizados, 500 grupos repetidos abrangendo 2.449 linhas e 316 grupos com rótulos conflitantes abrangendo 1.975 linhas. Mediana de 101 palavras e 182 tokens BERTimbau; 7.204 textos excedem 256 tokens. Holdout: 3.024 linhas (`c1` 952, `c234` 1.036, `c5` 1.036); desenvolvimento: 17.068. Validação dos folds: 5.580, 5.617 e 5.871 linhas. Semente 20260924; três folds **gerados**, nenhum modelo treinado. Interseção de grupos zero em todas as fronteiras; todas as linhas foram atribuídas e cada linha de desenvolvimento entra uma vez em validação interna.
- **Artefatos salvos:** `src/audit_and_split.py`, `data/splits_grouped_v1.json`, `data/row_manifest.csv`, `reports/etapa1_audit.md`, `reports/etapa1_audit.json`, atualização de `.gitignore` e deste plano. `data/` e o JSON com trechos de exemplo são ignorados por Git para proteger os dados.
- **Problemas, limitações e correções:** primeira execução identificou o campo numérico e foi ajustada para mantê-lo; impressão de trechos no console encontrou caracteres incompatíveis com CP1252 e passou a usar escape ASCII, preservando o relatório UTF-8. A anotação inicial do plano sobre `c6` estava errada: o texto da página 2 do PDF diz `{c1,c234,c5}`. A correção não afeta os rótulos nem métricas posteriores. Grupos de texto idêntico com rótulos distintos foram preservados. Nenhuma limpeza de conteúdo foi aplicada.
- **Decisão e justificativa:** usar `grouped_v1_seed_20260924`; escolhido o candidato 37 entre 256 divisões agrupadas por equilíbrio de tamanho e classes, sem avaliação de modelo. Manter a validação final reservada até a Etapa 5. Todos os parâmetros e índices estão explícitos e persistidos.
- **GPU experimental acumulada / orçamento restante:** nenhuma GPU usada nesta etapa; mantém-se o consumo da Etapa 0, 0,944166 s de passo medido, com orçamento de 2–4 horas praticamente intacto.
- **Critérios de saída verificados:** relatório de auditoria e casos representativos, índices reproduzíveis, proporções por classe, ausência de vazamento por grupos e protocolo congelado. Releitura dos artefatos confirmou 20.092 linhas e ausência de interseção de grupos.
- **Novo estado da etapa:** Concluída.
- **Próxima etapa proposta:** Etapa 2, baselines e instrumentação; **não iniciar sem autorização explícita do usuário**.

**Sessão complementar — 24/09/2026 16:42–16:44 BRT, Etapa 1 já concluída**

- **Autorização recebida:** usuário pediu um documento com todas as linhas de `train.xlsx` que pertencem a grupos de rótulos conflitantes para consulta ao professor. O pedido não autorizou iniciar a Etapa 2.
- **Estado ao iniciar:** Etapa 1 concluída, divisões e auditoria congeladas; Etapa 2 pendente.
- **Arquivos e versões de entrada:** `train.xlsx` com SHA-256 `0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818`; `data/row_manifest.csv` e protocolo da Etapa 1.
- **Ambiente e comandos executados:** Windows 11, Python 3.14.7, openpyxl 3.1.5; `python src/export_conflicts.py`; verificação por releitura da tabela Markdown e comparação de cada linha/rótulo com `data/row_manifest.csv`.
- **Trabalho realizado e resultados:** gerado documento de conferência com os 316 grupos e as 1.975 linhas Excel envolvidas, separadas por `c1`, `c234` e `c5`. Em 247 grupos há ao menos uma variante de texto literalmente igual com rótulos diferentes; são 291 variantes literais conflitantes. O relatório distingue esses casos dos conflitos que surgem apenas após a normalização de caixa/espaços. Todos os 1.975 pares linha/rótulo foram conferidos; nenhuma linha foi omitida ou duplicada.
- **Artefatos salvos:** `reports/conflitos_rotulos_train.md`, gerador `src/export_conflicts.py`, atualização de `.gitignore` e deste plano. O relatório é ignorado por Git porque contém localizadores de dados do conjunto de treino.
- **Problemas, limitações e correções:** a planilha não informa se as linhas repetidas representam avaliações independentes ou erro de anotação. O documento não inclui o texto completo das respostas; deve ser usado com `train.xlsx`. Nenhum rótulo ou índice de divisão foi alterado.
- **Decisão e justificativa:** apresentar os conflitos ao professor antes de decidir qualquer limpeza; não presumir que duplicatas devem ser removidas. Eventual decisão futura que altere os dados exigirá revisão documentada do protocolo e das avaliações.
- **GPU experimental acumulada / orçamento restante:** nenhuma GPU nesta sessão; consumo anterior da Etapa 0 permanece 0,944166 s de passo medido.
- **Critérios de saída verificados:** documento Markdown criado, contagens e pares linha/rótulo conferidos contra a planilha/manifesto; Etapa 1 permanece concluída.
- **Novo estado da etapa:** Etapa 1 concluída; Etapa 2 pendente.
- **Próxima etapa proposta:** aguardar orientação do professor, se houver, e autorização explícita do usuário para iniciar a Etapa 2.

**Sessão — 24/09/2026 17:20–17:25 BRT, Etapa 2**

- **Autorização recebida:** usuário autorizou explicitamente iniciar a Etapa 2.
- **Estado ao iniciar:** Etapa 2 pendente, Etapas 0–1 concluídas; dados, rótulos e índices agrupados da Etapa 1 preservados. Não houve retorno do professor sobre os rótulos conflitantes; foram mantidos conforme protocolo.
- **Arquivos e versões de entrada:** `train.xlsx` SHA-256 `0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818`; divisão `grouped_v1_seed_20260924` em `data/splits_grouped_v1.json`; Python 3.14.7, scikit-learn 1.7.2, numpy 2.5.2, openpyxl 3.1.5, joblib 1.6.0.
- **Ambiente e comandos executados:** Windows 11, `.venv`, CPU com quatro threads; `python src/run_baseline.py --run-id baseline_20260924_1724`. Releitura de checkpoint com `joblib.load` e predição em cinco linhas de validação; validação estrutural do SVG por parser XML. Execução principal: 28,842 s de parede; ajuste de classificadores com `C=0,5`: 4,535 s somados nos três folds.
- **Trabalho realizado:** implementadas métricas reutilizáveis, registro por execução, checkpoints por fold/configuração e gráficos SVG de séries para próximos experimentos. Avaliada classe majoritária obtida somente do treino de cada fold. TF-IDF aprendido no treino de cada fold, seguido de regressão logística com busca pequena (`C=0,5` e `C=2,0`). Foram calculadas métricas de treino e validação, acurácia, macro-F1, recall por classe e matriz de confusão. A validação final reservada não foi avaliada.
- **Resultados:** classe majoritária: acurácia média de validação 33,76%, macro-F1 16,83%. TF-IDF + regressão `C=0,5`: acurácia por fold 44,61%, 44,13%, 45,38%; média 44,71%, desvio amostral 0,63 ponto percentual, macro-F1 médio 44,45%, treino médio 71,48%. `C=2,0`: média de validação 44,21%, treino médio 84,53%. Diferença selecionada ante classe majoritária: +10,94 pontos percentuais. Recalls médios com `C=0,5`: `c1` 41,64%, `c234` 37,45%, `c5` 54,72%. Matriz e tempos detalhados no relatório. Nenhum aviso de convergência. Semente 20260924; três folds executados.
- **Artefatos salvos:** `configs/baseline.json`, `src/run_baseline.py`, `src/experiment_metrics.py`, `src/plot_curves.py`, `runs/etapa2/baseline_20260924_1724/metrics.json`, `config.json`, `curve.json`, seis checkpoints em `models/baseline/baseline_20260924_1724/`, `reports/etapa2_baseline.md`, `reports/etapa2_baseline_curve.svg` e este plano.
- **Problemas, limitações e correções:** diferença treino–validação de 26,78 pontos percentuais com `C=0,5`, sugerindo sobreajuste; a classe `c234` tem o menor recall. O resultado histórico de ~46% não tem divisão/protocolo comprovado, então não foi usado como comparação direta. A avaliação final permanece intacta. Nenhum rótulo conflitante foi removido.
- **Decisão e justificativa:** fixar `C=0,5` como baseline de referência por maior acurácia média nos folds (44,71% frente a 44,21% de `C=2,0`) e menor sobreajuste. Não extrapolar para desempenho no teste; comparar os candidatos de BERT neste mesmo protocolo.
- **GPU experimental acumulada / orçamento restante:** nenhuma GPU nesta etapa; permanece 0,944166 s de passo medido da Etapa 0, com orçamento de 2–4 horas praticamente intacto.
- **Critérios de saída verificados:** baseline reproduzível com parâmetros e divisões fixados; três folds, métricas reais, gráfico e checkpoints persistidos. Um checkpoint foi recarregado e produziu previsões válidas. A validação final não participou da seleção.
- **Novo estado da etapa:** Concluída.
- **Próxima etapa proposta:** Etapa 3, BERTimbau mínimo e benchmark de custo; **não iniciar sem autorização explícita do usuário**.

**Sessão — 24/09/2026 17:38–17:58 BRT, Etapa 3**

- **Autorização recebida:** usuário autorizou explicitamente iniciar a Etapa 3.
- **Estado ao iniciar:** Etapas 0–2 concluídas; baseline TF-IDF fixado em 44,71% de acurácia média nos três folds agrupados; validação final reservada.
- **Arquivos e versões de entrada:** `train.xlsx` SHA-256 `0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818`; divisão `grouped_v1_seed_20260924` SHA-256 `aa9c99a79ccccc3655399761c53098f5fd3d770c9aa6c8b68be29c49eba3586b`; PyTorch 2.13.0+rocm10.0.0, transformers 4.56.2, tokenizers 0.22.1; pesos pré-treinados de `neuralmind/bert-base-portuguese-cased` no cache local.
- **Ambiente e comandos executados:** Windows 11, Python 3.14.7, AMD Radeon RX 7600; `python src/bert_stage3.py benchmark --run-id bert_stage3_benchmark_20260924_1748` e `python src/bert_stage3.py short --run-id bert_stage3_short_20260924_1753`, ambos fora do isolamento de comandos do Codex após diagnóstico. O mesmo benchmark dentro do isolamento falhou antes do primeiro forward; artefato de falha preservado.
- **Trabalho realizado:** classificador BERTimbau Base para três classes com mapa fixo `c1:0`, `c234:1`, `c5:2`; texto original, tokenização, truncamento inicial em 256 tokens e padding dinâmico. Treino com microbatch 2, acumulação de quatro passos, AdamW, `weight_decay=0,01`, semente fixa; 12 microbatches de benchmark, depois uma passagem curta em 1.024 linhas de treino e avaliações periódicas em 512 linhas do fold 1. Early stopping com paciência de duas avaliações, seleção e recarga do melhor checkpoint. Curvas de loss e acurácia salvas.
- **Resultados:** benchmark de 12 microbatches (24 linhas efetivamente vistas) e três passos de otimizador: 2,715 s de treino, 4,503 s total, pico alocado 2.365.955.584 bytes, reservado 2.573.205.504 bytes. Corrida curta: 512 microbatches/128 passos de otimizador, 118,324 s de treino e avaliações, 121,914 s total; 0,1341 s/microbatch, 8,654 exemplos/s incluindo avaliações; pico alocado 2.370.174.464 bytes, reservado 2.602.565.632 bytes. Melhor acurácia de validação 37,89% e macro-F1 29,34% no passo 96, em 512 linhas amostradas; nenhuma predição `c1` nesse ponto. Early stopping não disparou. Uma época de treino com as 11.488 linhas do fold 1 foi projetada em 770 s antes de avaliações e salvamentos; ainda não medida. O checkpoint recarregado gerou logits finitos com forma `[5,3]` e rótulos válidos.
- **Artefatos salvos:** `configs/bert_stage3.json`, `src/bert_stage3.py`, métricas em `runs/etapa3/bert_stage3_benchmark_20260924_1748/metrics.json` e `runs/etapa3/bert_stage3_short_20260924_1753/metrics.json`, checkpoint e tokenizer em `models/bert_stage3/bert_stage3_short_20260924_1753/best/`, `reports/etapa3_benchmark.md`, curvas `reports/etapa3_accuracy_curve.svg` e `reports/etapa3_loss_curve.svg`, diagnóstico da tentativa falha `runs/etapa3/bert_stage3_benchmark_20260924_1742/failure.json`, revisão de `ENVIRONMENT.md` e deste plano.
- **Problemas, limitações e correções:** corrigidos um erro de sintaxe no gráfico e a inicialização das estatísticas ROCm. Dentro do isolamento do Codex, até operações simples da GPU passaram a falhar com `hipErrorInvalidImage`; fora dele, o mesmo BERTimbau concluiu ambos os treinos. PyTorch avisou que variantes de atenção eficiente para AMD são experimentais; não foram habilitadas. A corrida curta usa subconjunto e uma época; 37,89% não pode ser comparado diretamente ao baseline de fold completo, nem tratado como parâmetro ótimo. A validação final não foi acessada.
- **Decisão e justificativa:** o fine-tuning é funcional na RX 7600 fora do isolamento; manter BERTimbau como abordagem principal para a Etapa 4. Usar a medição de cerca de 12,8 minutos por época de treino do fold 1, mais validação e salvamento, como estimativa inicial de custo, com revisão após execuções completas. Não ativar a alternativa de embeddings congelados sem necessidade.
- **GPU experimental acumulada / orçamento restante:** 126,417 s de parede nas duas execuções bem-sucedidas desta etapa, com 121,039 s medidos dentro dos laços de treino/avaliação; mais 0,944166 s de passo da Etapa 0. Cerca de 2,1 minutos de execução experimental medidos, restando aproximadamente 118–238 minutos do orçamento de 2–4 horas. As tentativas falhas dentro do isolamento não concluíram passos de treino.
- **Critérios de saída verificados:** implementação mínima funcional, benchmark empírico de tempo/memória, execução curta com curvas e validação periódica, melhor checkpoint salvo e recarregado, previsões válidas; nenhuma linha do holdout final usada.
- **Novo estado da etapa:** Concluída.
- **Próxima etapa proposta:** Etapa 4, busca enxuta e curva de aprendizado; **não iniciar sem autorização explícita do usuário**.

**Sessão — 24/09/2026 18:02–18:58 BRT, Etapa 4**

- **Autorização recebida:** usuário autorizou explicitamente iniciar a Etapa 4.
- **Estado ao iniciar:** Etapas 0–3 concluídas; BERTimbau Base funcional na RX 7600; baseline TF-IDF `C=0,5` com 44,71% de acurácia média nos três folds completos; holdout final reservado.
- **Arquivos e versões de entrada:** `train.xlsx` SHA-256 `0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818`; divisão `grouped_v1_seed_20260924` SHA-256 `aa9c99a79ccccc3655399761c53098f5fd3d770c9aa6c8b68be29c49eba3586b`; PyTorch 2.13.0+rocm10.0.0 e transformers 4.56.2. Subconjunto da Etapa 4 persistido com 4.096 linhas de treino e 1.024 de validação do fold 1.
- **Ambiente e comandos executados:** Windows 11, Python 3.14.7, RX 7600; `python src/prepare_stage4_subset.py`; `python src/bert_stage4.py <id> --run-id <id_de_execucao>` para `start256_lr2e5`, `headtail256_lr2e5`, `start512_lr2e5` e `start256_lr3e5`; `python src/baseline_stage4_subset.py`; `python src/summarize_stage4.py`. Treinos GPU executados fora do isolamento de comandos do Codex conforme diagnóstico da Etapa 3.
- **Trabalho realizado:** comparação de quatro hipóteses no mesmo subconjunto e semente, com máximo de duas épocas, batch efetivo 8, `weight_decay=0,01`, avaliação a cada 128 passos, parada antecipada e melhor checkpoint salvo. Variados representação (início/início + fim), janela (256/512) e taxa (`2e-5`/`3e-5`); batch e decaimento fixos para isolar esses fatores. TF-IDF `C=0,5` reajustado no mesmo subconjunto, com acurácia de 44,24% e macro-F1 de 43,90% na mesma validação. Gerados curvas individuais e gráfico comparativo.
- **Resultados:** início 512 `2e-5`: 45,80% de acurácia, 45,35% macro-F1, melhor passo 896, +1,56 pp ante TF-IDF, 18,68 min, 3,26 GB alocados no pico; início + fim 256 `2e-5`: 45,21%, 44,13% macro-F1, passo 896, +0,98 pp, 12,38 min, 2,37 GB; início 256 `2e-5`: 41,60%, 41,37% macro-F1, passo 128, 6,22 min, parada no 512; início 256 `3e-5`: 40,72%, 40,25% macro-F1, passo 128, 6,24 min, parada no 512. Na validação, 357 textos ultrapassam 256 tokens e 99 ultrapassam 512. Os melhores checkpoints dos dois líderes foram no passo 896; houve queda de acurácia no passo 1.024. Todos os quatro checkpoints foram recarregados e produziram logits finitos e classes válidas.
- **Artefatos salvos:** `configs/bert_stage4.json`, `src/prepare_stage4_subset.py`, `src/bert_stage4.py`, `src/baseline_stage4_subset.py`, `src/summarize_stage4.py`, `data/stage4_subset.json`, `runs/etapa4/baseline_same_subset.json`, quatro diretórios de `runs/etapa4/stage4_*/`, checkpoints em `models/bert_stage4/stage4_*/best/`, `models/baseline/stage4_subset_c0_5.joblib`, `reports/etapa4_search.md`, curvas em `reports/etapa4/`, este plano.
- **Problemas, limitações e correções:** a melhora é pequena e sujeita ao ruído de uma única validação de 1.024 linhas e à seleção do melhor passo entre várias avaliações. A diferença para o baseline de 44,71% da Etapa 2 não é comparável por usar tamanhos/protocolo distintos; foi criado baseline no mesmo subconjunto para a comparação da triagem. Recall por classe oscila, particularmente `c1`; não se conclui superioridade. Não houve consulta ao holdout. A estratégia por trechos completos não foi executada, pois as hipóteses de janela 512 e início + fim já reduziram a perda de conteúdo dentro do orçamento.
- **Decisão e justificativa:** selecionar **início 512 `2e-5`** e **início + fim 256 `2e-5`** como finalistas. O primeiro teve melhor acurácia e macro-F1; o segundo ficou 0,59 pp atrás com 6,30 min a menos e cerca de 0,88 GB a menos de pico. Priorizar a confirmação de início 512 nos folds e avaliar o segundo conforme o saldo de GPU. Não fixar modelo final ainda.
- **GPU experimental acumulada / orçamento restante:** 2.610,998 s (43,52 min) de comandos GPU na Etapa 4; mais 126,417 s na Etapa 3 e cerca de 9,44 s de comando na Etapa 0, total aproximado de 45,6 min. Restam aproximadamente 74–194 min do orçamento experimental de 2–4 h. Tempo de comando inclui inicialização, avaliação e salvamento.
- **Critérios de saída verificados:** quatro candidatos com configuração/identificador, métricas, tempos, memória e checkpoints persistidos; tabela ordenada, curvas e comparação no mesmo subconjunto; dois finalistas com justificativa quantitativa; holdout preservado.
- **Novo estado da etapa:** Concluída.
- **Próxima etapa proposta:** Etapa 5, confirmação por folds e escolha final; **não iniciar sem autorização explícita do usuário**.

**Sessão complementar — 24/09/2026 19:15–20:42 BRT, Etapa 4 (concluída)**

- **Autorização recebida:** usuário solicitou executar os quatro testes adicionais descritos na conversa: início + fim 256 `3e-5`; início + fim 512 `2e-5`; início 512 `3e-5`; início + fim 512 `3e-5`.
- **Estado ao iniciar:** busca inicial da Etapa 4 concluída às 18:58 BRT, com início 512 `2e-5` e início + fim 256 `2e-5` como finalistas provisórios. Nenhum fold de confirmação ou holdout avaliado.
- **Arquivos de entrada:** mesma planilha e hashes, divisão agrupada, subset `stage4_fold1_stratified_4096_1024_seed_20260924` e baseline TF-IDF no mesmo subconjunto. Nenhum índice ou rótulo foi alterado.
- **Ambiente e comandos:** Windows 11, Python 3.14.7, RX 7600/ROCm. Executados `python src/bert_stage4.py headtail256_lr3e5 --run-id stage4_headtail256_lr3e5_20260924_1918`; `python src/bert_stage4.py headtail512_lr2e5 --run-id stage4_headtail512_lr2e5_20260924_1945`; `python src/bert_stage4.py start512_lr3e5 --run-id stage4_start512_lr3e5_20260924_2010`; `python src/bert_stage4.py headtail512_lr3e5 --run-id stage4_headtail512_lr3e5_20260924_2045`; e `python src/summarize_stage4.py`. As corridas GPU ocorreram fora do isolamento de comandos.
- **Trabalho realizado:** ampliada a grade para completar as oito combinações de duas representações, dois comprimentos e duas taxas. Mantidos seed, lote efetivo, weight decay, número máximo de épocas, subconjunto e protocolo de seleção originais. O agregador passou a gerar comparações por comprimento. Preservados todos os resultados anteriores.
- **Resultados adicionais:** início + fim 256 `3e-5`: acurácia 43,07%, macro-F1 41,38%, melhor passo 896, 12,42 min, pico 2,37 GB; início + fim 512 `2e-5`: 45,21%, macro-F1 43,48%, passo 896, 18,86 min, 3,26 GB; início 512 `3e-5`: 44,04%, macro-F1 43,11%, passo 896, 18,81 min, 3,26 GB; início + fim 512 `3e-5`: 44,82%, macro-F1 43,90%, passo 1.024, 18,80 min, 3,26 GB. O melhor segue início 512 `2e-5`: 45,80%, macro-F1 45,35%, versus TF-IDF 44,24%/43,90% no mesmo subconjunto. Selecionados provisoriamente para Etapa 5: início 512 `2e-5` e início + fim 256 `2e-5`, por acurácia, macro-F1 e custo. A confirmação por folds ainda falta.
- **Artefatos salvos:** revisão de `configs/bert_stage4.json`, `src/summarize_stage4.py`, `reports/etapa4_search.md`, `reports/etapa4/comparison_accuracy_256.svg`, `reports/etapa4/comparison_accuracy_512.svg`, oito curvas individuais atualizadas/acrescentadas, `runs/etapa4/comparison_summary.json`, métricas e checkpoints dos quatro novos IDs listados nos comandos.
- **Problemas, limitações e correções:** quatro variantes adicionais ficaram autorizadas após o primeiro encerramento da Etapa 4; registradas como complemento, sem apagar medições anteriores. O consumo real (68,89 min adicionais; 112,40 min na Etapa 4 completa) excedeu a estimativa inicial de 60–90 min devido às quatro corridas de 512 tokens. Acumulado experimental atualizado para aproximadamente 114,67 min; saldo estimado 5–125 min conforme o limite efetivo de 2–4 h. Uma única amostra/seed, oscilação grande de validação e seleção entre passos limitam as conclusões. Holdout final preservado.
- **Decisão e justificativa:** manter os dois finalistas indicados acima. Início + fim 512 `2e-5` igualou a acurácia de início + fim 256 `2e-5`, mas teve macro-F1 menor e custou cerca de 6,48 min a mais. As taxas `3e-5` não melhoraram de forma consistente. Na Etapa 5, priorizar o finalista de 512 tokens; executar o segundo apenas dentro do saldo efetivo e registrar folds concluídos e incerteza.
- **Critérios de saída verificados:** oito candidatos com IDs, configuração, métricas, tempo, pico de memória, curvas e checkpoints; comparação com baseline pareado; dois finalistas provisórios; validação final não acessada.
- **Novo estado:** Etapa 4 concluída após complemento; Etapa 5 pendente.

**Sessão — 24/09/2026 22:56–23:23 BRT, Etapa 5 (parte 1; um caso hoje)**

- **Autorização recebida:** usuário autorizou iniciar a Etapa 5; hoje executar apenas um candidato em um fold. O limite inicial de uma hora pode ser ultrapassado se isso for necessário para concluir esse único caso. O restante fica para amanhã, quando o usuário disponibilizará mais quatro horas.
- **Estado ao iniciar:** Etapa 4 concluída com oito candidatos; finalistas provisórios: início 512 `2e-5` e início + fim 256 `2e-5`. Nenhum fold BERT completo tinha sido confirmado. O holdout segue reservado.
- **Plano da parte de hoje:** confirmar o finalista de maior acurácia no fold 1 completo (11.488 treino/5.580 validação), até o passo 896, com avaliações espaçadas nos passos 384, 768 e 896 para limitar o custo da validação extensa. Concluir esse único caso mesmo que passe de uma hora; não iniciar outro candidato/fold hoje.
- **Ambiente:** Windows 11, Python 3.14.7, RX 7600/ROCm; reaproveitar código e protocolo da Etapa 4, respeitando a divisão agrupada. Baseline TF-IDF do fold 1 completo `C=0,5`: 44,61% acurácia, 44,35% macro-F1.
- **Execução e resultados:** `python src/bert_stage4.py start512_lr2e5 --run-id etapa5_start512_lr2e5_fold1_full_20260924_2300 --fold 1 --full-fold --max-steps 896 --eval-every 384 --stage 5`. Loader de treino baseado nas 11.488 linhas do fold 1, mas treino limitado a 896 passos (0,624 época; 7.168 exemplos processados); validação integral de 5.580 linhas, seed `20260924`; avaliações nos passos 384, 768 e 896. Melhor checkpoint no passo 896: **43,85% acurácia**, **43,23% macro-F1**, recalls `c1` 44,43%, `c234` 30,74%, `c5` 56,16%. TF-IDF `C=0,5` no fold 1: 44,61%/44,35% (acurácia/macro-F1); diferença BERT −0,76 pp em acurácia e −1,12 pp em macro-F1. Tempo 1.376,361 s (22,94 min), pico alocado 3,25 GB. Checkpoint recarregado com sucesso, logits finitos `[5,3]`. Só este candidato/fold foi executado hoje; holdout preservado.
- **Artefatos:** `configs/bert_stage5.json`; código reutilizável estendido em `src/bert_stage4.py`; métricas e configuração em `runs/etapa5/etapa5_start512_lr2e5_fold1_full_20260924_2300/`; checkpoint em `models/bert_stage5/etapa5_start512_lr2e5_fold1_full_20260924_2300/best/`; curvas e análise em `reports/etapa5_part1.md` e `reports/etapa5/`.
- **Limitações e decisão parcial:** avaliação de um fold não confirma estabilidade nem escolhe o modelo final. A comparação com baseline não tem duração equivalente: o TF-IDF usou as 11.488 linhas de treino e o BERT processou 7.168 (0,624 época) até o passo 896. Assim, a acurácia menor do BERT é sinal preliminar, não motivo para descartar o candidato. Amanhã definir duração consistente para folds e avaliar também o finalista alternativo dentro da janela de quatro horas. O orçamento inicial de busca (0–4) totaliza cerca de 114,67 min; com este caso, o uso experimental soma 137,61 min. A janela adicional de quatro horas para Etapa 5 foi autorizada pelo usuário independentemente desse saldo.
- **Novo estado:** Etapa 5 continua em andamento; parte 1 concluída. Retomar amanhã na própria Etapa 5; não iniciar Etapa 6.

**Aditamento de escopo — 24/09/2026, Etapa 5**

- **Autorização recebida:** usuário pediu incluir a confirmação nos folds 2 e 3 mesmo se as execuções não couberem nas quatro horas de janela inicialmente disponíveis amanhã.
- **Decisão registrada:** executar os dois finalistas nos folds 2 e 3 com protocolo e duração consistentes; caso necessário, continuar em sessões posteriores até concluir. Não encerrar a confirmação desses folds só porque a janela inicial de quatro horas terminou.

**Atualização do plano — 24/09/2026 23:50 BRT, subdivisão da Etapa 5**

- **Solicitação:** usuário pediu que a própria seção da Etapa 5 no plano enumerasse as subdivisões.
- **Alteração:** registrada a sequência (a) primeira corrida preliminar, concluída; (b) fixar duração comum; (c) comparar ambos finalistas no fold 1; (d) confirmar ambos nos folds 2 e 3, mesmo se ultrapassar a janela de quatro horas; (e) agregar métricas e escolher; (f) avaliar o holdout uma única vez depois de congelar a escolha.
- **Estado:** Etapa 5 continua em andamento; somente (a) está concluída.

**Sessão — 24/09/2026 23:56 BRT, Etapa 5b (protocolo comum)**

- **Autorização/escopo:** usuário autorizou executar a subdivisão (b) e solicitou que seja pedida autorização antes de cada subdivisão da Etapa 5. Portanto, nenhum experimento da subdivisão (c) foi iniciado nesta sessão.
- **Decisão:** fixado protocolo de até duas épocas para cada finalista em cada fold; validação integral a cada 384 passos e no fim de cada época; early stopping com mínimo de 512 passos e paciência de três avaliações a partir desse mínimo. Acurácia é o critério primário de seleção do checkpoint e macro-F1 desempata. A comparação usa TF-IDF `C=0,5` nos mesmos folds.
- **Detalhe por fold:** com lote efetivo 8, os máximos são 1.436, 1.431 e 1.399 passos por época nos folds 1–3, respectivamente. Grupos incompletos de acumulação são descartados no fim da época, sem carregar gradientes entre épocas; a contagem de exemplos omitidos fica registrada por execução. Isso mantém as épocas independentes apesar dos tamanhos diferentes dos folds.
- **Revisão de implementação:** `src/bert_stage4.py` passou a avaliar também no limite de época e a contar a paciência somente depois do passo mínimo. Resultados anteriores permanecem intactos. O caso 5a, limitado ao passo 896 (0,624 época), é exploratório e será refeito em 5c sob o protocolo comum.
- **Artefatos:** `configs/bert_stage5_protocol.json`; `reports/etapa5_protocol.md`; alteração em `src/bert_stage4.py`.
- **Novo estado:** subdivisões 5a e 5b concluídas; etapa 5 em andamento. Próxima ação é a subdivisão 5c, que requer autorização explícita do usuário.

**Sessão — 24/09/2026 23:59–25/09/2026 01:10 BRT, Etapa 5c (comparação no fold 1)**

- **Autorização recebida:** usuário autorizou iniciar a subdivisão 5c. O escopo é executar os dois finalistas no fold 1 com o protocolo comum da subdivisão 5b; esta autorização não inclui iniciar as subdivisões seguintes.
- **Plano de execução:** rodar sequencialmente `start512_lr2e5` e `headtail256_lr2e5`, ambos com treino e validação completos do fold 1, até duas épocas, avaliações a cada 384 passos e ao fim de cada época, early stopping e comparação com TF-IDF `C=0,5` do mesmo fold.
- **Estado ao iniciar:** holdout intacto; corrida anterior de `start512_lr2e5` permanece preservada como preliminar; nenhum experimento 5c do fold 1 ainda concluído.
- **Resultados parciais e artefatos:** `start512_lr2e5` completou duas épocas no fold 1: melhor passo 2.688, acurácia 45,14%, macro-F1 44,51%; TF-IDF `C=0,5` no mesmo fold teve 44,61%/44,35%. `headtail256_lr2e5` foi adiado para amanhã de manhã por solicitação do usuário. Ver `reports/etapa5c_fold1_partial.md`. Não iniciar fold 2/3 nesta subdivisão.
- **Ajuste de escopo (25/09/2026):** usuário pediu que, após concluir a execução atual de `start512_lr2e5`, o estado seja salvo e `headtail256_lr2e5` fique para amanhã de manhã. Não iniciar o segundo candidato nesta sessão; manter 5c em andamento até ele ser executado.
- **Execução parcial concluída:** a primeira tentativa no isolamento falhou em zero passos com `hipErrorInvalidImage`; a repetição fora do isolamento concluiu normalmente. Comando: `python src/bert_stage4.py start512_lr2e5 --run-id etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed --fold 1 --full-fold --eval-every 384 --stage 5`. Duas épocas completas, 2.872 passos; melhor passo 2.688, 45,143% de acurácia e 44,507% de macro-F1, contra TF-IDF `C=0,5` no mesmo fold 44,606%/44,349% (+0,54/+0,16 pp). Acurácia e macro-F1 do último passo 2.872 caíram para 44,176%/42,215%, então o checkpoint selecionado segue sendo o melhor (2.688). Tempo 4.241,518 s (70,69 min), pico alocado 3,25 GB; recarga válida com logits finitos `[5,3]`.
- **Artefatos e limitação:** métricas em `runs/etapa5/etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed/metrics.json`; checkpoint em `models/bert_stage5/etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed/best/`; curvas em `reports/etapa5/`; síntese em `reports/etapa5c_fold1_partial.md`. A pequena vantagem sobre TF-IDF é de um único fold e não confirma superioridade geral; recall de `c234` continua inferior ao baseline. O holdout não foi consultado.
- **Consumo experimental acumulado:** cerca de 208,30 min de tempo de comando GPU — 114,67 min nas Etapas 0–4, 22,94 min da corrida preliminar 5a e 70,69 min desta corrida 5c. A tentativa isolada que falhou antes do primeiro passo não entra nessa soma.
- **Novo estado:** execução de `start512_lr2e5` concluída; não foi iniciado `headtail256_lr2e5` conforme pedido. Subdivisão 5c e Etapa 5 continuam em andamento; retomar amanhã de manhã com o segundo finalista no fold 1.

**Atualização do plano — 25/09/2026 01:24 BRT, futura Etapa 5c.1**

- **Solicitação:** integrar ablação controlada de conflitos após 5c e antes de 5d, sem executar novos treinos, alterar dados originais, refazer folds ou consultar o holdout. Pedir autorização antes de iniciar a nova subdivisão.
- **Inspeção prévia:** lidos o plano, relatórios e configurações das Etapas 1–5, inventário de registros/checkpoints, `data/splits_grouped_v1.json`, `data/row_manifest.csv` e código de agrupamento/treino/métricas. A fonte e divisão continuam com hashes `0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818` e `aa9c99a79ccccc3655399761c53098f5fd3d770c9aa6c8b68be29c49eba3586b`. Não há repositório Git no diretório atual; futuros manifests registrarão commit apenas se Git estiver disponível.
- **Compatibilidade verificada apenas por leitura:** fold 1 com 11.488 exemplos de treino, 5.580 de validação e zero grupos compartilhados. No treino há 169 grupos conflitantes/1.223 linhas: B teria 10.265 linhas; C teria 10.806, após tratar 92 grupos por maioria única e remover 77 grupos empatados. As contagens são projeções da regra, não resultados de treinamento nem manifests autorizados.
- **Decisão de integração:** inserir 5c.1 pendente com A/B/C no treino do fold 1, referência BERT fixada após 5c, controle A reutilizado se estritamente equivalente; reorganizar 5d para confirmar política Original versus melhor alternativa nos folds 2 e 3 e depois ambos os finalistas sob a política congelada. 5e congela modelo + política de dados + protocolo; 5f consulta o holdout uma vez; Etapa 6 recebe somente a decisão definitiva. Métricas adicionais de A poderão ser derivadas da matriz de confusão já salva.
- **Arquivos:** `plan.md` atualizado; criados `configs/bert_stage5_conflict_ablation.json` e `reports/etapa5_conflict_ablation.md` como especificação da execução futura. Nenhum código, índice persistido, dataset original, relatório histórico ou checkpoint foi alterado.
- **Novo estado:** somente esta **atualização do plano** foi concluída. A 5c permanece parcial; a 5c.1 e as subdivisões seguintes permanecem pendentes. A 5c.1 requer autorização explícita após a conclusão da 5c.

**Retomada — 25/09/2026 10:42–11:18 BRT, conclusão da Etapa 5c**

- **Autorização:** usuário pediu “Retoma a 5c”; foi executado somente o finalista restante `headtail256_lr2e5` no fold 1. Comando: `python src/bert_stage4.py headtail256_lr2e5 --run-id etapa5c_headtail256_lr2e5_fold1_20260925_resume --fold 1 --full-fold --eval-every 384 --stage 5`.
- **Resultado:** treino Original de 11.488 linhas, validação integral de 5.580, seed `20260924`, lote efetivo 8. Melhor checkpoint no passo 1.436: 44,803% de acurácia e 44,644% de macro-F1; early stopping no passo 2.304 após 1,604 época. Tempo 2.138,175 s (35,64 min); pico alocado 2,37 GB; recarga do checkpoint válida com logits finitos `[5,3]`.
- **Comparação e decisão:** `start512_lr2e5` manteve a maior acurácia (45,143% contra 44,803%, diferença +0,341 pp), embora `headtail256_lr2e5` tenha macro-F1 ligeiramente maior (44,644% contra 44,507%). Pelo critério fixado em 5b, `start512_lr2e5` é o BERT de referência da ablação 5c.1. Ambos os finalistas continuam previstos para a confirmação posterior nos folds 2 e 3 sob a política de dados escolhida. Ver `reports/etapa5c_fold1_final.md`.
- **Artefatos:** métricas em `runs/etapa5/etapa5c_headtail256_lr2e5_fold1_20260925_resume/metrics.json`; checkpoint em `models/bert_stage5/etapa5c_headtail256_lr2e5_fold1_20260925_resume/best/`; curvas em `reports/etapa5/`. A corrida 512, a corrida preliminar 5a e o relatório parcial foram preservados.
- **Estado:** 5c concluída; 5c.1 **pendente**, com B/C ainda não gerados nem treinados. Holdout intacto. Solicitar autorização específica antes de iniciar 5c.1.

**Sessão — 25/09/2026 11:48–15:11 BRT, Etapa 5c.1 (ablação de conflitos, fold 1)**

- **Autorização recebida:** usuário autorizou iniciar 5c.1. Não iniciou 5d.
- **Integridade e manifests:** criados `data/stage5_conflict_ablation/fold1_original.json`, `fold1_remove_conflicts.json` e `fold1_majority_conflicts.json`, com hashes SHA-256 em sidecars `.sha256`. `src/prepare_stage5_conflict_ablation.py` conferiu hashes da fonte, split e row manifest; ordem exata dos índices; A igual ao treino original; nenhum exemplo conflitante em B; C sem conflito nem grupo empatado; rótulos/classes preservados; nenhuma migração entre partições; validação e holdout idênticos. Asserções passaram antes da GPU e novamente em `--validate-only`. Holdout não foi avaliado.
- **Controle A:** reutilizado `etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed` após comprovar fonte/split, fold completo, ordem dos índices, candidato, seed, modelo/tokenizer, parâmetros de otimização, protocolo, versões e checkpoint compatíveis. O loader de manifestos é um seletor dos índices de treino; o loop de treino/avaliação não foi alterado.
- **Treinos novos:** B (`etapa5c1_B_remove_conflicts_fold1_20260925`) usou 10.265 exemplos, removeu 1.223 (10,65%), completou 2 épocas/2.566 passos, melhor passo 2.304: acurácia 45,090%, macro-F1 44,255%, weighted-F1 44,137%; 62,96 min, pico alocado 3,26 GB. C (`etapa5c1_C_majority_conflicts_fold1_20260925`) usou 10.806 exemplos, removeu 682 (5,94%), early stopping no passo 2.688 (1,991 épocas), melhor passo 1.536: acurácia 44,946%, macro-F1 44,666%, weighted-F1 44,610%; 64,20 min, pico alocado 3,27 GB. Ambos recarregaram com logits finitos `[5,3]`.
- **Comparação:** A manteve 45,143% de acurácia (macro-F1 44,507%; weighted-F1 44,479%). Δ B−A: −0,054/−0,252/−0,342 pp para accuracy/macro-F1/weighted-F1. Δ C−A: −0,197/+0,159/+0,131 pp. C melhorou macro-F1, mas nenhuma alternativa superou A na acurácia principal. B/C redistribuíram recall entre classes e reduziram recall de `c5` em relação a A; as matrizes e métricas por classe estão no relatório.
- **Decisão e estado:** política Original segue para confirmação na 5d; não há alternativa a confirmar. 5c.1 concluída. A subdivisão 5d permanece pendente e requer autorização explícita. Ver `reports/etapa5_conflict_ablation.md` e `configs/bert_stage5_conflict_ablation.json`.

**Sessão — 25/09/2026 16:56–17:28 BRT, Etapa 5c.2 (diagnóstico incremental)**

- **Autorização recebida:** usuário forneceu instrução explícita para inserir a subdivisão 5c.2 antes da 5d e executá-la incrementalmente. A instrução proíbe acesso ao holdout e novas buscas de hiperparâmetros; qualquer treino novo exige proposta prévia.
- **Estado ao iniciar:** 5c e 5c.1 concluídas; 5d pendente. Fold 1 contém treino/validação já estabelecidos; holdout permanece reservado.
- **Objetivo desta sessão:** formalizar 5c.2 no plano, analisar os artefatos existentes e completar os diagnósticos possíveis sem treino novo. Não iniciar 5d.
- **Arquivos e versões de entrada:** `train.xlsx`, `ep1-enunciado.pdf`, métricas/checkpoints dos experimentos 5c e 5c.1, `data/splits_grouped_v1.json`, `data/row_manifest.csv`; dependências registradas nos manifests das corridas.
- **Execução e resultados:** criou-se `src/diagnose_stage5_dataset_limit.py`. O checkpoint A foi inferido sem gradientes na GPU (ROCm PyTorch 2.13.0, Transformers 4.56.2, RX 7600); duração exata da inferência não foi persistida pelo script. Não houve treinamento. O resultado reproduziu exatamente accuracy/macro-F1/matriz da validação registrada na 5c. Treino completo: 59,03% accuracy, 58,39% macro-F1, gap 13,88 p.p.; validação: 45,14%, 44,51%. Previsões e probabilidades em 5.580 linhas da validação estão em `runs/etapa5/diagnose_fold1_dataset_limit_20260925/`; recarga e métricas bateram com A.
- **Análises:** calculadas precision/recall/F1 por classe, matriz absoluta e normalizada, pares de erro e estatísticas top-1/margem/entropia; criada amostra determinística de 60 exemplos com entrada efetiva decodificada em `reports/etapa5_dataset_limit_diagnosis_examples.md`. Similaridade TF-IDF lexical nos 1.890 exemplos verdadeiros c234 comparou vizinhos das três classes sem treinar classificador; resultado salvo em `tfidf_similarity.json`. A planilha de treino oferece apenas `resp_text` e `clarity`; não havia outro texto para teste controlado de contexto. `test*.xlsx` não foi aberto.
- **Conclusões documentadas:** c234 é a classe mais difícil e as suas previsões têm menor margem/maior entropia; 71,4% dos erros são entre classes adjacentes, com 28,6% entre extremos. Apenas 1,01% dos erros têm confiança ≥0,80. A similaridade lexical dos textos c234 fica um pouco mais alta com c234 que com extremos, mas os vizinhos distribuem-se quase igualmente entre as três classes. O BERT excede o TF-IDF no fold 1 por margens pequenas; A/B/C quase não mudam accuracy. As evidências e limites estão em `reports/etapa5_dataset_limit_diagnosis.md` e seu apêndice. Não se concluiu teto absoluto, erro de anotação individual ou benefício de contexto ausente.
- **Holdout e integridade:** nenhum rótulo mudou, nenhum fold foi criado, nenhum `test*.xlsx` foi aberto; a leitura da planilha extraiu apenas linhas pertencentes ao treino e validação do fold 1 e descartou as demais. Holdout permanece intacto.
- **Novo estado:** 5c.2 concluída; Etapa 5 continua em andamento; 5d permanece pendente e exige autorização explícita. Recomenda-se confirmar a configuração atual nos folds 2 e 3 quando autorizado.

**Revisão qualitativa — 25/09/2026, 60 exemplos da 5c.2**

- **Solicitação:** usuário pediu revisão dos 60 exemplos do apêndice, descrevendo padrões observáveis sem alterar rótulos ou tratar discordância como prova de anotação incorreta.
- **Material revisto:** texto efetivamente fornecido ao BERT, rótulo observado, previsão, confiança, probabilidades e motivo de seleção de todos os 60 exemplos; também foram lidos seus contextos completos (até 512 tokens).
- **Observações:** respostas com linguagem institucional padronizada surgem em todas as classes. Há mensagens longas de recusa/encaminhamento com citações legais e mensagens muito curtas que remetem a anexo/link/contato. As discordâncias incluem quatro `c234→c1` de alta confiança em respostas do Banco do Brasil com modelo de texto semelhante e quatro `c1→c5` de alta confiança em respostas/encaminhamentos curtos ou objetivos; isto caracteriza erro do modelo frente ao rótulo usado na avaliação, não evidência de que o rótulo seja errado. Conteúdo de anexo ausente torna impossível julgar a resposta anexada apenas pelo campo `resp_text` em exemplos como “segue em anexo, resposta para conhecimento”.
- **Conflitos e representatividade:** os 60 itens foram intencionalmente estratificados e incluem 48 discordâncias; não estimam prevalência de erro. Não há grupo normalizado repetido dentro da amostra. Na validação completa do fold 1 há 93 grupos com rótulos conflitantes (423 linhas), uma possível inconsistência entre avaliações, sem adjudicação disponível. Os padrões qualitativos e as limitações foram acrescentados a `reports/etapa5_dataset_limit_diagnosis.md`; o apêndice completo foi preservado. Nenhum rótulo ou métrica foi alterado.
- **Estado:** 5c.2 permanece concluída; 5d continua pendente, sem autorização ou execução nesta revisão.

**Início da sessão — 25/09/2026 17:44 BRT, Etapa 5d**

- **Autorização recebida:** usuário autorizou “Pode iniciar a 5d”. Escopo desta sessão limitado à confirmação sob a política Original nos folds 2 e 3 para os dois finalistas BERT; nenhuma etapa 5e/f ou Etapa 6 fica autorizada por esta mensagem.
- **Estado ao iniciar:** 5c, 5c.1 e 5c.2 concluídas; 5d pendente. Fold 1 possui resultados dos dois finalistas sob protocolo comum, além da comparação A/B/C. Holdout preservado e proibido nesta etapa.
- **Entradas/protocolo:** `train.xlsx` e `data/splits_grouped_v1.json` da divisão `grouped_v1_seed_20260924`; configuração `configs/bert_stage5_protocol.json`; candidatos `start512_lr2e5` e `headtail256_lr2e5`; política Original; seed 20260924; até duas épocas; validação completa a cada 384 passos e no limite de época; early stopping conforme protocolo; critério acurácia com macro-F1 para desempate.
- **Plano de execução:** treinar sequencialmente os dois finalistas nos folds 2 e 3; reutilizar os resultados 5c do fold 1. As corridas serão persistidas em `runs/etapa5/`, checkpoints em `models/bert_stage5/`, curvas e síntese em `reports/`. Não avaliar holdout, não criar folds e não alterar rótulos.
- **Ambiente/comandos/resultados:** a preencher após preflight e cada execução.
- **Novo estado:** 5d em andamento; próxima subdivisão proibida até autorização específica.

**Progresso — 25/09/2026, 5d, primeiro candidato no fold 2**

- **Corrida concluída:** `start512_lr2e5`, run `etapa5d_start512_lr2e5_fold2_20260925`; 11.451 treino/5.617 validação; Original; seed 20260924; duas épocas completas/2.862 passos. Melhor checkpoint no passo 2.304: accuracy 45,540%, macro-F1 45,471%; último passo 2.862: accuracy 45,148%, macro-F1 44,580%. Early stopping não acionado. Tempo de parede 4.168,687 s (69,48 min), pico alocado 3,252 GB. Checkpoint recarregado, logits `[5,3]` finitos.
- **Comparação contextual:** TF-IDF `C=0,5` no fold 2: 44,134% accuracy e 43,881% macro-F1; comparação descritiva, pois o estimador e custo diferem. Resultado BERT deste fold excede o baseline em +1,407 p.p. accuracy e +1,590 p.p. macro-F1.
- **Artefatos:** `runs/etapa5/etapa5d_start512_lr2e5_fold2_20260925/metrics.json` e `config.json`; checkpoint em `models/bert_stage5/etapa5d_start512_lr2e5_fold2_20260925/best/`; curvas `reports/etapa5/etapa5d_start512_lr2e5_fold2_20260925_accuracy.svg` e `_loss.svg`.
- **Estado:** primeira de quatro corridas da 5d concluída; segunda corrida, `headtail256_lr2e5` fold 2, iniciada. Holdout permanece intacto. Não calcular escolha final nem avançar para 5e até terminar as quatro corridas e consolidar conforme o plano.

**Retomada — 25/09/2026 20:56 BRT, Etapa 5d**

- **Autorização/escopo:** retomada solicitada pelo usuário com base neste plano; continuar exclusivamente a 5d, cuja autorização está registrada acima. Não iniciar 5e/5f ou Etapa 6.
- **Verificação do estado:** não havia processo Python ativo. A segunda corrida estava concluída e seus artefatos persistidos, embora a última linha do plano ainda a registrasse como iniciada.
- **Segunda corrida concluída:** `headtail256_lr2e5`, run `etapa5d_headtail256_lr2e5_fold2_20260925`; treino 11.451, validação 5.617, duas épocas/2.862 passos; melhor checkpoint no passo 2.304 com accuracy 45,042% e macro-F1 44,818%; último passo 44,294%/44,472%. Early stopping não acionado; 2.695,592 s (44,93 min), pico alocado 2,373 GB; recarga válida, logits finitos `[5,3]`. Artefatos em `runs/etapa5/etapa5d_headtail256_lr2e5_fold2_20260925/`, `models/bert_stage5/etapa5d_headtail256_lr2e5_fold2_20260925/best/` e curvas `reports/etapa5/`.
- **Estado após retomada:** 2 de 4 corridas da 5d concluídas; faltam os dois finalistas no fold 3. Holdout intacto. Nenhuma agregação/seleção final executada.
- **Ambiente/comando e resultados das execuções restantes:** a preencher após cada corrida.

**Progresso — 25/09/2026, 5d, candidato `start512_lr2e5` no fold 3**

- **Comando:** `.venv\Scripts\python.exe src/bert_stage4.py start512_lr2e5 --run-id etapa5d_start512_lr2e5_fold3_20260925_resume --fold 3 --full-fold --eval-every 384 --stage 5` (Windows 11, Python 3.14.7, RX 7600/ROCm; ambiente do projeto).
- **Resultado:** treino Original de 11.197 linhas e validação de 5.871; duas épocas completas/2.798 passos. Melhor checkpoint no passo 2.688: accuracy 44,337% e macro-F1 44,093%. Última avaliação: 43,330%/42,486%. Early stopping não acionado; tempo de parede 4.205,731 s (70,10 min), pico alocado 3,248 GB. Checkpoint recarregado com logits finitos `[5,3]`.
- **Artefatos:** métricas em `runs/etapa5/etapa5d_start512_lr2e5_fold3_20260925_resume/metrics.json`; checkpoint em `models/bert_stage5/etapa5d_start512_lr2e5_fold3_20260925_resume/best/`; curvas em `reports/etapa5/`.
- **Estado:** 3 de 4 corridas da 5d concluídas. Falta somente `headtail256_lr2e5` no fold 3. Ainda não consolidar/selecionar finalista nem consultar o holdout.

**Conclusão — 25/09/2026 23:00 BRT, Etapa 5d**

- **Quarta corrida:** `.venv\Scripts\python.exe src/bert_stage4.py headtail256_lr2e5 --run-id etapa5d_headtail256_lr2e5_fold3_20260925_resume --fold 3 --full-fold --eval-every 384 --stage 5`; treino 11.197, validação 5.871; duas épocas/2.798 passos; melhor checkpoint no passo 2.688: accuracy 44,882% e macro-F1 44,914%. Último passo 2.798: 44,461%/43,811%. Early stopping não acionado; 2.701,351 s (45,02 min), pico alocado 2,373 GB; recarga válida com logits finitos `[5,3]`. Métricas em `runs/etapa5/etapa5d_headtail256_lr2e5_fold3_20260925_resume/metrics.json`, checkpoint em `models/bert_stage5/etapa5d_headtail256_lr2e5_fold3_20260925_resume/best/`, curvas em `reports/etapa5/`.
- **Consolidação:** executado `src/summarize_stage5d.py`, que verificou candidate/fold, recarga e campo de holdout das seis corridas, e pareou as métricas com TF-IDF `C=0,5`. `start512_lr2e5`: 45,007% accuracy média (DP 0,613 p.p.), 44,690% macro-F1; `headtail256_lr2e5`: 44,909% (DP 0,122 p.p.), 44,792%; baseline: 44,705%/44,453%. A regra de acurácia média aponta `start512_lr2e5`, por +0,098 p.p.; a alternativa início + fim tem +0,102 p.p. em macro-F1 médio e custo médio 41,86 min/corrida contra 70,09 min. Diferença pequena e não prova superioridade estatística. Comparação por fold e limitações em `reports/etapa5d_confirmation.md`; valores completos em `runs/etapa5/stage5d_confirmation_summary.json`.
- **Integridade:** hashes da fonte e divisão conferidos pelo resumo contra o baseline; holdout marcado não avaliado em todas as corridas. Sem alterações a rótulos, índices ou divisão.
- **Estado e parada:** 5d concluída; Etapa 5 continua em andamento. Próxima subdivisão é 5e (congelar modelo, política e protocolo), ainda pendente e exige autorização explícita. Nenhuma seleção de configuração de treino final ou consulta ao holdout foi feita.

**Início — 25/09/2026 23:15 BRT, Etapa 5e**

- **Autorização recebida:** usuário autorizou explicitamente “Pode rodar a etapa 5e”. Escopo limitado à análise e ao congelamento do modelo, da política de dados e do protocolo de treino final; não iniciar 5f ou Etapa 6.
- **Ambiente:** Windows 11, projeto `.venv` (Python 3.14.7), edição de configurações e documentos; nenhuma GPU ou treinamento previsto.
- **Objetivo:** auditar as métricas completas dos seis runs BERT e do baseline, definir a especificação única do treinamento final e persistir sua configuração reproduzível. Manter a validação final reservada para a subdivisão 5f.
- **Revisão documental de 5d:** a conferência cruzada dos `metrics.json` e `data/splits_grouped_v1.json` encontrou contagens incorretas no registro manual do fold 3. As duas corridas são 11.197 linhas de treino e 5.871 de validação (não 11.193/5.595). Métricas, checkpoint e divisão já usados estão corretos; corrigir os registros anteriores sem recalcular ou mudar resultados.

**Conclusão — 25/09/2026 23:27 BRT, Etapa 5e**

- **Análise:** confirmadas seis execuções do BERT e o baseline pareado; reconstituídas matrizes agregadas e recalls por classe a partir dos checkpoints selecionados. `start512_lr2e5` obteve 45,007% de acurácia média e 44,690% de macro-F1; `headtail256_lr2e5`, 44,909% e 44,792%; TF-IDF, 44,705% e 44,453%. Diferenças entre finalistas são pequenas, com tradeoff de classe: início + fim tem recall médio `c234` maior (+5,77 p.p.), início 512 tem `c1` (+3,44 p.p.) e `c5` (+2,83 p.p.) maior. Conforme a regra primária de acurácia já fixada, congelado `start512_lr2e5`; não se afirma superioridade estatística.
- **Configuração congelada:** modelo/tokenizer `neuralmind/bert-base-portuguese-cased` na revisão `94d69c95f98f7d5b2a8700c420230ae10def0baa`, classificação `c1/c234/c5`, representação start, 512 tokens, AdamW `2e-5`, `weight_decay=0,01`, sem scheduler/warmup, batch efetivo 8, seed `20260924`. Política Original retém todas as linhas e rótulos, incluindo os 1.975 itens em 316 grupos conflitantes.
- **Duração do treino final:** melhores passos do candidato selecionado correspondem a 1,8719/1,6101/1,9214 épocas nos folds 1/2/3; média 1,8011. Com 20.092 exemplos e 2.511 steps/época, congelados 4.523 updates, equivalentes a 1,8011 épocas. O treino final ocorrerá após a auditoria 5f com todos os dados, sem validação ou early stopping, salvando ao fim desse limite fixo.
- **Artefatos:** `configs/bert_stage5_final.json` e `reports/etapa5e_final_spec.md`. Nenhuma GPU, treino, avaliação do holdout ou leitura de `test.xlsx` foi feita. Configuração em JSON carregada e valores centrais conferidos.
- **Estado e parada:** 5e concluída; 5f pendente. Solicitar autorização explícita antes de consultar o holdout; ainda não iniciar a Etapa 6.

**Início — 26/09/2026 08:34 BRT, Etapa 5f**

- **Autorização recebida:** usuário autorizou explicitamente “Pode iniciar a 5f”. Escopo limitado à auditoria única 5f; não iniciar Etapa 6.
- **Estado ao iniciar:** 5e concluída e especificação congelada em `configs/bert_stage5_final.json`; 5f pendente. Holdout ainda não consultado nesta execução.
- **Objetivo/protocolo:** ajustar do zero o modelo congelado somente nos 17.068 índices de desenvolvimento, sem validação/seleção, por duração equivalente de 1,8011 épocas (3.842 updates); depois executar uma única inferência sobre os 3.024 índices holdout e registrar métricas e previsões sem retunar.
- **Integridade:** confirmar hashes da fonte/divisão e disjunção dos índices/grupos antes do treino; modelo/tokenizer na revisão congelada, carregados localmente. `test.xlsx` não faz parte desta etapa.
- **Ambiente, artefatos, resultados e horários:** a preencher após preflight e execução.
- **Novo estado:** 5f em andamento; parar ao concluir a auditoria e pedir autorização antes da Etapa 6.

**Conclusão — 26/09/2026 09:29 BRT, Etapa 5f**

- **Treino de auditoria:** execução `etapa5f_start512_lr2e5_audit_20260926`; modelo inicializado do checkpoint pré-treinado congelado e ajustado somente nos 17.068 índices de desenvolvimento. Foram concluídos os 3.842 updates fixos (1,8012 épocas equivalentes), sem validação, early stopping ou seleção. Tempo 2.834,67 s (47,24 min), pico de memória alocada 3,03 GiB.
- **Integridade:** hashes de `train.xlsx`, divisão e manifesto de linhas conferidos; nenhuma sobreposição de índices ou grupos entre desenvolvimento e holdout. O holdout foi aberto para a avaliação somente após o checkpoint de auditoria ter sido salvo e teve uma única passagem de inferência. `test.xlsx` não foi acessado.
- **Resultado holdout (n=3.024):** acurácia 45,966%, macro-F1 44,523%, loss 1,0429. Recalls: `c1` 51,261% (n=952), `c234` 24,131% (n=1.036), `c5` 62,934% (n=1.036). Matriz: `[[488,188,276],[353,250,433],[194,190,652]]`. Descritivamente, acurácia próxima à média dos folds internos (45,007%); comparação não demonstra ganho. Recall baixo em `c234` continua como limitação. Resultado não alterou a escolha ou protocolo congelado.
- **Artefatos:** relatório `reports/etapa5f_holdout_audit.md`; métricas, previsões, log e manifesto em `runs/etapa5f/etapa5f_start512_lr2e5_audit_20260926/`; checkpoint em `models/bert_stage5f/etapa5f_start512_lr2e5_audit_20260926/final/`; runner em `src/run_stage5f_holdout_audit.py`.
- **Estado e parada:** Etapa 5 concluída. Etapa 6 continua pendente e não foi iniciada; solicitar autorização explícita.

**Início — 26/09/2026 09:34 BRT, Etapa 6**

- **Autorização recebida:** usuário autorizou explicitamente “Pode iniciar a etapa 6”. Escopo limitado ao treino integral e à validação do artefato final; não iniciar a Etapa 7.
- **Entrada:** configuração congelada em `configs/bert_stage5_final.json` e auditoria 5f concluída. Usar a política Original e todas as 20.092 linhas de `train.xlsx`, inclusive holdout, conforme previsto antes da auditoria.
- **Protocolo congelado:** BERTimbau Base e tokenizer na revisão `94d69c95f98f7d5b2a8700c420230ae10def0baa`; cabeça nova de 3 classes; início/512 tokens; seed `20260924`; AdamW `2e-5`, `weight_decay=0,01`, batch efetivo 8, sem scheduler/warmup, validação ou early stopping; duração fixa 4.523 updates.
- **Integridade/parada:** registrar hashes e manifestar os índices usados. Não voltar a calcular métricas do holdout nem usar o seu resultado para mudar configuração. Validar recarga e saída do modelo em exemplos de treino; não abrir `test.xlsx` nem iniciar inferência da Etapa 7.
- **Ambiente, comando, artefatos, resultados e horários:** a preencher após preflight e execução.
- **Novo estado:** Etapa 6 em andamento; parar após o modelo estar salvo e validado, e solicitar autorização para a Etapa 7.

**Conclusão — 26/09/2026 10:40 BRT, Etapa 6**

- **Execução:** `.venv\Scripts\python.exe src/run_stage6_final.py --run-id etapa6_final_20260926`; 20.092 exemplos, todos os rótulos da política Original, sem validação/early stopping e sem retuning; 4.523 updates completos (1,8013 épocas equivalentes). Treino em 3.401,84 s (56,70 min), pico de memória alocada 3.266.404.352 bytes (3,04 GiB), AMD Radeon RX 7600.
- **Integridade:** hashes da configuração congelada, fonte, divisão e manifesto verificados. Foram manifestados todos os índices usados. Nenhuma reavaliação do holdout ou acesso a `test.xlsx`; o holdout foi incluído no treino integral conforme decisão congelada na 5e.
- **Validação do artefato:** modelo e tokenizer recarregados de `models/bert_final/`; em cinco linhas de treino, previsões repetidas idênticas, logits/probabilidades `[5,3]`, probabilidades finitas somando 1 e classes válidas. Validação passou.
- **Artefatos:** modelo `models/bert_final/`; run, log e manifesto em `runs/etapa6/etapa6_final_20260926/`; resumo `reports/etapa6/etapa6_final_20260926_summary.json`; relatório `reports/etapa6_final.md`; inferência `src/predict_final.py` e treino `src/run_stage6_final.py`.
- **Estado e parada:** Etapa 6 concluída. Etapa 7 permanece pendente, depende da inspeção de `test1.xlsx` e de autorização específica; não iniciada.

**Correção de arquivo — 26/09/2026 10:46 BRT**

- **Esclarecimento do usuário:** `test1.xlsx` é justamente o arquivo do conjunto de teste mencionado na Etapa 7; a nota histórica de que os nomes não correspondiam foi superada por esta confirmação.
- **Atualização:** Etapa 7 agora registra `test1.xlsx` como disponível e aguarda autorização específica. O arquivo não foi aberto nem analisado nesta correção.


**Início — 26/09/2026 10:53 BRT, Etapa 7**

- **Autorização:** o usuário autorizou explicitamente “Pode executar a etapa 7”. Escopo: inferir somente no arquivo de teste e entregar a planilha preenchida; não iniciar a Etapa 8.
- **Arquivo e especificação:** 	est1.xlsx, aba 	est1, 900 respostas, colunas esp_text e clarity; a coluna clarity está vazia em todas as linhas. O destino das predições está claro; nenhuma etiqueta de teste será usada para seleção ou avaliação.
- **Modelo:** artefato final validado da Etapa 6 em models/bert_final/, classes c1, c234 e c5, máximo 512 tokens; inferência em lotes.
- **Execução:** ID $runId; relatório/log e dados técnicos em uns/etapa7/etapa7_20260926_105326_ca987906/; saída pretendida em outputs/etapa7_20260926_105326_ca987906/test1_predito.xlsx. Original preservado.
- **Validação prevista:** manter aba, cabeçalhos, ordem/contagem das 900 linhas e coluna A; confirmar classes válidas, amostra e reabertura do arquivo exportado.
- **Novo estado:** Etapa 7 em andamento; interromper após validar a entrega e solicitar autorização para a Etapa 8.


**Conclusão — 26/09/2026 11:05 BRT, Etapa 7**

- **Inferência:** modelo final da Etapa 6 executado em 900 textos de `test1.xlsx`, somente na GPU AMD Radeon RX 7600, em lotes de 8 e máximo 512 tokens; 43,45 s. A tentativa GPU dentro do sandbox falhou com kernel ROCm inválido; por solicitação do usuário, execução fora do sandbox concluiu. Nenhum rótulo do teste foi usado para avaliação ou seleção.
- **Distribuição predita:** `c1` 319, `c234` 176, `c5` 405. Não interpretar contagens como desempenho; o teste não contém rótulos.
- **Planilha:** saída `outputs/etapa7_20260926_105326_ca987906/test1_predito.xlsx`; aba única `test1`, 900 linhas, cabeçalhos `resp_text` e `clarity`, 900 células de predição preenchidas. A coluna original de texto permaneceu idêntica. Arquivo original preservado. Reabertura e inspeção visual passaram.
- **Integridade:** SHA-256 do original e da saída, além das verificações estruturais, documentados em `reports/etapa7_inferencia.md` e `runs/etapa7/etapa7_20260926_105326_ca987906/`.
- **Estado e parada:** Etapa 7 concluída. Parar aqui e solicitar autorização explícita para iniciar a Etapa 8.

**Adendo comparativo iniciado — 26/09/2026 11:10 BRT**

- **Solicitação:** o usuário pediu executar TF-IDF + regressão logística no mesmo holdout da auditoria BERT para tornar a comparação mais justa.
- **Protocolo congelado:** ajustar uma vez em exatamente os 17.068 índices de desenvolvimento usados pela auditoria BERT; usar o baseline já selecionado por validação agrupada (`C=0,5`, unigramas+bigrama, `min_df=3`, até 100.000 termos, regressão logística `lbfgs`, até 400 iterações); avaliar somente nos mesmos 3.024 índices do holdout. Não testar outro `C` nem retunar com o resultado.
- **Integridade:** verificar hashes da fonte/divisão, alinhamento de todos os índices com as previsões BERT já salvas e reproduzir a métrica BERT registrada antes de comparar.
- **Autorização:** solicitação explícita recebida; esta comparação usa o holdout para um baseline fixo, sem alterar modelo/configuração.
- **Estado:** comparação em andamento; resultado em `reports/etapa5f_tfidf_holdout_comparison.md`, runner em `src/run_stage5f_tfidf_holdout.py`.


**Conclusão do adendo comparativo — 26/09/2026 11:14 BRT**

- **Execução:** TF-IDF + regressão logística `C=0,5` ajustado nos mesmos 17.068 índices de desenvolvimento e avaliado nos mesmos 3.024 índices de holdout do BERT 5f. Parâmetros congelados antes da consulta; nenhum retuning. Ajuste em 44 iterações. Hashes, alinhamento das previsões e métricas BERT recalculadas foram validados.
- **Resultados pareados:** TF-IDF: acurácia 45,437%, macro-F1 45,056%; BERT: 45,966%, 44,523%. Vantagem do BERT em acurácia de +0,529 p.p. (16 exemplos); TF-IDF +0,533 p.p. em macro-F1, com recall `c234` maior. McNemar exato: discordâncias corretas exclusivas BERT/TF-IDF 395/379, `p=0,590`; sem evidência clara de diferença de acurácia.
- **Artefatos:** relatório `reports/etapa5f_tfidf_holdout_comparison.md`, métricas e previsões em `runs/etapa5f/etapa5f_tfidf_holdout_20260926_1115/`, modelo em `models/baseline/etapa5f_tfidf_holdout_20260926_1115/` e runner `src/run_stage5f_tfidf_holdout.py`.
- **Estado:** comparação complementar concluída. A avaliação serve à resposta comparativa solicitada; não mudou os parâmetros ou modelos congelados e não iniciou etapa nova.


**Atualização da Etapa 8 — 26/09/2026 18:49 BRT**

- **Pedido do usuário:** usar Google Docs para o relatório e Google Presentations/Google Slides para a apresentação; foi enviado o modelo C:\Users\KABUM\Downloads\ep1-modelo-relatorio.pdf.
- **Leitura do modelo:** PDF de uma página com nove itens de relatório. Confirma ZIP contendo relatório, PDF da apresentação e planilha Excel com rótulos do teste; requer nomes/números USP do grupo, estratégia/modelo final, pré-processamento, parâmetros/faixas, valores ótimos, procedimento treino/teste e reprodução, métrica do modelo final, link de repositório e instruções de reprodução. O modelo não determina o formato do relatório dentro do ZIP.
- **Mudança:** Etapa 8 agora especifica criação nativa nos dois serviços Google, exportação PDF da apresentação, inclusão do modelo PDF como referência e verificação dos formatos do ZIP. A formulação anterior sobre divergência entre slides foi substituída pelo modelo recebido.
- **Pendências para a futura Etapa 8:** coletar nomes e números USP dos integrantes, obter o link real do repositório e confirmar o formato de exportação do relatório exigido para o ZIP. A ausência desses dados não bloqueia esta atualização do plano.
- **Limite de escopo:** somente o plano foi atualizado; a Etapa 8 continua pendente e não foram criados documentos, apresentações ou compartilhamentos no Google.


**Início da Etapa 8 — 26/09/2026 19:00 BRT**

- **Autorização:** usuário pediu “Pode iniciar a etapa 8”. Criar relatório no Google Docs, apresentação no Google Presentations/Slides e pacote de entrega conforme o modelo PDF recebido.
- **Esclarecimentos recebidos:** deixar placeholders explícitos para nomes e números USP; criar repositório GitHub público de código e enviar diretamente à branch main; o usuário adicionará depois a exportação do relatório ao ZIP.
- **Escopo do repositório público:** código, configurações e instruções de reprodução. Não publicar planilhas de treino/teste, previsões de teste, checkpoints, logs de execução ou dados pessoais ausentes.
- **Estado:** Etapa 8 em andamento; produzir e conferir os documentos nativos, o PDF da apresentação, o ZIP preparado e o repositório antes de encerrar.


**Preparação da Etapa 8 — 26/09/2026 19:18 BRT**

- **Repositório público:** `https://github.com/Zennitte/ep1-claridade-esic-bertimbau`, branch `main`, commit inicial `f45f9ad`. Publicados somente código, configurações, lockfile e instruções. Planilhas, predições, relatórios de execução e pesos ficaram fora do Git.
- **Relatório nativo:** `https://docs.google.com/document/d/1dxOCIxqwmr5rT8ZPA9xBPtjjNrNEpjqk6awSxCzZ7RM`. As nove seções e três tabelas foram conferidas após importação; a exportação PDF do Google Docs foi inspecionada em três páginas. Há placeholders explícitos para nomes e números USP.
- **Apresentação nativa:** `https://docs.google.com/presentation/d/1HdwG7amYnsb1tIEvjqjVHbPuZPyO6uoNZWczXu4MoSs`. Oito slides editáveis; PDF exportado em `outputs/etapa8/apresentacao_ep1.pdf` e inspecionado visualmente. Os slides mantêm a distinção entre auditoria do holdout e inferência no teste sem rótulos.
- **ZIP parcial:** `outputs/etapa8/EP1_ACH2118_parcial_sem_relatorio.zip`, contendo `apresentacao_ep1.pdf` e `test1_predito.xlsx`. Integridade ZIP confirmada; SHA-256 do PDF `e8064bc17a83f2939e2a372274425a5d849e27525d8b3145eeda23a74c22d002` e da planilha `4e6e149ad9f9407b51890ee0c4e31a09589568d090e765293864945ee7e24a8c`.
- **Reprodução mínima:** `src/predict_test_xlsx.py` executado em duas linhas de amostra no CPU; ambas as previsões coincidiram com a planilha da Etapa 7.
- **Pendente do usuário:** substituir os placeholders no relatório e na capa dos slides pelos integrantes efetivos; exportar o relatório no formato exigido pela disciplina e incluí-lo no ZIP antes da submissão. O ZIP ainda não é a entrega completa.
