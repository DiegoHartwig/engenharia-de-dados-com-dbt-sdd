# ADR-002 — Uso de Português no Projeto

## Status

Aceita.

## Contexto

Este projeto tem como objetivo demonstrar boas práticas de Engenharia de Dados com dbt e Spec-Driven Development de forma didática, acessível e bem documentada.

Como a base utilizada é brasileira, pública e relacionada ao e-commerce da Olist, foi avaliada a possibilidade de desenvolver o projeto majoritariamente em português do Brasil.

A decisão envolve não apenas a documentação, mas também a nomenclatura dos modelos dbt, especificações, testes, marts, critérios de aceite e decisões arquiteturais.

## Decisão

O projeto será desenvolvido em português do Brasil.

Devem ser escritos em português:

- README;
- documentação técnica;
- especificações SDD;
- planos técnicos;
- listas de tarefas;
- decisões arquiteturais;
- descrições de modelos dbt;
- descrições de colunas;
- critérios de aceite;
- nomes dos modelos dbt das camadas silver e gold;
- nomes de testes singulares;
- nomes de marts analíticos.

Termos técnicos oficiais do ecossistema dbt poderão ser mantidos em inglês quando forem nomes próprios ou conceitos amplamente utilizados, como:

- dbt;
- source;
- model;
- seed;
- snapshot;
- macro;
- test;
- freshness;
- incremental;
- lineage;
- materialization.

## Convenções adotadas

As tabelas ingeridas na camada `bronze` devem preservar os nomes próximos da origem sempre que possível.

Exemplo:

```text
olist_orders_dataset
olist_customers_dataset
olist_order_items_dataset
```

A partir da camada `silver`, os modelos deverão usar nomes em português.

Exemplos:

```text
silver_pedidos
silver_clientes
silver_itens_pedido
silver_pagamentos
silver_avaliacoes
silver_produtos
silver_vendedores
```

Na camada `gold`, os modelos também deverão usar nomes em português.

Exemplos:

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
```

## Consequências positivas

Esta decisão traz os seguintes benefícios:

- torna o projeto mais didático para profissionais brasileiros;
- facilita a leitura das especificações e regras de negócio;
- melhora a clareza dos modelos analíticos;
- aproxima o projeto do contexto da base utilizada;
- reforça o objetivo educacional e de portfólio;
- facilita a publicação futura de conteúdos explicativos em português.

## Consequências negativas

Esta decisão também traz alguns cuidados:

- pode reduzir a acessibilidade para leitores internacionais;
- algumas ferramentas, documentações e exemplos da comunidade usam inglês como padrão;
- alguns termos técnicos não devem ser traduzidos de forma artificial;
- será necessário manter consistência na nomenclatura em português.

## Alternativas consideradas

### Alternativa 1 — Projeto totalmente em inglês

Essa alternativa foi considerada por ser comum em projetos open source e por facilitar o acesso internacional.

No entanto, foi descartada nesta fase porque o objetivo principal do projeto é didático e voltado à demonstração de boas práticas em português.

### Alternativa 2 — Documentação em português e código em inglês

Essa alternativa também foi considerada.

Ela teria a vantagem de manter o código próximo de padrões internacionais, mas reduziria a proposta didática de demonstrar um projeto completo de Engenharia de Dados em português.

### Alternativa 3 — Projeto híbrido sem regra definida

Essa alternativa foi descartada porque poderia gerar inconsistência entre documentação, modelos, testes e critérios de aceite.

## Critérios de aceite da decisão

Esta decisão será considerada corretamente aplicada quando:

- a documentação principal estiver em português;
- as especificações SDD estiverem em português;
- os modelos silver e gold estiverem nomeados em português;
- os testes singulares estiverem nomeados em português;
- os critérios de aceite estiverem em português;
- os termos técnicos oficiais do dbt forem preservados quando fizer sentido;
- a nomenclatura for consistente ao longo do projeto.

## Revisão futura

Esta decisão poderá ser revista caso o projeto passe a ter como objetivo principal publicação internacional, colaboração com pessoas não falantes de português ou adaptação para um template open source global.

Nesse caso, poderá ser criada uma nova ADR propondo uma estratégia bilíngue ou uma versão em inglês da documentação.
