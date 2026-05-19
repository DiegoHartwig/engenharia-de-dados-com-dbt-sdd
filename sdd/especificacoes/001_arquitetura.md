# Especificação 001 — Arquitetura do Projeto

## 1. Objetivo

Este documento especifica a arquitetura inicial do projeto **Engenharia de Dados com dbt e SDD**.

A arquitetura foi definida para demonstrar boas práticas de Engenharia de Dados com dbt, utilizando uma abordagem de desenvolvimento orientado por especificações.

O objetivo é manter uma arquitetura simples, didática e profissional, permitindo aplicar:

- arquitetura em camadas;
- ingestão de dados públicos;
- transformação com dbt;
- testes automatizados;
- modelos incrementais;
- documentação técnica;
- critérios de aceite;
- validação por camada.

## 2. Visão geral da arquitetura

A arquitetura inicial do projeto será:

```text
Dataset público Olist
    ↓
Ingestão com Airbyte
    ↓
PostgreSQL - bronze
    ↓
dbt - silver
    ↓
dbt - gold
    ↓
marts analíticos
```

A camada `bronze` será a camada de entrada dos dados no PostgreSQL.

As camadas `silver` e `gold` serão construídas com dbt.

## 3. Componentes principais

### 3.1 Dataset público Olist

A base pública da Olist será utilizada como fonte de dados do projeto.

Ela contém arquivos relacionados a:

- clientes;
- pedidos;
- itens de pedido;
- pagamentos;
- avaliações;
- produtos;
- vendedores;
- geolocalização;
- tradução de categorias de produtos.

A base será utilizada como cenário de exemplo para demonstrar boas práticas de modelagem, transformação, testes e documentação em dbt.

### 3.2 Airbyte

O Airbyte será utilizado para realizar a ingestão dos arquivos da Olist para o PostgreSQL.

Nesta primeira fase, o Airbyte terá apenas a responsabilidade de carregar os dados para a camada `bronze`.

O Airbyte não deverá ser utilizado para aplicar regras de negócio, transformação analítica, deduplicação ou enriquecimento dos dados.

### 3.3 PostgreSQL

O PostgreSQL será utilizado como banco de dados analítico local do projeto.

Ele armazenará os schemas:

```text
bronze
silver
gold
```

O schema `bronze` receberá os dados ingeridos.

Os schemas `silver` e `gold` serão gerenciados pelo dbt.

### 3.4 dbt

O dbt será a principal ferramenta de transformação, modelagem, testes e documentação do projeto.

O dbt será responsável por:

- declarar as fontes da camada `bronze` como `sources`;
- construir modelos da camada `silver`;
- construir modelos da camada `gold`;
- aplicar testes genéricos;
- aplicar testes singulares;
- aplicar testes customizados;
- documentar modelos e colunas;
- gerar lineage;
- implementar modelos incrementais quando fizer sentido.

## 4. Camadas da arquitetura

## 4.1 Bronze

A camada `bronze` representa a entrada dos dados no projeto.

Responsabilidades da camada `bronze`:

- receber os dados ingeridos pelo Airbyte;
- preservar os dados próximos da origem;
- manter nomes e estrutura da origem sempre que possível;
- servir como base rastreável para as transformações do dbt.

A camada `bronze` não deve:

- aplicar regras de negócio;
- deduplicar registros;
- criar métricas;
- enriquecer dados;
- renomear colunas para fins analíticos;
- alterar o significado dos dados.

## 4.2 Silver

A camada `silver` representa os dados limpos, padronizados e qualificados.

Responsabilidades da camada `silver`:

- aplicar casts de tipos;
- traduzir e padronizar nomes de colunas para português;
- padronizar valores;
- tratar duplicidades quando necessário;
- aplicar regras de qualidade;
- aplicar regras de negócio intermediárias;
- preparar entidades confiáveis para a camada `gold`.

A camada `silver` deve evitar métricas analíticas finais.

Seu papel principal é qualificar, organizar e tornar os dados confiáveis para consumo analítico posterior.

## 4.3 Gold

A camada `gold` representa a camada analítica do projeto.

Responsabilidades da camada `gold`:

- criar dimensões;
- criar fatos;
- criar marts analíticos;
- calcular métricas;
- consolidar regras de negócio;
- preparar dados para consumo analítico;
- demonstrar modelos incrementais quando fizer sentido;
- validar consistência analítica com testes dbt.

A camada `gold` deve entregar dados prontos para análise.

## 5. Fluxo de dados

O fluxo de dados será:

```text
Arquivos CSV da Olist
    ↓
Airbyte
    ↓
Tabelas PostgreSQL no schema bronze
    ↓
dbt sources
    ↓
Modelos silver
    ↓
Modelos gold
    ↓
Marts analíticos
```

