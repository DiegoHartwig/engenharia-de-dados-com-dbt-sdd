# Constituição do Projeto

## 1. Propósito

Este projeto tem como propósito demonstrar boas práticas de Engenharia de Dados com dbt, utilizando uma abordagem de **Spec-Driven Development** aplicada ao contexto de projetos de dados.

O objetivo não é apenas construir um pipeline analítico, mas também experimentar e documentar uma forma organizada de desenvolver projetos dbt a partir de especificações, regras, planos, tarefas, testes e critérios de aceite.

A base pública da Olist será utilizada como cenário de exemplo. O foco principal do projeto não está na análise do e-commerce em si, mas na construção de um projeto modelo, didático e tecnicamente consistente.

## 2. Princípios gerais

Este projeto deve seguir os seguintes princípios:

1. Toda implementação relevante deve partir de uma especificação.
2. As decisões arquiteturais devem ser documentadas.
3. O código dbt deve ser simples, legível e rastreável.
4. As camadas de dados devem ter responsabilidades bem definidas.
5. Os testes devem ser tratados como parte central do desenvolvimento.
6. A documentação deve explicar o motivo das decisões, não apenas o funcionamento técnico.
7. As transformações devem ser implementadas com foco em clareza, qualidade e manutenibilidade.
8. O projeto deve ser didático, mas sem abrir mão de boas práticas profissionais.

## 3. Princípio das camadas

O projeto utilizará três camadas principais:

