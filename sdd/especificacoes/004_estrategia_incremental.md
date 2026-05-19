# Especificação 004 — Estratégia Incremental

## 1. Objetivo

Este documento define a estratégia de uso de modelos incrementais no projeto.

O objetivo é estabelecer quando, por que e como um modelo dbt deve ser implementado como incremental, evitando o uso desse recurso apenas como demonstração técnica sem necessidade conceitual.

Neste projeto, modelos incrementais serão utilizados para demonstrar boas práticas de dbt avançado, controle de atualização, definição de chave única, critérios de aceite e validação.

## 2. Princípio geral

A regra principal será:

```text
Um modelo só deve ser incremental quando existir uma justificativa clara de negócio, volume, atualização ou aprendizado técnico.
```

Modelos incrementais não devem ser criados apenas para aumentar a complexidade do projeto.

Eles devem representar cenários em que faz sentido processar apenas dados novos ou alterados.

## 3. Relação entre SDD e incremental

Todo modelo incremental deve possuir uma especificação antes da implementação.

A especificação deve definir:

- motivo para o modelo ser incremental;
- grão do modelo;
- chave única;
- coluna de controle incremental;
- regra de atualização;
- comportamento em execução incremental;
- comportamento em `full-refresh`;
- testes obrigatórios;
- critérios de aceite.

O fluxo esperado será:

```text
Especificação do modelo
    ↓
Definição da estratégia incremental
    ↓
Plano técnico
    ↓
Implementação dbt
    ↓
Testes
    ↓
Validação
```

## 4. Quando usar modelo incremental

Um modelo poderá ser incremental quando atender a pelo menos um dos critérios abaixo:

- representar dados com crescimento ao longo do tempo;
- possuir coluna de data adequada para controle incremental;
- possuir chave única ou chave de negócio clara;
- representar fato, evento ou mart acumulativo;
- ter lógica que se beneficie de processamento parcial;
- demonstrar um padrão útil e reutilizável de dbt avançado.

Exemplos de modelos candidatos:

- `fato_pedidos`;
- `fato_itens_pedido`;
- `mart_vendas_diarias`;
- `mart_vendas_mensais`;
- `mart_desempenho_entregas`.

## 5. Quando não usar modelo incremental

Um modelo não deve ser incremental quando:

- possuir baixo volume e reconstrução simples;
- representar dimensão pequena e estável;
- não possuir coluna confiável de controle incremental;
- não possuir chave única clara;
- depender de muitas atualizações históricas;
- for mais simples e seguro reconstruir tudo;
- a lógica incremental aumentar risco sem benefício real.

Exemplos de modelos que provavelmente não precisam ser incrementais na primeira fase:

- `dim_clientes`;
- `dim_produtos`;
- `dim_vendedores`;
- modelos simples da camada `silver`;
- tabelas pequenas de domínio ou tradução.

## 6. Camadas e incrementalidade

### 6.1 Bronze

A camada `bronze` não será criada pelo dbt neste projeto.

Ela será carregada pela ferramenta de ingestão e preservará os dados próximos da origem.

Portanto, a estratégia incremental do dbt não se aplica diretamente à camada bronze nesta primeira fase.

### 6.2 Silver

A camada `silver` poderá ser inicialmente materializada como `view` ou `table`.

Modelos silver só devem ser incrementais se houver justificativa clara.

Como a silver tem papel de qualificação, limpeza e padronização, a primeira versão do projeto poderá manter os modelos silver como `view` ou `table` para facilitar validação e rastreabilidade.

### 6.3 Gold

A camada `gold` será a principal candidata ao uso de modelos incrementais.

Isso ocorre porque fatos e marts analíticos geralmente representam dados acumulados ao longo do tempo.

Modelos gold candidatos a incremental:

- fatos de pedidos;
- fatos de itens de pedido;
- marts diários;
- marts mensais;
- métricas acumuladas por período.

## 7. Estratégia incremental padrão

A estratégia incremental padrão será baseada em coluna de data.

Exemplo conceitual:

```sql
{% if is_incremental() %}
    where data_compra > (
        select coalesce(max(data_compra), '1900-01-01')
        from {{ this }}
    )
{% endif %}
```

Essa abordagem deve ser usada apenas quando:

- a coluna de data for confiável;
- novos registros sempre possuírem data maior que os registros anteriores;
- não houver necessidade relevante de reprocessar atualizações antigas.

## 8. Chave única

Todo modelo incremental deve definir uma chave única.

Exemplo:

```sql
{{
    config(
        materialized='incremental',
        unique_key='pedido_id'
    )
}}
```

A chave única deve estar alinhada ao grão do modelo.

Exemplos:

- `pedido_id` para uma linha por pedido;
- `pedido_id + item_pedido_id` para uma linha por item de pedido;
- `data_venda` para mart diário;
- `mes_venda` para mart mensal;
- `cliente_id + mes_referencia` para mart mensal por cliente.

Quando a chave for composta, avaliar o uso de surrogate key ou testes com combinação de colunas.

## 9. Coluna de controle incremental

A coluna de controle incremental deve representar o avanço dos dados ao longo do tempo.

