# ADR-001 — Uso da Bronze como Landing Zone

## Status

Aceita.

## Contexto

Este projeto tem como objetivo principal demonstrar boas práticas de Engenharia de Dados com dbt, utilizando Spec-Driven Development, arquitetura em camadas, modelos incrementais, testes automatizados e documentação técnica.

Inicialmente foi considerada uma arquitetura com quatro camadas:

```text
raw → bronze → silver → gold
```

Nesse desenho, a camada `raw` seria responsável por armazenar os dados exatamente como recebidos da origem, enquanto a camada `bronze` faria uma primeira padronização técnica.

Entretanto, para este projeto, o foco principal não está na complexidade da ingestão ou no armazenamento histórico bruto dos arquivos. O foco está em:

- dbt;
- SQL avançado;
- testes automatizados;
- modelos incrementais;
- documentação;
- Spec-Driven Development;
- boas práticas de Analytics Engineering.

Como a base utilizada é pública, estática e composta por arquivos CSV da Olist, foi avaliado que a criação de uma camada `raw` separada aumentaria a complexidade inicial sem trazer ganho proporcional para os objetivos desta fase do projeto.

## Decisão

A camada `bronze` será utilizada como camada de aterrissagem dos dados, recebendo diretamente os arquivos públicos da Olist no PostgreSQL.

A arquitetura da primeira fase será:

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

Neste projeto, a camada `bronze` assumirá o papel de preservar os dados próximos da origem.

Na camada `bronze`:

- os dados devem ser mantidos o mais próximo possível dos arquivos originais;
- os nomes de colunas da origem devem ser preservados sempre que possível;
- não devem ser aplicadas regras de negócio;
- não deve haver deduplicação;
- não devem ser criadas métricas;
- não deve haver enriquecimento analítico;
- não devem ser feitas renomeações para português com finalidade analítica;
- metadados técnicos gerados pela ferramenta de ingestão podem ser mantidos.

As transformações de limpeza, padronização, tradução de nomes, tipagem, deduplicação e aplicação de regras de negócio serão realizadas a partir da camada `silver`.

## Consequências positivas

Esta decisão traz os seguintes benefícios:

- simplifica a arquitetura inicial do projeto;
- reduz o esforço de configuração da ingestão;
- mantém o foco principal em dbt e SDD;
- evita criar camadas redundantes para uma base pública e estática;
- facilita a explicação didática do fluxo;
- preserva a separação entre entrada de dados, qualificação e camada analítica;
- permite evoluir futuramente para uma camada `raw`, se necessário.

## Consequências negativas

Esta decisão também traz alguns cuidados:

- a camada `bronze` passa a acumular o papel de landing zone;
- não haverá uma camada `raw` separada para armazenamento completamente isolado dos arquivos originais;
- em cenários produtivos mais complexos, essa decisão poderia ser insuficiente;
- caso a ingestão passe a envolver múltiplas fontes, arquivos mutáveis ou histórico de cargas, uma camada `raw` poderá ser necessária.

## Alternativas consideradas

### Alternativa 1 — Criar camada raw e bronze separadas

Arquitetura:

```text
raw → bronze → silver → gold
```

Essa alternativa foi considerada mais completa, porém mais complexa para o escopo inicial.

Ela faria mais sentido em um projeto produtivo com múltiplas fontes, histórico de ingestão, auditoria de arquivos originais e necessidade de replay.

Não foi escolhida nesta fase para manter o foco em dbt, testes, incremental e SDD.

### Alternativa 2 — Ingerir direto na silver

Arquitetura:

```text
silver → gold
```

Essa alternativa foi descartada porque misturaria ingestão com qualificação dos dados.

A camada `silver` deve representar dados tratados e confiáveis. Portanto, ela não deve receber diretamente arquivos brutos da origem.

### Alternativa 3 — Usar apenas uma camada analítica

Arquitetura:

```text
bronze → marts
```

Essa alternativa foi descartada porque reduziria a capacidade didática do projeto.

O objetivo é demonstrar boas práticas de modelagem em camadas, testes por camada e evolução dos dados desde a origem até o consumo analítico.

## Critérios de aceite da decisão

Esta decisão será considerada corretamente aplicada quando:

- as tabelas ingeridas a partir da Olist estiverem no schema `bronze`;
- a camada `bronze` preservar os nomes e estrutura da origem sempre que possível;
- as transformações de limpeza e padronização ocorrerem apenas na camada `silver`;
- as regras de negócio consolidadas e métricas forem implementadas na camada `gold`;
- o README, a constituição SDD e as especificações refletirem a arquitetura `bronze → silver → gold`.

## Revisão futura

Esta decisão poderá ser revista caso o projeto evolua para cenários como:

- ingestão de múltiplas fontes;
- dados mutáveis;
- cargas recorrentes;
- necessidade de histórico bruto de arquivos;
- necessidade de replay de ingestão;
- orquestração com Airflow;
- processamento distribuído com Spark;
- integração com lakehouse, Trino ou Databricks.

Nesse caso, poderá ser criada uma nova ADR propondo a introdução de uma camada `raw` antes da `bronze`.
