# Plano Técnico 002 — Ingestão da Camada Bronze

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome do plano | Ingestão da camada bronze |
| Tipo | Ingestão |
| Relacionado à spec | `sdd/especificacoes/001_arquitetura.md` |
| ADR relacionada | `sdd/decisoes/ADR-004-uso-de-ingestao-simples-via-python.md` |
| Status | Revisado |
| Responsável | Diego Hartwig |

## 2. Objetivo do plano

Este plano define como será realizada a ingestão dos arquivos públicos da Olist para o PostgreSQL, utilizando a camada `bronze` como ponto de entrada dos dados no projeto.

O objetivo é carregar os arquivos CSV no schema `bronze`, preservando os dados o mais próximo possível da origem, sem aplicar regras de negócio, deduplicações, enriquecimentos ou transformações analíticas.

## 3. Decisão de ingestão

A ingestão será feita por meio de um script Python simples e versionado no repositório.

A decisão foi registrada em:

```text
sdd/decisoes/ADR-004-uso-de-ingestao-simples-via-python.md
```

A arquitetura da ingestão será:

```text
CSV Olist
    ↓
Script Python de ingestão
    ↓
PostgreSQL - bronze
```

## 4. Escopo

Este plano cobre:

- organização dos arquivos CSV da Olist em `dados/brutos/`;
- validação da presença dos arquivos esperados;
- criação de script Python de ingestão;
- leitura dos arquivos CSV;
- criação das tabelas no schema `bronze`;
- carga dos dados no PostgreSQL;
- preservação da estrutura original dos dados;
- validação da carga no schema `bronze`;
- registro da validação da ingestão.

## 5. Fora de escopo

Este plano não cobre:

- criação de modelos dbt;
- criação de modelos silver;
- criação de modelos gold;
- testes dbt;
- modelos incrementais;
- dashboards;
- Airflow;
- Spark;
- Trino;
- IA;
- RAG;
- transformações analíticas durante a ingestão.

## 6. Dependências

| Tipo | Nome | Descrição |
|---|---|---|
| Banco | PostgreSQL | Banco local executando via Docker Compose |
| Schema | `bronze` | Schema de destino dos dados ingeridos |
| Dataset | Olist | Base pública brasileira de e-commerce |
| Linguagem | Python | Linguagem usada no script de ingestão |
| Biblioteca | pandas | Leitura dos arquivos CSV |
| Biblioteca | SQLAlchemy | Escrita dos dados no PostgreSQL |
| Biblioteca | psycopg2 | Driver de conexão com PostgreSQL |
| Pasta | `dados/brutos/` | Pasta local com os arquivos CSV da Olist |

## 7. Arquivos esperados da Olist

Os arquivos esperados em `dados/brutos/` são:

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

## 8. Estrutura proposta para ingestão

Criar uma pasta específica para scripts de ingestão:

```text
ingestao/
├── carregar_bronze_olist.py
└── README.md
```

O script principal será:

```text
ingestao/carregar_bronze_olist.py
```

## 9. Estratégia de nomes das tabelas bronze

As tabelas na camada `bronze` devem preservar nomes próximos aos arquivos originais.

Tabelas esperadas:

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

A regra será:

```text
nome_do_arquivo_csv_sem_extensao → nome_da_tabela_bronze
```

Exemplo:

```text
olist_orders_dataset.csv → bronze.olist_orders_dataset
```

## 10. Estratégia de leitura dos arquivos

O script deverá:

- localizar os arquivos em `dados/brutos/`;
- validar se todos os arquivos esperados existem;
- ler cada CSV com `pandas`;
- preservar os nomes originais das colunas;
- carregar cada arquivo para uma tabela no schema `bronze`;
- substituir a tabela em caso de nova execução;
- registrar logs simples no terminal.

## 11. Estratégia de escrita no PostgreSQL

