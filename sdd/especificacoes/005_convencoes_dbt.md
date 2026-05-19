# Especificação 005 — Convenções dbt

## 1. Objetivo

Este documento define as convenções adotadas para o projeto dbt.

O objetivo é garantir consistência, legibilidade, rastreabilidade e padronização entre modelos, testes, documentação, materializações e organização dos arquivos.

Estas convenções devem ser seguidas durante a implementação dos modelos `silver`, `gold`, testes, macros, seeds e demais artefatos dbt.

## 2. Princípios gerais

As convenções do projeto devem seguir os seguintes princípios:

- clareza acima de abreviação;
- nomes descritivos;
- SQL legível;
- separação clara entre camadas;
- documentação junto da implementação;
- testes conectados às especificações;
- uso consistente de `source()` e `ref()`;
- materializações escolhidas com justificativa;
- modelos alinhados ao grão definido em spec.

## 3. Idioma

O projeto será desenvolvido em português do Brasil.

Devem estar em português:

- nomes dos modelos `silver` e `gold`;
- nomes dos marts;
- nomes dos testes singulares;
- descrições de modelos;
- descrições de colunas;
- comentários explicativos;
- especificações;
- planos;
- tarefas;
- validações;
- documentação técnica.

Termos oficiais do dbt podem permanecer em inglês, como:

- `dbt`;
- `source`;
- `model`;
- `seed`;
- `snapshot`;
- `macro`;
- `test`;
- `freshness`;
- `incremental`;
- `lineage`;
- `materialization`.

## 4. Estrutura do projeto dbt

A estrutura esperada do projeto dbt será:

```text
dbt/
├── dbt_project.yml
├── packages.yml
├── models/
│   ├── sources/
│   │   └── sources.yml
│   ├── silver/
│   │   ├── silver_clientes.sql
│   │   ├── silver_pedidos.sql
│   │   ├── silver_itens_pedido.sql
│   │   ├── silver_pagamentos.sql
│   │   ├── silver_avaliacoes.sql
│   │   ├── silver_produtos.sql
│   │   └── silver_vendedores.sql
│   └── gold/
│       ├── dim_clientes.sql
│       ├── dim_produtos.sql
│       ├── dim_vendedores.sql
│       ├── fato_pedidos.sql
│       ├── fato_itens_pedido.sql
│       ├── mart_vendas_diarias.sql
│       ├── mart_vendas_mensais.sql
│       ├── mart_desempenho_entregas.sql
│       └── mart_satisfacao_clientes.sql
├── tests/
├── macros/
├── seeds/
└── snapshots/
```

Essa estrutura pode evoluir caso o projeto cresça, mas qualquer mudança relevante deve ser documentada.

## 5. Convenções de schemas

O banco PostgreSQL deverá utilizar três schemas principais:

```text
bronze
silver
gold
```

A responsabilidade de cada schema será:

- `bronze`: dados ingeridos próximos da origem;
- `silver`: dados limpos, padronizados e qualificados;
- `gold`: dados analíticos, fatos, dimensões e marts.

## 6. Convenções da camada bronze

A camada `bronze` será criada pela ingestão.

O dbt deve tratar as tabelas bronze como `sources`.

As tabelas bronze devem preservar nomes próximos da origem.

Exemplos:

```text
olist_customers_dataset
olist_orders_dataset
olist_order_items_dataset
olist_order_payments_dataset
olist_order_reviews_dataset
olist_products_dataset
olist_sellers_dataset
olist_geolocation_dataset
product_category_name_translation
```

A bronze não deve aplicar:

- renomeação analítica;
- tradução de colunas;
- regra de negócio;
- deduplicação;
- cálculo de métricas;
- enriquecimento de dados.

## 7. Convenções de sources

As tabelas da bronze devem ser declaradas em:

```text
dbt/models/sources/sources.yml
```

Nome sugerido da source:

```text
olist
```

Exemplo:

```yaml
version: 2

sources:
  - name: olist
    schema: bronze
    description: "Tabelas da base pública da Olist ingeridas na camada bronze."
    tables:
      - name: olist_orders_dataset
        description: "Tabela de pedidos da Olist preservada próxima da origem."
```

