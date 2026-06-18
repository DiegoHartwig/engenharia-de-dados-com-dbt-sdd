# Validação do modelo silver_pedidos

## Modelo

`silver_pedidos`

## Camada

Silver

## Objetivo da validação

Validar se o modelo `silver_pedidos` foi criado conforme a especificação definida para a camada silver, preservando a granularidade original da origem e aplicando apenas tratamentos simples de padronização, tipagem e renomeação de colunas.

## Origem dos dados

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

## Critérios validados

### Estrutura

O modelo contém as seguintes colunas:

| Coluna | Descrição |
|---|---|
| id_pedido | Identificador único do pedido |
| id_cliente | Identificador do cliente associado ao pedido |
| status_pedido | Status do pedido padronizado em minúsculas |
| data_hora_compra | Data e hora em que o pedido foi realizado |
| data_hora_aprovacao | Data e hora em que o pedido foi aprovado |
| data_hora_entrega_transportadora | Data e hora de entrega à transportadora |
| data_hora_entrega_cliente | Data e hora de entrega ao cliente |
| data_estimada_entrega | Data estimada de entrega do pedido |

### Mapeamento de colunas

| Origem | Destino |
|---|---|
| order_id | id_pedido |
| customer_id | id_cliente |
| order_status | status_pedido |
| order_purchase_timestamp | data_hora_compra |
| order_approved_at | data_hora_aprovacao |
| order_delivered_carrier_date | data_hora_entrega_transportadora |
| order_delivered_customer_date | data_hora_entrega_cliente |
| order_estimated_delivery_date | data_estimada_entrega |

### Regras aplicadas

- `order_id` recebe `trim`;
- `customer_id` recebe `trim`;
- `order_status` recebe `lower(trim())`;
- campos de data/hora convertidos para `timestamp` via `cast`;
- granularidade original preservada: um registro por pedido;
- sem join, agregação, métricas de negócio ou deduplicação.

## Testes dbt executados

| Teste | Coluna | Resultado |
|---|---|---|
| not_null | id_pedido | PASS |
| unique | id_pedido | PASS |
| not_null | id_cliente | PASS |
| not_null | status_pedido | PASS |
| not_null | data_hora_compra | PASS |
| not_null | data_estimada_entrega | PASS |

Total: **6/6 PASS**

## Comandos executados

```bash
dbt run --select silver_pedidos
dbt test --select silver_pedidos
dbt docs generate
```

## Resultado

| Comando | Resultado |
|---|---|
| `dbt run` | `CREATE VIEW` — OK |
| `dbt test` | 6/6 PASS |
| `dbt docs generate` | Catálogo gerado com sucesso |

## Status

Validado.

## Observações

O modelo `silver_pedidos` representa a segunda entidade tratada da camada silver.

Campos de data/hora que podem ser nulos na origem (`data_hora_aprovacao`, `data_hora_entrega_transportadora`, `data_hora_entrega_cliente`) foram mantidos sem teste de `not_null`, pois refletem o ciclo de vida natural do pedido — nem todo pedido é aprovado, enviado ou entregue.

Ele não aplica regras analíticas finais; métricas derivadas como tempo de entrega ou identificação de atraso pertencem à camada gold.
