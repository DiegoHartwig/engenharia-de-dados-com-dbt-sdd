# Plano Técnico — silver_clientes

## 1. Referência

Especificação: `sdd/especificacoes/modelos/silver_clientes.md`

## 2. Estratégia de implementação

O modelo será implementado com CTEs simples para manter o SQL legível e rastreável:

1. **`fonte_clientes`** — seleciona apenas as colunas necessárias da source bronze.
2. **`clientes_padronizados`** — aplica as transformações de limpeza e renomeação.
3. **select final** — projeta todas as colunas do CTE anterior.

## 3. Dependências

| Dependência | Tipo | Referência |
|---|---|---|
| `olist_customers_dataset` | source | `{{ source('bronze', 'olist_customers_dataset') }}` |

Nenhuma dependência de modelo dbt.

## 4. Materialização

`view` — padrão configurado em `dbt_project.yml` para a camada silver.

Não há necessidade de tabela ou incremental nesta versão.

## 5. Estrutura do SQL

```sql
with fonte_clientes as (
    select colunas da origem
    from {{ source('bronze', 'olist_customers_dataset') }}
),

clientes_padronizados as (
    select
        trim(customer_id) as id_cliente,
        trim(customer_unique_id) as id_cliente_unico,
        customer_zip_code_prefix as prefixo_cep_cliente,
        lower(trim(customer_city)) as cidade_cliente,
        upper(trim(customer_state)) as estado_cliente
    from fonte_clientes
)

select * from clientes_padronizados
```

## 6. Documentação YAML

O modelo será documentado em `dbt/models/silver/schema.yml` com:

- descrição do modelo;
- descrição de todas as colunas;
- testes genéricos: `not_null`, `unique`.

## 7. Testes a implementar

Todos os testes serão declarados via YAML genérico nesta versão.

Nenhum teste singular será necessário nesta primeira versão.

## 8. Ordem de execução

1. Atualizar `dbt/models/sources/sources.yml` para garantir que o source esteja nomeado como `bronze`.
2. Criar `dbt/models/silver/silver_clientes.sql`.
3. Atualizar `dbt/models/silver/schema.yml`.
4. Executar `dbt run --select silver_clientes`.
5. Executar `dbt test --select silver_clientes`.
6. Executar `dbt docs generate`.
7. Registrar validação.

## 9. Riscos técnicos

- O source `olist_customers_dataset` deve existir no schema `bronze` do PostgreSQL. A ingestão bronze já foi validada, portanto esse risco é baixo.
- O nome do source no `sources.yml` deve ser `bronze` (não `olist_bronze`) para que a referência `source('bronze', ...)` funcione.

## 10. Decisões pendentes

Nenhuma.
