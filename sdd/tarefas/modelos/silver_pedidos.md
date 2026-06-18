# Tarefas: silver_pedidos

## Modelo

`silver_pedidos`

## Camada

Silver

## Referências

- Especificação: `sdd/especificacoes/modelos/silver_pedidos.md`
- Plano: `sdd/planos/modelos/silver_pedidos.md`

---

## Checklist

### Documentação SDD

- [x] Criar especificação do modelo (`sdd/especificacoes/modelos/silver_pedidos.md`)
- [x] Criar plano de implementação (`sdd/planos/modelos/silver_pedidos.md`)
- [x] Criar lista de tarefas (`sdd/tarefas/modelos/silver_pedidos.md`)

### Implementação dbt

- [ ] Criar o modelo SQL (`dbt/models/silver/silver_pedidos.sql`)
- [ ] Configurar testes no `schema.yml` (`dbt/models/silver/schema.yml`)

### Execução e validação

- [ ] Executar `dbt run --select silver_pedidos`
- [ ] Executar `dbt test --select silver_pedidos`
- [ ] Gerar documentação com `dbt docs generate`

### Fechamento SDD

- [ ] Criar arquivo de validação (`sdd/validacoes/modelos/silver_pedidos.md`)
- [ ] Revisar `git diff` antes do commit
- [ ] Commitar as alterações
