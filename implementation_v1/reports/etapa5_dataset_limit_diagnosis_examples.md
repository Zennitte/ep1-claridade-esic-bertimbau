# Apêndice — amostra qualitativa da 5c.2

Amostra determinística de 60 linhas da validação do fold 1. Os rótulos foram preservados. A seleção cobre acertos/erros de confiança alta/baixa e os seis sentidos de confusão entre classes. Confiança alta/baixa foi definida pelos quartis 75/25 da confiança top-1 na validação.

## Exemplo 1 — linha Excel 478

- Seleção: correct_high_confidence
- Verdadeiro → predito: `c1` → `c1`
- Probabilidades: c1=0.9001, c234=0.0730, c5=0.0269
- Confiança top-1 / margem top-1−top-2 / entropia: 0.9001 / 0.8271 / 0.3830 nats
- Grupo normalizado (SHA-256): `0c65069377af8aad92240585f55a7b5099a47f7c5d4bbf17230eaa40de8e4542`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Sr ( a ). Luis Cesar, Encaminhamos - lhe resposta da Diretoria de Gestão de Pessoas do Banco do Brasil ao seu pedido de informação : " O acompanhamento do desempenho dos funcionário é realizado em sistema interno, disponível para acesso permanente dos funcionários utilizando chave e senha pessoal. Além de consultar todas as informações a respeito do resultado de sua avaliação de desempenho, o funcionário também pode consultar regras e esclarecimentos sobre procedimentos adotados por meio do normativo interno e treinamento disponível na universidade corporativa. A lei de acesso à Informação, por sua vez, regulamenta a publicação de informação que são de caráter ou interesse público. Assim comunicamos a impossibilidade de fornecimento das informações solicitadas, tendo em vista a inexistência de amparo legal. Atenciosamente, Elder Almeida de Castro Gerente Executivo " Atenciosamente, Serviço de Informação ao Cidadão do Banco do Brasil SICBB Recurso Conforme a Lei 12527 / 11 em seu artigo Art. 15, no caso de indeferimento de acesso a informações ou às razões da negativa do acesso, poderá o interessado interpor recurso contra a decisão no prazo de 10 ( dez ) dias a contar da sua ciência. Parágrafo único. O recurso será dirigido à autoridade hierarquicamente superior à que exarou a decisão impugnada, que deverá se manifestar no prazo de 5 ( cinco ) dias.

## Exemplo 2 — linha Excel 9439

- Seleção: correct_low_confidence
- Verdadeiro → predito: `c1` → `c1`
- Probabilidades: c1=0.3441, c234=0.3186, c5=0.3373
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3441 / 0.0069 / 1.0981 nats
- Grupo normalizado (SHA-256): `77d411052dc83d4def315c448b96c952fae89dae4069be1658e6a8c185bddd22`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Senhor ( a ) Solicitante, Em atenção à sua demanda por informação, encaminhamos arquivo ( s ) anexo ( s ) contendo a resposta elaborada pela Unidade responsável pelo tema / assunto da demanda. Registre - se que, conforme o art. 21 do Decreto 7. 724 / 2012, nos casos de negativa de acesso à informação ou não fornecimento das razões da negativa do acesso, o requerente poderá apresentar recurso no prazo de dez dias, contado da ciência da decisão. Atenciosamente, Serviço de Informação ao Cidadão - SIC / MJSP ( 61 ) 2025 - 3949 - sic @ mj. gov. br

## Exemplo 3 — linha Excel 9458

- Seleção: correct_high_confidence
- Verdadeiro → predito: `c1` → `c1`
- Probabilidades: c1=0.9073, c234=0.0658, c5=0.0269
- Confiança top-1 / margem top-1−top-2 / entropia: 0.9073 / 0.8415 / 0.3644 nats
- Grupo normalizado (SHA-256): `4d581b4712082412843f86a5168ee4af8f67e9ee9792fdd70f41812abf1fb66b`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> PREZADO CIDADãO, A COORDENAçãO DO PROGRAMA FARMáCIA POPULAR INFORMA QUE SEGUE EM ANEXO PLANILHA DE DADOS REFERENTE A QUANTIDADE DE PRODUTOS FORNECIDOS PELO MINISTéRIO DA SAúDE ATRAVéS DO PROGRAMA FARMáCIA POPULAR DO BRASIL, MENSALMENTE EM 2017 E 2018, CONFORME SOLICITADO. ATENCIOSAMENTE,

## Exemplo 4 — linha Excel 9901

- Seleção: correct_low_confidence
- Verdadeiro → predito: `c1` → `c1`
- Probabilidades: c1=0.3434, c234=0.3296, c5=0.3270
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3434 / 0.0138 / 1.0984 nats
- Grupo normalizado (SHA-256): `77417500f9e7892bfd382e7b5d77cabd2b0eadea8f8d86e889996ab9bc09567c`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezada ( o ) Cidadã ( o ), As infomações a respeito do grupo de pesquisa solicitato podem ser encontradas no endereço http : / / dgp. cnpq. br / dgp / espelhogrupo / 1718964546663817 # equipamentos _ softwares Atenciosamente, Serviço de Informação ao Cidadão

## Exemplo 5 — linha Excel 9986

- Seleção: correct_high_confidence
- Verdadeiro → predito: `c1` → `c1`
- Probabilidades: c1=0.9091, c234=0.0645, c5=0.0264
- Confiança top-1 / margem top-1−top-2 / entropia: 0.9091 / 0.8445 / 0.3594 nats
- Grupo normalizado (SHA-256): `1c5851991ed46f405e94cde1b8c311e751a8f6fead5f3847a74785c07f269b72`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> PREZADO CIDADãO, A COORDENAçãO DO PROGRAMA FARMáCIA POPULAR INFORMA QUE SEGUE EM ANEXO PLANILHA DE DADOS REFERENTE A QUANTIDADE DE PRODUTOS FORNECIDOS PELO MINISTéRIO DA SAúDE ATRAVéS DO PROGRAMA FARMáCIA POPULAR DO BRASIL, MENSALMENTE EM 2017 E 2018, CONFORME SOLICITADO. ATENDIMENTO,

## Exemplo 6 — linha Excel 11098

- Seleção: correct_high_confidence
- Verdadeiro → predito: `c1` → `c1`
- Probabilidades: c1=0.9036, c234=0.0686, c5=0.0278
- Confiança top-1 / margem top-1−top-2 / entropia: 0.9036 / 0.8349 / 0.3751 nats
- Grupo normalizado (SHA-256): `2b74da61ab501a0c51ebde204aec4fd2bddc3a974cabed19f6e20ac40ea5f98c`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> PREZADO CIDADãO, COORDENAçãO DO PROGRAMA FARMáCIA POPULAR INFORMA QUE SEGUE EM ANEXO PLANILHA DE DADOS REFERENTE A QUANTIDADE DE PRODUTOS FORNECIDOS PELO MINISTéRIO DA SAúDE ATRAVéS DO PROGRAMA FARMáCIA POPULAR DO BRASIL, MENSALMENTE EM 2017 E 2018, CONFORME SOLICITADO. ATENCIOSAMENTE,

## Exemplo 7 — linha Excel 18573

- Seleção: correct_high_confidence
- Verdadeiro → predito: `c1` → `c1`
- Probabilidades: c1=0.9024, c234=0.0727, c5=0.0249
- Confiança top-1 / margem top-1−top-2 / entropia: 0.9024 / 0.8297 / 0.3752 nats
- Grupo normalizado (SHA-256): `fdc58116d65eacbaf5041b2448c96e129883bd4320a9cebeb55f2e8cae3f3fb9`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Sr ( a ). Luis, Encaminhamos - lhe resposta da Diretoria Gestão de Pessoas do Banco do Brasil ao seu pedido de informação : " Prezado Senhor Luis Cesar Lopes Zeredo, O pedido de informações é uma solicitação de esclarecimentos a funcionário com o intuito de elucidar alguma ocorrência. Qualquer administrador do Banco do Brasil tem a prerrogativa de encaminhar pedido de informações aos funcionários, sem que obrigatoriamente esse registro seja feito em sistema corporativo, haja vista que a gestão de pessoas, de recursos, de processos e das informações observando direcionadores institucionais, está dentre suas responsabilidades. Assim, a informação solicitada por V. não está disponível nos sistemas do Banco. Atenciosamente Adriano Weber Scheeren Gerente Executivo " Atenciosamente, Serviço de Informação ao Cidadão do Banco do Brasil SICBB Recurso Conforme a Lei 12527 / 11 em seu artigo Art. 15, no caso de indeferimento de acesso a informações ou às razões da negativa do acesso, poderá o interessado interpor recurso contra a decisão no prazo de 10 ( dez ) dias a contar da sua ciência. Parágrafo único. O recurso será dirigido à autoridade hierarquicamente superior à que exarou a decisão impugnada, que deverá se manifestar no prazo de 5 ( cinco ) dias.

## Exemplo 8 — linha Excel 19893

