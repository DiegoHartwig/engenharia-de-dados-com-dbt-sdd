# Tarefas 001 — Configuração Inicial do Projeto

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome | Configuração inicial do projeto |
| Tipo | Configuração |
| Spec relacionada | `sdd/especificacoes/000_visao_geral.md` |
| Plano relacionado | `sdd/planos/001_configuracao_inicial.md` |
| Status | Em andamento |
| Responsável | Diego Hartwig |

## 2. Objetivo

Organizar as tarefas necessárias para preparar o ambiente inicial do projeto, incluindo estrutura do repositório, arquivos de configuração, PostgreSQL via Docker, schemas principais e preparação para ingestão da base Olist na camada bronze.

## 3. Pré-requisitos

Antes de iniciar esta lista de tarefas, verificar:

- [ ] O repositório GitHub foi criado.
- [ ] O repositório local está clonado ou inicializado.
- [ ] O Git está configurado no ambiente local.
- [ ] O Docker Desktop está instalado.
- [ ] O Docker Desktop está em execução.
- [ ] O VS Code ou editor equivalente está disponível.
- [ ] O terminal PowerShell está disponível.
- [ ] A constituição do projeto foi criada.
- [ ] O fluxo SDD foi criado.
- [ ] As ADRs iniciais foram criadas.
- [ ] As especificações gerais iniciais foram criadas.

## 4. Tarefas de estrutura do repositório

- [ ] Confirmar existência da pasta `dados/`.
- [ ] Confirmar existência da pasta `dados/brutos/`.
- [ ] Confirmar existência da pasta `dbt/`.
- [ ] Confirmar existência da pasta `documentacao/`.
- [ ] Confirmar existência da pasta `sdd/`.
- [ ] Confirmar existência da pasta `sdd/decisoes/`.
- [ ] Confirmar existência da pasta `sdd/especificacoes/`.
- [ ] Confirmar existência da pasta `sdd/especificacoes/modelos/`.
- [ ] Confirmar existência da pasta `sdd/planos/`.
- [ ] Confirmar existência da pasta `sdd/planos/modelos/`.
- [ ] Confirmar existência da pasta `sdd/tarefas/`.
- [ ] Confirmar existência da pasta `sdd/tarefas/modelos/`.
- [ ] Confirmar existência da pasta `sdd/templates/`.
- [ ] Confirmar existência da pasta `sdd/validacoes/`.
- [ ] Remover pasta `especificacoes/` da raiz, caso exista e esteja vazia.
- [ ] Confirmar que as especificações estão centralizadas dentro de `sdd/especificacoes/`.

## 5. Tarefas de documentação SDD

- [ ] Confirmar existência de `sdd/constituicao.md`.
- [ ] Confirmar existência de `sdd/fluxo_sdd.md`.
- [ ] Confirmar existência de `sdd/decisoes/ADR-001-uso-da-bronze-como-landing-zone.md`.
- [ ] Confirmar existência de `sdd/decisoes/ADR-002-uso-de-portugues-no-projeto.md`.
- [ ] Confirmar existência de `sdd/decisoes/ADR-003-uso-de-sdd-adaptado-para-dbt.md`.
- [ ] Confirmar existência de `sdd/templates/template_spec_modelo.md`.
- [ ] Confirmar existência de `sdd/templates/template_plano.md`.
- [ ] Confirmar existência de `sdd/templates/template_tarefas.md`.
- [ ] Confirmar existência de `sdd/especificacoes/000_visao_geral.md`.
- [ ] Confirmar existência de `sdd/especificacoes/001_arquitetura.md`.
- [ ] Confirmar existência de `sdd/especificacoes/002_estrategia_de_camadas.md`.
- [ ] Confirmar existência de `sdd/especificacoes/003_estrategia_de_testes_dbt.md`.
- [ ] Confirmar existência de `sdd/especificacoes/004_estrategia_incremental.md`.
- [ ] Confirmar existência de `sdd/especificacoes/005_convencoes_dbt.md`.
- [ ] Confirmar existência de `sdd/planos/001_configuracao_inicial.md`.

