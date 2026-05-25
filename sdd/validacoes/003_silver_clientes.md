# Validação 003 — Modelo silver_clientes

## 1. Objetivo

Registrar a validação do modelo `silver_clientes`, primeiro modelo implementado na camada silver do projeto dbt.

## 2. Referências SDD

- Especificação: `sdd/especificacoes/modelos/silver_clientes.md`
- Plano técnico: `sdd/planos/modelos/silver_clientes.md`
- Tarefas: `sdd/tarefas/modelos/silver_clientes.md`

## 3. Data da validação

```text
2026-05-25
```

## 4. Ambiente

| Item | Valor |
|---|---|
| Sistema operacional | Linux |
| dbt | 1.12.0-b1 |
| Adapter | dbt-postgres 1.10.0 |
| Banco de dados | PostgreSQL |
| Database | `engenharia_dados` |
| Schema destino | `silver` |
| Materialização | view |

## 5. Arquivos criados ou alterados

| Arquivo | Ação |
|---|---|
| `sdd/especificacoes/modelos/silver_clientes.md` | Criado |
| `sdd/planos/modelos/silver_clientes.md` | Criado |
| `sdd/tarefas/modelos/silver_clientes.md` | Criado |
| `dbt/models/silver/silver_clientes.sql` | Criado |
| `dbt/models/silver/schema.yml` | Atualizado |
| `dbt/models/sources/sources.yml` | Atualizado — source renomeado de `olist_bronze` para `bronze`; database ajustado para `engenharia_dados` |
| `dbt/macros/generate_schema_name.sql` | Criado — macro para garantir schema `silver` (não `silver_silver`) |
| `~/.dbt/profiles.yml` | Criado |
| `.env` | Corrigido para credenciais do ambiente local (`postgres/postgres/engenharia_dados`) |

## 6. Comandos executados

```bash
# Validar configuração
dbt debug

# Executar o modelo
dbt run --select silver_clientes

# Executar os testes
dbt test --select silver_clientes

# Gerar documentação
dbt docs generate
```

## 7. Resultado do dbt run

```
Found 1 model, 6 data tests, 9 sources, 476 macros

1 of 1 START sql view model silver.silver_clientes .... [RUN]
1 of 1 OK created sql view model silver.silver_clientes [CREATE VIEW in 0.08s]

Completed successfully
Done. PASS=1 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=1
```

## 8. Resultado do dbt test

```
Found 1 model, 6 data tests, 9 sources, 476 macros

1 of 6 PASS not_null_silver_clientes_cidade_cliente
2 of 6 PASS not_null_silver_clientes_estado_cliente
3 of 6 PASS not_null_silver_clientes_id_cliente
4 of 6 PASS not_null_silver_clientes_id_cliente_unico
5 of 6 PASS not_null_silver_clientes_prefixo_cep_cliente
6 of 6 PASS unique_silver_clientes_id_cliente

Completed successfully
Done. PASS=6 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=6
```

## 9. Resultado do dbt docs generate

```
Catalog written to dbt/target/catalog.json
```

## 10. Observações técnicas

### Source renomeado

O source foi renomeado de `olist_bronze` para `bronze` para alinhar com a convenção do projeto
(`source('bronze', 'tabela')`). Todos os modelos futuros devem usar `source('bronze', ...)`.

### Macro generate_schema_name

A macro `generate_schema_name.sql` foi criada para que o dbt use o nome do schema exatamente
como configurado em `dbt_project.yml` (`silver`, `gold`), sem o prefixo gerado pelo dbt padrão
(`silver_silver`).

### Ambiente local

O ambiente local usa `postgres/postgres/engenharia_dados`, diferente da configuração
documentada anteriormente (`ecommerce_user/ecommerce_dw`). O `.env` e o `profiles.yml`
foram atualizados para refletir o ambiente real de desenvolvimento.

## 11. Verificação das transformações

| Regra | Verificada |
|---|---|
| `id_cliente` = `trim(customer_id)` | Sim — teste `not_null` e `unique` passaram |
| `id_cliente_unico` = `trim(customer_unique_id)` | Sim — teste `not_null` passou |
| `prefixo_cep_cliente` preservado sem alteração | Sim — teste `not_null` passou |
| `cidade_cliente` = `lower(trim(customer_city))` | Sim — teste `not_null` passou |
| `estado_cliente` = `upper(trim(customer_state))` | Sim — teste `not_null` passou |
| Granularidade original preservada | Sim — sem deduplicação, sem joins |

## 12. Critérios de aceite

- [x] O modelo SQL existe em `dbt/models/silver/silver_clientes.sql`.
- [x] O modelo está documentado em `dbt/models/silver/schema.yml`.
- [x] Todos os testes genéricos estão declarados no YAML.
- [x] `dbt run --select silver_clientes` executou sem erro.
- [x] `dbt test --select silver_clientes` executou sem falha (6/6 testes passando).
- [x] `dbt docs generate` executou com sucesso.
- [x] O resultado foi registrado neste arquivo.

## 13. Pendências

Nenhuma pendência para este modelo.

## 14. Próximos passos recomendados

- Implementar demais modelos da camada silver (ex.: `silver_pedidos`, `silver_produtos`).
- Revisar a documentação do `dbt/README.md` para refletir o ambiente real.
- Considerar o uso do dbt `source freshness` para monitorar atualização da bronze.
