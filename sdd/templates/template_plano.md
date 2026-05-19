# Plano Técnico: <nome_do_item>

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome do plano | `<nome_do_plano>` |
| Tipo | `<configuração/camada/modelo/teste/macro/documentação>` |
| Relacionado à spec | `<caminho_da_spec>` |
| Status | `<rascunho/em execução/concluído>` |
| Responsável | `<nome>` |

## 2. Objetivo do plano

Descrever o objetivo técnico deste plano.

Este campo deve responder:

- o que será implementado;
- por que será implementado;
- qual especificação este plano atende;
- qual resultado técnico é esperado.

## 3. Escopo

Descrever o que está dentro do escopo deste plano.

Exemplos:

- criar modelo SQL;
- criar documentação YAML;
- criar testes dbt;
- criar macro;
- configurar materialização incremental;
- validar execução com `dbt build`.

## 4. Fora de escopo

Descrever explicitamente o que não será tratado neste plano.

Exemplos:

- criação de dashboard;
- orquestração com Airflow;
- uso de IA;
- alteração na ingestão;
- criação de novos modelos não relacionados.

## 5. Dependências

Listar dependências técnicas ou lógicas.

| Tipo | Nome | Descrição |
|---|---|---|
| source | `<nome_da_source>` | `<descrição>` |
| model | `<nome_do_modelo>` | `<descrição>` |
| macro | `<nome_da_macro>` | `<descrição>` |
| seed | `<nome_da_seed>` | `<descrição>` |

## 6. Arquivos que serão criados ou alterados

| Arquivo | Ação | Descrição |
|---|---|---|
| `<caminho_do_arquivo>` | `<criar/alterar/remover>` | `<descrição>` |

Exemplo:

| Arquivo | Ação | Descrição |
|---|---|---|
| `dbt/models/silver/silver_pedidos.sql` | criar | Modelo silver de pedidos |
| `dbt/models/silver/schema.yml` | alterar | Documentação e testes do modelo |
| `dbt/tests/assert_entrega_nao_antecede_compra.sql` | criar | Teste singular de consistência de datas |

## 7. Estratégia de implementação

Descrever como a implementação será feita.

Exemplos:

- criar CTE de origem;
- aplicar casts;
- renomear colunas;
- aplicar deduplicação com `row_number`;
- calcular campos derivados;
- criar joins com dimensões;
- configurar modelo incremental;
- adicionar testes YAML;
- criar testes singulares.

## 8. Estratégia SQL

Quando aplicável, descrever a estratégia SQL.

Exemplos:

- CTEs principais;
- joins necessários;
- filtros;
- agregações;
- window functions;
- tratamento de nulos;
- regras com `case when`;
- estratégia de deduplicação;
- estratégia para evitar duplicidade no grão.

## 9. Estratégia de materialização

Informar a materialização prevista.

| Item | Valor |
|---|---|
| Materialização | `<view/table/incremental/ephemeral>` |
| Justificativa | `<motivo>` |
| Configurações dbt | `<configurações previstas>` |

Exemplo:

```sql
{{
    config(
        materialized='incremental',
        unique_key='pedido_id'
    )
}}
```

## 10. Estratégia incremental

Preencher apenas se houver modelo incremental.

| Item | Valor |
|---|---|
| Chave única | `<coluna>` |
| Coluna incremental | `<coluna>` |
| Regra incremental | `<descrição>` |
| Full-refresh | `<comportamento esperado>` |

Exemplo:

> Processar apenas registros com `data_compra` maior que a maior `data_compra` já existente no destino.

## 11. Estratégia de testes

Listar os testes que serão implementados.

### 11.1 Testes genéricos nativos

- [ ] `not_null`
- [ ] `unique`
- [ ] `accepted_values`
- [ ] `relationships`

### 11.2 Testes singulares

- [ ] `<nome_do_teste>.sql`

### 11.3 Testes genéricos customizados

- [ ] `<nome_do_teste_customizado>`

### 11.4 Testes com packages

- [ ] `<package>.<teste>`

## 12. Critérios de aceite

A implementação será considerada concluída quando:

- [ ] os arquivos previstos forem criados ou alterados;
- [ ] o modelo respeitar a especificação;
- [ ] a materialização estiver correta;
- [ ] os testes previstos estiverem implementados;
- [ ] a documentação YAML estiver preenchida;
- [ ] o comando `dbt build --select <seletor>` executar com sucesso;
- [ ] a validação estiver registrada em `sdd/validacoes/`.

## 13. Riscos e cuidados

Listar riscos técnicos.

Exemplos:

- dados nulos em campos esperados como obrigatórios;
- duplicidade inesperada na origem;
- inconsistência entre datas;
- valores monetários negativos;
- joins que podem alterar o grão;
- estratégia incremental que pode ignorar atualizações tardias.

## 14. Pendências

Listar pendências conhecidas.

- [ ] `<pendência>`

## 15. Observações

Registrar observações adicionais, decisões locais ou dúvidas.