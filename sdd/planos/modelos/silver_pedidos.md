# Plano de implementação: silver_pedidos

## Modelo

`silver_pedidos`

## Camada

Silver

## Referência

Especificação: `sdd/especificacoes/modelos/silver_pedidos.md`

---

## Etapas de implementação

### 1. Criar o arquivo SQL do modelo

Criar o arquivo:

```
dbt/models/silver/silver_pedidos.sql
```

O SQL deve:

- referenciar a origem via `{{ source('bronze', 'olist_orders_dataset') }}`;
- aplicar `trim` em `order_id` e `customer_id`;
- aplicar `lower(trim())` em `order_status`;
- converter os campos de data/hora para `timestamp` usando `cast`;
- renomear todas as colunas conforme o mapeamento da especificação;
- não conter joins, agregações, métricas ou deduplicação.

Estrutura esperada do SQL:

```sql
with fonte as (
    select * from {{ source('bronze', 'olist_orders_dataset') }}
)

select
    trim(order_id)                                          as id_pedido,
    trim(customer_id)                                       as id_cliente,
    lower(trim(order_status))                               as status_pedido,
    cast(order_purchase_timestamp as timestamp)             as data_hora_compra,
    cast(order_approved_at as timestamp)                    as data_hora_aprovacao,
    cast(order_delivered_carrier_date as timestamp)         as data_hora_entrega_transportadora,
    cast(order_delivered_customer_date as timestamp)        as data_hora_entrega_cliente,
    cast(order_estimated_delivery_date as timestamp)        as data_estimada_entrega
from fonte
```

### 2. Atualizar o schema.yml da camada silver

Arquivo a atualizar:

```
dbt/models/silver/schema.yml
```

Adicionar a entrada do modelo `silver_pedidos` com:

- descrição do modelo;
- descrição de cada coluna;
- testes: `not_null` e `unique` em `id_pedido`; `not_null` nas demais colunas obrigatórias.

### 3. Executar e validar o modelo

Executar a partir da pasta `dbt/`:

```bash
dbt run --select silver_pedidos
dbt test --select silver_pedidos
dbt docs generate
```

### 4. Criar o arquivo de validação SDD

Criar o arquivo:

```
sdd/validacoes/modelos/silver_pedidos.md
```

Registrar o resultado da execução, confirmando que o modelo foi materializado e os testes passaram.

---

## Estratégia de validação

1. Verificar se todas as colunas esperadas estão presentes no resultado;
2. Confirmar que `id_pedido` é único e não nulo;
3. Confirmar que `status_pedido` está em minúsculas;
4. Confirmar que os campos de data/hora têm tipo `timestamp`;
5. Confirmar que a contagem de registros no silver é igual à da origem bronze.

---

## Riscos e cuidados

| Risco | Cuidado |
|---|---|
| Campos de data/hora com valores nulos | O `cast` para `timestamp` retorna `null` sem erro; verificar se é esperado |
| `order_status` com valores fora do padrão | `lower(trim())` não filtra valores inesperados; aceitar nesta versão |
| Granularidade duplicada na origem bronze | Verificar com `count` vs `count distinct` em `order_id` antes de declarar `unique` |
| Schema `silver` inexistente | Confirmar que a macro `generate_schema_name` está configurada corretamente |
