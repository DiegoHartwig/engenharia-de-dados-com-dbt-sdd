# Especificação do Modelo: <nome_do_modelo>

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome do modelo | `<nome_do_modelo>` |
| Camada | `<bronze/silver/gold>` |
| Tipo de modelo | `<source/model/dim/fato/mart>` |
| Materialização prevista | `<view/table/incremental/ephemeral>` |
| Responsável | `<nome>` |
| Status | `<rascunho/em desenvolvimento/validado>` |

## 2. Objetivo

Descrever o objetivo do modelo.

Este campo deve responder:

- por que este modelo existe;
- qual problema ele resolve;
- quem ou qual camada irá consumi-lo;
- qual valor ele agrega ao pipeline.

Exemplo:

> Consolidar os dados de pedidos da Olist em uma estrutura limpa, padronizada e confiável, servindo como base para fatos e marts analíticos da camada gold.

## 3. Camada

Informar a camada do modelo e justificar seu papel dentro dela.

Exemplo:

> Este modelo pertence à camada `silver`, pois realiza padronização, tipagem, renomeação de colunas e aplicação de regras básicas de qualidade sobre os dados brutos da camada `bronze`.

## 4. Grão do modelo

Descrever o nível de detalhe da tabela.

Exemplos:

- uma linha por pedido;
- uma linha por item de pedido;
- uma linha por cliente;
- uma linha por produto;
- uma linha por dia de venda;
- uma linha por pedido e forma de pagamento.

O grão deve ser claro, pois ele orienta testes de unicidade, chaves e agregações.

## 5. Fontes e dependências

Listar todas as fontes ou modelos usados.

| Tipo | Nome | Descrição |
|---|---|---|
| source | `source('olist', 'olist_orders_dataset')` | Tabela bronze de pedidos |
| ref | `ref('silver_clientes')` | Modelo silver de clientes |

## 6. Chave primária ou chave de negócio

Informar a chave principal esperada do modelo.

Exemplo:

```text
pedido_id

Ou, em caso de chave composta:

pedido_id + item_pedido_id
7. Colunas esperadas
| Coluna     | Tipo esperado | Obrigatória | Descrição     |
| ---------- | ------------- | ----------- | ------------- |
| `<coluna>` | `<tipo>`      | `<sim/não>` | `<descrição>` |


Exemplo:

| Coluna        | Tipo esperado | Obrigatória | Descrição                                 |
| ------------- | ------------- | ----------- | ----------------------------------------- |
| pedido_id     | text          | sim         | Identificador único do pedido             |
| cliente_id    | text          | sim         | Identificador do cliente                  |
| status_pedido | text          | sim         | Status atual do pedido                    |
| data_compra   | timestamp     | sim         | Data e hora em que o pedido foi realizado |


Descrever as principais transformações previstas.

Exemplos:

renomear colunas da origem para português;
converter campos de data para timestamp;
converter valores monetários para numeric;
padronizar textos em minúsculo;
remover espaços em branco;
tratar duplicidades com row_number;
calcular campos derivados;
aplicar regras condicionais com case when.
9. Regras de negócio

Listar regras de negócio que o modelo deve respeitar.

Exemplos:

pedidos cancelados não devem compor receita líquida;
pedidos entregues devem possuir data de entrega;
a data de entrega não pode ser anterior à data da compra;
avaliações devem possuir nota entre 1 e 5;
pagamentos devem possuir valor maior ou igual a zero.
10. Regras de qualidade

Listar regras de qualidade esperadas.

Exemplos:

chave primária não pode ser nula;
chave primária deve ser única;
chaves estrangeiras devem existir nas dimensões relacionadas;
campos monetários não podem ser negativos;
campos de status devem possuir valores aceitos;
datas futuras não devem existir quando não fizer sentido.
11. Testes dbt esperados
11.1 Testes genéricos nativos

Listar testes nativos esperados.

Exemplos:

not_null
unique
accepted_values
relationships
11.2 Testes singulares

Listar testes SQL específicos esperados.

Exemplos:

assert_entrega_nao_antecede_compra.sql
assert_pedidos_sem_valor_negativo.sql
11.3 Testes genéricos customizados

Listar testes customizados esperados.

Exemplos:

valor_positivo
data_nao_futura
11.4 Testes com packages

Listar testes de packages, quando aplicável.

Exemplos:

dbt_utils.unique_combination_of_columns
12. Estratégia incremental

Preencher apenas se o modelo for incremental.

| Item                           | Definição                      |
| ------------------------------ | ------------------------------ |
| Modelo incremental?            | `<sim/não>`                    |
| Chave única                    | `<coluna>`                     |
| Coluna de controle incremental | `<coluna de data/hora>`        |
| Estratégia                     | `<append/merge/delete+insert>` |
| Comportamento em full-refresh  | `<descrição>`                  |


Descrever a regra incremental.

Exemplo:

O modelo deve processar apenas pedidos com data_compra maior que a maior data_compra já existente no destino. Em caso de full-refresh, toda a tabela será reconstruída.

13. Critérios de aceite

A implementação será considerada aceita quando:

 o modelo SQL existir no diretório correto;
 a materialização estiver configurada corretamente;
 o modelo respeitar o grão definido;
 as colunas obrigatórias estiverem presentes;
 os testes genéricos esperados estiverem implementados;
 os testes singulares esperados estiverem implementados, quando aplicável;
 a documentação YAML estiver preenchida;
 dbt build --select <nome_do_modelo> executar com sucesso;
 a validação estiver registrada em sdd/validacoes/.
14. Observações

Registrar decisões, dúvidas, limitações ou pontos de atenção relacionados ao modelo.

Exemplos:

campo pode conter nulos na origem;
regra de negócio assumida por falta de documentação da fonte;
teste será implementado em fase posterior;
modelo será inicialmente table e poderá evoluir para incremental.