## 6. Tarefas de arquivos de configuração

- [ ] Criar ou revisar `.gitignore`.
- [ ] Garantir que `.env` está ignorado pelo Git.
- [ ] Garantir que arquivos CSV em `dados/brutos/` estão ignorados pelo Git.
- [ ] Garantir que arquivos ZIP em `dados/brutos/` estão ignorados pelo Git.
- [ ] Criar ou revisar `.env.example`.
- [ ] Criar ou revisar `docker-compose.yml`.
- [ ] Revisar `README.md` para refletir a arquitetura `bronze → silver → gold`.

## 7. Tarefas do `.gitignore`

O arquivo `.gitignore` deve conter pelo menos:

```text
.env
.venv/
venv/
__pycache__/
*.pyc
dados/brutos/*.csv
dados/brutos/*.zip
dbt/target/
dbt/dbt_packages/
dbt/logs/
.DS_Store
Thumbs.db
.vscode/
.idea/
```

Tarefas:

- [ ] Verificar se `.env` está no `.gitignore`.
- [ ] Verificar se `dados/brutos/*.csv` está no `.gitignore`.
- [ ] Verificar se `dados/brutos/*.zip` está no `.gitignore`.
- [ ] Verificar se pastas temporárias do dbt estão no `.gitignore`.
- [ ] Verificar se pastas de ambiente Python estão no `.gitignore`.

## 8. Tarefas do `.env.example`

O arquivo `.env.example` deve conter variáveis de exemplo para o PostgreSQL.

Exemplo:

```env
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=ecommerce_password
POSTGRES_DB=ecommerce_dw
POSTGRES_PORT=5432
```

Tarefas:

- [ ] Criar ou revisar `.env.example`.
- [ ] Garantir que não existam senhas reais no arquivo.
- [ ] Garantir que o arquivo esteja versionado no Git.
- [ ] Criar `.env` local, se necessário.
- [ ] Garantir que `.env` não esteja versionado.

## 9. Tarefas do Docker Compose

O arquivo `docker-compose.yml` deve subir um PostgreSQL local.

Configurações esperadas:

- container: `engenharia_dados_dbt_postgres`;
- imagem: `postgres:16`;
- banco: `ecommerce_dw`;
- usuário: `ecommerce_user`;
- porta: `5432`;
- volume persistente para dados do PostgreSQL.

Tarefas:

- [ ] Criar ou revisar serviço `postgres`.
- [ ] Configurar variáveis de ambiente do PostgreSQL.
- [ ] Configurar porta `5432`.
- [ ] Configurar volume persistente.
- [ ] Configurar healthcheck do PostgreSQL.
- [ ] Validar sintaxe do `docker-compose.yml`.

## 10. Tarefas de execução do PostgreSQL

Comandos previstos:

```powershell
docker compose up -d
```

```powershell
docker ps
```

Tarefas:

- [ ] Subir o PostgreSQL com Docker Compose.
- [ ] Verificar se o container está em execução.
- [ ] Verificar logs do container, se necessário.
- [ ] Confirmar que a porta `5432` está acessível.
- [ ] Validar se o volume foi criado.

## 11. Tarefas de conexão no PostgreSQL

Comando previsto:

```powershell
docker exec -it engenharia_dados_dbt_postgres psql -U ecommerce_user -d ecommerce_dw
```

Tarefas:

- [ ] Conectar no PostgreSQL via `psql` dentro do container.
- [ ] Confirmar acesso ao banco `ecommerce_dw`.
- [ ] Validar usuário `ecommerce_user`.
- [ ] Sair do `psql` com `\q`.

## 12. Tarefas de criação dos schemas

Dentro do PostgreSQL, executar:

```sql
create schema if not exists bronze;
create schema if not exists silver;
create schema if not exists gold;
```

Depois validar:

```sql
select schema_name
from information_schema.schemata
where schema_name in ('bronze', 'silver', 'gold')
order by schema_name;
```

Tarefas:

- [ ] Criar schema `bronze`.
- [ ] Criar schema `silver`.
- [ ] Criar schema `gold`.
- [ ] Validar existência dos três schemas.
- [ ] Registrar o resultado na validação da configuração inicial.

