# Validação 001 — Configuração Inicial do Projeto

## 1. Objetivo

Registrar a validação da configuração inicial do projeto, incluindo a execução do PostgreSQL via Docker Compose e a criação dos schemas principais utilizados pela arquitetura do projeto.

## 2. Plano relacionado

- `sdd/planos/001_configuracao_inicial.md`

## 3. Tarefas relacionadas

- `sdd/tarefas/001_configuracao_inicial.md`

## 4. Data da validação

Preencher manualmente com a data da execução.

Exemplo:

```text
2026-05-19
```

## 5. Ambiente

| Item | Valor |
|---|---|
| Sistema operacional | Windows |
| Banco de dados | PostgreSQL |
| Execução | Docker Compose |
| Container | `engenharia_dados_dbt_postgres` |
| Database | `ecommerce_dw` |
| Schemas esperados | `bronze`, `silver`, `gold` |

## 6. Comandos executados

### 6.1 Subida do PostgreSQL

```powershell
docker compose up -d
```

### 6.2 Verificação dos containers

```powershell
docker ps
```

### 6.3 Conexão no PostgreSQL

```powershell
docker exec -it engenharia_dados_dbt_postgres psql -U ecommerce_user -d ecommerce_dw
```

### 6.4 Criação dos schemas

```sql
create schema if not exists bronze;
create schema if not exists silver;
create schema if not exists gold;
```

### 6.5 Validação dos schemas

```sql
select schema_name
from information_schema.schemata
where schema_name in ('bronze', 'silver', 'gold')
order by schema_name;
```

## 7. Resultado esperado

A consulta de validação deve retornar os três schemas:

```text
bronze
gold
silver
```

## 8. Resultado obtido

Preencher após execução.

```text
<colar_resultado_aqui>
```

## 9. Critérios de aceite

- [ ] O PostgreSQL subiu com sucesso via Docker Compose.
- [ ] O container `engenharia_dados_dbt_postgres` ficou em execução.
- [ ] Foi possível conectar no banco `ecommerce_dw`.
- [ ] O schema `bronze` foi criado.
- [ ] O schema `silver` foi criado.
- [ ] O schema `gold` foi criado.
- [ ] A consulta em `information_schema.schemata` retornou os três schemas esperados.
- [ ] A configuração inicial está pronta para a etapa de ingestão.

## 10. Pendências

- [ ] Baixar a base pública da Olist.
- [ ] Configurar ingestão dos arquivos para o schema `bronze`.
- [ ] Configurar o projeto dbt.
- [ ] Criar `sources.yml` apontando para as tabelas bronze.

## 11. Conclusão

A configuração inicial será considerada validada quando o PostgreSQL estiver em execução e os schemas `bronze`, `silver` e `gold` existirem no banco `ecommerce_dw`.
