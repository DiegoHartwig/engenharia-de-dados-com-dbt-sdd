# Instruções para Claude Code

## Contexto do projeto

Este repositório é um projeto de Engenharia de Dados com dbt e Spec-Driven Development.

O objetivo principal é demonstrar boas práticas de dbt, testes automatizados, modelos incrementais, documentação técnica e desenvolvimento orientado por especificações.

A base pública da Olist será usada apenas como cenário de exemplo.

## Arquivos de referência obrigatórios

Antes de alterar código, leia:

- `README.md`
- `sdd/constituicao.md`
- `sdd/fluxo_sdd.md`
- `sdd/decisoes/ADR-001-uso-da-bronze-como-landing-zone.md`
- `sdd/decisoes/ADR-004-uso-de-ingestao-simples-via-python.md`
- `sdd/planos/002_ingestao_bronze.md`
- `sdd/tarefas/002_ingestao_bronze.md`

## Regras do projeto

- O projeto deve permanecer em português do Brasil.
- A camada `bronze` deve preservar os dados próximos da origem.
- A ingestão deve ser simples, via Python, sem Airbyte nesta fase.
- Não aplicar regras de negócio na ingestão.
- Não traduzir colunas na bronze.
- Não deduplicar na bronze.
- Não criar métricas na bronze.
- A transformação será feita posteriormente no dbt, nas camadas `silver` e `gold`.
- Não adicionar IA, RAG, Spark, Airflow, Trino ou Databricks nesta fase.

## Tarefa atual

Implementar e testar a ingestão dos arquivos CSV da Olist para o schema `bronze` do PostgreSQL.

Arquivos esperados:

- `ingestao/carregar_bronze_olist.py`
- `ingestao/README.md`
- `requirements.txt`

O script deve:

- ler os arquivos de `dados/brutos/`;
- validar se todos os CSVs esperados existem;
- conectar no PostgreSQL usando variáveis do `.env`;
- criar o schema `bronze`, se necessário;
- carregar os CSVs para tabelas no schema `bronze`;
- usar o nome do arquivo sem `.csv` como nome da tabela;
- usar carga full com substituição da tabela;
- exibir logs simples com quantidade de registros carregados;
- encerrar com erro claro se algum arquivo estiver ausente.

## Comandos úteis

```powershell
pip install -r requirements.txt
python ingestao\carregar_bronze_olist.py
docker exec -it engenharia_dados_dbt_postgres psql -U ecommerce_user -d ecommerce_dw

Critérios de aceite

A tarefa será aceita quando:

- o script executar sem erro;
- as tabelas forem criadas no schema bronze;
- os 9 arquivos CSV forem carregados;
- as contagens forem exibidas no terminal;
- os CSVs não forem versionados no Git;
- .env não for versionado;
- .env.example estiver atualizado;
- o resultado puder ser registrado em sdd/validacoes/002_ingestao_bronze.md.