# Especificação 002 — Estratégia de Camadas

## 1. Objetivo

Esta especificação define a estratégia de camadas adotada no projeto.

O objetivo é deixar claro o papel de cada camada, o tipo de transformação permitido em cada uma, os limites entre elas e como os testes dbt devem ser aplicados ao longo do fluxo.

A arquitetura do projeto será baseada em três camadas principais:

```text
bronze → silver → gold
```

A regra conceitual adotada será:

```text
Bronze preserva.
Silver qualifica.
Gold entrega valor analítico.
```

## 2. Contexto

Este projeto utiliza a base pública da Olist como cenário de exemplo para demonstrar boas práticas de Engenharia de Dados com dbt e Spec-Driven Development.

Como o foco da primeira fase está em dbt, SQL avançado, testes automatizados, modelos incrementais e documentação técnica, foi decidido que a camada `bronze` será usada como camada de aterrissagem dos dados.

Essa decisão está documentada em:

```text
sdd/decisoes/ADR-001-uso-da-bronze-como-landing-zone.md
```

## 3. Visão geral das camadas

A arquitetura lógica será:

```text
Arquivos CSV da Olist
    ↓
PostgreSQL - bronze
    ↓
dbt - silver
    ↓
dbt - gold
    ↓
marts analíticos
```

Cada camada terá uma responsabilidade específica:

| Camada | Responsabilidade principal |
|---|---|
| Bronze | Preservar dados próximos da origem |
| Silver | Limpar, padronizar e qualificar os dados |
| Gold | Entregar fatos, dimensões, métricas e marts analíticos |

## 4. Camada Bronze

### 4.1 Propósito

A camada `bronze` representa a entrada dos dados no projeto.

Neste projeto, os arquivos CSV da Olist serão ingeridos diretamente no schema `bronze` do PostgreSQL.

A camada bronze deve preservar os dados o mais próximo possível da origem, mantendo estrutura, nomes de colunas e conteúdo original sempre que possível.

### 4.2 Responsabilidades

A camada bronze deve:

- receber os dados ingeridos a partir dos arquivos públicos da Olist;
- preservar os nomes originais das colunas sempre que possível;
- preservar o conteúdo original dos arquivos;
- manter os dados em uma estrutura próxima à origem;
- servir como ponto de partida rastreável para as transformações do dbt;
- permitir testes estruturais básicos sobre os dados recebidos.

### 4.3 O que não deve acontecer na Bronze

A camada bronze não deve:

- aplicar regras de negócio;
- criar métricas;
- deduplicar registros;
- enriquecer dados;
- traduzir nomes de colunas para português;
- alterar o significado dos campos;
- filtrar registros inválidos;
- consolidar dados entre tabelas;
- criar fatos, dimensões ou marts analíticos.

### 4.4 Exemplos de tabelas Bronze

Exemplos esperados de tabelas na camada bronze:

```text
bronze.olist_orders_dataset
bronze.olist_customers_dataset
bronze.olist_order_items_dataset
bronze.olist_order_payments_dataset
bronze.olist_order_reviews_dataset
bronze.olist_products_dataset
bronze.olist_sellers_dataset
bronze.olist_geolocation_dataset
bronze.product_category_name_translation
```

### 4.5 Testes esperados na Bronze

Na camada bronze, os testes devem ser mais estruturais e menos opinativos.

Exemplos de testes possíveis:

- existência de chaves principais;
- `not_null` em identificadores essenciais;
- `unique` quando a origem indicar unicidade;
- `accepted_values` em campos controlados simples;
- validações básicas de volume;
- validações de relacionamento apenas quando forem evidentes na estrutura da origem.

Exemplos:

```text
order_id não deve ser nulo em olist_orders_dataset.
customer_id não deve ser nulo em olist_customers_dataset.
order_status deve conter apenas valores conhecidos.
```

## 5. Camada Silver

### 5.1 Propósito

A camada `silver` representa os dados limpos, padronizados, tipados e qualificados.

É a camada responsável por transformar os dados próximos da origem em entidades confiáveis para uso analítico.

### 5.2 Responsabilidades

A camada silver deve:

- renomear colunas para português;
- aplicar casts de tipos;
- padronizar textos e valores;
- tratar duplicidades quando necessário;
- aplicar regras de negócio intermediárias;
- validar relacionamentos entre entidades;
- organizar entidades principais;
- preparar os dados para a camada gold;
- tornar os dados mais legíveis e confiáveis.

### 5.3 Transformações permitidas na Silver

Na camada silver, são permitidas transformações como:

- conversão de datas para `date` ou `timestamp`;
- conversão de valores monetários para tipos numéricos;
- padronização de campos textuais;
- renomeação de colunas;
- criação de colunas derivadas simples;
- tratamento de nulos;
- deduplicação com `row_number`;
- aplicação de regras com `case when`;
- joins de apoio quando necessários para qualificação da entidade.

### 5.4 O que evitar na Silver

A camada silver deve evitar:

- criação de métricas finais de negócio;
- agregações analíticas finais;
- tabelas diretamente voltadas a dashboard;
- regras de apresentação;
- cálculos consolidados de KPIs;
- perda do grão original sem justificativa;
- joins que transformem a entidade em um mart analítico.

### 5.5 Exemplos de modelos Silver

Exemplos esperados de modelos na camada silver:

```text
silver_pedidos
silver_clientes
silver_itens_pedido
silver_pagamentos
silver_avaliacoes
silver_produtos
silver_vendedores
silver_geolocalizacao
silver_traducao_categoria_produto
```

