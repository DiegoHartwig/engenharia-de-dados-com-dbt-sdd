# Especificação 000 — Visão Geral do Projeto

## 1. Objetivo

Este projeto tem como objetivo demonstrar boas práticas de Engenharia de Dados com dbt, utilizando uma abordagem de Spec-Driven Development aplicada a projetos de dados.

A proposta é construir um pipeline analítico simples, didático e profissional, usando a base pública brasileira de e-commerce da Olist como cenário de exemplo.

O foco principal do projeto não é a análise do e-commerce em si, mas a construção de um projeto modelo que demonstre:

- arquitetura em camadas;
- uso profissional de dbt;
- SQL avançado;
- testes automatizados;
- modelos incrementais;
- documentação técnica;
- critérios de aceite;
- decisões arquiteturais;
- desenvolvimento orientado por especificações.

## 2. Problema que o projeto busca resolver

Projetos de dados muitas vezes são desenvolvidos diretamente no código, sem uma etapa clara de especificação, validação e documentação das decisões.

Isso pode gerar problemas como:

- regras de negócio implícitas dentro do SQL;
- testes criados apenas depois da implementação;
- ausência de critérios claros de aceite;
- baixa rastreabilidade entre requisito, transformação e validação;
- dificuldade de manutenção;
- dependência excessiva do conhecimento de quem criou o pipeline;
- uso superficial do dbt, limitado apenas à execução de SQL.

Este projeto busca demonstrar uma forma mais organizada de desenvolver pipelines analíticos com dbt, conectando especificações, planos, tarefas, modelos, testes e validações.

## 3. Objetivos principais

Os objetivos principais do projeto são:

- criar um projeto dbt estruturado e didático;
- aplicar Spec-Driven Development em um contexto de Engenharia de Dados;
- demonstrar arquitetura em camadas com bronze, silver e gold;
- ingerir dados públicos na camada bronze;
- transformar e qualificar os dados na camada silver;
- criar modelos analíticos na camada gold;
- implementar testes dbt em diferentes níveis;
- demonstrar uso de modelos incrementais;
- documentar decisões arquiteturais;
- registrar critérios de aceite e validações;
- criar uma referência reutilizável para futuros projetos dbt.

## 4. Objetivos fora do escopo inicial

Nesta primeira fase, o projeto não tem como objetivo implementar:

- dashboards;
- IA;
- RAG;
- banco vetorial;
- Airflow;
- Spark;
- Trino;
- Databricks;
- CI/CD;
- ambiente produtivo;
- orquestração de pipelines;
- processamento distribuído.

Esses itens poderão ser considerados em fases futuras.

O foco inicial será:

```text
dbt + SQL avançado + testes + incremental + documentação + SDD
```

## 5. Dataset utilizado

O projeto utilizará a base pública brasileira de e-commerce da Olist.

A base contém arquivos relacionados a:

- clientes;
- pedidos;
- itens de pedido;
- pagamentos;
- avaliações;
- produtos;
- vendedores;
- geolocalização;
- tradução de categorias de produtos.

A base será usada como cenário prático para demonstrar boas práticas de modelagem, transformação e validação de dados.

## 6. Arquitetura de alto nível

A arquitetura inicial do projeto será:

```text
Dataset público Olist
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
```

## 7. Camadas do projeto

### 7.1 Bronze

A camada bronze representa a entrada dos dados no PostgreSQL.

Nesta camada, os dados devem ser preservados o mais próximo possível da origem.

A bronze não deve aplicar:

- regras de negócio;
- deduplicação;
- enriquecimento;
- métricas;
- renomeações analíticas;
- transformações de significado.

### 7.2 Silver

A camada silver representa os dados limpos, padronizados e qualificados.

Nesta camada serão aplicados:

- casts;
- renomeação de colunas para português;
- padronização de valores;
- tratamento de duplicidades;
- regras de negócio;
- validações de qualidade;
- preparação das entidades principais.

### 7.3 Gold

A camada gold representa a camada analítica.

Nesta camada serão criados:

- dimensões;
- fatos;
- marts analíticos;
- métricas;
- indicadores;
- modelos incrementais, quando fizer sentido.

## 8. Princípio das camadas

O princípio adotado será:

```text
Bronze preserva.
Silver qualifica.
Gold entrega valor analítico.
```

## 9. SDD aplicado ao projeto

O projeto seguirá uma abordagem de SDD adaptada para dbt.

O fluxo será:

```text
Constituição
    ↓
Decisão arquitetural
    ↓
Especificação
    ↓
Plano técnico
    ↓
Tarefas
    ↓
Implementação dbt
    ↓
Validação
    ↓
Documentação
```

Cada implementação relevante deve estar conectada a uma especificação, plano técnico, lista de tarefas e validação.

## 10. Principais entregáveis

Os principais entregáveis do projeto serão:

- estrutura SDD documentada;
- decisões arquiteturais registradas em ADRs;
- especificações gerais;
- especificações por modelo;
- planos técnicos;
- listas de tarefas;
- projeto dbt configurado;
- sources da camada bronze;
- modelos silver;
- modelos gold;
- testes dbt;
- modelos incrementais;
- documentação YAML;
- registros de validação;
- README explicativo.

## 11. Stack inicial

A stack inicial do projeto será composta por:

- PostgreSQL;
- dbt;
- Docker;
- Airbyte;
- SQL;
- Git/GitHub.

## 12. Critérios gerais de sucesso

O projeto será considerado bem-sucedido quando:

- a arquitetura bronze, silver e gold estiver implementada;
- o projeto dbt estiver funcional;
- os modelos principais possuírem especificações;
- os modelos principais possuírem documentação;
- os testes dbt estiverem implementados;
- houver pelo menos um modelo incremental;
- as decisões arquiteturais estiverem registradas;
- o fluxo SDD estiver aplicado de forma prática;
- os comandos dbt principais executarem com sucesso;
- o repositório puder ser entendido sem depender do histórico de conversas.

## 13. Riscos e cuidados

Principais riscos do projeto:

- excesso de documentação sem utilidade prática;
- specs muito detalhadas para modelos simples;
- tentativa de incluir tecnologias fora do escopo inicial;
- transformação indevida na camada bronze;
- testes criados sem conexão com regras de negócio ou qualidade;
- modelos incrementais criados apenas para demonstrar recurso técnico;
- perda de foco entre estudar dbt e estudar SDD.

Para mitigar esses riscos, o projeto seguirá a regra:

```text
Toda especificação deve orientar código, teste, decisão técnica ou validação.
```

## 14. Evoluções futuras

Possíveis evoluções futuras incluem:

- criação de dashboard;
- orquestração com Airflow;
- ingestão ou processamento com Spark;
- consulta analítica com Trino;
- versão em Databricks;
- integração com CI/CD;
- documentação com dbt docs;
- aplicação de IA ou RAG sobre documentação e metadados;
- formalização com GitHub Spec Kit ou OpenSpec.

Essas evoluções não fazem parte da primeira fase.
