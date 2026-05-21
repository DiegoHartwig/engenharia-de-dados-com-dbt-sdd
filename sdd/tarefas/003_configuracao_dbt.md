# Tarefas 003 — Configuração Inicial do dbt

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome | Configuração inicial do projeto dbt |
| Tipo | Configuração |
| Plano relacionado | `sdd/planos/003_configuracao_dbt.md` |
| ADR relacionada | `sdd/decisoes/ADR-001-uso-da-bronze-como-landing-zone.md` |
| Status | Em andamento |
| Responsável | Diego Hartwig |

## 2. Objetivo

Organizar as tarefas necessárias para configurar a estrutura inicial do projeto dbt, preparando o ambiente para as futuras implementações das camadas `silver` e `gold`.

## 3. Pré-requisitos

Antes de iniciar esta lista de tarefas, verificar:

- [ ] O PostgreSQL está em execução via Docker Compose.
- [ ] O banco `ecommerce_dw` está acessível.
- [ ] O schema `bronze` existe com as 9 tabelas da Olist carregadas.
- [ ] A ingestão bronze foi validada (`sdd/validacoes/002_ingestao_bronze.md` existe).
- [ ] O Python está instalado no ambiente.
- [ ] O `requirements.txt` está atualizado.

## 4. Tarefas de documentação SDD

- [ ] Criar `sdd/planos/003_configuracao_dbt.md`.
- [ ] Criar `sdd/tarefas/003_configuracao_dbt.md`.

## 5. Tarefas de estrutura de diretórios

Criar dentro da pasta `dbt/`:

```text
dbt/
├── dbt_project.yml
├── README.md
├── models/
│   ├── sources/
│   │   └── sources.yml
│   ├── silver/
│   │   └── schema.yml
│   └── gold/
│       └── schema.yml
├── macros/
├── seeds/
├── snapshots/
└── tests/
```

Tarefas:

- [ ] Confirmar que a pasta `dbt/` existe.
- [ ] Criar pasta `dbt/models/`.
- [ ] Criar pasta `dbt/models/sources/`.
- [ ] Criar pasta `dbt/models/silver/`.
- [ ] Criar pasta `dbt/models/gold/`.
- [ ] Criar pasta `dbt/macros/`.
- [ ] Criar pasta `dbt/seeds/`.
- [ ] Criar pasta `dbt/snapshots/`.
- [ ] Criar pasta `dbt/tests/`.

## 6. Tarefas de criação do dbt_project.yml

Configurações esperadas:

- Nome do projeto: `engenharia_de_dados_com_dbt_sdd`
- Profile: `engenharia_de_dados_com_dbt_sdd`
- `model-paths`
- `test-paths`
- `seed-paths`
- `macro-paths`
- `snapshot-paths`
- `clean-targets`
- models silver com schema `silver` e materialização `view`
- models gold com schema `gold` e materialização `table`

Tarefas:

- [ ] Criar `dbt/dbt_project.yml`.
- [ ] Configurar nome do projeto.
- [ ] Configurar profile.
- [ ] Configurar paths dos artefatos.
- [ ] Configurar clean-targets.
- [ ] Configurar schemas e materializações das camadas.

## 7. Tarefas de criação do sources.yml

Tabelas a declarar no schema `bronze`:

```text
olist_customers_dataset
olist_geolocation_dataset
olist_order_items_dataset
olist_order_payments_dataset
olist_order_reviews_dataset
olist_orders_dataset
olist_products_dataset
olist_sellers_dataset
product_category_name_translation
```

Tarefas:

- [ ] Criar `dbt/models/sources/sources.yml`.
- [ ] Declarar source `olist_bronze` apontando para o schema `bronze`.
- [ ] Declarar `olist_customers_dataset` com descrição.
- [ ] Declarar `olist_geolocation_dataset` com descrição.
- [ ] Declarar `olist_order_items_dataset` com descrição.
- [ ] Declarar `olist_order_payments_dataset` com descrição.
- [ ] Declarar `olist_order_reviews_dataset` com descrição.
- [ ] Declarar `olist_orders_dataset` com descrição.
- [ ] Declarar `olist_products_dataset` com descrição.
- [ ] Declarar `olist_sellers_dataset` com descrição.
- [ ] Declarar `product_category_name_translation` com descrição.

## 8. Tarefas de criação dos schema.yml das camadas

- [ ] Criar `dbt/models/silver/schema.yml` com cabeçalho mínimo.
- [ ] Criar `dbt/models/gold/schema.yml` com cabeçalho mínimo.

