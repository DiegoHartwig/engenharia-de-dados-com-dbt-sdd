# Fluxo SDD do Projeto

## 1. Objetivo

Este documento define o fluxo de **Spec-Driven Development** adotado neste projeto de Engenharia de Dados com dbt.

O objetivo é estabelecer uma forma organizada de transformar requisitos, regras de negócio e decisões técnicas em modelos dbt documentados, testados e validados.

Neste projeto, o SDD não será tratado apenas como documentação. Ele será usado como método de desenvolvimento.

## 2. Fluxo principal

O fluxo oficial do projeto será:

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

3. Constituição

A constituição define os princípios gerais do projeto.

Ela descreve:

propósito do projeto;
responsabilidades das camadas;
regras de uso do dbt;
estratégia de testes;
convenções de idioma;
restrições da primeira fase;
critérios gerais de qualidade.

Arquivo:
sdd/constituicao.md

A constituição deve orientar todas as decisões do projeto.

4. Decisões arquiteturais

Decisões importantes devem ser registradas como ADRs.

As ADRs devem explicar:

contexto;
decisão tomada;
motivo da decisão;
consequências;
alternativas consideradas, quando aplicável.

Pasta:
sdd/decisoes/

Exemplos:
ADR-001-uso-da-bronze-como-landing-zone.md
ADR-002-uso-de-portugues-no-projeto.md
ADR-003-uso-de-sdd-adaptado-para-dbt.md

5. Especificações

As especificações descrevem o que deve ser construído.

Elas podem existir em dois níveis:

5.1 Especificações gerais

Usadas para definir decisões amplas do projeto.

Exemplos:
sdd/especificacoes/001_arquitetura.md
sdd/especificacoes/002_estrategia_de_camadas.md
sdd/especificacoes/003_estrategia_de_testes_dbt.md
sdd/especificacoes/004_estrategia_incremental.md

5.2 Especificações por modelo

Usadas para definir modelos dbt específicos.

Pasta:
sdd/especificacoes/modelos/

Exemplos:
sdd/especificacoes/modelos/silver_pedidos.md
sdd/especificacoes/modelos/fato_pedidos.md
sdd/especificacoes/modelos/mart_vendas_diarias.md

Cada especificação de modelo deve responder:

qual é o objetivo do modelo;
qual é a camada;
qual é o grão;
quais fontes serão utilizadas;
quais colunas são esperadas;
quais regras de negócio serão aplicadas;
quais regras de qualidade serão verificadas;
quais testes dbt são esperados;
qual é a estratégia incremental, quando aplicável;
quais são os critérios de aceite.
6. Planos técnicos

O plano técnico descreve como uma especificação será implementada.

A especificação define o que precisa ser feito.

O plano técnico define como será feito.

Pasta:

sdd/planos/

Um plano pode conter:

ordem de implementação;
dependências entre modelos;
materializações;
estratégia de joins;
estratégia de incremental;
testes a implementar;
riscos técnicos;
decisões pendentes.

Exemplo:

sdd/planos/003_configuracao_dbt.md
sdd/planos/modelos/fato_pedidos.md

7. Tarefas

As tarefas quebram o plano técnico em passos executáveis.

Pasta:

sdd/tarefas/

Exemplo:
# Tarefas — fato_pedidos

- [ ] Criar especificação do modelo
- [ ] Criar plano técnico
- [ ] Criar modelo SQL
- [ ] Criar documentação YAML
- [ ] Adicionar testes genéricos
- [ ] Criar testes singulares necessários
- [ ] Executar `dbt build --select fato_pedidos`
- [ ] Registrar validação

As tarefas devem ser objetivas e verificáveis.

8. Implementação dbt

A implementação deve ocorrer somente depois de existir pelo menos uma especificação mínima.

Os principais artefatos dbt serão:

dbt/models/
dbt/tests/
dbt/macros/
dbt/seeds/
dbt/snapshots/

A implementação deve seguir os princípios:

usar source() para tabelas da camada bronze;
usar ref() entre modelos dbt;
manter SQL legível;
documentar modelos e colunas;
aplicar testes compatíveis com a criticidade do modelo;
evitar lógica desnecessariamente complexa;
manter rastreabilidade entre especificação, modelo, testes e validação.
9. Validação

A validação registra se a implementação atendeu aos critérios definidos.

Pasta:

sdd/validacoes/

A validação pode conter:

comando executado;
data da execução;
modelos validados;
testes executados;
resultado;
erros encontrados;
ajustes aplicados;
pendências conhecidas.

Exemplo de comandos:

dbt debug
dbt run
dbt test
dbt build
dbt build --select fato_pedidos

10. Documentação

A documentação final do projeto deve refletir o que foi construído.

Ela pode ficar em:

documentacao/

ou nos próprios arquivos YAML do dbt.

A documentação deve explicar:

arquitetura;
camadas;
modelos;
testes;
regras de negócio;
estratégia incremental;
decisões arquiteturais;
limitações conhecidas.

11. Fluxo para criação de um novo modelo dbt

Para criar um novo modelo dbt, seguir o fluxo:

1. Criar especificação do modelo
2. Criar plano técnico do modelo
3. Criar lista de tarefas
4. Implementar SQL do modelo
5. Documentar modelo e colunas no YAML
6. Criar testes dbt
7. Executar dbt build
8. Registrar validação
9. Atualizar documentação, se necessário
12. Fluxo para alteração de um modelo existente

Para alterar um modelo existente:

1. Revisar especificação existente
2. Atualizar especificação, se necessário
3. Registrar decisão arquitetural, se a mudança for relevante
4. Atualizar plano ou tarefas
5. Alterar implementação dbt
6. Executar validação
7. Atualizar documentação

Nenhuma mudança relevante deve acontecer apenas no SQL sem atualização da especificação correspondente.

13. Relação entre SDD e testes dbt

Sempre que uma especificação definir uma regra de qualidade ou regra de negócio, deve-se avaliar se essa regra pode ser representada como teste dbt.

Exemplo:

Regra na especificação:

O valor total do pedido não pode ser negativo.

Possíveis implementações dbt:

teste genérico customizado valor_positivo;
teste singular assert_pedidos_sem_valor_negativo.sql.

Regra na especificação:

Cada pedido deve aparecer uma única vez na fato_pedidos.

Possível implementação dbt:

teste unique na coluna pedido_id.
14. Critério de pronto

Uma entrega será considerada pronta quando:

existir especificação correspondente;
existir implementação dbt;
existir documentação mínima;
existirem testes compatíveis;
o comando dbt build executar com sucesso;
a validação estiver registrada;
as decisões relevantes estiverem documentadas.

15. Uso com assistentes de IA

Assistentes de IA podem ser utilizados para apoiar o desenvolvimento, desde que respeitem a constituição do projeto.

Antes de gerar código, o assistente deve considerar:

README.md;
sdd/constituicao.md;
sdd/fluxo_sdd.md;
especificações existentes;
decisões arquiteturais existentes;
padrões de nomenclatura;
escopo da primeira fase.

O assistente não deve alterar decisões arquiteturais sem atualizar as especificações e ADRs correspondentes.