- Seleção: correct_high_confidence
- Verdadeiro → predito: `c1` → `c1`
- Probabilidades: c1=0.9127, c234=0.0645, c5=0.0228
- Confiança top-1 / margem top-1−top-2 / entropia: 0.9127 / 0.8482 / 0.3465 nats
- Grupo normalizado (SHA-256): `a09af37b59873a73d684a394b597412f81f2fa1b21613f51db2a02dbb5d8143c`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Sr ( a ). Luis Cesar, Encaminhamos - lhe resposta da Diretoria de Gestão de Pessoas do Banco do Brasil ao seu pedido de informação : " Prezado Luis Cesar Lopes Zeredo, Informamos que seu recurso não poderá ser atendido com fundamentos no art. 13, incisos III do Decreto 7. 724 / 2012 combinados com o princípio da supremacia do interesse público em relação ao interesse privado. Ressaltamos que os benefícios para o fornecimento de uma determinada informação a um único cidadão são bastante inferiores aos custos gerados à Administração ( impacto direto nas demandas rotineiras, carência de recursos humanos, dificuldades operacionais para se localizar a informação dado o tempo decorrido, etc. ), de maneira a contrariar o interesse público. Atenciosamente Katia Maria Rodrigues Bastos Gerente Executiva " Atenciosamente, Serviço de Informação ao Cidadão do Banco do Brasil SICBB Recurso Conforme a Lei 12527 / 11 em seu artigo Art. 15, no caso de indeferimento de acesso a informações ou às razões da negativa do acesso, poderá o interessado interpor recurso contra a decisão no prazo de 10 ( dez ) dias a contar da sua ciência. Parágrafo único. O recurso será dirigido à autoridade hierarquicamente superior à que exarou a decisão impugnada, que deverá se manifestar no prazo de 5 ( cinco ) dias.

## Exemplo 9 — linha Excel 3549

- Seleção: error_c1_to_c234
- Verdadeiro → predito: `c1` → `c234`
- Probabilidades: c1=0.3305, c234=0.3446, c5=0.3249
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3446 / 0.0140 / 1.0983 nats
- Grupo normalizado (SHA-256): `fa3932e7725750ea135276842b95239cfd7312308d81e9b989c387ef02bfd278`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Senhor, Conforme estabelece o Estatuto Social dos Correios ( Decreto 8. 016 de 17 / 05 / 13 ) o exercício social compreenderá o período de de janeiro a 31 de dezembro de cada ano ( art. 37 ) e ao final de cada ano serão elaboradas as Demonstrações Financeiras ( art. 38 ). O resultado financeiro do exercício de 2016 está em fase de apuração e o prazo para divulgação é até o dia 30 / 04 / 17, conforme artigo 40 do Estatuto e legislações aplicáveis. Acrescentamos que, para a divulgação pública, é necessário aprovação das Demonstrações Financeiras pela Diretoria Executiva, Conselhos de Administração e Fiscal e Assembleia Geral, bem como parecer das Auditorias Independente e Interna. Os resultados dos exercícios estão disponíveis no sítio público no endereço : http : / / www. correios. com. br / sobre - correios / a - empresa / publicacoes / demonstracoes - financeiras. Os Correios agradecem a sua compreensão. Vanessa Sandri Barbosa Chefe do Departamento de Contabilidade VIFIC Eventuais recursos devem ser dirigidos ao Vice - presidente de Finanças e Controles de acordo com o Art. 21 do Decreto 7. 724 / 2012 que regulamenta a Lei de Acesso a Informação - Lei 12. 527 / 2011, no prazo de 10 dias, a contar do recebimento desta resposta. Serviço de Informação ao Cidadão Empresa Brasileira de Correios e Telégrafos

## Exemplo 10 — linha Excel 8040

- Seleção: error_low_confidence, error_c1_to_c234
- Verdadeiro → predito: `c1` → `c234`
- Probabilidades: c1=0.3363, c234=0.3386, c5=0.3252
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3386 / 0.0023 / 1.0985 nats
- Grupo normalizado (SHA-256): `181a7437a671964fcdb8526295610e525141dacd3f1d842d5293d7214e6d46fd`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezada Senhora, Em atenção ao requerimento formulado, cumpre - nos informar que a demanda foi encaminhada à Secretaria da Receita Federal, que se pronunciou conforme abaixo : " Em resposta à solicitação, cumpre observar - se que Sobradinho - DF não é município. E os dados disponíveis tratam, especificamente, de UF ou de Município. " Considerando o disposto no art. 19, inc. II, c / c o art. 21, caput, do Decreto n. 7. 724, de 2012, informa - se que poderá ser apresentado recurso, no prazo de 10 dias, contado da ciência da decisão. Atenciosamente, Serviço de Informação ao Cidadão Ministério da Fazenda

## Exemplo 11 — linha Excel 8491

- Seleção: error_c1_to_c234
- Verdadeiro → predito: `c1` → `c234`
- Probabilidades: c1=0.1839, c234=0.5854, c5=0.2307
- Confiança top-1 / margem top-1−top-2 / entropia: 0.5854 / 0.3548 / 0.9632 nats
- Grupo normalizado (SHA-256): `bc0d49c33ce747e38746974a9bfd0e1ebb9a27ca095d13707e18ce0bffbb5d57`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Welliton Barros de Magalhães, boa tarde! Reportamos ao Decreto abaixo, o qual determina a obrigatoriedade da publicação referente aos quantitativos de lotação dos cargos nos meses de janeiro e julho de cada ano, a saber : DECRETO 7. 311, DE 22 DE SETEMBRO DE 2010. Dispõe sobre os quantitativos de lotação dos cargos dos níveis de classificação C, D e E integrantes do Plano de Carreira dos Cargos Técnico - Administrativos em Educação, de que trata a Lei no 11. 091, de 12 de janeiro de 2005, nos Institutos Federais de Educação, Ciência e Tecnologia vinculados ao Ministério da Educação, e altera o Decreto no 7. 232, de 19 de julho de 2010. Art. 4o O Ministério da Educação publicará, em janeiro e julho de cada ano, versão atualizada do Anexo, contemplando as redistribuições de cargos que tiverem sido realizadas no período imediatamente anterior, demonstrando, para cada entidade, o total de cargos dos níveis de classificação C, D e E. Portanto, segue o link que atualiza e disponibiliza o quadro de acordo com os preceitos regidos no referido Decreto. http : / / portal. ifsuldeminas. edu. br / dgp / relacao - de - cargos Para eventuais dúvidas, você pode ligar no telefone 35 34496150 e falar com a Kátia. Ou e - mail dgp @ ifsuldeminas. edu. br Atenciosamente,

## Exemplo 12 — linha Excel 10158

- Seleção: error_c1_to_c234
- Verdadeiro → predito: `c1` → `c234`
- Probabilidades: c1=0.2233, c234=0.6037, c5=0.1729
- Confiança top-1 / margem top-1−top-2 / entropia: 0.6037 / 0.3804 / 0.9429 nats
- Grupo normalizado (SHA-256): `2744841c0fd5d8a32045748354797fd8edd455aca5c95d164be44964e2fc6472`
- Entrada truncada em 512 tokens: `True`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Senhor Gabriel, Em resposta à sua solicitação, apresentamos a planilha anexa registrando a quantidade de vagas e cargos existentes nas localidades relacionadas, esclarecendo que 217 empregados que ocupam os respectivos cargos foram contratados através de concurso público, 10 empregados com admissão por decisão judicial, 45 empregados com admissão anterior à Constituição Federal de 05 / 10 / 88 e 05 empregados pela Anistia Collor Lei 8878 / 94 e Dec. 6077. A Diretoria Regional de Minas Gerais possui contrato para prestação de serviços através de Mão de Obra Temporária ( MOT ). Esta contratação tem amparo legal na Lei 6019 / 74 e no Decreto 73. 841 / 74, que regulamenta a contratação de trabalho temporário para atender uma necessidade transitória ou acréscimo extraordinário de serviço. Esta contratação é destinada a atender as demandas das nossas unidades operacionais, que serão preenchidas de acordo com a necessidade dos Centros de Distribuição Domiciliaria CDD. A quantidade de mão de obra temporária e respectiva localidade dos postos de trabalho encontram - se no quadro anexo. Em relação a quantidade de mortes, aposentadorias, demissões, exonerações relacionadas ao cargo de carteiro nas cidades citadas a partir de 22 / 03 / 2011 até janeiro de 2016, informamos que ocorreram 32 desligamentos no período, sendo 07 desligamentos em função da Adesão ao Plano de Desligamento Incentivado para Aposentados ( PDIA ) e o restante foram demissões a pedido dos empregados, dispensa no Contrato de Experiência por iniciativa do Empregador e resilições no Contrato de Experiência por iniciativa dos empregados. No tocante à definição do número de candidatos convocados para prestar serviços nas localidades relacionadas, tem como base a necessidade de efetivo apontada nos trabalhos técnicos de dimensionamento de recursos, envolvendo o volume da carga postal e fluxo dos objetos postais, conjugada com a liberação de vagas pelos Órgãos de Controle das Estatais e disponibilizadas a partir da Administração Central dos Correios em Brasília - DF. Sobre as convocações de candidatos aprovados no Concurso tornadas sem efeito nas localidades citadas, foram publicadas no Anexo I do Edital 011 / 2011, 18 vagas para a localidade de Juiz de Fora, sendo 15 para a ampla concorrência e 03 para as pessoas com deficiência. Foram aprovados 184 candidatos, sendo 86 foram contratados, ao passo que 57 candidatos ainda não foram convocados, 21 candidatos foram considerados inaptos nos exames médicos

## Exemplo 13 — linha Excel 14004

- Seleção: error_c1_to_c234
- Verdadeiro → predito: `c1` → `c234`
- Probabilidades: c1=0.3314, c234=0.3455, c5=0.3231
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3455 / 0.0141 / 1.0982 nats
- Grupo normalizado (SHA-256): `83d8573611aaeae5b443576ed702030fc50c6cb36d613cdc3d69dd188ef64746`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Cidadão, Informamos que estamos elaborando a resposta para o atendimento de sua demanda, pedimos que aguarde mais alguns dias. Estamos à disposição para quaisquer esclarecimentos.

## Exemplo 14 — linha Excel 18022