## 9. Tarefas de atualização do requirements.txt

- [ ] Abrir `requirements.txt`.
- [ ] Adicionar `dbt-postgres` ao arquivo.
- [ ] Instalar dependências com `pip install -r requirements.txt`.
- [ ] Confirmar que o dbt está acessível com `dbt --version`.

## 10. Tarefas de configuração do profile local

O arquivo `profiles.yml` não deve ser versionado no repositório.

Ele deve ser criado manualmente em `~/.dbt/profiles.yml` ou na pasta `dbt/` (sem versionar).

Conteúdo esperado do profile:

```yaml
engenharia_de_dados_com_dbt_sdd:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: ecommerce_user
      password: ecommerce_password
      port: 5432
      dbname: ecommerce_dw
      schema: silver
      threads: 4
```

Tarefas:

- [ ] Criar `profiles.yml` localmente em `~/.dbt/profiles.yml`.
- [ ] Confirmar que `profiles.yml` não está versionado no Git.
- [ ] Documentar exemplo de profile no `dbt/README.md`.

## 11. Tarefas de validação do dbt

Executar dentro da pasta `dbt/`:

```powershell
cd dbt
dbt debug
dbt parse
dbt ls
```

Tarefas:

- [ ] Executar `dbt debug` e confirmar que a conexão funciona.
- [ ] Executar `dbt parse` e confirmar que não há erros.
- [ ] Executar `dbt ls` e confirmar que os sources aparecem na listagem.
- [ ] Registrar saída dos comandos na validação.

## 12. Tarefas de criação do dbt/README.md

O README deve conter:

- objetivo da pasta `dbt/`;
- estrutura de diretórios;
- instruções de configuração do `profiles.yml`;
- exemplo de profile com valores fictícios;
- comandos úteis do dbt.

Tarefas:

- [ ] Criar `dbt/README.md`.
- [ ] Documentar objetivo da configuração dbt.
- [ ] Documentar estrutura de diretórios.
- [ ] Documentar criação do `profiles.yml` com valores de exemplo.
- [ ] Documentar comandos úteis.

## 13. Tarefas de versionamento

- [ ] Executar `git status`.
- [ ] Confirmar que `profiles.yml` não aparece no Git.
- [ ] Versionar os arquivos criados.
- [ ] Fazer commit da configuração inicial do dbt.

Arquivos a versionar:

```text
dbt/dbt_project.yml
dbt/README.md
dbt/models/sources/sources.yml
dbt/models/silver/schema.yml
dbt/models/gold/schema.yml
requirements.txt
sdd/planos/003_configuracao_dbt.md
sdd/tarefas/003_configuracao_dbt.md
```

## 14. Tarefas de registro de validação

- [ ] Criar `sdd/validacoes/003_configuracao_dbt.md`.
- [ ] Registrar data da execução.
- [ ] Registrar resultado do `dbt debug`.
- [ ] Registrar resultado do `dbt parse`.
- [ ] Registrar resultado do `dbt ls`.
- [ ] Registrar arquivos criados.
- [ ] Registrar pendências conhecidas.
- [ ] Registrar conclusão da etapa.

## 15. Critérios de conclusão

Esta lista de tarefas será considerada concluída quando:

- [ ] a estrutura de diretórios `dbt/` existir completa;
- [ ] o `dbt_project.yml` estiver configurado corretamente;
- [ ] o `sources.yml` declarar as 9 tabelas bronze;
- [ ] o `requirements.txt` incluir `dbt-postgres`;
- [ ] o `dbt debug` executar com sucesso;
- [ ] o `dbt parse` executar sem erros;
- [ ] o `dbt ls` listar os sources;
- [ ] o `profiles.yml` não estiver versionado;
- [ ] a validação `sdd/validacoes/003_configuracao_dbt.md` existir;
- [ ] as alterações estiverem versionadas no Git.

## 16. Pendências

- [ ] Instalar `dbt-postgres` e verificar compatibilidade com o ambiente.
- [ ] Iniciar planejamento dos modelos silver após conclusão desta etapa.

## 17. Observações

A configuração inicial do dbt é uma etapa de preparação do ambiente.

Nenhum modelo SQL será criado nesta etapa.

A declaração dos sources é o primeiro artefato dbt formal do projeto e estabelece o contrato entre a camada bronze e as transformações futuras.

Os modelos silver e gold serão planejados e implementados em planos subsequentes, seguindo o fluxo SDD.
