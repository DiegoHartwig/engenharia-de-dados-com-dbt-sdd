# Especificação do modelo silver_pedidos

## Modelo

`silver_pedidos`

## Camada

Silver

## Objetivo

Limpar, padronizar e renomear as colunas da tabela de pedidos da Olist, preservando a granularidade original de um registro por pedido. Nenhuma regra de negócio analítica deve ser aplicada nesta camada.

## Origem

Source dbt:

```sql
source('bronze', 'olist_orders_dataset')
```

Tabela física de origem:

```
bronze.olist_orders_dataset
```

## Destino

```
silver.silver_pedidos
```

## Granularidade

Um registro por pedido (`order_id`). A granularidade da origem deve ser preservada integralmente.

## Mapeamento de colunas

| Origem | Destino | Tipo esperado |
|---|---|---|
| order_id | id_pedido | varchar |
| customer_id | id_cliente | varchar |
| order_status | status_pedido | varchar |
| order_purchase_timestamp | data_hora_compra | timestamp |
| order_approved_at | data_hora_aprovacao | timestamp |
| order_delivered_carrier_date | data_hora_entrega_transportadora | timestamp |
| order_delivered_customer_date | data_hora_entrega_cliente | timestamp |
| order_estimated_delivery_date | data_estimada_entrega | timestamp |

## Regras de transformação

- `order_id` deve receber `trim`;
- `customer_id` deve receber `trim`;
- `order_status` deve receber `lower(trim())`;
- campos de data/hora devem ser convertidos para `timestamp` quando aplicável;
- a granularidade original deve ser preservada.

## Regras que NÃO devem ser aplicadas na silver

- não fazer join com outras tabelas;
- não agregar ou sumarizar dados;
- não calcular métricas de negócio (ex.: tempo de entrega, atraso);
- não deduplicar nesta primeira versão;
- não criar colunas derivadas analíticas.

## Testes esperados

Os testes deverão ser definidos no `schema.yml` da camada silver:

| Coluna | Testes |
|---|---|
| id_pedido | not_null, unique |
| id_cliente | not_null |
| status_pedido | not_null |
| data_hora_compra | not_null |
| data_estimada_entrega | not_null |

## Critérios de aceite

- O modelo é materializado com sucesso no schema `silver`;
- Todos os testes dbt passam sem falhas;
- As colunas seguem o mapeamento definido nesta especificação;
- As regras de transformação estão aplicadas corretamente;
- A granularidade de um registro por pedido é preservada;
- A documentação dbt é gerada com sucesso via `dbt docs generate`.
