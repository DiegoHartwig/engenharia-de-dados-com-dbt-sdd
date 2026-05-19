# ADR-004 — Uso de Ingestão Simples via Python para Arquivos CSV

## Status

Aceita.

## Contexto

Este projeto tem como objetivo principal demonstrar boas práticas de Engenharia de Dados com dbt, utilizando Spec-Driven Development, arquitetura em camadas, modelos incrementais, testes automatizados e documentação técnica.

Inicialmente foi considerada a utilização do Airbyte para realizar a ingestão dos arquivos CSV da base pública da Olist para o PostgreSQL.

A arquitetura prevista era:

```text
CSV Olist
    ↓
Airbyte
    ↓
PostgreSQL - bronze
    ↓
dbt - silver
    ↓
dbt - gold
```

Entretanto, a base utilizada neste projeto é composta por um conjunto pequeno e estático de arquivos CSV.

Como o foco principal do projeto está em dbt, testes, modelos incrementais e Spec-Driven Development, foi avaliado que o uso do Airbyte nesta fase adicionaria complexidade operacional desnecessária.

A ingestão, neste momento, não é o principal objeto de estudo do projeto. Ela deve apenas carregar os dados para a camada `bronze` de forma simples, rastreável e reproduzível.

## Decisão

A ingestão dos arquivos CSV da Olist será feita por meio de um script Python simples, versionado no próprio repositório.

A arquitetura da primeira fase passa a ser:

```text
CSV Olist
    ↓
Script Python de ingestão
    ↓
PostgreSQL - bronze
    ↓
dbt - silver
    ↓
dbt - gold
```

O script deverá:

- ler os arquivos CSV localizados em `dados/brutos/`;
- criar as tabelas no schema `bronze`;
- preservar os nomes originais das colunas sempre que possível;
- carregar os dados no PostgreSQL;
- manter os dados próximos da origem;
- não aplicar regras de negócio;
- não traduzir colunas para português;
- não deduplicar registros;
- não criar métricas;
- registrar logs simples de execução.

## Consequências positivas

Esta decisão traz os seguintes benefícios:

- reduz a complexidade operacional inicial;
- evita gasto de tempo com configuração de uma ferramenta de ingestão para poucos arquivos estáticos;
- mantém o foco principal em dbt e SDD;
- facilita a reprodução do projeto por outras pessoas;
- permite versionar a lógica de ingestão no repositório;
- simplifica a execução em ambiente local;
- reduz dependência de recursos computacionais;
- torna o projeto mais didático.

## Consequências negativas

Esta decisão também traz alguns cuidados:

- a ingestão não demonstrará uso de uma ferramenta especializada como Airbyte;
- alguns recursos de conectores, logs e sincronização automática não estarão disponíveis;
- será necessário manter o script de ingestão no projeto;
- em cenários produtivos com múltiplas fontes, Airbyte ou outra ferramenta de ingestão poderia ser mais adequada.

## Alternativas consideradas

### Alternativa 1 — Usar Airbyte

Essa alternativa foi considerada inicialmente por representar uma ferramenta moderna de ingestão.

Foi descartada nesta fase porque a base é pequena, estática e composta apenas por arquivos CSV.

O uso do Airbyte poderia desviar o foco do projeto, que está em dbt, testes, incremental e SDD.

### Alternativa 2 — Usar comandos manuais de COPY no PostgreSQL

Essa alternativa foi considerada por ser simples e rápida.

Foi descartada como estratégia principal porque comandos manuais seriam menos reproduzíveis e menos organizados do que um script versionado.

### Alternativa 3 — Usar pandas e SQLAlchemy

Essa alternativa foi considerada adequada para a primeira fase.

Ela permite implementar uma ingestão simples, clara e reproduzível, mantendo o foco do projeto.

## Critérios de aceite da decisão

Esta decisão será considerada corretamente aplicada quando:

- existir um script de ingestão versionado no repositório;
- o script carregar os arquivos de `dados/brutos/`;
- as tabelas forem criadas no schema `bronze`;
- os nomes das tabelas preservarem nomes próximos aos arquivos originais;
- os nomes das colunas forem preservados sempre que possível;
- não houver transformação analítica na ingestão;
- os dados forem carregados no PostgreSQL;
- a validação da ingestão bronze for registrada em `sdd/validacoes/`;
- o README ou a documentação refletir a decisão.

## Impacto nas especificações e planos

Esta decisão altera a estratégia inicialmente prevista nos documentos de ingestão.

Os seguintes documentos devem ser revisados quando necessário:

- `sdd/planos/002_ingestao_bronze.md`;
- `sdd/tarefas/002_ingestao_bronze.md`;
- `README.md`, se mencionar Airbyte como ferramenta obrigatória;
- documentação técnica da arquitetura.

A referência ao Airbyte poderá permanecer como evolução futura, mas não como dependência da primeira fase.

## Revisão futura

Esta decisão poderá ser revista caso o projeto evolua para cenários como:

- múltiplas fontes de dados;
- ingestão recorrente;
- conectores externos;
- integração com APIs;
- necessidade de sincronização automática;
- orquestração com Airflow;
- ambiente mais próximo de produção.

Nesses casos, poderá ser criada uma nova ADR propondo o uso de Airbyte, Meltano, dlt, Airflow, Spark ou outra ferramenta de ingestão.