- Seleção: error_c1_to_c234
- Verdadeiro → predito: `c1` → `c234`
- Probabilidades: c1=0.1688, c234=0.5827, c5=0.2485
- Confiança top-1 / margem top-1−top-2 / entropia: 0.5827 / 0.3341 / 0.9610 nats
- Grupo normalizado (SHA-256): `1affc9c227283ae36850140886706d8d6ab5e706cc6bcd2d850ccbb9d2196f54`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Senhor, Cumprimentando - o, reportamo - nos ao pedido de informação em epígrafe para informar - que estamos impossibilitados de informar o quantitativos de vagas disponíveis para o cargo de técnico em contabilidade em razão de problemas no sistema siapenet ( fechamento / homolagação da folha ) o que nos impossibilita de consultarmos o total de vaga. Mas, esta informação poderá ser obtida consultando o site da Funrio, concursos IFPA e a página do IFPA www. ifpa. edu. br > onde constam as nomeações. As vagas ofertadas no concursos são decorrentes de vacância / criação de vagas / redistribuição. A vaga decorrente da redistribuição de servidor deste IFPA para o IFPI ocorrida em 08 / 06 / 2016, seção 2, página 33 do DOU, será disponibilizada para o edital de remoção interna de nr. 018 / 2016 que já encontra - se disponível site do IFPA. As nomeações poderão ser acompanhadas no site do IFPA. Dúvidas entrar em contato com a coordenação geral de gestão de pessoas ou servidor responsável pelas nomeações, por meio do telefone ( 91 ) 3342 - 0621. Atenciosamente, equipe e - sic port. 0748 / 2016

## Exemplo 15 — linha Excel 19201

- Seleção: error_c1_to_c234
- Verdadeiro → predito: `c1` → `c234`
- Probabilidades: c1=0.1690, c234=0.6078, c5=0.2232
- Confiança top-1 / margem top-1−top-2 / entropia: 0.6078 / 0.3846 / 0.9378 nats
- Grupo normalizado (SHA-256): `31ad5d52026126ad93a661de15bcb3f60103b5d697658bd4cbda56c1ac9148b6`
- Entrada truncada em 512 tokens: `True`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Cidadão ( ), 1. Conforme solicitação através do E - SIC, site CGU, informamos que : 1. 1. Em atenção ao pedido de acesso à informação feito por Vossa Senhoria, por meio do E - SIC, Lei 12. 527 de Novembro de 2011, informamos o seguinte referente ao Programa Minha Casa Minha Vida. Primeiramente cumpre - nos informar que o PMCMV é operacionalizado por meio da concessão de subsídiosb provenientes do OGU e de financiamentos habitacionais a pessoas físicas, de acordo com o seu enquadramento, baseado na renda familiar bruta mensal. A operacionalização do Programa no âmbito do PNHU é dividida em subprogramas em que a concessão de subsídio ou financiamento ocorre de forma estratificada em Faixas, dispostas da seguinte forma : Recursos Fundo de Arrendamento Residencial ( FAR ) Faixa 1 : a ) Objetiva conceder financiamento habitacional fortemente subvencionado, sob a forma de parcelamento, sem juros, às famílias indicadas pelo Município ou Governo do Estado / Distrito Federal, com renda mensal bruta até R $ 1. 800, 00, para aquisição de unidades habitacionais urbanas produzidas com recursos do Orçamento Geral da União ( OGU ) integralizados no Fundo de Arrendamento Residencial ( FAR ), nesta Faixa do PMCMV, o valor aportado pelos beneficiários é ínfimo quando comparado ao valor do subsídio concedido e do valor total do imóvel, b ) Busca atender famílias com renda até R $ 3. 600, 00 nas operações enquadradas nas situações provenientes de emergência ou de calamidade pública reconhecida pelo Ministério da Integração Nacional e nas operações vinculadas às programações orçamentárias do PAC, que demandem reassentamento, remanejamento ou substituição de unidades habitacionais. 2. 1. 2. Recursos do Fundo de Desenvolvimento Social FDS ( MCMV - E ) Faixa 1 : visa à concessão de financiamento fortemente subvencionado, sem juros, às famílias com renda mensal bruta de até R $ 1. 800, 00, admitindo - se até R $ 2. 350, 00 para até 10 % das famílias atendidas em cada empreendimento, organizadas sob a forma coletiva, para aquisição de unidades habitacionais urbanas produzidas por Entidades Organizadoras, devidamente habilitadas no Ministério das Cidades, com recursos do Or

## Exemplo 16 — linha Excel 19719

- Seleção: error_c1_to_c234
- Verdadeiro → predito: `c1` → `c234`
- Probabilidades: c1=0.3224, c234=0.3433, c5=0.3343
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3433 / 0.0090 / 1.0983 nats
- Grupo normalizado (SHA-256): `f0397dfe6ad6225567726edc45eaaaa4f049aaa018bac838ff6290f14aadcab7`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Sr. Marco Aurelio Asinelli Hasselmann : Em resposta a sua solicitação, informamos que os dados solicitados seguem em planilha anexa. Continuamos a sua disposição. Atenciosamente, SIC - Serviço de Informação ao Cidadão Companhia de Pesquisa de Recursos Minerais - CPRM. OBS. : Destacamos que se pode apresentar recurso ou reclamação, no prazo de 10 ( dez ) dias contados da ciência da decisão, às seguintes instâncias : 1. À autoridade hierarquicamente superior à que emitiu a resposta ( instância recursal ), 2. À autoridade máxima do órgão ou entidade ( instância ), 3. À Controladoria - Geral da União ( instância ), 4. À Comissão Mista de Reavaliação de Informações ( instância ). É importante também destacar que o recurso somente poderá ser dirigido à CGU depois de ser apreciado pelas autoridades competentes no próprio órgão ou entidade.

## Exemplo 17 — linha Excel 4350

- Seleção: error_c1_to_c5
- Verdadeiro → predito: `c1` → `c5`
- Probabilidades: c1=0.3251, c234=0.3288, c5=0.3461
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3461 / 0.0173 / 1.0982 nats
- Grupo normalizado (SHA-256): `6385ee0e6e93c71f3f6197dc29e00af556fc5dddb53d70f2fa97d308ac89bb99`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Senhor, Ao cumprimentá - lo informamos que a sua Ocorrência tem providências parciais, para obter maiores informações entre em contato com o 0800618080. Segue as providências parciais : PROVIDÊNCIAS PARCIAIS : APÓS A INTERVENÇÃO FEDERAL NA GEREX / IBAMA / STM / PA, DURANTE O PERÍODO DE ( 28 / 04 / 2014 A 26 / 06 / 2014 ). I ) Em, 04. 08. 2016, conforme registro no Livro de Protocolo de Correspondência 0001 / 2016, Página 6, Controle de Entrega de Correspondência 00009, através do DESPACHO. 02048. 001250 / 2016 - 11 GABIN SANTARÉM / PA / IBAMA, de 04. 08. 2016, GUIA DE TRAMITAÇÃO de 04 / 08 / 2016 ( 10h : 19min. ) e, TRAMITAÇÃO DE DOCUMENTO de 04 / 08 / 2016 ( 10h : 19min. ). Encaminhamos esta ocorrência em atenção ao SEAMB - Serviço de Apoio Ambiental de Santarém / PA, para providências a serem julgadas necessárias. Atenciosamente, SIC Serviço de Informação ao Cidadão do Ibama SCEN Setor de Clubes Esportivos Norte Trecho 02 Ed. Sede do Ibama Bloco : I CEP : 70. 818 - 900 - Brasília DF

## Exemplo 18 — linha Excel 5086

- Seleção: error_c1_to_c5
- Verdadeiro → predito: `c1` → `c5`
- Probabilidades: c1=0.3242, c234=0.3293, c5=0.3465
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3465 / 0.0173 / 1.0982 nats
- Grupo normalizado (SHA-256): `f29e3e76b7c697975ceda6b82ef5f5ccabe5b0be4432eb5019eaeabcacee9f83`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Sr. José Ricardo, Em atendimento à sua solicitação, encaminho o caminho disponível no site oficial da ANP para o acesso aos Relatórios de Incidente : PÁGINA INICIAL > PRODUÇÃO E EXPLORAÇÃO DE ÓLEO E GÁS > SEGURANÇA OPERACIONAL E MEIO AMBIENTE > RELATÓRIOS DE INVESTIGAÇÃO DE INCIDENTES : http : / / www. anp. gov. br / wwwanp / exploracao - e - producao - de - oleo - e - gas / seguranca - operacional - e - meio - ambiente / relatorios - de - investigacao - de - acidentes Caso a resposta não atenda à vossa demanda, solicitamos que efetue um novo pedido. Atenciosamente Serviço de Informação ao Cidadão - SIC

## Exemplo 19 — linha Excel 8160

- Seleção: error_low_confidence, error_c1_to_c5
- Verdadeiro → predito: `c1` → `c5`
- Probabilidades: c1=0.3389, c234=0.3214, c5=0.3396
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3396 / 0.0007 / 1.0983 nats
- Grupo normalizado (SHA-256): `1ea72043cd4c84fc6ec43a88f79b167413d8659968b97ce0f45034863d97d655`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado cidadão, Temos a esclarecer que recebemos o retorno do seu recurso de informação via formulário de resposta, datado de 21 / 09 / 2017, encaminhado pela Diretoria de Qualidade Ambiental ( Diqua ) https : / / 1drv. ms / u / s! AgSFh2dQK - JygVIIXmrWiI4k7Veb Atenciosamente, SIC Serviço de Informação ao Cidadão do Ibama SCEN Setor de Clubes Esportivos Norte Trecho 02 Ed. Sede do Ibama Bloco : I CEP : 70. 818 - 900 - Brasília - DF sic @ ibama. gov. br

## Exemplo 20 — linha Excel 11525

