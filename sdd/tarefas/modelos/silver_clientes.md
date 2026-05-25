# Tarefas — silver_clientes

Referência: `sdd/especificacoes/modelos/silver_clientes.md`
Plano: `sdd/planos/modelos/silver_clientes.md`

## Tarefas

- [x] Criar especificação do modelo (`sdd/especificacoes/modelos/silver_clientes.md`)
- [x] Criar plano técnico (`sdd/planos/modelos/silver_clientes.md`)
- [x] Atualizar `dbt/models/sources/sources.yml` — renomear source de `olist_bronze` para `bronze`
- [x] Criar modelo SQL (`dbt/models/silver/silver_clientes.sql`)
- [x] Documentar modelo e colunas em `dbt/models/silver/schema.yml`
- [x] Executar `dbt run --select silver_clientes`
- [x] Executar `dbt test --select silver_clientes`
- [x] Executar `dbt docs generate`
- [x] Registrar validação em `sdd/validacoes/003_silver_clientes.md`