As sources devem possuir, quando aplicável:

- descrição da tabela;
- descrição das colunas principais;
- testes estruturais;
- freshness, se houver coluna técnica de carga adequada.

## 8. Convenções da camada silver

Modelos da camada `silver` devem representar entidades limpas, padronizadas e qualificadas.

Padrão de nome:

```text
silver_<entidade>
```

Exemplos:

```text
silver_clientes
silver_pedidos
silver_itens_pedido
silver_pagamentos
silver_avaliacoes
silver_produtos
silver_vendedores
silver_geolocalizacao
```

Na silver, as colunas devem ser renomeadas para português e com nomes claros.

Exemplo:

```text
order_id → pedido_id
customer_id → cliente_id
order_status → status_pedido
order_purchase_timestamp → data_compra
```

A camada silver deve priorizar:

- casts;
- padronização;
- limpeza;
- deduplicação quando necessária;
- preparação das entidades;
- regras intermediárias de qualidade;
- integridade entre entidades.

## 9. Convenções da camada gold

Modelos da camada `gold` devem representar dados prontos para consumo analítico.

Tipos principais:

- dimensões;
- fatos;
- marts.

### 9.1 Dimensões

Padrão de nome:

```text
dim_<entidade>
```

Exemplos:

```text
dim_clientes
dim_produtos
dim_vendedores
```

Dimensões devem ter:

- uma linha por entidade;
- chave única;
- atributos descritivos;
- documentação de colunas;
- testes de unicidade e obrigatoriedade.

### 9.2 Fatos

Padrão de nome:

```text
fato_<processo_ou_evento>
```

Exemplos:

```text
fato_pedidos
fato_itens_pedido
```

Fatos devem ter:

- grão explícito;
- chaves para dimensões;
- métricas;
- datas relevantes;
- testes de integridade;
- critérios de aceite definidos.

### 9.3 Marts

Padrão de nome:

```text
mart_<assunto_analitico>
```

Exemplos:

```text
mart_vendas_diarias
mart_vendas_mensais
mart_desempenho_entregas
mart_satisfacao_clientes
```

Marts devem ter:

- foco analítico claro;
- grão explícito;
- métricas documentadas;
- regras de cálculo descritas;
- testes de consistência.

## 10. Convenções de colunas

A partir da camada silver, as colunas devem ser nomeadas em português.

Regras gerais:

- usar letras minúsculas;
- usar `snake_case`;
- evitar abreviações pouco claras;
- usar nomes descritivos;
- manter consistência entre modelos;
- nomes de datas devem começar com `data_`;
- indicadores booleanos devem começar com `is_`, `possui_` ou `flag_`, conforme contexto;
- valores monetários devem iniciar com `valor_`;
- quantidades devem iniciar com `quantidade_`.

Exemplos:

```text
pedido_id
cliente_id
produto_id
vendedor_id
data_compra
data_entrega_cliente
valor_total_pedido
quantidade_itens
status_pedido
is_pedido_atrasado
```

## 11. Convenções de SQL

O SQL deve priorizar clareza e legibilidade.

Regras:

- usar CTEs para organizar etapas;
- nomear CTEs de forma descritiva;
- evitar `select *` em modelos finais;
- explicitar colunas selecionadas;
- usar `source()` para tabelas bronze;
- usar `ref()` para modelos dbt;
- evitar lógica complexa sem necessidade;
- manter transformações na camada correta;
- usar comentários apenas quando agregarem clareza.

Exemplo de estrutura recomendada:

```sql
with pedidos_origem as (

    select
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp
    from {{ source('olist', 'olist_orders_dataset') }}

),

pedidos_tipados as (

    select
        order_id as pedido_id,
        customer_id as cliente_id,
        order_status as status_pedido,
        cast(order_purchase_timestamp as timestamp) as data_compra
    from pedidos_origem

)

select *
from pedidos_tipados
```

## 12. Convenções de materialização