- Seleção: error_c1_to_c5
- Verdadeiro → predito: `c1` → `c5`
- Probabilidades: c1=0.0409, c234=0.1252, c5=0.8339
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8339 / 0.7087 / 0.5424 nats
- Grupo normalizado (SHA-256): `59723f3db80ae993cd822cd6e3b8127ad1487de60e8019f70a14e28a88c5c3ac`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Senhor, O Ministério das Relações Exteriores não conta com serviços terceirizados de call center. O contrato de terceirização de recepcionistas está disponível no sítio do Ministério, acessível pelo seguinte endereço eletrônico : http : / / www. itamaraty. gov. br / pt - BR / acesso - a - informacao / licitacoes - e - contratos Atenciosamente, Serviço de Informação ao Cidadão Ministério das Relações Exteriores

## Exemplo 21 — linha Excel 13419

- Seleção: error_c1_to_c5
- Verdadeiro → predito: `c1` → `c5`
- Probabilidades: c1=0.0444, c234=0.1121, c5=0.8435
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8435 / 0.7314 / 0.5273 nats
- Grupo normalizado (SHA-256): `f9ca7c0bca51b16fe889199f1bc49b3cfc6499cbf7a0bb8d2c028fb90b541f57`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezada cidadã, A informação solicitada encontra - se em http : / / dai - mre. serpro. gov. br / e https : / / concordia. itamaraty. gov. br / Atenciosamente, Serviço de Informação ao Cidadão Ministério das Relações Exteriores

## Exemplo 22 — linha Excel 15194

- Seleção: error_low_confidence, error_c1_to_c5
- Verdadeiro → predito: `c1` → `c5`
- Probabilidades: c1=0.3338, c234=0.3320, c5=0.3342
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3342 / 0.0003 / 1.0986 nats
- Grupo normalizado (SHA-256): `b0911c681433eb3d46f437c10a262ab61375b76419436e3856ba592940f195b2`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Senhor ( a ), Em atendimento ao pedido de informação registrado sob o protocolo 23480 - 026943 / 2018 - 40, segue resposta elaborada pela unidade responsável : " Informamos que a participante deixou o cartão resposta em branco, por este motivo não possui nota vinculada. " Caso queira solicitar mais informações, é necessário registrar uma nova demanda no e - SIC, para que corram os prazos de atendimento previstos pela Lei de Acesso à Informação. Quando for negado o pedido de acesso à informação, o Decreto 7. 724, de 16 de maio de 2012, estabelece que se resguarda ao interessado a possibilidade de apresentação de recurso, no prazo de 10 ( dez ) dias. Nesse caso, o recurso será direcionado ao dirigente da Diretoria de Gestão e Planejamento - DGP. Atenciosamente, Serviço de Informação ao Cidadão SIC - Inep Ouvidoria do Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira Edifício Villa Lobos Sede do Inep, térreo Setor de Indústrias Gráficas, quadra 04, lote 327 CEP : 70610 - 908 Brasília / DF e - SIC : http : / / www. acessoainformacao. gov. br / sistema /

## Exemplo 23 — linha Excel 15206

- Seleção: error_c1_to_c5
- Verdadeiro → predito: `c1` → `c5`
- Probabilidades: c1=0.0306, c234=0.1135, c5=0.8559
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8559 / 0.7424 / 0.4869 nats
- Grupo normalizado (SHA-256): `3f31c66259d163b53e373ca93c1182b21faef59aed999632386ffa0dc6c0db77`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado, Em resposta ao seu pedido informamos que a Dataprev não tem nenhum contrato com este escopo. Atenciosamente, SIC / DATAPREV

## Exemplo 24 — linha Excel 16676

- Seleção: error_c1_to_c5
- Verdadeiro → predito: `c1` → `c5`
- Probabilidades: c1=0.0391, c234=0.1271, c5=0.8339
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8339 / 0.7068 / 0.5403 nats
- Grupo normalizado (SHA-256): `f43b654fd776938d12b9c89326db81be8e1a651481c808b794c5aedacf05dc93`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Ao Senhor Jorge. Em atenção ao pedido SIC, cadastrado pelo n 08850000171201796, encaminhamos o contrato e os aditivos solicitados em anexo. Na oportunidade, informamos que Vossa Senhoria tem o direito de recorrer desta decisão no prazo de 10 ( dez ) dias, a contar de sua ciência. A autoridade competente para apreciação de seu recurso é a Sra Chefe de Gabinete deste Departamento. Atenciosamente, SIC / DEPEN

## Exemplo 25 — linha Excel 1396

- Seleção: error_high_confidence, error_c234_to_c1
- Verdadeiro → predito: `c234` → `c1`
- Probabilidades: c1=0.9101, c234=0.0667, c5=0.0232
- Confiança top-1 / margem top-1−top-2 / entropia: 0.9101 / 0.8434 / 0.3536 nats
- Grupo normalizado (SHA-256): `4cd32008c650ba725c2f8b11f232dde482143a07898bb50aa0328b6028535149`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Sr ( a ). Cesar, Encaminhamos - lhe resposta da Diretoria de Gestão de Pessoas do Banco do Brasil ao seu pedido de informação : " Prezado Cesar, Deixamos de prestar a informação conforme previsto no inciso II do Art. 13 do Decreto 7. 724 / 12, abaixo transcrito : Art. 13. Não serão atendidos pedidos de acesso à informação : I - genéricos, II - desproporcionais ou desarrazoados, ou III - que exijam trabalhos adicionais de análise, interpretação ou consolidação de dados e informações, ou serviço de produção ou tratamento de dados que não seja de competência do órgão ou entidade. Dessa forma, orientamos que você esclareça melhor quais seriam as informações desejadas para que possamos avaliar a possibilidade do fornecimento, considerando o contido no Art. 31 da Lei 12. 527, que trata das condições a serem observadas para o fornecimento de informações de caráter pessoal. Atenciosamente, Ana Cristina Rosa Garcia Gerente Executiva " Atenciosamente, Serviço de Informação ao Cidadão do Banco do Brasil SICBB Recurso Conforme a Lei 12527 / 11 em seu artigo Art. 15, no caso de indeferimento de acesso a informações ou às razões da negativa do acesso, poderá o interessado interpor recurso contra a decisão no prazo de 10 ( dez ) dias a contar da sua ciência. Parágrafo único. O recurso será dirigido à autoridade hierarquicamente superior à que exarou a decisão impugnada, que deverá se manifestar no prazo de 5 ( cinco ) dias.

## Exemplo 26 — linha Excel 2779

- Seleção: error_high_confidence, error_c234_to_c1
- Verdadeiro → predito: `c234` → `c1`
- Probabilidades: c1=0.8917, c234=0.0826, c5=0.0256
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8917 / 0.8091 / 0.4021 nats
- Grupo normalizado (SHA-256): `25aebf8b75760b31cb756fc28defd784ced10b5e82b068c3002a0f1b9275110a`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Sr ( a ). Luis Cesar, Encaminhamos - lhe resposta da Diretoria de Gestão de Pessoas do Banco do Brasil ao seu pedido de informação : " Prezado Sr. Luis Cesar, Indeferimos pedido sob a égide do inciso III, do art. 13, do Decreto regulamentador da LAI. Com relação ao pedido da legislação do ano de 2007, a mesma se encontra disponível para qualquer cidadão no site oficial http : / / www2. planalto. gov. br /. Informamos que as normas internas seguem à risca a legislação regente da época, e no caso, em função do período solicitado, já prescreveram e exigiriam um trabalho adicional de busca, pesquisa e consolidação das informações. Ademais, ressaltamos que qualquer pretensão trabalhista encontra - se limitada pelo prazo de prescrição quinquenal, conforme art., XXIX CRFB concordando com art. 11, da CLT. Kátia Maria Rodrigues Bastos Gerente Executivo " Atenciosamente, Serviço de Informação ao Cidadão do Banco do Brasil SICBB Recurso Conforme a Lei 12527 / 11 em seu artigo Art. 15, no caso de indeferimento de acesso a informações ou às razões da negativa do acesso, poderá o interessado interpor recurso contra a decisão no prazo de 10 ( dez ) dias a contar da sua ciência. Parágrafo único. O recurso será dirigido à autoridade hierarquicamente superior à que exarou a decisão impugnada, que deverá se manifestar no prazo de 5 ( cinco ) dias.

## Exemplo 27 — linha Excel 2924

- Seleção: error_low_confidence, error_c234_to_c1
- Verdadeiro → predito: `c234` → `c1`
- Probabilidades: c1=0.3401, c234=0.3221, c5=0.3378
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3401 / 0.0023 / 1.0983 nats
- Grupo normalizado (SHA-256): `a715ebd29ba9e312c037a4bcfd4fa1909b54791552e8d08b8b449a7991ebf30b`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Cidadão, Temos a esclarecer que recebemos o retorno do seu recurso de informação via formulário de resposta, datado de 20 / 04 / 2016, encaminhado pela Coordenação - Geral de Recursos Humanos - Cgreh Atenciosamente, SIC Serviço de Informação ao Cidadão do Ibama SCEN Setor de Clubes Esportivos Norte Trecho 02 Ed. Sede do Ibama Bloco : I CEP : 70. 818 - 900 - Brasília - DF sic @ ibama. gov. br

## Exemplo 28 — linha Excel 9343

