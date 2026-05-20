# Validação 002 — Ingestão da Camada Bronze

## 1. Objetivo

Registrar a validação da ingestão dos arquivos CSV da base pública da Olist para o schema `bronze` do PostgreSQL, conforme definido no plano técnico e na ADR-004.

## 2. Plano relacionado

- `sdd/planos/002_ingestao_bronze.md`

## 3. Tarefas relacionadas

- `sdd/tarefas/002_ingestao_bronze.md`

## 4. Data da validação

```text
2026-05-19
```

## 5. Ambiente

| Item | Valor |
|---|---|
| Sistema operacional | Windows 10 Pro |
| Python | 3.11 |
| Banco de dados | PostgreSQL 16 |
| Execução | Docker Compose |
| Container | `engenharia_dados_dbt_postgres` |
| Database | `ecommerce_dw` |
| Schema destino | `bronze` |

## 6. Script utilizado

```text
ingestao/carregar_bronze_olist.py
```

## 7. Comando executado

```powershell
python ingestao\carregar_bronze_olist.py
```

## 8. Arquivos CSV carregados

| Arquivo | Tabela bronze |
|---|---|
| `olist_customers_dataset.csv` | `bronze.olist_customers_dataset` |
| `olist_geolocation_dataset.csv` | `bronze.olist_geolocation_dataset` |
| `olist_order_items_dataset.csv` | `bronze.olist_order_items_dataset` |
| `olist_order_payments_dataset.csv` | `bronze.olist_order_payments_dataset` |
| `olist_order_reviews_dataset.csv` | `bronze.olist_order_reviews_dataset` |
| `olist_orders_dataset.csv` | `bronze.olist_orders_dataset` |
| `olist_products_dataset.csv` | `bronze.olist_products_dataset` |
| `olist_sellers_dataset.csv` | `bronze.olist_sellers_dataset` |
| `product_category_name_translation.csv` | `bronze.product_category_name_translation` |

## 9. Contagem de registros por tabela

| Tabela | Registros |
|---|---|
| `bronze.olist_customers_dataset` | 99.441 |
| `bronze.olist_geolocation_dataset` | 1.000.163 |
| `bronze.olist_order_items_dataset` | 112.650 |
| `bronze.olist_order_payments_dataset` | 103.886 |
| `bronze.olist_order_reviews_dataset` | 99.224 |
| `bronze.olist_orders_dataset` | 99.441 |
| `bronze.olist_products_dataset` | 32.951 |
| `bronze.olist_sellers_dataset` | 3.095 |
| `bronze.product_category_name_translation` | 71 |
| **Total** | **1.550.922** |

## 10. Observações sobre colunas e tipos

Os nomes originais das colunas foram preservados. Todos os campos de texto foram carregados como `text`. Campos numéricos inteiros foram inferidos como `bigint` pelo pandas (ex.: `customer_zip_code_prefix`). Campos de data foram carregados como `text`, mantendo o comportamento esperado da camada bronze — nenhuma conversão de tipo foi aplicada.

Exemplo de estrutura da tabela `bronze.olist_orders_dataset`:

```text
order_id                      | text
customer_id                   | text
order_status                  | text
order_purchase_timestamp      | text
order_approved_at             | text
order_delivered_carrier_date  | text
order_delivered_customer_date | text
order_estimated_delivery_date | text
```

## 11. Verificação das regras da camada bronze

| Regra | Atendida |
|---|---|
| Nomes originais das colunas preservados | Sim |
| Sem tradução de colunas para português | Sim |
| Sem deduplicação | Sim |
| Sem regras de negócio aplicadas | Sim |
| Sem filtros analíticos | Sim |
| Sem agregações | Sim |
| Sem enriquecimento de dados | Sim |
| Dados próximos da origem | Sim |

## 12. Verificação do versionamento

| Item | Status |
|---|---|
| CSVs ignorados pelo `.gitignore` | Sim |
| `.env` ignorado pelo `.gitignore` | Sim |
| `.env.example` versionado | Sim |
| Script `carregar_bronze_olist.py` versionado | Sim |
| `requirements.txt` versionado | Sim |

## 13. Critérios de aceite

- [x] O script executou sem erro.
- [x] As tabelas foram criadas no schema `bronze`.
- [x] Os 9 arquivos CSV foram carregados.
- [x] As contagens foram exibidas no terminal.
- [x] Os CSVs não estão versionados no Git.
- [x] O `.env` não está versionado.
- [x] O `.env.example` está atualizado.
- [x] O resultado foi registrado em `sdd/validacoes/002_ingestao_bronze.md`.

## 14. Pendências

- [ ] Configurar o projeto dbt.
- [ ] Criar `sources.yml` apontando para as tabelas bronze.
- [ ] Iniciar modelagem da camada silver.

## 15. Conclusão

A ingestão da camada bronze foi concluída com sucesso. Os 9 arquivos CSV da base pública da Olist foram carregados para o schema `bronze` do PostgreSQL com um total de 1.550.922 registros. Os dados foram preservados próximos da origem, sem aplicação de regras de negócio, transformações ou deduplicação. O projeto está pronto para a etapa de configuração do dbt e modelagem da camada silver.
