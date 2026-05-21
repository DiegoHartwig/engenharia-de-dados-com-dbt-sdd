# Validação 003 — Configuração Inicial do dbt

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome | Configuração inicial do projeto dbt |
| Data da execução | 2026-05-20 |
| Responsável | Diego Hartwig |
| Plano relacionado | `sdd/planos/003_configuracao_dbt.md` |
| Tarefas relacionadas | `sdd/tarefas/003_configuracao_dbt.md` |
| Status | Concluído |

## 2. Objetivo da validação

Confirmar que a configuração inicial do projeto dbt foi realizada com sucesso, incluindo:

- estrutura de diretórios criada;
- `dbt_project.yml` configurado corretamente;
- `sources.yml` declarando as 9 tabelas bronze;
- `profiles.yml` local funcional;
- comandos `dbt debug`, `dbt parse` e `dbt ls` executando com sucesso.

## 3. Arquivos criados

| Arquivo | Status |
|---|---|
| `dbt/dbt_project.yml` | Criado |
| `dbt/README.md` | Criado |
| `dbt/models/sources/sources.yml` | Criado |
| `dbt/models/silver/schema.yml` | Criado |
| `dbt/models/gold/schema.yml` | Criado |
| `dbt/macros/.gitkeep` | Criado |
| `dbt/seeds/.gitkeep` | Criado |
| `dbt/snapshots/.gitkeep` | Criado |
| `dbt/tests/.gitkeep` | Criado |
| `sdd/planos/003_configuracao_dbt.md` | Criado |
| `sdd/tarefas/003_configuracao_dbt.md` | Criado |

## 4. Arquivos alterados

| Arquivo | Alteração |
|---|---|
| `requirements.txt` | Adicionado `dbt-postgres` |
| `.gitignore` | Adicionado `profiles.yml` e `dbt/profiles.yml` |

## 5. Arquivo criado localmente (não versionado)

| Arquivo | Status |
|---|---|
| `~/.dbt/profiles.yml` | Criado localmente, não versionado |

## 6. Resultado do dbt debug

Executado na pasta `dbt/`.

```
16:55:31  Running with dbt=1.12.0-b1
16:55:31  dbt version: 1.12.0-b1
16:55:31  python version: 3.11.3
16:55:31  Using profiles dir at C:\Users\Diego\.dbt
16:55:31  Using profiles.yml file at C:\Users\Diego\.dbt\profiles.yml
16:55:31  Using dbt_project.yml file at dbt\dbt_project.yml
16:55:31  adapter type: postgres
16:55:31  adapter version: 1.10.0
16:55:31  Configuration:
16:55:31    profiles.yml file [OK found and valid]
16:55:31    dbt_project.yml file [OK found and valid]
16:55:31  Required dependencies:
16:55:31   - git [OK found]
16:55:31  Connection:
16:55:31    host: localhost
16:55:31    port: 5432
16:55:31    user: ecommerce_user
16:55:31    database: ecommerce_dw
16:55:31    schema: silver
16:55:35    Connection test: [OK connection ok]
16:55:35  All checks passed!
```

**Resultado: sucesso.**

## 7. Resultado do dbt parse

Executado na pasta `dbt/`.

```
16:57:10  Running with dbt=1.12.0-b1
16:57:11  Unable to do partial parsing because saved manifest not found. Starting full parse.
16:57:14  [WARNING]: Configuration paths exist in your dbt_project.yml file which do not apply to any resources.
There are 2 unused configuration paths:
- models.engenharia_de_dados_com_dbt_sdd.gold
- models.engenharia_de_dados_com_dbt_sdd.silver
16:57:14  Performance info: target/perf_info.json
```

**Resultado: sucesso sem erros.**

Os avisos sobre `unused configuration paths` para silver e gold são esperados, pois ainda não existem modelos SQL nessas camadas. As configurações estão corretas e serão utilizadas quando os modelos forem criados.

## 8. Resultado do dbt ls

Executado na pasta `dbt/`.

```
17:00:22  Running with dbt=1.12.0-b1
17:00:22  Found 9 sources, 475 macros
source:engenharia_de_dados_com_dbt_sdd.olist_bronze.olist_customers_dataset
source:engenharia_de_dados_com_dbt_sdd.olist_bronze.olist_geolocation_dataset
source:engenharia_de_dados_com_dbt_sdd.olist_bronze.olist_order_items_dataset
source:engenharia_de_dados_com_dbt_sdd.olist_bronze.olist_order_payments_dataset
source:engenharia_de_dados_com_dbt_sdd.olist_bronze.olist_order_reviews_dataset
source:engenharia_de_dados_com_dbt_sdd.olist_bronze.olist_orders_dataset
source:engenharia_de_dados_com_dbt_sdd.olist_bronze.olist_products_dataset
source:engenharia_de_dados_com_dbt_sdd.olist_bronze.olist_sellers_dataset
source:engenharia_de_dados_com_dbt_sdd.olist_bronze.product_category_name_translation
```

**Resultado: 9 sources listados corretamente.**

## 9. Versões utilizadas

| Componente | Versão |
|---|---|
| dbt-core | 1.12.0-b1 |
| dbt-postgres | 1.10.0 |
| Python | 3.11.3 |
| PostgreSQL | (via Docker local) |

## 10. Observações

- Os avisos de `unused configuration paths` são esperados e serão resolvidos automaticamente quando os primeiros modelos silver e gold forem criados.
- O `profiles.yml` foi criado em `~/.dbt/profiles.yml` e não foi versionado no repositório.
- O `.gitignore` foi atualizado para proteger o `profiles.yml` caso seja criado dentro da pasta `dbt/`.
- A pasta `~/.dbt/` não existia antes desta etapa e foi criada durante a configuração.

## 11. Pendências conhecidas

- Nenhuma pendência para esta etapa de configuração.
- Próxima etapa: planejamento e implementação dos modelos da camada silver.

## 12. Conclusão

A configuração inicial do projeto dbt foi concluída com sucesso.

O projeto dbt está conectado ao PostgreSQL local, reconhece os 9 sources da camada bronze e está pronto para receber os modelos das camadas silver e gold.

Todos os critérios de aceite definidos em `sdd/planos/003_configuracao_dbt.md` foram atendidos.