## 13. Tarefas dos dados Olist

A base pública da Olist deverá ser baixada e armazenada localmente.

Pasta esperada:

```text
dados/brutos/
```

Arquivos esperados:

```text
olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

Tarefas:

- [ ] Baixar a base pública da Olist.
- [ ] Extrair os arquivos, se necessário.
- [ ] Colocar os CSVs em `dados/brutos/`.
- [ ] Conferir se todos os arquivos esperados existem.
- [ ] Confirmar que os CSVs não aparecem no `git status`.
- [ ] Documentar no README como obter a base, se necessário.

## 14. Tarefas de preparação para Airbyte

A ingestão será feita em etapa posterior.

Tarefas preparatórias:

- [ ] Confirmar que o PostgreSQL está acessível para ferramentas externas.
- [ ] Identificar host de conexão adequado no Windows.
- [ ] Definir destino PostgreSQL no schema `bronze`.
- [ ] Confirmar nomes esperados das tabelas bronze.
- [ ] Garantir que nenhuma transformação analítica seja feita na ingestão.

## 15. Tarefas de preparação para dbt

A configuração do dbt será feita em etapa posterior.

Tarefas preparatórias:

- [ ] Confirmar existência da pasta `dbt/`.
- [ ] Definir que as sources apontarão para o schema `bronze`.
- [ ] Definir que modelos `silver` e `gold` serão criados pelo dbt.
- [ ] Confirmar convenções em `sdd/especificacoes/005_convencoes_dbt.md`.
- [ ] Confirmar estratégia de testes em `sdd/especificacoes/003_estrategia_de_testes_dbt.md`.
- [ ] Confirmar estratégia incremental em `sdd/especificacoes/004_estrategia_incremental.md`.

## 16. Tarefas de validação

Criar registro de validação em:

```text
sdd/validacoes/001_configuracao_inicial.md
```

A validação deve registrar:

- comandos executados;
- resultado do Docker Compose;
- status do container PostgreSQL;
- schemas criados;
- pendências encontradas.

Tarefas:

- [ ] Criar arquivo de validação.
- [ ] Registrar comandos executados.
- [ ] Registrar evidências textuais.
- [ ] Registrar pendências, se houver.
- [ ] Confirmar critérios de aceite do plano técnico.

## 17. Tarefas de versionamento

- [ ] Executar `git status`.
- [ ] Revisar arquivos alterados.
- [ ] Garantir que CSVs e `.env` não serão commitados.
- [ ] Fazer commit dos arquivos de documentação e configuração.
- [ ] Enviar alterações para o GitHub.

Commit sugerido para esta lista de tarefas:

```powershell
git add sdd/tarefas/001_configuracao_inicial.md
git commit -m "docs: adiciona tarefas da configuracao inicial"
git push
```

## 18. Critérios de conclusão

Esta lista de tarefas será considerada concluída quando:

- [ ] estrutura do repositório estiver organizada;
- [ ] documentação SDD inicial estiver criada;
- [ ] plano técnico inicial estiver criado;
- [ ] PostgreSQL estiver funcional via Docker Compose;
- [ ] schemas `bronze`, `silver` e `gold` existirem;
- [ ] pasta `dados/brutos/` estiver pronta;
- [ ] dataset Olist estiver disponível localmente;
- [ ] arquivos sensíveis e dados brutos estiverem ignorados pelo Git;
- [ ] validação inicial estiver registrada;
- [ ] alterações estiverem versionadas no GitHub.

## 19. Pendências

- [ ] Executar configuração do PostgreSQL.
- [ ] Baixar dataset Olist.
- [ ] Definir e executar ingestão com Airbyte.
- [ ] Criar projeto dbt.
- [ ] Configurar sources.

## 20. Observações

Esta lista de tarefas representa a transição da fase metodológica SDD para a fase prática do projeto.

O objetivo é manter o projeto organizado sem perder o foco principal: dbt, testes, modelos incrementais e desenvolvimento orientado por especificações.
