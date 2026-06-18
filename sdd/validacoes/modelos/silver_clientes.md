# Validação do modelo silver_clientes

## Modelo

`silver_clientes`

## Camada

Silver

## Objetivo da validação

Validar se o modelo `silver_clientes` foi criado conforme a especificação definida para a camada silver, preservando a granularidade original da origem e aplicando apenas tratamentos simples de padronização, tipagem e renomeação de colunas.

## Origem dos dados

Source dbt:

```sql
source('bronze', 'olist_customers_dataset')
```

Tabela física de origem:

```
bronze.olist_customers_dataset
```

## Destino

```
silver.silver_clientes
```

## Critérios validados

### Estrutura

O modelo deve conter as seguintes colunas:

| Coluna | Descrição |
|---|---|
| id_cliente | Identificador do cliente no pedido |
| id_cliente_unico | Identificador único do cliente |
| prefixo_cep_cliente | Prefixo do CEP do cliente |
| cidade_cliente | Cidade do cliente |
| estado_cliente | Estado do cliente |

### Mapeamento de colunas

| Origem | Destino |
|---|---|
| customer_id | id_cliente |
| customer_unique_id | id_cliente_unico |
| customer_zip_code_prefix | prefixo_cep_cliente |
| customer_city | cidade_cliente |
| customer_state | estado_cliente |

### Regras aplicadas

- `customer_id` deve receber `trim`;
- `customer_unique_id` deve receber `trim`;
- `customer_city` deve receber `lower(trim())`;
- `customer_state` deve receber `upper(trim())`;
- a granularidade original deve ser preservada;
- não deve haver join;
- não deve haver agregação;
- não deve haver cálculo de métrica de negócio;
- não deve haver deduplicação nesta primeira versão.

## Testes dbt esperados

Os testes definidos no `schema.yml` devem validar:

| Coluna | Testes |
|---|---|
| id_cliente | not_null, unique |
| id_cliente_unico | not_null |
| prefixo_cep_cliente | not_null |
| cidade_cliente | not_null |
| estado_cliente | not_null |

## Comandos de validação

Executar a partir da pasta `dbt/`:

```bash
dbt run --select silver_clientes
dbt test --select silver_clientes
dbt docs generate
```

## Resultado esperado

O modelo deve ser materializado com sucesso no schema `silver`.

Os testes dbt devem executar sem falhas.

A documentação dbt deve ser gerada com sucesso.

## Status

Validado.

## Observações

O modelo `silver_clientes` representa a primeira entidade tratada da camada silver.

Ele não aplica regras analíticas finais, pois esse tipo de regra pertence à camada gold.
