# Tarefas: <nome_do_item>

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome | `<nome_do_item>` |
| Tipo | `<configuração/camada/modelo/teste/macro/documentação>` |
| Spec relacionada | `<caminho_da_spec>` |
| Plano relacionado | `<caminho_do_plano>` |
| Status | `<não iniciado/em andamento/concluído>` |
| Responsável | `<nome>` |

## 2. Objetivo

Descrever brevemente o objetivo desta lista de tarefas.

Exemplo:

> Organizar as tarefas necessárias para implementar o modelo `silver_pedidos`, incluindo SQL, documentação, testes e validação.

## 3. Pré-requisitos

Antes de iniciar esta lista de tarefas, verificar:

- [ ] A constituição do projeto foi consultada.
- [ ] O fluxo SDD foi consultado.
- [ ] A especificação correspondente existe.
- [ ] O plano técnico correspondente existe.
- [ ] As dependências técnicas estão disponíveis.
- [ ] O ambiente local está funcionando.

## 4. Tarefas de especificação

- [ ] Criar ou revisar a especificação relacionada.
- [ ] Confirmar objetivo do item.
- [ ] Confirmar camada de destino.
- [ ] Confirmar grão esperado, quando aplicável.
- [ ] Confirmar fontes ou modelos de entrada.
- [ ] Confirmar regras de negócio.
- [ ] Confirmar regras de qualidade.
- [ ] Confirmar testes dbt esperados.
- [ ] Confirmar critérios de aceite.

## 5. Tarefas de planejamento técnico

- [ ] Criar ou revisar o plano técnico.
- [ ] Confirmar arquivos que serão criados ou alterados.
- [ ] Confirmar estratégia SQL.
- [ ] Confirmar estratégia de materialização.
- [ ] Confirmar estratégia incremental, se aplicável.
- [ ] Confirmar estratégia de testes.
- [ ] Registrar riscos e cuidados conhecidos.
- [ ] Registrar pendências conhecidas.

## 6. Tarefas de implementação dbt

- [ ] Criar ou alterar o modelo SQL.
- [ ] Usar `source()` para tabelas da camada bronze, quando aplicável.
- [ ] Usar `ref()` para dependências entre modelos dbt.
- [ ] Aplicar nomes de colunas em português a partir da camada silver.
- [ ] Aplicar casts necessários.
- [ ] Aplicar regras de transformação previstas.
- [ ] Aplicar regras de negócio previstas.
- [ ] Garantir que o modelo respeita o grão definido.
- [ ] Configurar a materialização correta.
- [ ] Configurar incremental, se aplicável.

## 7. Tarefas de documentação dbt

- [ ] Criar ou atualizar arquivo YAML do modelo.
- [ ] Adicionar descrição do modelo.
- [ ] Adicionar descrição das principais colunas.
- [ ] Documentar chave primária ou chave de negócio.
- [ ] Documentar relacionamentos relevantes.
- [ ] Documentar regras de negócio importantes.
- [ ] Documentar testes associados.

## 8. Tarefas de testes dbt

### 8.1 Testes genéricos nativos

- [ ] Adicionar testes `not_null`.
- [ ] Adicionar testes `unique`.
- [ ] Adicionar testes `accepted_values`.
- [ ] Adicionar testes `relationships`.

### 8.2 Testes singulares

- [ ] Criar testes singulares necessários em `dbt/tests/`.
- [ ] Garantir que cada teste singular representa uma regra de negócio ou qualidade.
- [ ] Nomear testes singulares em português.
- [ ] Validar se o teste retorna apenas registros inválidos.

### 8.3 Testes genéricos customizados

- [ ] Criar macro de teste customizado, se necessário.
- [ ] Documentar o objetivo do teste customizado.
- [ ] Aplicar o teste customizado no YAML.
- [ ] Validar funcionamento do teste customizado.

### 8.4 Testes com packages

- [ ] Avaliar necessidade de package, como `dbt_utils`.
- [ ] Adicionar package, se necessário.
- [ ] Executar `dbt deps`, se aplicável.
- [ ] Aplicar testes do package, se fizer sentido.

## 9. Tarefas de validação

- [ ] Executar `dbt debug`, quando aplicável.
- [ ] Executar `dbt run --select <seletor>`.
- [ ] Executar `dbt test --select <seletor>`.
- [ ] Executar `dbt build --select <seletor>`.
- [ ] Corrigir erros encontrados.
- [ ] Confirmar que os testes esperados passaram.
- [ ] Confirmar que o modelo respeita os critérios de aceite.
- [ ] Registrar validação em `sdd/validacoes/`.

## 10. Tarefas de revisão

- [ ] Revisar SQL para clareza e legibilidade.
- [ ] Verificar se não há transformação fora da camada correta.
- [ ] Verificar se nomes seguem as convenções do projeto.
- [ ] Verificar se a documentação está coerente com a implementação.
- [ ] Verificar se as specs continuam alinhadas ao código.
- [ ] Verificar se o plano técnico foi seguido.
- [ ] Verificar se há necessidade de ADR.

## 11. Critérios de conclusão

Esta lista de tarefas será considerada concluída quando:

- [ ] a especificação estiver atualizada;
- [ ] o plano técnico estiver atualizado;
- [ ] os arquivos dbt previstos estiverem implementados;
- [ ] a documentação YAML estiver preenchida;
- [ ] os testes previstos estiverem implementados;
- [ ] `dbt build --select <seletor>` executar com sucesso;
- [ ] a validação estiver registrada;
- [ ] não houver pendências críticas abertas.

## 12. Pendências

- [ ] `<pendência>`

## 13. Observações

Registrar observações adicionais, decisões locais ou dúvidas encontradas durante a execução.