### 5.6 Testes esperados na Silver

Na camada silver, os testes devem validar qualidade, consistência e integridade.

Exemplos de testes:

- `not_null` em chaves principais;
- `unique` em chaves naturais ou técnicas;
- `relationships` entre entidades;
- `accepted_values` em campos padronizados;
- testes singulares para validade de datas;
- testes customizados para valores positivos;
- testes para garantir deduplicação;
- testes para regras de negócio intermediárias.

Exemplos:

```text
pedido_id deve ser único em silver_pedidos.
cliente_id em silver_pedidos deve existir em silver_clientes.
data_entrega_cliente não pode ser anterior à data_compra.
valor_pagamento não pode ser negativo.
```

## 6. Camada Gold

### 6.1 Propósito

A camada `gold` representa a camada analítica do projeto.

Ela deve conter modelos preparados para consumo, incluindo dimensões, fatos e marts analíticos.

### 6.2 Responsabilidades

A camada gold deve:

- criar dimensões analíticas;
- criar fatos;
- criar marts de negócio;
- consolidar métricas;
- aplicar regras de negócio finais;
- definir indicadores;
- organizar dados para consumo analítico;
- utilizar modelos incrementais quando fizer sentido;
- documentar métricas e regras de cálculo.

### 6.3 Transformações permitidas na Gold

Na camada gold, são permitidas transformações como:

- joins entre entidades qualificadas da silver;
- agregações;
- cálculo de métricas;
- criação de indicadores;
- criação de flags analíticas;
- construção de fatos e dimensões;
- cálculo de evolução temporal;
- uso de window functions;
- criação de rankings;
- criação de marts por tema.

### 6.4 Exemplos de modelos Gold

Exemplos esperados de modelos na camada gold:

```text
dim_clientes
dim_produtos
dim_vendedores
fato_pedidos
fato_itens_pedido
mart_vendas_diarias
mart_vendas_mensais
mart_desempenho_entregas
mart_satisfacao_clientes
mart_desempenho_produtos
```

### 6.5 Testes esperados na Gold

Na camada gold, os testes devem validar consistência analítica.

Exemplos de testes:

- `unique` em chaves de dimensões;
- `not_null` em chaves de fatos;
- `relationships` entre fatos e dimensões;
- testes de métricas não negativas;
- testes de grão dos modelos;
- testes de consistência de indicadores;
- testes de regras de aceite dos marts.

Exemplos:

```text
cliente_id deve ser único em dim_clientes.
pedido_id deve ser único em fato_pedidos.
fato_pedidos.cliente_id deve existir em dim_clientes.
receita_total não pode ser negativa em mart_vendas_diarias.
```

## 7. Estratégia de nomenclatura por camada

A nomenclatura deve seguir o idioma principal do projeto: português do Brasil.

### 7.1 Bronze

Na bronze, os nomes devem preservar a origem sempre que possível.

Exemplo:

```text
olist_orders_dataset
olist_customers_dataset
```

### 7.2 Silver

Na silver, os modelos devem usar o prefixo `silver_`.

Exemplo:

```text
silver_pedidos
silver_clientes
silver_produtos
```

### 7.3 Gold

Na gold, os modelos devem usar prefixos conforme seu tipo:

```text
dim_
fato_
mart_
```

Exemplos:

```text
dim_clientes
fato_pedidos
mart_vendas_diarias
```

## 8. Estratégia de materialização

A estratégia inicial de materialização será definida por camada.

| Camada | Materialização inicial sugerida | Observação |
|---|---|---|
| Bronze | tabela física criada pela ingestão | Gerenciada pelo Airbyte/PostgreSQL |
| Silver | view ou table | Preferir clareza e facilidade de validação no início |
| Gold | table ou incremental | Usar incremental quando houver ganho técnico e didático |

A decisão final de materialização de cada modelo deve ser registrada na especificação do modelo.

## 9. Relação com SDD

Cada camada deve possuir regras claras antes da implementação.

As especificações devem orientar:

- quais modelos serão criados;
- qual é o grão esperado;
- quais transformações pertencem à camada;
- quais testes são obrigatórios;
- quais critérios de aceite devem ser atendidos.

Nenhum modelo relevante deve ser implementado apenas com base em intenção informal.

## 10. Critérios de aceite

Esta estratégia será considerada corretamente aplicada quando:

- as tabelas ingeridas estiverem no schema `bronze`;
- a camada bronze preservar os dados próximos da origem;
- a camada silver for responsável por limpeza, tipagem e padronização;
- a camada gold for responsável por fatos, dimensões e marts;
- os modelos seguirem a nomenclatura definida;
- os testes forem aplicados de acordo com a responsabilidade de cada camada;
- as especificações por modelo respeitarem os limites entre bronze, silver e gold.

## 11. Riscos e cuidados

Principais riscos:

- transformar dados indevidamente na bronze;
- criar métricas finais na silver;
- criar modelos gold sem grão claro;
- criar testes sem relação com regras de qualidade;
- usar incremental sem justificativa;
- misturar regras técnicas e regras analíticas na mesma camada;
- tornar o projeto burocrático demais.

## 12. Evolução futura

Esta estratégia poderá evoluir se o projeto passar a incluir:

- camada `raw`;
- Airflow;
- Spark;
- Trino;
- Databricks;
- lakehouse;
- dados incrementais reais;
- CI/CD;
- contratos de dados mais formais.

Qualquer mudança relevante na estrutura de camadas deverá ser registrada em uma nova ADR.