A escrita será feita no PostgreSQL usando `pandas.to_sql()` com SQLAlchemy.

Na primeira fase, a estratégia será carga completa com substituição:

```text
if_exists='replace'
```

Essa decisão é aceitável porque:

- a base é pública e estática;
- a bronze representa aterrissagem inicial;
- o foco do projeto está nas transformações dbt;
- a carga precisa ser simples e reproduzível.

## 12. Estratégia de tipos

Na camada `bronze`, os tipos poderão ser inferidos automaticamente pelo pandas/SQLAlchemy.

Como a bronze deve preservar a origem, não é obrigatório corrigir tipos nesta etapa.

Ajustes de tipos serão feitos na camada `silver`.

Cuidados:

- campos de data podem entrar como texto;
- campos monetários podem entrar como texto ou numérico;
- campos de identificador devem preservar seu conteúdo original;
- valores nulos devem ser preservados.

## 13. Estratégia de configuração

O script deve ler as configurações de conexão a partir de variáveis de ambiente.

Variáveis esperadas:

```env
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=ecommerce_password
POSTGRES_DB=ecommerce_dw
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
```

O arquivo `.env` deve ser usado localmente e não deve ser versionado.

O arquivo `.env.example` deve ser versionado.

## 14. Estratégia de validação

Após a ingestão, devem ser validados:

- existência das tabelas no schema `bronze`;
- quantidade de tabelas carregadas;
- quantidade de registros por tabela;
- amostra de registros;
- preservação dos nomes principais das colunas;
- ausência de transformações analíticas;
- ausência de arquivos CSV versionados no Git.

Consultas sugeridas:

```sql
select table_schema, table_name
from information_schema.tables
where table_schema = 'bronze'
order by table_name;
```

```sql
select count(*) as total_registros
from bronze.olist_orders_dataset;
```

```sql
select *
from bronze.olist_orders_dataset
limit 10;
```

## 15. Critérios de aceite

Este plano será considerado concluído quando:

- [ ] os arquivos CSV da Olist estiverem em `dados/brutos/`;
- [ ] os arquivos CSV não estiverem versionados no Git;
- [ ] o PostgreSQL estiver em execução;
- [ ] o schema `bronze` existir;
- [ ] existir um script Python de ingestão;
- [ ] o script carregar os arquivos CSV para o schema `bronze`;
- [ ] as tabelas esperadas existirem no PostgreSQL;
- [ ] a contagem de registros for registrada;
- [ ] uma amostra dos dados for validada;
- [ ] nenhuma transformação analítica for aplicada na ingestão;
- [ ] a validação da ingestão for registrada em `sdd/validacoes/`.

## 16. Riscos e cuidados

Principais riscos:

- arquivos CSV ausentes;
- problemas de encoding;
- inferência incorreta de tipos;
- dados brutos serem versionados por engano;
- falha de conexão com PostgreSQL;
- substituição acidental de tabelas bronze;
- transformação indevida durante a ingestão.

Cuidados:

- manter a bronze próxima da origem;
- não traduzir colunas na ingestão;
- não corrigir dados na ingestão;
- validar contagens após a carga;
- manter o script simples;
- documentar qualquer comportamento inesperado.

## 17. Pendências

- [ ] Criar pasta `ingestao/`.
- [ ] Criar script `carregar_bronze_olist.py`.
- [ ] Criar `requirements.txt`.
- [ ] Atualizar `.env.example` com `POSTGRES_HOST`.
- [ ] Executar primeira carga.
- [ ] Registrar validação da ingestão bronze.

## 18. Observações

A ingestão bronze é uma etapa de entrada do projeto.

O objetivo não é demonstrar transformações nesta etapa, mas criar uma base rastreável para que o dbt possa executar as transformações nas camadas `silver` e `gold`.

A decisão de não usar Airbyte nesta fase foi registrada para preservar o foco do projeto em dbt, testes, modelos incrementais e SDD.