As materializações devem ser escolhidas de acordo com o papel do modelo.

Sugestão inicial:

- `silver`: `view` ou `table`;
- `dim`: `table`;
- `fato`: `incremental` quando houver justificativa;
- `mart`: `table` ou `incremental`, conforme estratégia;
- modelos auxiliares simples: `ephemeral`, se fizer sentido.

Nenhuma materialização deve ser escolhida sem justificativa.

Modelos incrementais devem seguir a especificação:

```text
sdd/especificacoes/004_estrategia_incremental.md
```

## 13. Convenções de documentação YAML

Todo modelo relevante deve ser documentado em YAML.

A documentação deve incluir:

- descrição do modelo;
- descrição das colunas principais;
- testes aplicados;
- relacionamentos;
- regras importantes;
- observações sobre grão ou materialização.

Exemplo:

```yaml
version: 2

models:
  - name: silver_pedidos
    description: "Modelo silver com pedidos limpos, tipados e padronizados."
    columns:
      - name: pedido_id
        description: "Identificador único do pedido."
        tests:
          - not_null
          - unique
```

## 14. Convenções de testes

Testes devem seguir a especificação:

```text
sdd/especificacoes/003_estrategia_de_testes_dbt.md
```

Testes singulares devem ser nomeados em português.

Padrão:

```text
assert_<regra_em_portugues>.sql
```

Exemplos:

```text
assert_entrega_nao_antecede_compra.sql
assert_pedidos_sem_valor_negativo.sql
assert_avaliacao_entre_1_e_5.sql
assert_pedido_entregue_possui_data_entrega.sql
```

Testes customizados devem ter nomes curtos e reutilizáveis.

Exemplos:

```text
valor_positivo
data_nao_futura
texto_nao_vazio
```

## 15. Convenções de macros

Macros devem ser criadas apenas quando houver reutilização clara.

Padrão de nome:

```text
<acao_ou_regra>
```

Exemplos:

```text
valor_positivo
gerar_chave_surrogate
normalizar_texto
```

Macros devem ser:

- simples;
- reutilizáveis;
- documentadas;
- testáveis quando aplicável.

## 16. Convenções de seeds

Seeds devem ser usados para tabelas pequenas de domínio ou mapeamento.

Exemplos possíveis:

- tradução de status;
- mapeamento de categorias;
- domínios controlados.

Seeds não devem substituir fontes principais de dados.

## 17. Convenções de snapshots

Snapshots não fazem parte do escopo obrigatório da primeira fase.

Poderão ser avaliados futuramente para cenários de histórico de mudanças.

Exemplo futuro:

- histórico de alteração de clientes;
- histórico de status de pedidos;
- histórico de atributos de produtos.

## 18. Convenções de commits

As mensagens de commit devem estar em português, seguindo estilo Conventional Commits.

Exemplos:

```text
feat: adiciona modelo silver de pedidos
docs: adiciona especificacao da estrategia de testes dbt
test: adiciona testes de qualidade para pedidos
fix: corrige regra de calculo de atraso de entrega
refactor: reorganiza modelos da camada gold
chore: ajusta configuracao inicial do dbt
```

## 19. Critérios de aceite

Esta especificação será considerada corretamente aplicada quando:

- a estrutura do projeto dbt seguir a organização definida;
- as sources estiverem documentadas;
- os modelos silver e gold seguirem os padrões de nome;
- colunas da silver e gold estiverem em português;
- modelos relevantes tiverem documentação YAML;
- testes seguirem a estratégia definida;
- modelos incrementais seguirem a estratégia incremental;
- SQL estiver legível e organizado;
- commits seguirem o padrão definido.

## 20. Evolução futura

Estas convenções podem evoluir conforme o projeto crescer.

Mudanças relevantes devem ser documentadas em ADR ou atualização desta especificação.

Possíveis evoluções:

- separação de schemas por ambiente;
- adoção de convenções para CI/CD;
- padronização de exposures;
- uso de metrics;
- regras adicionais para snapshots;
- uso formal de dbt contracts;
- integração com dbt docs.
