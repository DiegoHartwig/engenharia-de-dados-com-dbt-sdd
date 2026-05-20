# Ingestão

Esta pasta contém os scripts responsáveis pela ingestão dos dados brutos para a camada `bronze`.

## Objetivo

A ingestão da primeira fase do projeto carrega os arquivos CSV da base pública da Olist para o PostgreSQL.

A estratégia foi definida na ADR:

```text
sdd/decisoes/ADR-004-uso-de-ingestao-simples-via-python.md
```

## Arquitetura da ingestão

```text
CSV Olist
    ↓
Script Python
    ↓
PostgreSQL - bronze
```

## Script principal

```text
ingestao/carregar_bronze_olist.py
```

## Regras da camada bronze

A camada `bronze` deve preservar os dados próximos da origem.

Nesta etapa, o script não deve:

- aplicar regras de negócio;
- traduzir colunas para português;
- deduplicar registros;
- criar métricas;
- enriquecer dados;
- aplicar filtros analíticos.

As transformações serão feitas posteriormente no dbt, nas camadas `silver` e `gold`.

## Pré-requisitos

O PostgreSQL deve estar em execução:

```powershell
docker compose up -d
```

As dependências Python devem estar instaladas:

```powershell
pip install -r requirements.txt
```

O arquivo `.env` deve conter:

```env
POSTGRES_HOST=localhost
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=ecommerce_password
POSTGRES_DB=ecommerce_dw
POSTGRES_PORT=5432
```

Os arquivos CSV devem estar em:

```text
dados/brutos/
```

## Execução

Na raiz do projeto, execute:

```powershell
python ingestao\carregar_bronze_olist.py
```

## Resultado esperado

As tabelas serão criadas no schema `bronze`, usando o nome do arquivo CSV sem a extensão.

Exemplo:

```text
olist_orders_dataset.csv → bronze.olist_orders_dataset
```