Exemplos possíveis:

- `data_compra`;
- `data_aprovacao`;
- `data_entrega_cliente`;
- `data_venda`;
- `mes_venda`;
- `data_referencia`.

Critérios para escolha:

- deve existir no modelo;
- deve ter tipo adequado;
- deve ter baixa ocorrência de nulos;
- deve representar corretamente a entrada de novos dados;
- deve estar documentada na especificação do modelo.

## 10. Atualizações tardias

Atualizações tardias ocorrem quando registros antigos são alterados depois de já terem sido processados.

Exemplo:

- um pedido comprado em janeiro recebe atualização de entrega em fevereiro;
- uma avaliação é registrada depois da entrega;
- um pagamento é ajustado após a compra.

Na primeira fase do projeto, a estratégia incremental poderá ser simplificada.

Entretanto, modelos sujeitos a atualizações tardias devem documentar esse risco.

Possíveis estratégias futuras:

- janela de reprocessamento;
- `delete+insert`;
- `merge`;
- snapshots;
- full-refresh periódico.

## 11. Full-refresh

Todo modelo incremental deve possuir comportamento esperado para `full-refresh`.

O comando:

```bash
dbt build --full-refresh --select <nome_do_modelo>
```

deve reconstruir completamente o modelo.

A especificação do modelo deve indicar:

- se o modelo suporta `full-refresh`;
- quando o `full-refresh` deve ser usado;
- quais riscos existem;
- quais testes devem ser executados após o `full-refresh`.

## 12. Testes obrigatórios para modelos incrementais

Todo modelo incremental deve possuir testes compatíveis com seu grão e criticidade.

Testes esperados:

- `not_null` na chave única;
- `unique` na chave única, quando simples;
- teste de combinação única quando a chave for composta;
- testes de relacionamento com dimensões, quando aplicável;
- testes de métricas não negativas;
- testes de validade da coluna incremental;
- testes singulares para regras críticas.

Exemplo:

```yaml
models:
  - name: fato_pedidos
    columns:
      - name: pedido_id
        tests:
          - not_null
          - unique
```

Para chave composta, avaliar:

```yaml
tests:
  - dbt_utils.unique_combination_of_columns:
      combination_of_columns:
        - pedido_id
        - item_pedido_id
```

## 13. Critérios de aceite para modelo incremental

Um modelo incremental será considerado aceito quando:

- possuir especificação;
- possuir plano técnico;
- justificar o uso de incremental;
- definir chave única;
- definir coluna de controle incremental;
- possuir materialização configurada;
- executar com `dbt build`;
- executar com `dbt build --full-refresh`;
- possuir testes compatíveis com seu grão;
- ter validação registrada;
- documentar riscos de atualização tardia, quando aplicável.

## 14. Modelos candidatos na primeira fase

Na primeira fase, os principais candidatos a modelos incrementais são:

### 14.1 `fato_pedidos`

Motivo:

- representa eventos de pedidos;
- possui data de compra;
- possui chave clara;
- é adequado para demonstrar fato incremental.

Possível chave única:

```text
pedido_id
```

Possível coluna incremental:

```text
data_compra
```

### 14.2 `mart_vendas_diarias`

Motivo:

- representa agregação por dia;
- possui data de referência;
- permite demonstrar incremental em mart analítico.

Possível chave única:

```text
data_venda
```

Possível coluna incremental:

```text
data_venda
```

### 14.3 `mart_vendas_mensais`

Motivo:

- representa agregação por mês;
- permite uso de window functions para comparação mensal;
- permite demonstrar atualização incremental por período.

Possível chave única:

```text
mes_venda
```

Possível coluna incremental:

```text
mes_venda
```

## 15. Riscos e cuidados

Principais riscos da estratégia incremental:

- ignorar registros atualizados tardiamente;
- usar coluna incremental inadequada;
- gerar duplicidade por chave única incorreta;
- aplicar incremental em modelo que deveria ser reconstruído;
- dificultar testes e depuração;
- usar incremental antes de entender bem o grão do modelo.

Para mitigar esses riscos:

- o grão deve estar explícito;
- a chave única deve ser testada;
- a coluna incremental deve ser documentada;
- deve existir validação com execução incremental e `full-refresh`;
- riscos conhecidos devem aparecer na spec do modelo.

## 16. Relação com modelos futuros

A estratégia incremental poderá evoluir em fases futuras.

Possíveis evoluções:

- uso de `merge`, se o banco e o adapter suportarem adequadamente;
- janela de reprocessamento;
- snapshots para histórico de alterações;
- incremental por partição;
- comparação entre execução full e incremental;
- testes automatizados em CI/CD;
- orquestração com Airflow.

Essas evoluções não fazem parte da primeira fase obrigatória.

## 17. Decisão da primeira fase

Na primeira fase, o projeto deverá conter pelo menos um modelo incremental implementado e validado.

Modelo preferencial:

```text
fato_pedidos
```

Modelo adicional recomendado:

```text
mart_vendas_diarias
```

A implementação incremental deve ser simples, documentada e rastreável, priorizando clareza sobre complexidade.
