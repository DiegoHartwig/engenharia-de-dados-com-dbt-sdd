# Plano Técnico 003 — Configuração Inicial do dbt

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome do plano | Configuração inicial do projeto dbt |
| Tipo | Configuração |
| Relacionado à spec | `sdd/constituicao.md` |
| ADR relacionada | `sdd/decisoes/ADR-001-uso-da-bronze-como-landing-zone.md` |
| Status | Em execução |
| Responsável | Diego Hartwig |

## 2. Objetivo do plano

Este plano define como será realizada a configuração inicial do projeto dbt dentro da pasta `dbt/`, preparando a estrutura para as futuras implementações das camadas `silver` e `gold`.

O objetivo desta etapa é:

- criar a estrutura de diretórios padrão do dbt;
- configurar o arquivo `dbt_project.yml` com as camadas, schemas e materializações;
- declarar as tabelas bronze da Olist como sources no arquivo `sources.yml`;
- atualizar o `requirements.txt` com a dependência `dbt-postgres`;
- documentar o perfil local necessário no `dbt/README.md`;
- validar a configuração com `dbt debug`, `dbt parse` e `dbt ls`.

A configuração do dbt não inclui modelos SQL nesta etapa. Modelos silver e gold serão criados em planos subsequentes.

## 3. Escopo

Este plano cobre:

- criação da pasta `dbt/` com estrutura padrão;
- criação do arquivo `dbt/dbt_project.yml`;
- criação do arquivo `dbt/README.md`;
- criação do arquivo `dbt/models/sources/sources.yml` com as 9 tabelas bronze da Olist;
- criação de `schema.yml` vazio em `dbt/models/silver/` e `dbt/models/gold/`;
- criação das pastas `macros/`, `seeds/`, `snapshots/` e `tests/` dentro de `dbt/`;
- atualização do `requirements.txt` com `dbt-postgres`;
- orientação sobre criação local do `profiles.yml`;
- execução de `dbt debug`, `dbt parse` e `dbt ls`;
- registro desta validação em `sdd/validacoes/003_configuracao_dbt.md`.

## 4. Fora de escopo

Este plano não cobre:

- criação de modelos SQL silver ou gold;
- criação de testes dbt avançados;
- criação de macros;
- criação de seeds;
- criação de snapshots;
- criação de modelos incrementais;
- configuração de CI/CD;
- dashboards;
- Airflow, Spark, Trino ou Databricks;
- alteração na ingestão bronze;
- alteração no script Python de ingestão.

## 5. Dependências

| Tipo | Nome | Descrição |
|---|---|---|
| Banco | PostgreSQL | Banco local executando via Docker Compose |
| Schema | `bronze` | Schema com as tabelas da Olist já carregadas |
| Arquivo | `profiles.yml` | Perfil local do dbt (não versionado) |
| Pacote | `dbt-postgres` | Adaptador dbt para PostgreSQL |
| Ingestão | `ingestao/carregar_bronze_olist.py` | Script Python que carregou as tabelas bronze |

## 6. Arquivos que serão criados ou alterados

| Arquivo | Ação | Descrição |
|---|---|---|
| `dbt/dbt_project.yml` | criar | Configuração principal do projeto dbt |
| `dbt/README.md` | criar | Documentação da pasta dbt, incluindo instrução de `profiles.yml` |
| `dbt/models/sources/sources.yml` | criar | Declaração das 9 tabelas bronze da Olist como sources |
| `dbt/models/silver/schema.yml` | criar | Placeholder para documentação futura da camada silver |
| `dbt/models/gold/schema.yml` | criar | Placeholder para documentação futura da camada gold |
| `dbt/macros/.gitkeep` | criar | Manter a pasta macros no versionamento |
| `dbt/seeds/.gitkeep` | criar | Manter a pasta seeds no versionamento |
| `dbt/snapshots/.gitkeep` | criar | Manter a pasta snapshots no versionamento |
| `dbt/tests/.gitkeep` | criar | Manter a pasta tests no versionamento |
| `requirements.txt` | alterar | Adicionar dependência `dbt-postgres` |

