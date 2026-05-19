# Especificação 003 — Estratégia de Testes dbt

## 1. Objetivo

Este documento define a estratégia de testes dbt adotada no projeto.

O objetivo é estabelecer como os testes serão planejados, documentados, implementados e validados ao longo das camadas `bronze`, `silver` e `gold`.

Neste projeto, os testes não serão tratados como uma etapa complementar. Eles fazem parte central do processo de desenvolvimento orientado por especificações.

## 2. Princípio geral

Toda regra de qualidade ou regra de negócio descrita em uma especificação deve ser avaliada como candidata a teste dbt.

A regra principal será:

```text
Se uma regra é importante para confiar no dado, ela deve ser documentada e, sempre que possível, testada.
```

## 3. Relação entre SDD e testes dbt

A estratégia de testes deve partir das especificações.

O fluxo esperado é:

```text
Especificação
    ↓
Regra de qualidade ou negócio
    ↓
Teste dbt esperado
    ↓
Implementação no YAML, SQL ou macro
    ↓
Execução com dbt test ou dbt build
    ↓
Registro de validação
```

Exemplo:

Regra especificada:

```text
Cada pedido deve possuir um identificador obrigatório.
```

Implementação possível:

```yaml
columns:
  - name: pedido_id
    tests:
      - not_null
```

Exemplo:

Regra especificada:

```text
A data de entrega não pode ser anterior à data da compra.
```

Implementação possível:

```sql
select *
from {{ ref('fato_pedidos') }}
where data_entrega_cliente < data_compra
```

## 4. Tipos de testes utilizados

O projeto deve demonstrar diferentes tipos de testes do dbt.

### 4.1 Testes genéricos nativos

Testes fornecidos pelo próprio dbt.

Exemplos:

- `not_null`;
- `unique`;
- `accepted_values`;
- `relationships`.

### 4.2 Testes singulares

Testes SQL criados em arquivos específicos dentro da pasta `dbt/tests/`.

Esses testes devem retornar apenas registros inválidos.

Exemplos:

- pedidos com valor negativo;
- entregas com data anterior à compra;
- avaliações fora da faixa esperada;
- pedidos entregues sem data de entrega;
- pagamentos associados a pedidos inexistentes.

### 4.3 Testes genéricos customizados

Testes criados como macros reutilizáveis.

Exemplos:

- `valor_positivo`;
- `data_nao_futura`;
- `texto_nao_vazio`;
- `percentual_valido`.

### 4.4 Testes com packages

Testes fornecidos por packages externos, quando fizer sentido.

O package mais provável para este projeto é:

- `dbt_utils`.

Exemplos de testes possíveis:

- `dbt_utils.unique_combination_of_columns`;
- `dbt_utils.expression_is_true`;
- `dbt_utils.not_null_proportion`.

Packages devem ser usados apenas quando agregarem clareza ou reutilização ao projeto.

## 5. Estratégia de testes por camada

## 5.1 Bronze

A camada `bronze` representa os dados próximos da origem.

Como a bronze deve preservar a estrutura original dos arquivos, os testes nesta camada devem ser mais estruturais e menos opinativos.

Na camada bronze, os testes devem validar principalmente:

- existência de chaves importantes;
- unicidade quando a origem indicar unicidade;
- valores aceitos em campos controlados;
- existência mínima de dados;
- consistência básica da origem;
- relacionamentos evidentes entre arquivos, quando aplicável.

Exemplos de testes na bronze:

- `order_id` não nulo em pedidos;
- `customer_id` não nulo em clientes;
- `order_status` dentro dos valores esperados;
- `review_score` entre os valores possíveis da origem;
- `order_id` único em `olist_orders_dataset`, caso a origem respeite esse grão.

A bronze não deve conter testes que exijam regras analíticas já transformadas.

## 5.2 Silver

A camada `silver` representa dados limpos, padronizados e qualificados.

Na silver, os testes devem ser mais rigorosos do que na bronze.

Na camada silver, os testes devem validar:

- chaves primárias;
- chaves estrangeiras;
- relacionamentos entre entidades;
- deduplicação;
- validade de datas;
- valores monetários;
- campos obrigatórios;
- status padronizados;
- consistência das regras de negócio intermediárias.

Exemplos de testes na silver:

- `pedido_id` não nulo;
- `pedido_id` único em `silver_pedidos`;
- `cliente_id` de `silver_pedidos` deve existir em `silver_clientes`;
- `status_pedido` deve estar em lista de valores aceitos;
- `valor_pagamento` não pode ser negativo;
- `nota_avaliacao` deve estar entre 1 e 5;
- data de entrega não pode ser anterior à data da compra.

## 5.3 Gold

A camada `gold` representa a camada analítica.

Na gold, os testes devem validar a confiabilidade dos fatos, dimensões e marts.

Na camada gold, os testes devem validar:

- unicidade de dimensões;
- unicidade de fatos no grão definido;
- integridade entre fatos e dimensões;
- métricas não negativas;
- indicadores coerentes;
- grão correto dos marts;
- consistência de agregações;
- regras de aceite dos modelos analíticos.

Exemplos de testes na gold:

- `cliente_id` único em `dim_clientes`;
- `produto_id` único em `dim_produtos`;
- `pedido_id` único em `fato_pedidos`;
- `cliente_id` em `fato_pedidos` deve existir em `dim_clientes`;
- `valor_total_pedido` não pode ser negativo;
- `quantidade_pedidos` não pode ser negativa;
- `receita_total` não pode ser negativa;
- `data_venda` não pode ser nula em `mart_vendas_diarias`.

## 6. Testes esperados por tipo de modelo

### 6.1 Sources

Os `sources` representam tabelas ingeridas na camada bronze.

Testes esperados:

- `not_null` em chaves principais;
- `unique` quando a origem possuir uma chave única clara;
- `accepted_values` em campos de status ou categorias controladas;
- freshness apenas se houver coluna técnica de carga adequada.

### 6.2 Modelos silver

Testes esperados:

- `not_null`;
- `unique`;
- `relationships`;
- `accepted_values`;
- testes singulares de qualidade;
- testes customizados reutilizáveis, quando fizer sentido.

### 6.3 Dimensões

Testes esperados:

- chave da dimensão não nula;
- chave da dimensão única;
- campos descritivos relevantes não nulos, quando aplicável;
- valores aceitos em atributos categóricos.

### 6.4 Fatos

Testes esperados:

- chave do fato ou chave de negócio não nula;
- unicidade no grão definido;
- relacionamentos com dimensões;
- métricas não negativas;
- regras de consistência temporal;
- testes singulares para regras de negócio críticas.

### 6.5 Marts

Testes esperados:

- chave ou combinação de chaves única no grão do mart;
- métricas não negativas;
- datas obrigatórias;
- indicadores consistentes;
- critérios de aceite específicos do mart.

## 7. Convenções de nomenclatura

Os testes singulares devem ser nomeados em português, de forma clara e descritiva.

Padrão recomendado:

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

Testes customizados devem usar nomes curtos e reutilizáveis.

Exemplos:

```text
valor_positivo
data_nao_futura
texto_nao_vazio
```

## 8. Severidade dos testes

Por padrão, testes críticos devem falhar a execução.

Quando necessário, alguns testes poderão ser configurados como aviso (`warn`) em vez de erro (`error`).

Critérios para `error`:

- quebra de chave primária;
- ausência de campos obrigatórios;
- relacionamento inválido;
- métrica negativa indevida;
- regra de negócio crítica violada.

Critérios para `warn`:

- pequena proporção de nulos toleráveis;
- inconsistência conhecida da origem;
- regra ainda em observação;
- validação exploratória.

A severidade deve ser documentada quando for diferente do padrão.

## 9. Estratégia de implementação

Os testes serão implementados em três locais principais:

### 9.1 YAML dos modelos

Usado para testes genéricos nativos e customizados.

Exemplo:

```yaml
models:
  - name: silver_pedidos
    columns:
      - name: pedido_id
        tests:
          - not_null
          - unique
```

### 9.2 Pasta de testes singulares

Usada para regras específicas em SQL.

Caminho:

```text
dbt/tests/
```

Exemplo:

```text
dbt/tests/assert_entrega_nao_antecede_compra.sql
```

### 9.3 Pasta de macros

Usada para testes genéricos customizados.

Caminho:

```text
dbt/macros/
```

Exemplo:

```text
dbt/macros/test_valor_positivo.sql
```

## 10. Critérios de aceite

A estratégia de testes será considerada corretamente aplicada quando:

- as regras de qualidade estiverem descritas nas especificações;
- os testes esperados estiverem documentados nas specs dos modelos;
- os testes genéricos nativos forem usados quando aplicável;
- testes singulares forem criados para regras específicas;
- pelo menos um teste genérico customizado for implementado;
- testes de relacionamento forem aplicados entre modelos relevantes;
- pelo menos um package de testes for avaliado ou utilizado, quando fizer sentido;
- `dbt test` executar com sucesso para os modelos implementados;
- `dbt build` executar com sucesso para o fluxo validado;
- as validações forem registradas em `sdd/validacoes/`.

## 11. Riscos e cuidados

Principais riscos:

- criar testes apenas para cumprir checklist;
- testar regras que ainda não foram especificadas;
- criar testes duplicados sem necessidade;
- aplicar testes muito fortes na bronze e quebrar o princípio de preservação;
- deixar regras críticas sem teste;
- criar testes singulares difíceis de entender;
- usar packages sem necessidade real.

Para evitar esses problemas, todo teste deve estar associado a pelo menos uma das seguintes finalidades:

- validar uma regra de negócio;
- validar uma regra de qualidade;
- proteger o grão de um modelo;
- validar integridade entre entidades;
- evitar regressão;
- aumentar a confiança no dado analítico.

## 12. Evolução futura

Possíveis evoluções da estratégia de testes:

- adicionar testes com `dbt_expectations`;
- configurar severidade diferenciada por ambiente;
- implementar testes de volume;
- implementar testes de freshness;
- integrar testes ao CI/CD;
- gerar documentação automática dos testes;
- medir cobertura de testes por camada;
- criar relatório de qualidade por modelo.
