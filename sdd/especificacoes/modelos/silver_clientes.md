# Especificação — silver_clientes

## 1. Objetivo

Criar uma entidade tratada de clientes na camada silver, a partir dos dados brutos da tabela `bronze.olist_customers_dataset`.

O modelo deve produzir um registro por `customer_id`, com colunas renomeadas para o padrão do projeto (português), valores padronizados e campos limpos.

## 2. Camada

`silver`

## 3. Grão

Um registro por `customer_id`.

A granularidade da origem é preservada nesta versão inicial. Não há deduplicação nesta primeira versão.

## 4. Fonte

| Source | Tabela |
|---|---|
| `bronze` | `olist_customers_dataset` |

Referência dbt: `{{ source('bronze', 'olist_customers_dataset') }}`

## 5. Colunas esperadas

| Coluna destino | Coluna origem | Transformação |
|---|---|---|
| `id_cliente` | `customer_id` | `trim()` |
| `id_cliente_unico` | `customer_unique_id` | `trim()` |
| `prefixo_cep_cliente` | `customer_zip_code_prefix` | sem transformação |
| `cidade_cliente` | `customer_city` | `lower(trim())` |
| `estado_cliente` | `customer_state` | `upper(trim())` |

## 6. Regras de transformação

- `id_cliente`: remover espaços em branco com `trim()`.
- `id_cliente_unico`: remover espaços em branco com `trim()`.
- `prefixo_cep_cliente`: preservar o valor original sem alteração de regra de negócio.
- `cidade_cliente`: aplicar `lower(trim())` para padronização em minúsculas.
- `estado_cliente`: aplicar `upper(trim())` para padronização em maiúsculas (sigla UF).

## 7. Regras de qualidade

- `id_cliente` não pode ser nulo.
- `id_cliente` deve ser único na tabela.
- `id_cliente_unico` não pode ser nulo.
- `prefixo_cep_cliente` não pode ser nulo.
- `cidade_cliente` não pode ser nula.
- `estado_cliente` não pode ser nulo.

## 8. Testes dbt esperados

| Coluna | Teste |
|---|---|
| `id_cliente` | `not_null`, `unique` |
| `id_cliente_unico` | `not_null` |
| `prefixo_cep_cliente` | `not_null` |
| `cidade_cliente` | `not_null` |
| `estado_cliente` | `not_null` |

## 9. Estratégia de materialização

`view` — padrão da camada silver definido em `dbt_project.yml`.

Não há necessidade de incremental nesta versão.

## 10. O que não será feito nesta versão

- Não será feita deduplicação.
- Não será feito join com outras tabelas.
- Não serão calculadas métricas.
- Não serão criadas colunas derivadas além das transformações listadas.

## 11. Critérios de aceite

- [ ] O modelo SQL existe em `dbt/models/silver/silver_clientes.sql`.
- [ ] O modelo está documentado em `dbt/models/silver/schema.yml`.
- [ ] Todos os testes genéricos estão declarados no YAML.
- [ ] `dbt run --select silver_clientes` executa sem erro.
- [ ] `dbt test --select silver_clientes` executa sem falha.
- [ ] O resultado está registrado em `sdd/validacoes/`.
