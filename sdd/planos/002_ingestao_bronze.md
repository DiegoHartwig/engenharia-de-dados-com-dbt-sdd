# Plano Técnico 002 — Ingestão da Camada Bronze

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome do plano | Ingestão da camada bronze |
| Tipo | Ingestão |
| Relacionado à spec | `sdd/especificacoes/001_arquitetura.md` |
| Status | Rascunho |
| Responsável | Diego Hartwig |

## 2. Objetivo do plano

Este plano define como será realizada a ingestão dos arquivos públicos da Olist para o PostgreSQL, utilizando a camada `bronze` como ponto de entrada dos dados no projeto.

O objetivo é carregar os arquivos CSV no schema `bronze`, preservando os dados o mais próximo possível da origem, sem aplicar regras de negócio, deduplicações, enriquecimentos ou transformações analíticas.

## 3. Escopo

Este plano cobre:

- organização dos arquivos CSV da Olist em `dados/brutos/`;
- validação da presença dos arquivos esperados;
- definição dos nomes das tabelas na camada `bronze`;
- configuração da ingestão para PostgreSQL;
- preservação da estrutura original dos dados;
- validação da carga no schema `bronze`;
- registro da validação da ingestão.

## 4. Fora de escopo

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

## 5. Dependências

| Tipo | Nome | Descrição |
|---|---|---|
| Banco | PostgreSQL | Banco local executando via Docker Compose |
| Schema | `bronze` | Schema de destino dos dados ingeridos |
| Dataset | Olist | Base pública brasileira de e-commerce |
| Ferramenta | Airbyte | Ferramenta prevista para ingestão dos CSVs |
| Pasta | `dados/brutos/` | Pasta local com os arquivos CSV da Olist |

## 6. Arquivos esperados da Olist

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

## 7. Estratégia de ingestão

A estratégia de ingestão será:

```text
CSV Olist
    ↓
Airbyte
    ↓
PostgreSQL schema bronze
```

A ingestão deverá preservar os dados próximos da origem.

Não devem ser aplicadas na ingestão:

- regras de negócio;
- renomeações para português;
- filtros analíticos;
- agregações;
- deduplicações;
- enriquecimentos;
- cálculo de métricas.

Essas transformações serão responsabilidade das camadas `silver` e `gold`.

## 8. Tabelas esperadas na bronze

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

Se a ferramenta de ingestão gerar nomes com prefixos, sufixos ou metadados próprios, essa diferença deverá ser registrada na validação.

## 9. Estratégia de tipos

Na camada `bronze`, os tipos poderão ser definidos automaticamente pela ferramenta de ingestão.

Como a bronze deve preservar a origem, não é obrigatório corrigir tipos nesta etapa.

Ajustes de tipos serão feitos na camada `silver`.

Cuidados:

- campos de data podem entrar como texto;
- campos monetários podem entrar como texto ou numérico;
- campos de identificador devem preservar seu conteúdo original;
- valores nulos devem ser preservados.

## 10. Metadados técnicos

A ferramenta de ingestão pode criar metadados técnicos.

Exemplos possíveis:

- identificador de carga;
- timestamp de carga;
- nome do arquivo;
- campos internos da ferramenta.

Esses metadados podem ser mantidos na bronze, desde que não alterem o significado dos dados originais.

Se existirem metadados gerados pela ferramenta, eles deverão ser documentados na validação da ingestão.

## 11. Estratégia de validação

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

## 12. Critérios de aceite

Este plano será considerado concluído quando:

- [ ] os arquivos CSV da Olist estiverem em `dados/brutos/`;
- [ ] os arquivos CSV não estiverem versionados no Git;
- [ ] o PostgreSQL estiver em execução;
- [ ] o schema `bronze` existir;
- [ ] a ferramenta de ingestão estiver configurada;
- [ ] os arquivos forem carregados para o schema `bronze`;
- [ ] as tabelas esperadas existirem no PostgreSQL;
- [ ] a contagem de registros for registrada;
- [ ] uma amostra dos dados for validada;
- [ ] nenhuma transformação analítica for aplicada na ingestão;
- [ ] a validação da ingestão for registrada em `sdd/validacoes/`.

## 13. Riscos e cuidados

Principais riscos:

- Airbyte gerar nomes de tabelas diferentes dos nomes esperados;
- Airbyte criar colunas técnicas adicionais;
- problemas de rede entre Airbyte e PostgreSQL;
- arquivos CSV com encoding incompatível;
- inferência incorreta de tipos;
- dados brutos serem versionados por engano;
- transformação indevida durante a ingestão.

Cuidados:

- manter a bronze próxima da origem;
- revisar nomes gerados pela ferramenta;
- registrar diferenças encontradas;
- não corrigir dados na ingestão;
- validar contagens após a carga;
- manter decisões relevantes documentadas.

## 14. Pendências

- [ ] Baixar a base pública da Olist.
- [ ] Confirmar todos os arquivos esperados.
- [ ] Definir instalação final do Airbyte local.
- [ ] Configurar origem dos arquivos CSV.
- [ ] Configurar destino PostgreSQL.
- [ ] Executar primeira carga.
- [ ] Registrar validação da ingestão bronze.

## 15. Observações

A ingestão bronze é uma etapa de entrada do projeto.

O objetivo não é demonstrar transformações nesta etapa, mas criar uma base rastreável para que o dbt possa executar as transformações nas camadas `silver` e `gold`.

Caso a ingestão com Airbyte fique excessivamente complexa para o escopo do projeto, poderá ser aberta uma nova ADR avaliando uma alternativa temporária de ingestão via Python ou comando SQL.