- Seleção: error_high_confidence, error_c234_to_c1
- Verdadeiro → predito: `c234` → `c1`
- Probabilidades: c1=0.8846, c234=0.0846, c5=0.0308
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8846 / 0.8000 / 0.4246 nats
- Grupo normalizado (SHA-256): `3ac868f5e13d8fcff95f87f1ceafeb699b9f2f3d6a398dee43a6b5ef62bad688`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Sr ( a ). Jenifer, Encaminhamos - lhe resposta da Diretoria de Gestão de Pessoas do Banco do Brasil ao seu pedido de informação : " Prezada Jenifer da Rosa, Em relação ao número de funcionários do Banco, a informação pública, passível de fornecimento por meio da Lei de Acesso à Informação é aquela divulgada no Diário Oficial da União, por meio da Portaria 09 da Sest, de 12. 05. 2017, limitando o número de funcionários do Banco do Brasil S. A. em 106. 659 funcionários. Agradecemos o contato. Elder Alberto A. de Castro Gerente Executivo " Atenciosamente, Serviço de Informação ao Cidadão do Banco do Brasil SICBB Recurso Conforme a Lei 12527 / 11 em seu artigo Art. 15, no caso de indeferimento de acesso a informações ou às razões da negativa do acesso, poderá o interessado interpor recurso contra a decisão no prazo de 10 ( dez ) dias a contar da sua ciência. Parágrafo único. O recurso será dirigido à autoridade hierarquicamente superior à que exarou a decisão impugnada, que deverá se manifestar no prazo de 5 ( cinco ) dias.

## Exemplo 29 — linha Excel 13943

- Seleção: error_low_confidence, error_c234_to_c1
- Verdadeiro → predito: `c234` → `c1`
- Probabilidades: c1=0.3386, c234=0.3289, c5=0.3326
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3386 / 0.0060 / 1.0985 nats
- Grupo normalizado (SHA-256): `674e011b6d180a3c56fe365ea6b4102a5fff0755c8aba7b902666913c3b5fd89`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Senhor ( a ), Com base nas informações fornecidas pela Gerência de Gestão da Arrecadação ( Gegar ), área técnica afeta ao assunto questionado, informamos que o CNPJ 49. 930. 514 / 0343 - 82, vinculado ao processo informado não apresenta restrição junto ao Cadin. Para maiores esclarecimentos, informamos que a Anvisa também disponibiliza a sua Central de Atendimento, por meio do 0800 642 9782 ( dias úteis, das 7h30 às 19h30 ) e por meio eletrônico, no Fale Conosco : ( http : / / portal. anvisa. gov. br / fale - conosco ) Atenciosamente, Agência Nacional de Vigilância Sanitária

## Exemplo 30 — linha Excel 14900

- Seleção: error_high_confidence, error_c234_to_c1
- Verdadeiro → predito: `c234` → `c1`
- Probabilidades: c1=0.8790, c234=0.0799, c5=0.0410
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8790 / 0.7991 / 0.4463 nats
- Grupo normalizado (SHA-256): `23177b70821cf11867ea1bca4f9083faa46ea7d1f03821c5df34a9f8c676ee03`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Sr ( a ). Saddan, Encaminhamos, em anexo, resposta ao seu pedido de informação. Atenciosamente, Serviço de Informação ao Cidadão do Banco do Brasil SICBB Recurso Conforme a Lei 12527 / 11 em seu artigo Art. 15, no caso de indeferimento de acesso a informações ou às razões da negativa do acesso, poderá o interessado interpor recurso contra a decisão no prazo de 10 ( dez ) dias a contar da sua ciência. Parágrafo único. O recurso será dirigido à autoridade hierarquicamente superior à que exarou a decisão impugnada, que deverá se manifestar no prazo de 5 ( cinco ) dias.

## Exemplo 31 — linha Excel 16688

- Seleção: error_c234_to_c1
- Verdadeiro → predito: `c234` → `c1`
- Probabilidades: c1=0.3514, c234=0.2982, c5=0.3504
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3514 / 0.0010 / 1.0958 nats
- Grupo normalizado (SHA-256): `15f20d85687b57d0d7e55dfebc443902532842040c0693111a138f855a04e7cd`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Senhor, Em atenção à sua demanda por informação, encaminhamos arquivo ( s ) anexo ( s ) contendo a resposta elaborada pela Unidade responsável pelo tema / assunto da demanda. Registre - se que, conforme o Decreto 7. 724 / 2012, art. 21, nos casos de : - Negativa de acesso à informação, ou - Não fornecimento das razões da negativa do acesso O requerente poderá apresentar recurso no prazo de dez dias, contado da ciência da decisão. O órgão deverá apreciar o Recurso no prazo de cinco dias, contado da sua apresentação. Atenciosamente, Serviço de Informação ao Cidadão - SIC / MJSP ( 61 ) 2025 - 3949 - sic @ mj. gov. br

## Exemplo 32 — linha Excel 16869

- Seleção: error_c234_to_c1
- Verdadeiro → predito: `c234` → `c1`
- Probabilidades: c1=0.3539, c234=0.3265, c5=0.3196
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3539 / 0.0275 / 1.0976 nats
- Grupo normalizado (SHA-256): `0374fb76d50d09720df8c088c3693bd3c18ed707dfa9d165412520cefdeb951b`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Caro solicitante, As informações solicitadas encontram - se em nosso sítio eletrônico, na aba " Contatos " que também pode ser acessada pelo link : https : / / ifce. edu. br / servicos / contatos # infraestrutura cordialmente, SIC / IFCE

## Exemplo 33 — linha Excel 698

- Seleção: correct_low_confidence
- Verdadeiro → predito: `c234` → `c234`
- Probabilidades: c1=0.3264, c234=0.3410, c5=0.3326
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3410 / 0.0084 / 1.0985 nats
- Grupo normalizado (SHA-256): `4714f3e8889d84d1c2ceaf74a642204a0cc32ad7ec00eec70e791f33c140bb85`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Senhora Monielly, bom dia. Em resposta ao pedido de informações registrado em 24 / 11 / 2018, sob o protocolo 99908. 000675 / 2018 - 30, os registros e documentos históricos que a Chesf detém encontram - se arquivados no Centro de Documentação ( CDOC ), em Recife, e estão disponíveis para consulta pública. Encaminhamos os contatos para que possa realizar o agendamento e comparecer pessoalmente, onde poderá verificar o conteúdo existente disponível : Alexandra Santos ( aledomi @ chesf. gov. br ), ( 81 ) 3229 - 2346 Caso tenha dificuldades, encaminhamos um segundo contato : Tércio Xavier ( txavier @ chesf. gov. br ), ( 81 ) 3229 - 2953. Atenciosamente, Serviço de Informação ao Cidadão - SIC 55 81 3229. 4888 sic @ chesf. gov. br

## Exemplo 34 — linha Excel 4793

- Seleção: correct_low_confidence
- Verdadeiro → predito: `c234` → `c234`
- Probabilidades: c1=0.3364, c234=0.3437, c5=0.3199
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3437 / 0.0074 / 1.0982 nats
- Grupo normalizado (SHA-256): `2fd62cd3ce1ac8411cf6edf4dd822e605882ec239de5f143f8da5b826ef2a41e`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Diego, Peço que você entre em contato com os pesquisadores Denise Gutierrez - fone ( 92 ) 3643 - 3360 e Carlos Cleomir - fone ( 92 ) 3643 - 3179. O correio eletrônico deles é dmdgutie @ inpa. gov. br e cleomir @ inpa. gov. br Eles poderão fornecer os dados que você tanto necessita. Peço desculpas pela demora na obtenção da informação Atenciosamente SIC / INPA

## Exemplo 35 — linha Excel 3832

- Seleção: error_c234_to_c5
- Verdadeiro → predito: `c234` → `c5`
- Probabilidades: c1=0.0432, c234=0.1392, c5=0.8176
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8176 / 0.6783 / 0.5749 nats
- Grupo normalizado (SHA-256): `12b3e0622120beb7057d21774c8eebee3304864685c44940d2e83cfb28f2f057`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezada ( o ) Cidadã ( o ), Encaminhamos, em anexo, questionário respondido. Atenciosamente, Serviço de Informação ao Cidadão

## Exemplo 36 — linha Excel 5735

- Seleção: error_c234_to_c5
- Verdadeiro → predito: `c234` → `c5`
- Probabilidades: c1=0.3204, c234=0.3339, c5=0.3457
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3457 / 0.0117 / 1.0981 nats
- Grupo normalizado (SHA-256): `12c55ac719bdecc184d4e38c9fa48e2af058f18e4dca9896bfb77602afaecd2f`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Aldo de Jesus Dias, Favor acessar o link https : / / www. ifpe. edu. br / servidor / tabelas / tabelas

## Exemplo 37 — linha Excel 6808

- Seleção: error_c234_to_c5
- Verdadeiro → predito: `c234` → `c5`
- Probabilidades: c1=0.0300, c234=0.1350, c5=0.8350
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8350 / 0.6999 / 0.5262 nats
- Grupo normalizado (SHA-256): `99e1cef65ee56ff51156f746346bff48ab25b8c1373860d69b848368ba4aeb30`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezada Mônica Bom dia Infelizmente, a Amazul, que é uma empresa nova, não tem nenhum projeto neste sentido. Somos uma empresa tecnológica, que desenvolve tecnologias na área nuclear. atenciosamente Prazo para recursos em primeira instância : 10 dias área para recursos de primeira instância : Ouvidoria

## Exemplo 38 — linha Excel 8743