```text
bronze → silver → gold

A regra conceitual é:
Bronze preserva.
Silver qualifica.
Gold entrega valor analítico.

4. Camada Bronze

A camada bronze representa a entrada dos dados no projeto.

Neste projeto, os arquivos públicos da Olist serão ingeridos diretamente no schema bronze do PostgreSQL.

A camada bronze deve preservar os dados o mais próximo possível da origem.

Na camada bronze:

não aplicar regras de negócio;
não deduplicar registros;
não criar métricas;
não enriquecer dados;
não renomear colunas para fins analíticos;
não alterar o significado dos dados;
preservar estrutura, nomes e conteúdo original sempre que possível.

A camada bronze pode conter metadados técnicos de carga quando a ferramenta de ingestão gerar esses campos automaticamente.

5. Camada Silver

A camada silver representa os dados limpos, padronizados e qualificados.

Na camada silver, os dados passam a ser preparados para uso analítico e para composição dos modelos da camada gold.

Na camada silver:

aplicar casts de tipos;
renomear colunas para português e para nomes mais claros;
padronizar valores;
tratar duplicidades quando necessário;
aplicar regras de negócio;
validar relacionamentos entre entidades;
preparar entidades confiáveis;
organizar os dados para facilitar o consumo pela camada gold.

A camada silver deve evitar métricas finais de negócio. Seu papel principal é qualificar e estruturar os dados.

6. Camada Gold

A camada gold representa a camada analítica do projeto.

Na camada gold serão construídos fatos, dimensões e marts analíticos preparados para consumo.

Na camada gold:

criar dimensões;
criar fatos;
criar marts analíticos;
calcular indicadores;
aplicar regras de negócio consolidadas;
utilizar modelos incrementais quando fizer sentido;
documentar métricas e regras de cálculo;
validar consistência dos resultados analíticos.

A camada gold deve entregar valor analítico de forma clara, documentada e testável.

7. Spec-Driven Development

Este projeto seguirá uma abordagem de desenvolvimento orientado por especificações.

Antes da implementação de modelos dbt relevantes, deve existir uma especificação descrevendo o que será construído.

As especificações devem responder, sempre que aplicável:

qual é o objetivo do modelo;
qual camada será utilizada;
qual é o grão da tabela;
quais fontes ou modelos serão utilizados;
quais colunas são esperadas;
quais regras de negócio serão aplicadas;
quais regras de qualidade devem ser verificadas;
quais testes dbt devem existir;
qual será a estratégia incremental, quando aplicável;
quais são os critérios de aceite.

O fluxo recomendado é:
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

8. Relação entre especificações e dbt

As especificações não devem ser documentos isolados.

Cada especificação relevante deve orientar diretamente a criação ou alteração de artefatos dbt, como:

modelos SQL;
arquivos YAML;
testes genéricos;
testes singulares;
macros;
seeds;
snapshots;
documentação;
critérios de aceite.

Sempre que uma regra de negócio ou regra de qualidade for definida em uma especificação, deve-se avaliar se ela pode ser transformada em teste dbt.

9. Testes dbt

Os testes são parte central deste projeto.

O projeto deve demonstrar o uso de diferentes tipos de testes do dbt, incluindo:

testes genéricos nativos;
testes singulares;
testes genéricos customizados;
testes de relacionamento;
testes de valores aceitos;
testes de qualidade por camada;
testes de regras de negócio.

Devem ser utilizados, quando fizer sentido:

not_null;
unique;
accepted_values;
relationships;
testes singulares em SQL;
testes customizados via macros;
packages como dbt_utils.

10. Estratégia de testes por camada
Bronze

Na camada bronze, os testes devem ser mais estruturais.

Exemplos:

chave principal não nula;
unicidade quando a origem indicar unicidade;
valores aceitos em campos controlados;
existência de dados;
validações básicas de integridade da origem.
Silver

Na camada silver, os testes devem validar qualidade e consistência.

Exemplos:

chaves não nulas;
deduplicação;
relacionamentos entre entidades;
validade de datas;
valores positivos;
regras de negócio intermediárias;
campos padronizados.
Gold

Na camada gold, os testes devem validar consistência analítica.

Exemplos:

unicidade de dimensões;
integridade entre fatos e dimensões;
métricas não negativas;
indicadores consistentes;
grão correto dos modelos;
regras de aceite dos marts.
11. Modelos incrementais

Modelos incrementais devem ser utilizados quando houver ganho didático e técnico.

Todo modelo incremental deve possuir especificação clara contendo:

motivo para ser incremental;
coluna de controle incremental;
chave única;
regra de atualização;
comportamento esperado em full-refresh;
critérios de aceite;
testes necessários.

Nenhum modelo deve ser incremental apenas para demonstrar recurso técnico sem necessidade conceitual.

12. Convenções de idioma

O projeto será desenvolvido em português do Brasil.

Devem ser escritos em português:

README;
especificações;
documentação;
decisões arquiteturais;
planos;
tarefas;
descrições de modelos;
descrições de colunas;
nomes de modelos analíticos;
nomes de testes singulares;
critérios de aceite.

Termos oficiais do ecossistema dbt podem ser mantidos em inglês quando fizer sentido, como:

dbt;
source;
model;
seed;
snapshot;
macro;
test;
freshness;
incremental;
lineage;
materialization.

13. Convenções de nomenclatura

Os modelos dbt devem utilizar nomes claros, descritivos e em português.

Exemplos esperados:
silver_pedidos
silver_clientes
silver_itens_pedido
dim_clientes
dim_produtos
fato_pedidos
mart_vendas_diarias
mart_desempenho_entregas

Os nomes devem seguir o padrão:
camada_entidade
ou
tipo_entidade

silver_pedidos
dim_clientes
fato_pedidos
mart_vendas_mensais

14. Documentação

A documentação deve ser tratada como parte do projeto, não como etapa opcional.

Todo modelo relevante deve possuir:

descrição do modelo;
descrição das colunas principais;
testes associados;
explicação do grão;
regras de negócio relevantes;
critérios de aceite, quando aplicável.

O projeto deve permitir que uma pessoa entenda a arquitetura, as decisões e os modelos sem depender do histórico de conversas.

15. Decisões arquiteturais

Decisões importantes devem ser registradas como ADRs na pasta:
sdd/decisoes/

Exemplos de decisões que devem ser documentadas:

uso da bronze como camada de aterrissagem;
uso de português no projeto;
uso de SDD adaptado para dbt;
escolha de materializações;
adoção de packages dbt;
mudança de estratégia incremental;
alteração na estrutura das camadas.
16. Validação

A validação deve ser feita por meio de comandos dbt e registros de aceite.

Sempre que um conjunto relevante de modelos for implementado, deve-se registrar:

comando executado;
modelos incluídos;
testes executados;
resultado;
ajustes realizados;
pendências conhecidas.

Exemplos de comandos:
dbt debug
dbt run
dbt test
dbt build
dbt build --select nome_do_modelo

17. Restrições da primeira fase

Nesta primeira fase, o projeto não deve incluir:

IA;
RAG;
banco vetorial;
dashboards;
Spark;
Airflow;
Trino;
Databricks.

Esses temas podem aparecer como evolução futura, mas não fazem parte do escopo inicial.

O foco da primeira fase é:
dbt + SQL avançado + testes + modelos incrementais + documentação + SDD

18. Critérios gerais de qualidade

Uma entrega será considerada adequada quando:

estiver alinhada com uma especificação;
possuir implementação dbt clara;
possuir documentação mínima;
possuir testes compatíveis com a criticidade do modelo;
puder ser executada com dbt build;
respeitar a arquitetura bronze, silver e gold;
preservar as decisões registradas;
contribuir para o objetivo didático e profissional do projeto.
19. Evolução do projeto

Esta constituição pode evoluir ao longo do projeto.

Qualquer alteração relevante deve ser feita de forma explícita, documentada e, quando necessário, acompanhada de uma nova decisão arquitetural.

A constituição deve servir como referência para orientar humanos e assistentes de IA durante o desenvolvimento.