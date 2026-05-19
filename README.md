# Engenharia de Dados com dbt e SDD

Projeto de Engenharia de Dados com dbt, utilizando **Spec-Driven Development**, arquitetura em camadas, modelos incrementais, testes automatizados e documentação técnica.

## Objetivo

Este projeto tem como objetivo demonstrar boas práticas de Engenharia de Dados e Analytics Engineering utilizando dbt.

A proposta é construir um pipeline analítico a partir de uma base pública de dados, passando pelas camadas `bronze`, `silver` e `gold`, com foco em:

- SQL avançado;
- modelagem analítica;
- arquitetura em camadas;
- desenvolvimento orientado por especificações;
- modelos incrementais;
- testes automatizados no dbt;
- documentação técnica;
- critérios de aceite por modelo.

## O que é SDD?

Neste projeto, SDD significa **Spec-Driven Development**, ou Desenvolvimento Orientado por Especificações.

Antes da implementação dos modelos dbt, serão criadas especificações descrevendo:

- objetivo do modelo;
- camada de destino;
- grão da tabela;
- fontes utilizadas;
- regras de negócio;
- regras de qualidade;
- testes esperados;
- estratégia incremental;
- critérios de aceite.

## Stack inicial

- PostgreSQL
- dbt
- Docker
- Airbyte
- SQL

## Dataset

O projeto utilizará a base pública brasileira de e-commerce da Olist como cenário de exemplo.

A base será usada apenas como suporte para demonstrar boas práticas de Engenharia de Dados com dbt. O foco principal do projeto não é a análise do e-commerce em si, mas a construção de um projeto modelo com boas práticas.

## Arquitetura proposta

```text
Dataset público
    ↓
Ingestão com Airbyte
    ↓
PostgreSQL - bronze
    ↓
dbt - silver
    ↓
dbt - gold
    ↓
marts analíticos