with fonte as (

    select
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp,
        order_approved_at,
        order_delivered_carrier_date,
        order_delivered_customer_date,
        order_estimated_delivery_date

    from {{ source('bronze', 'olist_orders_dataset') }}

),

renomeado as (

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

)

select *
from renomeado