- Seleção: error_c234_to_c5
- Verdadeiro → predito: `c234` → `c5`
- Probabilidades: c1=0.3077, c234=0.3461, c5=0.3463
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3463 / 0.0002 / 1.0971 nats
- Grupo normalizado (SHA-256): `9af95733eb742e04d58013fc78f14a1e52fc4c949f2990d6e9e75898ddd29418`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Senhor, Em atenção ao solicitado, referente ao Decreto 7. 845 / 2012, relacionamos abaixo as respostas dispostas em itens conforme questionamentos enviados : 1. O Ministério da Educação é registrado como órgão de registro nível 1, para fins de tratamento de informação classificadas em qualquer grau de sigilo? Segundo o decreto citado acima. RESPOSTA : Não. Relatórios sobre Informações Classificadas no âmbito do MEC podem ser encontradas no link : http : / / portal. mec. gov. br / informacoes - classificadas 2. Caso sim, como um órgão vinculado ao MEC poderia obter o registro nível 2 para tratamento de informações classificadas em qualquer grau de sigilo? RESPOSTA : xxxxx 3. Caso a reposta da primeira pergunta seja negativa. Há previsão, data ou informações de quando o MEC cadastrará como órgão de nível 1? RESPOSTA : Não. Atenciosamente, Subsecretaria de Assuntos Administrativos Ministério da Educação

## Exemplo 39 — linha Excel 10663

- Seleção: error_c234_to_c5
- Verdadeiro → predito: `c234` → `c5`
- Probabilidades: c1=0.3335, c234=0.3217, c5=0.3448
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3448 / 0.0113 / 1.0982 nats
- Grupo normalizado (SHA-256): `32689dc7537d57afb5927b1efbbc1c97c50a1b7a5972271b0c3e0db36534b9c7`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Senhor, Temos a esclarecer que recebemos o retorno do seu recurso de informação via formulário de resposta, datado de 02 / 03 / 2016, encaminhado pela Diretoria de Qualidade Ambiental - Diqua Atenciosamente, SIC Serviço de Informação ao Cidadão do Ibama SCEN Setor de Clubes Esportivos Norte Trecho 02 Ed. Sede do Ibama Bloco : I CEP : 70. 818 - 900 - Brasília - DF sic @ ibama. gov. br

## Exemplo 40 — linha Excel 10948

- Seleção: error_c234_to_c5
- Verdadeiro → predito: `c234` → `c5`
- Probabilidades: c1=0.3056, c234=0.3418, c5=0.3526
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3526 / 0.0108 / 1.0968 nats
- Grupo normalizado (SHA-256): `9266592f9657a92526896ce2854884a9c2be3973d5bf0742946edada2ff7a578`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezada Senhora, Informamos que sua solicitação é de competência do Cadastro Técnico Federal. Acesse o Formulário de Solicitação de Auxílio através do link http : / / servicos. ibama. gov. br / ctf / formulario _ solicitacao _ auxilio. php Para mais informações entre em contato diretamente com o Setor do Cadastro Técnico Federal, através do telefone ( 61 ) 3316 - 1677. Atenciosamente, SIC Serviço de Informação ao Cidadão do Ibama SCEN Setor de Clubes Esportivos Norte Trecho 02 Ed. Sede do Ibama Bloco : I CEP : 70. 818 - 900 - Brasília - DF

## Exemplo 41 — linha Excel 12879

- Seleção: error_c234_to_c5
- Verdadeiro → predito: `c234` → `c5`
- Probabilidades: c1=0.0290, c234=0.1166, c5=0.8544
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8544 / 0.7378 / 0.4877 nats
- Grupo normalizado (SHA-256): `ae2f7a4f65745a93192d51c9edb67a38c4168e36910e7e896a9671f4476b152a`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Senhor Iber, Esta empresa não possui nenhum processo minerário junto ao DNPM, não existe em nosso banco de dados. Só posso responder pelo DNPM e não pelo Governo federal como um todo. No DNPM ela não existe. Atenciosamente, SIC / DNPM

## Exemplo 42 — linha Excel 13082

- Seleção: error_c234_to_c5
- Verdadeiro → predito: `c234` → `c5`
- Probabilidades: c1=0.0347, c234=0.1088, c5=0.8565
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8565 / 0.7477 / 0.4907 nats
- Grupo normalizado (SHA-256): `29a7ef1d0df624cf42f02eac9f06f99e0f2b2acca961b75522067f88e5bf2f01`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado usuário, Em anexo a Norma Interna 01 / 2017. Atenciosamente, DIPOA / MAPA

## Exemplo 43 — linha Excel 4511

- Seleção: error_c5_to_c1
- Verdadeiro → predito: `c5` → `c1`
- Probabilidades: c1=0.3564, c234=0.3109, c5=0.3327
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3564 / 0.0238 / 1.0971 nats
- Grupo normalizado (SHA-256): `69293fc4d6593806bcd63aa7906204a49fb18d0016f3d3b8c429569c06cc2a6f`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezados, Considerando a sua natureza jurídica, de Empresa Pública Federal pertencente à Administração Indireta, esclarecemos que a Finep não está enquadrada no rol de entidades abrangidas pelo Decreto 1. 590 / 1995. Com relação à Instrução Normativa 01 / 2018 - MP / SGP, informamos ainda que a Finep não é integrante do Sistema de Pessoal Civil da Administração Federal - Sipec. Atenciosamente, Equipe do SIC

## Exemplo 44 — linha Excel 5308

- Seleção: error_c5_to_c1
- Verdadeiro → predito: `c5` → `c1`
- Probabilidades: c1=0.8065, c234=0.1095, c5=0.0839
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8065 / 0.6970 / 0.6236 nats
- Grupo normalizado (SHA-256): `64655bb25e4ddef6a3da4f817ef534f442959b17f36f504c1b03ffaebe3f3354`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Sr ( a ). Glauber, Encaminhamos - lhe, em anexo, resposta da Diretoria de Suprimentos, Infraestrutura e Patrimônio do Banco do Brasil ao seu pedido de informação. Atenciosamente, Serviço de Informação ao Cidadão do Banco do Brasil SICBB Recurso Conforme a Lei 12527 / 11 em seu artigo Art. 15, no caso de indeferimento de acesso a informações ou às razões da negativa do acesso, poderá o interessado interpor recurso contra a decisão no prazo de 10 ( dez ) dias a contar da sua ciência. Parágrafo único. O recurso será dirigido à autoridade hierarquicamente superior à que exarou a decisão impugnada, que deverá se manifestar no prazo de 5 ( cinco ) dias.

## Exemplo 45 — linha Excel 7440

- Seleção: error_c5_to_c1
- Verdadeiro → predito: `c5` → `c1`
- Probabilidades: c1=0.3517, c234=0.3513, c5=0.2970
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3517 / 0.0005 / 1.0956 nats
- Grupo normalizado (SHA-256): `5e1e6427658c415f0d3359314404a13232a623d747308742c0efbd7a8ae7570b`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Sr., O Coordenador - Geral da Dívida Ativa da União da Procuradoria - Geral da Fazenda Nacional, Dr. CRISTIANO NEUENSCHWANDER LINS DE MORAIS, atendendo à solicitação de informação formulada por Vossa Senhoria e, tendo em vista o disposto na Lei 12. 527, de 18 de novembro de 2011, encaminha, em anexo, planilha com os dados em que atendem aos itens 1 a 5, em relação ao item 6, informa que não estão disponibilizadas no sítio da PGFN de forma estruturada, tal como solicitado no presente pedido. Atende - se, assim, aos ditames dos artigos, inciso XXXIII, 37, §, inciso II, 216, §, da Constituição Federal, bem como à Lei 12. 527, de 18 de novembro de 2011, especialmente seu artigo. Considerando o disposto no art. 19, inc. II, c / c o art. 21, caput, do Decreto n. 7. 724, de 2012, informa - se que poderá ser apresentado recurso, no prazo de 10 dias, contado da ciência da decisão. Autoridade responsável pela apreciação do recurso :. Anelize Lenzi Ruas de Almeida, Diretora do Departamento de Gestão da Dívida Ativa da União. Atenciosamente, SIC PGFN Gabinete da Procuradoria - Geral da Fazenda Nacional. Acesse o nosso site para mais informações : www. pgfn. gov. br

## Exemplo 46 — linha Excel 7939

- Seleção: error_high_confidence, error_c5_to_c1
- Verdadeiro → predito: `c5` → `c1`
- Probabilidades: c1=0.9109, c234=0.0645, c5=0.0247
- Confiança top-1 / margem top-1−top-2 / entropia: 0.9109 / 0.8464 / 0.3531 nats
- Grupo normalizado (SHA-256): `d034f503dd4f0111cfc70d675da614ef56adc08edd4eb5108c462c29e917afbb`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Sr ( a ). Maria Debiasi, Encaminhamos - lhe resposta da Unidade de Canais do Banco do Brasil ao seu pedido de informação : Prezada Maria Debiasi Ehlers, Em resposta ao pleito referido à epígrafe, vimos por meio deste externar a impossibilidade de fornecimento, pelo Banco, dos dados solicitados, com base nos fundamentos expostos a seguir : 1. Os dados solicitados revestem - se de informações protegidas pelos sigilos comercial, empresarial e profissional, com potencial de atingir os negócios afetos à empresa, podendo prejudica - la frente à concorrência, com reflexos financeiros e acionários, 2. A negativa de entrega dos dados postulados encontra amparo legal nos arts. 170, IV e 173, §, inciso II, ambos da Constituição da República, art. 22, da Lei 12. 527 / 2011 ( Lei de Acesso à Informação LAI ) e arts., § e §, inciso I, do Decreto 7. 724 / 2012 ( Regulamento da LAI ). Atenciosamente, Jorge Luiz Costa Bahia Gerente de Divisão " Serviço de Informação ao Cidadão do Banco do Brasil SICBB Recurso Conforme a Lei 12527 / 11 em seu artigo Art. 15, no caso de indeferimento de acesso a informações ou às razões da negativa do acesso, poderá o interessado interpor recurso contra a decisão no prazo de 10 ( dez ) dias a contar da sua ciência. Parágrafo único. O recurso será dirigido à autoridade hierarquicamente superior à que exarou a decisão impugnada, que deverá se manifestar no prazo de 5 ( cinco ) dias.