## 7. Estrutura esperada após o plano

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

## 8. Configuração esperada do projeto dbt

### 8.1 Identificação do projeto

| Item | Valor |
|---|---|
| Nome do projeto | `engenharia_de_dados_com_dbt_sdd` |
| Profile | `engenharia_de_dados_com_dbt_sdd` |
| Banco | PostgreSQL |
| Database | `ecommerce_dw` |
| Source schema | `bronze` |
| Schema silver | `silver` |
| Schema gold | `gold` |

### 8.2 Materializações padrão

| Camada | Materialização |
|---|---|
| silver | `view` |
| gold | `table` |

As materializações poderão ser alteradas por modelo conforme a necessidade técnica de cada implementação futura.

### 8.3 Perfil local esperado

O arquivo `profiles.yml` deve ser criado manualmente pelo desenvolvedor em `~/.dbt/profiles.yml` ou na pasta `dbt/`.

O arquivo não deve ser versionado no repositório.

O conteúdo esperado está documentado no `dbt/README.md`.

## 9. Estratégia de materialização

| Item | Valor |
|---|---|
| Silver | `view` (padrão inicial, pode ser sobrescrito por modelo) |
| Gold | `table` (padrão inicial, pode ser sobrescrito por modelo) |
| Justificativa | Views para silver reduzem custo de armazenamento enquanto os modelos ainda estão sendo definidos. Tables para gold garantem desempenho no consumo analítico. |

## 10. Sources declarados

As seguintes tabelas bronze serão declaradas como sources no `sources.yml`:

```text
bronze.olist_customers_dataset
bronze.olist_geolocation_dataset
bronze.olist_order_items_dataset
bronze.olist_order_payments_dataset
bronze.olist_order_reviews_dataset
bronze.olist_orders_dataset
bronze.olist_products_dataset
bronze.olist_sellers_dataset
bronze.product_category_name_translation
```

## 11. Critérios de aceite

Esta configuração será considerada concluída quando:

- [ ] a estrutura de diretórios `dbt/` existir com todas as pastas esperadas;
- [ ] o arquivo `dbt_project.yml` estiver criado e correto;
- [ ] o arquivo `sources.yml` declarar as 9 tabelas bronze;
- [ ] o `requirements.txt` incluir `dbt-postgres`;
- [ ] o `dbt/README.md` documentar o `profiles.yml`;
- [ ] o comando `dbt debug` executar com sucesso;
- [ ] o comando `dbt parse` executar sem erros;
- [ ] o comando `dbt ls` listar os sources declarados;
- [ ] a validação for registrada em `sdd/validacoes/003_configuracao_dbt.md`.

## 12. Riscos e cuidados

- Não versionar o arquivo `profiles.yml` com credenciais reais.
- Verificar se a versão de `dbt-postgres` é compatível com a versão do PostgreSQL.
- Confirmar que o schema `bronze` existe no PostgreSQL antes de executar `dbt debug`.
- Não criar modelos SQL nesta etapa para não antecipar decisões de implementação das camadas silver e gold.

## 13. Pendências

- [ ] Criar estrutura de diretórios `dbt/`.
- [ ] Criar `dbt/dbt_project.yml`.
- [ ] Criar `dbt/models/sources/sources.yml`.
- [ ] Criar `dbt/README.md`.
- [ ] Atualizar `requirements.txt`.
- [ ] Instalar dependências.
- [ ] Criar `profiles.yml` local.
- [ ] Executar `dbt debug`.
- [ ] Executar `dbt parse`.
- [ ] Executar `dbt ls`.
- [ ] Registrar validação em `sdd/validacoes/003_configuracao_dbt.md`.

## 14. Observações

A configuração do dbt é uma etapa de preparação do ambiente.

O objetivo não é demonstrar transformações nesta etapa, mas criar uma base organizada para que os modelos silver e gold possam ser desenvolvidos de forma rastreável e seguindo as especificações do SDD.

A declaração dos sources é o primeiro artefato dbt formal do projeto, pois estabelece o contrato entre a camada bronze (ingestão Python) e as transformações futuras (dbt).
