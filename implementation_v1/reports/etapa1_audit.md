# Etapa 1 — auditoria e protocolo de divisão

**Fonte:** `train.xlsx`, aba `train`, SHA-256 `0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818`. Auditoria executada em 24/09/2026 com `python src/audit_and_split.py`. Índices fixados em `data/splits_grouped_v1.json`; índices são base zero entre as linhas de dados, e a linha Excel é `row_index + 2`. Relatório numérico completo em `reports/etapa1_audit.json`.

## Dados e qualidade

| Item | Resultado |
| --- | ---: |
| Linhas de dados | 20.092 |
| `c1` | 6.347 (31,59%) |
| `c234` | 6.853 (34,11%) |
| `c5` | 6.892 (34,30%) |
| Células vazias em texto/rótulo | 0 / 0 |
| `resp_text` armazenado como número | 1 (linha Excel 5028, rótulo `c1`) |
| Textos exatos distintos | 18.432 |
| Textos distintos após normalização de agrupamento | 18.143 |
| Grupos normalizados repetidos / linhas neles | 500 / 2.449 |
| Grupos repetidos com rótulos conflitantes / linhas neles | 316 / 1.975 |
| Maior grupo | 138 linhas |

O valor numérico em `resp_text` será convertido por `str(valor)` ao carregar dados para o modelo; o arquivo original não foi alterado. A conversão deve ser a mesma nos experimentos seguintes. Textos idênticos podem receber rótulos diferentes, possivelmente por avaliações subjetivas de usuários distintos. Mantemos cada linha e seu rótulo. A soma das classes majoritárias por grupo é 19.173 linhas, ou 95,43% do conjunto; esse é apenas um limite matemático para um classificador determinístico que veja somente o texto normalizado, não uma estimativa de desempenho.

| Comprimento | Mediana | P90 | P99 | Máximo |
| --- | ---: | ---: | ---: | ---: |
| Palavras | 101 | 309 | 741,09 | 1.821 |
| Caracteres | 709 | 2.122 | 5.040,36 | 12.125 |
| Tokens BERTimbau, incluindo especiais | 182 | 534,9 | 1.293,36 | 4.429 |

Com o tokenizer `neuralmind/bert-base-portuguese-cased`, 7.204 respostas (35,86%) excedem 256 tokens e 2.174 (10,82%) excedem 512 tokens. A Etapa 3 usará estes valores para escolher o comprimento inicial; esta etapa não define truncamento. Há 252 respostas de até cinco palavras e 573 com mais de 512 palavras. Foram identificados 7.936 textos com URL, 2.175 com endereço de e-mail e 5.919 com pelo menos um caractere de controle Unicode. Não houve remoção desses elementos. Espaços nas bordas aparecem em 20.091 textos e sequências de espaços internos em 17.080.

Foram examinados exemplos curtos, longos, medianos de cada classe e de grupo conflitante, com referências de linha e trechos mascarados no JSON local. O exemplo mais curto contém apenas uma saudação (linha Excel 2836, `c5`); o mais longo é uma resposta legal extensa (linha 14346, `c234`). O grupo da primeira linha de dados contém rótulos conflitantes. Esses casos reforçam que a divisão deve respeitar grupos e que a escolha de trecho precisa ser avaliada depois.

## Rótulos do enunciado

A página 2 de `ep1-enunciado.pdf` especifica `{c1,c234,c5}`. A anotação inicial do plano que afirmava `c6` estava incorreta; os rótulos da planilha e o enunciado concordam. Nenhum rótulo foi convertido.

## Normalização e divisão congeladas

A chave de grupo é o SHA-256 do texto após Unicode NFC, `casefold()` e colapso de qualquer sequência de espaços para um espaço. Essa normalização é usada **somente para agrupamento**; o texto original permanece como entrada dos modelos, salvo a conversão explícita da célula numérica. Não se removem pontuação, acentos, URLs nem cabeçalhos. Uma checagem confirmou ausência de colisões de hash nos 18.143 grupos desta amostra.

Com semente **20260924**, foram geradas 256 propostas por `GroupShuffleSplit(test_size=0.15)`. A proposta 37 foi escolhida pela menor soma do erro absoluto da fração de linhas e do maior desvio absoluto de proporção das classes. Essa escolha usou somente distribuição de rótulos e tamanho, sem métrica de modelo. A validação final não deve ser consultada durante a busca; abrir seus índices para treinar ou avaliar modelos antes da decisão da Etapa 5 violaria o protocolo.

| Partição | Linhas | `c1` | `c234` | `c5` |
| --- | ---: | ---: | ---: | ---: |
| Desenvolvimento | 17.068 | 5.395 | 5.817 | 5.856 |
| Validação final reservada | 3.024 (15,05%) | 952 | 1.036 | 1.036 |

Os três folds internos foram gerados por `StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=20260924)` **somente no desenvolvimento**.

| Fold | Treino | Validação | Validação `c1` | Validação `c234` | Validação `c5` |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 11.488 | 5.580 | 1.758 | 1.890 | 1.932 |
| 2 | 11.451 | 5.617 | 1.732 | 1.916 | 1.969 |
| 3 | 11.197 | 5.871 | 1.905 | 2.011 | 1.955 |

As verificações no script confirmaram interseção **zero** de chaves de grupo entre desenvolvimento e validação final e entre treino e validação de cada fold. Todas as linhas foram atribuídas exatamente uma vez à divisão externa; cada linha de desenvolvimento aparece exatamente uma vez como validação interna. O maior desvio de proporção de classe na validação final foi de 0,151 ponto percentual frente ao conjunto completo; os folds também preservam as três classes com desvio pequeno.

**Protocolo fixado:** usar `data/splits_grouped_v1.json` sem regenerá-lo para comparar modelos; conferir o hash de `train.xlsx` antes de carregar os índices; aprender qualquer preparação de texto, vocabulário ou modelo apenas no treino de cada fold. Usar a validação final uma única vez, depois de fixar o candidato e os hiperparâmetros na Etapa 5. Nenhuma GPU foi usada nesta etapa.