## 6. Organização esperada dos schemas

No PostgreSQL, a organização esperada será:

```text
bronze
silver
gold
```

### 6.1 Schema bronze

O schema `bronze` conterá as tabelas ingeridas a partir da Olist.

Exemplos esperados:

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

### 6.2 Schema silver

O schema `silver` conterá modelos limpos e padronizados.

Exemplos esperados:

```text
silver.silver_pedidos
silver.silver_clientes
silver.silver_itens_pedido
silver.silver_pagamentos
silver.silver_avaliacoes
silver.silver_produtos
silver.silver_vendedores
```

### 6.3 Schema gold

O schema `gold` conterá modelos analíticos.

Exemplos esperados:

```text
gold.dim_clientes
gold.dim_produtos
gold.dim_vendedores
gold.fato_pedidos
gold.fato_itens_pedido
gold.mart_vendas_diarias
gold.mart_vendas_mensais
gold.mart_desempenho_entregas
gold.mart_satisfacao_clientes
```

## 7. Responsabilidades por ferramenta

## 7.1 Airbyte

Responsável por:

- conectar na origem de dados;
- carregar os arquivos para o PostgreSQL;
- gravar os dados no schema `bronze`.

Não responsável por:

- aplicar regra de negócio;
- limpar dados;
- calcular métricas;
- criar fatos ou dimensões.

## 7.2 PostgreSQL

Responsável por:

- armazenar os dados;
- manter os schemas do projeto;
- servir como banco de execução para os modelos dbt.

## 7.3 dbt

Responsável por:

- transformar dados;
- organizar modelos por camada;
- aplicar testes;
- documentar modelos;
- controlar dependências;
- gerar lineage;
- materializar tabelas e views;
- implementar incrementalidade quando aplicável.

## 8. Decisões arquiteturais relacionadas

Esta especificação está relacionada às seguintes ADRs:

- `sdd/decisoes/ADR-001-uso-da-bronze-como-landing-zone.md`
- `sdd/decisoes/ADR-002-uso-de-portugues-no-projeto.md`
- `sdd/decisoes/ADR-003-uso-de-sdd-adaptado-para-dbt.md`

## 9. Regras arquiteturais

O projeto deve respeitar as seguintes regras:

1. A camada `bronze` deve preservar os dados próximos da origem.
2. A camada `silver` deve aplicar limpeza, padronização e qualificação.
3. A camada `gold` deve entregar valor analítico.
4. O Airbyte deve ser usado apenas para ingestão.
5. O dbt deve ser usado para transformação, testes e documentação.
6. Modelos relevantes devem possuir especificação antes da implementação.
7. Regras de qualidade devem ser avaliadas como testes dbt.
8. Decisões arquiteturais relevantes devem ser registradas em ADRs.
9. A primeira fase não deve incluir tecnologias fora do escopo inicial.

## 10. Fora do escopo arquitetural inicial

Nesta primeira fase, a arquitetura não incluirá:

- camada `raw`;
- Data Lake;
- Delta Lake;
- MinIO;
- Trino;
- Spark;
- Airflow;
- Databricks;
- dashboards;
- IA;
- RAG;
- banco vetorial;
- CI/CD.

Esses componentes poderão ser avaliados em fases futuras.

## 11. Critérios de aceite

Esta especificação será considerada atendida quando:

- os schemas `bronze`, `silver` e `gold` existirem no PostgreSQL;
- os dados da Olist forem ingeridos no schema `bronze`;
- as fontes da camada `bronze` forem declaradas no dbt como `sources`;
- os modelos `silver` forem criados a partir das fontes `bronze`;
- os modelos `gold` forem criados a partir dos modelos `silver`;
- a arquitetura estiver documentada no README;
- as decisões arquiteturais estiverem registradas em ADRs;
- o fluxo `bronze → silver → gold` estiver preservado;
- os comandos principais do dbt forem executados com sucesso.

## 12. Riscos e cuidados

Principais riscos:

- aplicar transformação indevida na camada `bronze`;
- criar modelos `gold` diretamente a partir da `bronze`;
- misturar regra de negócio com ingestão;
- criar complexidade excessiva antes de validar o dbt;
- incluir tecnologias fora do escopo inicial;
- criar specs sem relação prática com código, teste ou validação.

## 13. Evoluções futuras

Possíveis evoluções arquiteturais futuras:

- adicionar camada `raw`;
- adicionar orquestração com Airflow;
- adicionar processamento com Spark;
- consultar dados via Trino;
- migrar ou replicar arquitetura para Databricks;
- incluir dashboard;
- incluir CI/CD;
- incluir documentação automática com dbt docs;
- integrar validações automáticas em pipeline.
