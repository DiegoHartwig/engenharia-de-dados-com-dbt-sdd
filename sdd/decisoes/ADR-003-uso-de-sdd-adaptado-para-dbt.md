# ADR-003 — Uso de SDD Adaptado para dbt

## Status

Aceita.

## Contexto

Este projeto possui dois objetivos principais.

O primeiro objetivo é demonstrar boas práticas de Engenharia de Dados com dbt, incluindo arquitetura em camadas, SQL avançado, modelos incrementais, testes automatizados e documentação técnica.

O segundo objetivo é experimentar uma forma prática de aplicar **Spec-Driven Development** em projetos de dados, especialmente em projetos baseados em dbt.

Ferramentas e metodologias de SDD geralmente são pensadas para desenvolvimento de software tradicional. Entretanto, projetos de dados possuem características específicas, como:

- fontes de dados;
- camadas de transformação;
- modelos SQL;
- materializações;
- testes de dados;
- regras de qualidade;
- regras de negócio;
- documentação de modelos;
- documentação de colunas;
- critérios de aceite baseados em execução e validação;
- lineage;
- incrementalidade;
- contratos de dados.

Por isso, foi avaliada a necessidade de adaptar o fluxo de SDD para o contexto de Engenharia de Dados e Analytics Engineering com dbt.

## Decisão

O projeto adotará uma abordagem própria de **Spec-Driven Development adaptada para dbt**.

Essa abordagem será inspirada no fluxo:

```text
Constitution → Spec → Plan → Tasks → Implementation → Validation
```

No projeto, esse fluxo será representado da seguinte forma:

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

A estrutura principal ficará organizada em:

```text
sdd/
├── constituicao.md
├── fluxo_sdd.md
├── templates/
├── especificacoes/
├── planos/
├── tarefas/
├── decisoes/
└── validacoes/
```

As especificações serão utilizadas para orientar diretamente a criação dos artefatos dbt.

Cada modelo relevante deverá possuir, quando aplicável:

- especificação;
- plano técnico;
- lista de tarefas;
- modelo SQL;
- documentação YAML;
- testes dbt;
- validação registrada.

## Adaptação para dbt

No contexto deste projeto, SDD significa que as especificações devem orientar a implementação dos seguintes artefatos:

- `sources`;
- modelos `silver`;
- modelos `gold`;
- dimensões;
- fatos;
- marts;
- testes genéricos nativos;
- testes singulares;
- testes genéricos customizados;
- macros;
- seeds;
- snapshots, se aplicável;
- documentação;
- critérios de aceite.

As especificações de modelos devem conter, sempre que fizer sentido:

- objetivo do modelo;
- camada;
- tipo de materialização;
- grão;
- fontes utilizadas;
- chave primária;
- colunas esperadas;
- regras de negócio;
- regras de qualidade;
- testes dbt esperados;
- estratégia incremental;
- critérios de aceite.

## Relação entre SDD e testes dbt

Toda regra de qualidade ou regra de negócio definida em uma especificação deverá ser avaliada como candidata a teste dbt.

Exemplos:

| Regra especificada | Possível implementação dbt |
|---|---|
| Pedido deve ter identificador obrigatório | `not_null` |
| Pedido deve aparecer uma única vez | `unique` |
| Status deve estar dentro de valores esperados | `accepted_values` |
| Pedido deve possuir cliente válido | `relationships` |
| Valor total do pedido não pode ser negativo | teste customizado ou teste singular |
| Data de entrega não pode ser anterior à data da compra | teste singular |

Dessa forma, os testes não serão criados apenas depois do modelo pronto. Eles serão derivados das especificações.

## Consequências positivas

Esta decisão traz os seguintes benefícios:

- torna o processo de desenvolvimento mais organizado;
- melhora a rastreabilidade entre requisito, modelo, teste e validação;
- transforma regras de negócio em testes verificáveis;
- facilita o uso de assistentes de IA de forma controlada;
- reduz decisões implícitas no código SQL;
- melhora a documentação do projeto;
- cria um modelo reutilizável para outros projetos dbt;
- demonstra maturidade de Engenharia de Dados e Analytics Engineering.

## Consequências negativas

Esta decisão também traz alguns custos e cuidados:

- aumenta o volume inicial de documentação;
- pode tornar o desenvolvimento mais lento no começo;
- exige disciplina para manter especificações e código sincronizados;
- pode gerar burocracia se as specs forem detalhadas demais;
- requer critérios claros para decidir quais modelos precisam de specs completas.

## Critérios para evitar excesso de documentação

Para evitar burocracia, o projeto seguirá a regra:

```text
Toda especificação deve orientar código, teste, decisão técnica ou validação.
```

Não devem ser criadas especificações apenas para aumentar documentação.

As specs devem ser úteis para pelo menos um dos seguintes objetivos:

- orientar a implementação;
- definir regras de negócio;
- definir regras de qualidade;
- guiar testes dbt;
- justificar uma decisão técnica;
- definir critérios de aceite;
- facilitar manutenção futura.

## Alternativas consideradas

### Alternativa 1 — Não usar SDD

Essa alternativa foi descartada porque metade do objetivo do projeto é justamente experimentar e documentar uma forma prática de aplicar SDD em projetos dbt.

Sem SDD, o projeto seria apenas uma implementação dbt com boas práticas, mas perderia seu diferencial metodológico.

### Alternativa 2 — Usar uma ferramenta SDD sem adaptação

Foi considerada a possibilidade de adotar uma ferramenta ou framework de SDD de forma direta.

Essa alternativa foi descartada nesta fase porque projetos dbt possuem características específicas que exigem adaptação, como camadas de dados, testes de dados, materializações, sources, marts e critérios de aceite baseados em execução do dbt.

### Alternativa 3 — Usar apenas documentação livre

Essa alternativa foi descartada porque documentação livre não garante fluxo, rastreabilidade ou critérios consistentes.

O projeto precisa de uma metodologia clara para conectar especificações, planos, tarefas, modelos, testes e validações.

## Critérios de aceite da decisão

Esta decisão será considerada corretamente aplicada quando:

- existir uma constituição do projeto;
- existir um fluxo SDD documentado;
- existirem templates para specs, planos e tarefas;
- decisões arquiteturais relevantes forem registradas em ADRs;
- modelos relevantes tiverem especificações antes da implementação;
- regras de qualidade das specs forem refletidas em testes dbt;
- validações forem registradas após execuções relevantes;
- a documentação explicar como SDD foi aplicado ao dbt.

## Escopo inicial

Na primeira fase, o SDD será aplicado principalmente a:

- arquitetura geral;
- estratégia de camadas;
- estratégia de testes dbt;
- estratégia incremental;
- configuração inicial do dbt;
- modelos principais da camada silver;
- modelos principais da camada gold;
- marts analíticos;
- testes e critérios de aceite.

## Revisão futura

Esta decisão poderá ser revista caso o projeto passe a utilizar formalmente uma ferramenta específica de SDD ou caso seja necessário adaptar o fluxo para um contexto mais próximo de produção.

Possíveis evoluções futuras:

- adoção formal de GitHub Spec Kit;
- adoção formal de OpenSpec;
- criação de templates automatizados;
- integração com assistentes de IA;
- geração de specs a partir de issues;
- validação automática de critérios de aceite via CI/CD.
