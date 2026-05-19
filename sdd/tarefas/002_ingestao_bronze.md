# Tarefas 002 — Ingestão da Camada Bronze

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome | Ingestão da camada bronze |
| Tipo | Ingestão |
| Spec relacionada | `sdd/especificacoes/001_arquitetura.md` |
| Plano relacionado | `sdd/planos/002_ingestao_bronze.md` |
| Status | Não iniciado |
| Responsável | Diego Hartwig |

## 2. Objetivo

Organizar as tarefas necessárias para baixar a base pública da Olist, armazenar os arquivos localmente, preparar a ingestão e carregar os dados no schema `bronze` do PostgreSQL, preservando os dados próximos da origem.

## 3. Pré-requisitos

Antes de iniciar esta lista de tarefas, verificar:

- [ ] O PostgreSQL está em execução via Docker Compose.
- [ ] O banco `ecommerce_dw` está acessível.
- [ ] O schema `bronze` existe.
- [ ] O schema `silver` existe.
- [ ] O schema `gold` existe.
- [ ] A pasta `dados/brutos/` existe.
- [ ] O `.gitignore` ignora arquivos CSV em `dados/brutos/`.
- [ ] O plano técnico de ingestão bronze existe.
- [ ] A decisão ADR-001 sobre uso da bronze como landing zone foi registrada.

## 4. Tarefas de download do dataset

A base pública da Olist deve ser baixada e extraída localmente.

Arquivos esperados:

```text
olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

Tarefas:

- [ ] Acessar a página do dataset público da Olist.
- [ ] Baixar o arquivo compactado da base.
- [ ] Extrair os arquivos CSV.
- [ ] Copiar os CSVs para `dados/brutos/`.
- [ ] Conferir se todos os arquivos esperados existem.
- [ ] Garantir que os arquivos CSV não aparecem no `git status`.
- [ ] Registrar qualquer arquivo ausente ou nome divergente.

## 5. Tarefas de validação dos arquivos locais

Executar conferência local dos arquivos.

Tarefas:

- [ ] Conferir quantidade de arquivos CSV em `dados/brutos/`.
- [ ] Conferir nomes dos arquivos.
- [ ] Conferir se os arquivos não estão vazios.
- [ ] Conferir se os arquivos abrem corretamente em editor ou ferramenta de dados.
- [ ] Conferir se o encoding não apresenta problema visual evidente.
- [ ] Conferir se os separadores foram interpretados corretamente.

Comando sugerido no PowerShell:

```powershell
Get-ChildItem dados\brutos
```

## 6. Tarefas de preparação do destino PostgreSQL

Tarefas:

- [ ] Confirmar que o container `engenharia_dados_dbt_postgres` está em execução.
- [ ] Confirmar conexão com o banco `ecommerce_dw`.
- [ ] Confirmar existência do schema `bronze`.
- [ ] Confirmar usuário e senha de conexão.
- [ ] Confirmar porta local do PostgreSQL.
- [ ] Confirmar se o PostgreSQL poderá ser acessado pela ferramenta de ingestão.

Comando sugerido:

```powershell
docker ps
```

Comando sugerido para conexão:

```powershell
docker exec -it engenharia_dados_dbt_postgres psql -U ecommerce_user -d ecommerce_dw
```

Consulta sugerida:

```sql
select schema_name
from information_schema.schemata
where schema_name = 'bronze';
```

## 7. Tarefas de definição dos nomes das tabelas bronze

As tabelas esperadas na camada bronze são:

```text
bronze.olist_customers_dataset
bronze.olist_geolocation_dataset
bronze.olist_order_items_dataset
bronze.olist_order_payments_dataset
bronze.olist_order_reviews_dataset
bronze.olist_orders_dataset
bronze.olist_products_dataset
bronze.olist_sellers_dataset
bronze.product_category_name_translation
```

Tarefas:

- [ ] Confirmar se a ferramenta de ingestão permite definir os nomes das tabelas.
- [ ] Preservar nomes próximos aos arquivos originais.
- [ ] Evitar tradução de nomes na bronze.
- [ ] Evitar renomeações analíticas na bronze.
- [ ] Registrar divergências de nomes geradas pela ferramenta.

## 8. Tarefas de configuração da ingestão

A estratégia prevista é:

```text
CSV Olist → Airbyte → PostgreSQL bronze
```

Tarefas:

- [ ] Instalar ou subir o Airbyte localmente.
- [ ] Configurar origem dos arquivos CSV.
- [ ] Configurar destino PostgreSQL.
- [ ] Definir database `ecommerce_dw`.
- [ ] Definir schema de destino `bronze`.
- [ ] Definir credenciais de conexão.
- [ ] Testar conexão com origem.
- [ ] Testar conexão com destino.
- [ ] Criar conexão de sincronização.
- [ ] Garantir que a ingestão não aplica transformação analítica.

## 9. Tarefas de execução da ingestão

Tarefas:

- [ ] Executar carga dos arquivos CSV.
- [ ] Acompanhar logs da ingestão.
- [ ] Verificar se a carga finalizou com sucesso.
- [ ] Registrar erros, se houver.
- [ ] Corrigir configuração caso alguma tabela não seja carregada.
- [ ] Reexecutar ingestão se necessário.

## 10. Tarefas de validação das tabelas bronze

Após a ingestão, validar as tabelas criadas.

Consulta sugerida:

```sql
select table_schema, table_name
from information_schema.tables
where table_schema = 'bronze'
order by table_name;
```

Tarefas:

- [ ] Confirmar existência das tabelas no schema `bronze`.
- [ ] Comparar tabelas criadas com lista esperada.
- [ ] Registrar nomes finais das tabelas.
- [ ] Registrar tabelas ausentes, se houver.
- [ ] Registrar tabelas adicionais, se houver.

## 11. Tarefas de contagem de registros

Registrar contagem de registros por tabela.

Consultas sugeridas:

```sql
select count(*) as total_registros
from bronze.olist_orders_dataset;
```

```sql
select count(*) as total_registros
from bronze.olist_customers_dataset;
```

Tarefas:

- [ ] Contar registros de clientes.
- [ ] Contar registros de pedidos.
- [ ] Contar registros de itens de pedido.
- [ ] Contar registros de pagamentos.
- [ ] Contar registros de avaliações.
- [ ] Contar registros de produtos.
- [ ] Contar registros de vendedores.
- [ ] Contar registros de geolocalização.
- [ ] Contar registros de tradução de categorias.
- [ ] Registrar contagens na validação.

## 12. Tarefas de amostragem dos dados

Validar amostras das tabelas carregadas.

Consultas sugeridas:

```sql
select *
from bronze.olist_orders_dataset
limit 10;
```

```sql
select *
from bronze.olist_order_items_dataset
limit 10;
```

Tarefas:

- [ ] Validar amostra de clientes.
- [ ] Validar amostra de pedidos.
- [ ] Validar amostra de itens de pedido.
- [ ] Validar amostra de pagamentos.
- [ ] Validar amostra de avaliações.
- [ ] Validar amostra de produtos.
- [ ] Validar amostra de vendedores.
- [ ] Validar amostra de geolocalização.
- [ ] Validar amostra de tradução de categorias.

## 13. Tarefas de preservação da bronze

Confirmar que a bronze foi mantida próxima da origem.

Tarefas:

- [ ] Confirmar que nomes principais das colunas foram preservados.
- [ ] Confirmar que não houve tradução de colunas para português.
- [ ] Confirmar que não houve filtro analítico.
- [ ] Confirmar que não houve agregação.
- [ ] Confirmar que não houve deduplicação intencional.
- [ ] Confirmar se metadados técnicos foram criados pela ferramenta.
- [ ] Registrar metadados técnicos, se existirem.

## 14. Tarefas de validação SDD

Criar registro de validação em:

```text
sdd/validacoes/002_ingestao_bronze.md
```

A validação deve conter:

- data da execução;
- ferramenta utilizada;
- arquivos carregados;
- tabelas criadas;
- contagens de registros;
- observações sobre nomes e tipos;
- metadados técnicos, se existirem;
- pendências;
- conclusão.

Tarefas:

- [ ] Criar arquivo de validação.
- [ ] Registrar comandos ou passos executados.
- [ ] Registrar lista de arquivos CSV.
- [ ] Registrar lista de tabelas bronze.
- [ ] Registrar contagens.
- [ ] Registrar divergências.
- [ ] Registrar conclusão da ingestão.

## 15. Tarefas de versionamento

- [ ] Executar `git status`.
- [ ] Confirmar que os CSVs não aparecem no Git.
- [ ] Confirmar que `.env` não aparece no Git.
- [ ] Versionar apenas documentos e configurações.
- [ ] Fazer commit da tarefa, plano ou validação.
- [ ] Enviar alterações para o GitHub.

Commit sugerido para esta lista de tarefas:

```powershell
git add sdd/tarefas/002_ingestao_bronze.md
git commit -m "docs: adiciona tarefas da ingestao bronze"
git push
```

## 16. Critérios de conclusão

Esta lista de tarefas será considerada concluída quando:

- [ ] os arquivos CSV da Olist estiverem em `dados/brutos/`;
- [ ] os CSVs estiverem ignorados pelo Git;
- [ ] o PostgreSQL estiver em execução;
- [ ] o schema `bronze` existir;
- [ ] as tabelas bronze forem criadas;
- [ ] as contagens forem registradas;
- [ ] amostras forem validadas;
- [ ] a bronze preservar os dados próximos da origem;
- [ ] a validação `sdd/validacoes/002_ingestao_bronze.md` existir;
- [ ] as alterações documentais estiverem versionadas no GitHub.

## 17. Pendências

- [ ] Baixar a base da Olist.
- [ ] Definir configuração final do Airbyte.
- [ ] Executar ingestão.
- [ ] Registrar validação.
- [ ] Iniciar configuração do dbt após carga bronze.

## 18. Observações

A ingestão bronze deve ser simples e rastreável.

Qualquer dificuldade relevante com Airbyte deverá ser registrada. Caso seja necessário substituir temporariamente a ingestão por outro método, uma nova ADR deverá ser criada explicando a decisão.