## Exemplo 47 — linha Excel 11953

- Seleção: error_c5_to_c1
- Verdadeiro → predito: `c5` → `c1`
- Probabilidades: c1=0.3575, c234=0.3517, c5=0.2908
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3575 / 0.0057 / 1.0944 nats
- Grupo normalizado (SHA-256): `f146f31a8736c2e554351f722e125d42cf916fe4ca3d41ae9bb49e55d520603c`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Senhor, Cumprimentando - o cordialmente, informamos que nos casos de transferência de mantença de instituições de ensino superior a uma outra mantenedora a legislação educacional responsabiliza a sucessora, na pessoa de seu responsável legal, pela guarda e gestão do acervo acadêmico dos estudantes ( ver : art. 58, do Decreto 9. 235, de 2017, disponível no endereço http : / / www. planalto. gov. br / ccivil _ 03 / leis / L9394. htm ). Assim sendo, os ex - alunos da instituição transferida têm acesso garantido aos seus documentos acadêmicos. Note - se que, em caso de recusa de pedido de expedição de diploma, histórico escolar ou outro documento acadêmico de guarda obrigatória, aplica - se o Código Civil Brasileiro. Ou seja, a instituição de ensino superior fica em mora ( situação de descumprimento culposo ) mediante interpelação formal ( escrita e protocolar ) do interessado. Informamos, ainda, que a ESCOLA SUPERIOR DE EDUCAçãO CORPORATIVA ( ESEC ), código 2319, encontra - se em atividade, funciona no endereço Rua Luiz Fagundes, 1. 680, CEP 88106 - 000, São José, SC, tel. ( 48 ) 33579011, e é mantida pela Anhanguera Educacional Participações S / A, CNPJ 04. 310. 392 / 0001 - 46, cuja representante legal é a senhora GISLAINE MORENO ( DIRETORA DE DESENVOLVIMENTO INSTITUCIONAL ). Dessa forma, sugerimos que Vossa Senhoria solicite o documento à instituição. Atenciosamente, Assessoria da Secretaria de Regulação e Supervisão da Educação Superior do Ministério da Educação

## Exemplo 48 — linha Excel 16598

- Seleção: error_c5_to_c1
- Verdadeiro → predito: `c5` → `c1`
- Probabilidades: c1=0.8171, c234=0.1068, c5=0.0761
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8171 / 0.7102 / 0.6000 nats
- Grupo normalizado (SHA-256): `cf40f0bae4bea442024975d7bfe6a4e7c498c50f9c6e5f717c382d5af4edff7a`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Sr ( a ). Roberta, Encaminhamos - lhe, em anexo, resposta da Diretoria Governança de Entidades Ligadas do Banco do Brasil ao seu pedido de informação : " Conforme solicitado no SICBB, encaminhamos em anexo os arquivos enviados pela FBB para atendimento da demanda. Atenciosamente, Emerson Luís Zanin Gerente Executivo " Atenciosamente, Serviço de Informação ao Cidadão do Banco do Brasil SICBB Recurso Conforme a Lei 12527 / 11 em seu artigo Art. 15, no caso de indeferimento de acesso a informações ou às razões da negativa do acesso, poderá o interessado interpor recurso contra a decisão no prazo de 10 ( dez ) dias a contar da sua ciência. Parágrafo único. O recurso será dirigido à autoridade hierarquicamente superior à que exarou a decisão impugnada, que deverá se manifestar no prazo de 5 ( cinco ) dias.

## Exemplo 49 — linha Excel 16760

- Seleção: error_high_confidence, error_c5_to_c1
- Verdadeiro → predito: `c5` → `c1`
- Probabilidades: c1=0.8818, c234=0.0785, c5=0.0397
- Confiança top-1 / margem top-1−top-2 / entropia: 0.8818 / 0.8034 / 0.4387 nats
- Grupo normalizado (SHA-256): `b614f4766b6f27a7008f5d0da70924a3ad525ad66a6801e1d67e1c63ad5d38dd`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Sr ( a ). Helio, Encaminhamos, em anexo, resposta ao seu pedido de informação. Atenciosamente, Serviço de Informação ao Cidadão do Banco do Brasil SICBB Recurso Conforme a Lei 12527 / 11 em seu artigo Art. 15, no caso de indeferimento de acesso a informações ou às razões da negativa do acesso, poderá o interessado interpor recurso contra a decisão no prazo de 10 ( dez ) dias a contar da sua ciência. Parágrafo único. O recurso será dirigido à autoridade hierarquicamente superior à que exarou a decisão impugnada, que deverá se manifestar no prazo de 5 ( cinco ) dias.

## Exemplo 50 — linha Excel 18380

- Seleção: error_c5_to_c1
- Verdadeiro → predito: `c5` → `c1`
- Probabilidades: c1=0.3579, c234=0.3274, c5=0.3147
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3579 / 0.0305 / 1.0971 nats
- Grupo normalizado (SHA-256): `9012931eb43db38e011cc4ee2563a788fd866815ca6ea933a19a27a1d17cbda0`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Segue anexo a resposta do Ministério dos Transportes, Portos e Aviação Civil à solicitação de informação. Encaminhamos os documentos solicitados através da plataforma " WeTransfer ". Precisamos utilizar o site para o envio devido ao tamanho dos arquivos ultrapassarem os limites de anexo por e - mail. Alerto que o arquivo permanecerá disponível para download somente por 7 dias e para acessar os arquivos baixar o link para download. Se novas informações ou informações complementares se fizerem necessárias, abra um novo pedido no sistema e - SIC para prosseguirmos com o atendimento. Caso a resposta tenha sido negada sem justificativa, a Lei de Acesso à Informação prevê a possibilidade de interposição de recurso no prazo de 10 dias, contatos a partir da data de envio da resposta. O recurso poderá ser interposto pelos seguintes canais de atendimento : Sistema e - SIC : www. acessoainformacao. gov. br E - mail : sic @ transportes. gov. br Carta ou Presencial no endereço : Esplanada dos Ministérios, Bloco " R " CEP : 70. 044 - 900 - Brasília / DF Segunda à sexta, das 8h às 18h. Após o recebimento do recurso por parte do órgão, o prazo de resposta é de 5 dias corridos. Att, Lana Turner de Souza Serviço de Informações ao Cidadão - SIC

## Exemplo 51 — linha Excel 1500

- Seleção: error_c5_to_c234
- Verdadeiro → predito: `c5` → `c234`
- Probabilidades: c1=0.3322, c234=0.3432, c5=0.3247
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3432 / 0.0110 / 1.0984 nats
- Grupo normalizado (SHA-256): `9c5590d6f9d69e182d4e55bc01b8793ea783b33183fc9f0fa60ce0eb19d37658`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezada Senhora, Em atenção ao pedido formulado por Vossa Senhoria informamos que devido à grande quantidade de arquivos estes estão disponibilizados no Repositório de Arquivos do MEC, podendo ser acessado pelo link http : / / ramec. mec. gov. br / documentos - diversos / 6271 - sic - 23480016333201838 - banco - de - dados - das - respostas - dos - alunos - avaliacao - diagnostica - do - pnmalfa - 2018. Esclarecemos que o nome e a data de nascimento dos alunos foram preservados. Além disso, o código utilizado como identificação do aluno não era um campo obrigatório e também não era necessariamente o código INEP, tendo em vista a existência de alunos de ano que não vieram de creches públicas. Atenciosamente, Chefe de Gabinete Secretaria de Educação Básica Ministério da Educação

## Exemplo 52 — linha Excel 3547

- Seleção: error_c5_to_c234
- Verdadeiro → predito: `c5` → `c234`
- Probabilidades: c1=0.1929, c234=0.6115, c5=0.1956
- Confiança top-1 / margem top-1−top-2 / entropia: 0.6115 / 0.4160 / 0.9373 nats
- Grupo normalizado (SHA-256): `e1b330a4e57c3f48f0a1fae237410434b138222f5f75c9d12123ef68b0a611e6`
- Entrada truncada em 512 tokens: `True`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) Cidadão ( ), 1. Conforme solicitação através do E - SIC, site CGU, informamos que : 1. 1. o seguinte referente ao Programa Minha Casa Minha Vida. Primeiramente cumpre - nos informar que o PMCMV é operacionalizado por meio da concessão de subsídiosb provenientes do OGU e de financiamentos habitacionais a pessoas físicas, de acordo com o seu enquadramento, baseado na renda familiar bruta mensal. A operacionalização do Programa no âmbito do PNHU é dividida em subprogramas em que a concessão de subsídio ou financiamento ocorre de forma estratificada em Faixas, dispostas da seguinte forma : Recursos Fundo de Arrendamento Residencial ( FAR ) Faixa 1 : a ) Objetiva conceder financiamento habitacional fortemente subvencionado, sob a forma de parcelamento, sem juros, às famílias indicadas pelo Município ou Governo do Estado / Distrito Federal, com renda mensal bruta até R $ 1. 800, 00, para aquisição de unidades habitacionais urbanas produzidas com recursos do Orçamento Geral da União ( OGU ) integralizados no Fundo de Arrendamento Residencial ( FAR ), nesta Faixa do PMCMV, o valor aportado pelos beneficiários é ínfimo quando comparado ao valor do subsídio concedido e do valor total do imóvel, b ) Busca atender famílias com renda até R $ 3. 600, 00 nas operações enquadradas nas situações provenientes de emergência ou de calamidade pública reconhecida pelo Ministério da Integração Nacional e nas operações vinculadas às programações orçamentárias do PAC, que demandem reassentamento, remanejamento ou substituição de unidades habitacionais. 2. 1. 2. Recursos do Fundo de Desenvolvimento Social FDS ( MCMV - E ) Faixa 1 : visa à concessão de financiamento fortemente subvencionado, sem juros, às famílias com renda mensal bruta de até R $ 1. 800, 00, admitindo - se até R $ 2. 350, 00 para até 10 % das famílias atendidas em cada empreendimento, organizadas sob a forma coletiva, para aquisição de unidades habitacionais urbanas produzidas por Entidades Organizadoras, devidamente habilitadas no Ministério das Cidades, com recursos do Orçamento Geral da União ( OGU ) integralizados no Fundo de Desenvolvimento Social ( FDS ). 2. 1. 3. Recursos do FGTS Faixa 1,

