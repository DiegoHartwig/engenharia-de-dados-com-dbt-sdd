with fonte_clientes as (

    select
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    from {{ source('bronze', 'olist_customers_dataset') }}

),

clientes_padronizados as (

    select
        trim(customer_id)            as id_cliente,
        trim(customer_unique_id)     as id_cliente_unico,
        customer_zip_code_prefix     as prefixo_cep_cliente,
        lower(trim(customer_city))   as cidade_cliente,
        upper(trim(customer_state))  as estado_cliente
    from fonte_clientes

)

select
    id_cliente,
    id_cliente_unico,
    prefixo_cep_cliente,
    cidade_cliente,
    estado_cliente
from clientes_padronizados