## Exemplo 53 — linha Excel 4019

- Seleção: error_low_confidence, error_c5_to_c234
- Verdadeiro → predito: `c5` → `c234`
- Probabilidades: c1=0.3268, c234=0.3384, c5=0.3348
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3384 / 0.0036 / 1.0985 nats
- Grupo normalizado (SHA-256): `0ade011765fbd031139df3e04d1dcd33a29b5ae244b3731d1d29b1a836ba3253`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> A senhora somente pode adquirir uma animal da fauna brasileira, de um criador comercial devidamente registrado no Ibama, exigindo a nota fiscal do animal ( documento que comprova a origem legal do animal ). No site do Ibama ( www. ibama. gov. br ) no link fauna você vai poder encontrar a lista de criadores comerciais autorizados pelo Ibama. Dúvidas entre em contato com o setor de fauna através do telefone ( 61 ) 3316 - 1170. Atenciosamente, SIC Serviço de Informação ao Cidadão do Ibama SCEN Setor de Clubes Esportivos Norte Trecho 02 Ed. Sede do Ibama Bloco : I CEP : 70. 818 - 900 - Brasília - DF Horário de Atendimento : De segunda à Sexta Feira, das 08 : 00 às 12 : 00 - das 14 : 00 às 18 : 00 Horas

## Exemplo 54 — linha Excel 8336

- Seleção: error_c5_to_c234
- Verdadeiro → predito: `c5` → `c234`
- Probabilidades: c1=0.3281, c234=0.3515, c5=0.3204
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3515 / 0.0234 / 1.0978 nats
- Grupo normalizado (SHA-256): `990b597f9f025b1b8a260f4d10451499905ac5ba05c587133af6c69066ffd518`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezada Solicitante, Em atenção ao seu pedido de acesso à informação registrado no e - SIC, segue esclarecimentos da instituição : " Informamos que os dados para serem usadas como material de pesquisa para dissertação de Mestrado requer que o projeto seja encaminhado pelo Professor Orientador. Tratando - se de projeto que obtém informação que identifique instituições e / ou respondentes, informamos que o projeto deve conter a aprovação do Comitê de ética da Instituição. Caso entenda que o órgão não atendeu adequadamente, pode - se interpor recurso. Atenciosamente, Serviço de Informação ao Cidadão SIC / UFBA

## Exemplo 55 — linha Excel 13541

- Seleção: error_c5_to_c234
- Verdadeiro → predito: `c5` → `c234`
- Probabilidades: c1=0.1146, c234=0.5863, c5=0.2991
- Confiança top-1 / margem top-1−top-2 / entropia: 0.5863 / 0.2871 / 0.9223 nats
- Grupo normalizado (SHA-256): `969994865c076695c0efd3dd5ff17c5b6816ccccb756f53355952b3b8b0b7ed1`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Bom dia, segue resposta a sua solicitação : No momento estamos organizando um novo formato da realização de remoções dentro do IFSul. Neste mês teremos uma nova rodada de remoções, mas agora com todas as vagas disponíveis no IFSul. Após isto, algumas vagas poderão ser preenchidas por redistribuição e as demais irão para concurso públicos. Após demanda do Ministério Público Federal, tanto as remoções como as redistribuições estão em processo de regramento. Tão logo tenhamos estas definições e vagas a serem disponibilizadas, publicaremos no site do IFSul. Mas em específico sobre vagas para matemática, estamos aguardando dos câmpus que sejam enviadas as vagas disponíveis e as áreas para que possamos realizar o processo de remoção antes de qualquer outra forma de preenchimento. Neste processo conseguiremos visualizar as vagas e áreas disponíveis. Att. Diretor Executivo da Reitoria - - Diretoria Executiva da Reitoria Instituto Federal Sul - rio - grandense Rua Gonçalves Chaves, 3218 - sala 510 / 511 Centro Pelotas - RS CEP 96. 020 - 000 Tel. + 55 ( 53 ) 3026 - 6050 / 3026 - 6221 email : der @ ifsul. edu. br

## Exemplo 56 — linha Excel 15527

- Seleção: error_c5_to_c234
- Verdadeiro → predito: `c5` → `c234`
- Probabilidades: c1=0.2263, c234=0.5767, c5=0.1970
- Confiança top-1 / margem top-1−top-2 / entropia: 0.5767 / 0.3504 / 0.9737 nats
- Grupo normalizado (SHA-256): `821800efa9aff7df3acb16694e0f0e8da063484afc0219f18e94c6de4e82043c`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado ( a ) senhor ( a ), em atenção a sua demanda protocolada n & deg, 99933. 000046 / 2018 - 01, de 13 / 04 / 2018, segue anexo resposta oferecida pelo Gabinete da Presidência - GABIN, desta Conab. Informamos, caso seja do seu interesse, vossa senhoria poderá interpor recurso contra este posicionamento no prazo de dez dias, a contar da sua ciência, com respaldo no Art. 15 da Lei de Acesso à Informação n & deg, 12. 527 / 2011, combinado com Art. 21 & deg, do decreto 7724, de 16 / 05 / 2012.

## Exemplo 57 — linha Excel 15667

- Seleção: error_c5_to_c234
- Verdadeiro → predito: `c5` → `c234`
- Probabilidades: c1=0.3166, c234=0.3516, c5=0.3319
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3516 / 0.0197 / 1.0977 nats
- Grupo normalizado (SHA-256): `69f58fb6425e9cf343af523d543df9333e5c9d96cb831223741de4879e1ac7e8`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Segue em anexo, resposta para conhecimento.

## Exemplo 58 — linha Excel 17157

- Seleção: error_c5_to_c234
- Verdadeiro → predito: `c5` → `c234`
- Probabilidades: c1=0.0954, c234=0.5729, c5=0.3317
- Confiança top-1 / margem top-1−top-2 / entropia: 0.5729 / 0.2411 / 0.9094 nats
- Grupo normalizado (SHA-256): `b514309b28ca1ac6d44b7a9679fc89dcadaa7412054ec807cc8bcf27db8c8321`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Senhor, Cumprimentando - o cordialmente e em atendimento à demanda apresentada, informamos que não há previsão legal, prazos mínimo ou máximo, para a publicação de portaria de redistribuição. O Processo 23205. 005172 / 2014 - 82, em nome do demandante, foi encaminhado pela unidade SESU / DIFES / CGRH em 17 / 06 / 2019 e recebido na Coordenação de Administração de Pessoal ( CGGP / CAP / REDISTRIB ) em 18 / 06 / 2019, onde encontra - se até o momento. O trâmite necessário para a conclusão de processos de redistribuição varia conforme a instrução de cada processo, a existência de pendências ou a disponibilidade de consulta ao Sistema Integrado de Administração de Recursos Humanos ( SIAPE ), além do volume de processos em tramitação no MEC. Sugerimos o acompanhamento do trâmite por meio do site : https : / / protocolointegrado. gov. br, pelo setor de gestão de pessoas do seu órgão ou através do e - mail redistribuicaocggp @ mec. gov. br. A publicação pode ser acompanhada através da página da Imprensa Nacional, D. O. U, Seção 2, MEC ( www. in. gov. br ). Atenciosamente, Coordenação - Geral de Gestão de Pessoas Subsecretaria de Assuntos Administrativos Ministério da Educação

## Exemplo 59 — linha Excel 9733

- Seleção: correct_low_confidence
- Verdadeiro → predito: `c5` → `c5`
- Probabilidades: c1=0.3291, c234=0.3334, c5=0.3376
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3376 / 0.0042 / 1.0986 nats
- Grupo normalizado (SHA-256): `bd39af66e95f84204c4c48bcba0b130dd7e1154042d0d9942f2fc768e25cc412`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> EM ATENçãO A SOLICITAçãO, SEGUE DADOS DE COMPRA DO MEDICAMENTO FINGOLIMOIDE 0, 5MG.

## Exemplo 60 — linha Excel 15045

- Seleção: correct_low_confidence
- Verdadeiro → predito: `c5` → `c5`
- Probabilidades: c1=0.3361, c234=0.3197, c5=0.3442
- Confiança top-1 / margem top-1−top-2 / entropia: 0.3442 / 0.0081 / 1.0981 nats
- Grupo normalizado (SHA-256): `8c610838be9d009c7de56e2b16e430520d3f72a0a86bdf35c78ed9107473a55a`
- Entrada truncada em 512 tokens: `False`

Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):

> Prezado Cidadão, Temos a esclarecer que recebemos o retorno do seu recurso de informação via formulário de resposta, datado de 27 / 04 / 2016, encaminhado pela Diretoria de Licenciamento Ambiental - Dilic Atenciosamente, SIC Serviço de Informação ao Cidadão do Ibama SCEN Setor de Clubes Esportivos Norte Trecho 02 Ed. Sede do Ibama Bloco : I CEP : 70. 818 - 900 - Brasília - DF sic @ ibama. gov. br
