# Tarefas 002 — Ingestão da Camada Bronze

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome | Ingestão da camada bronze |
| Tipo | Ingestão |
| Spec relacionada | `sdd/especificacoes/001_arquitetura.md` |
| Plano relacionado | `sdd/planos/002_ingestao_bronze.md` |
| ADR relacionada | `sdd/decisoes/ADR-004-uso-de-ingestao-simples-via-python.md` |
| Status | Em andamento |
| Responsável | Diego Hartwig |

## 2. Objetivo

Organizar as tarefas necessárias para carregar a base pública da Olist no schema `bronze` do PostgreSQL usando um script Python simples, preservando os dados próximos da origem.

## 3. Pré-requisitos

Antes de iniciar esta lista de tarefas, verificar:

- [ ] O PostgreSQL está em execução via Docker Compose.
- [ ] O banco `ecommerce_dw` está acessível.
- [ ] O schema `bronze` existe.
- [ ] O schema `silver` existe.
- [ ] O schema `gold` existe.
- [ ] A pasta `dados/brutos/` existe.
- [ ] Os arquivos CSV da Olist estão em `dados/brutos/`.
- [ ] O `.gitignore` ignora arquivos CSV em `dados/brutos/`.
- [ ] O plano técnico de ingestão bronze existe.
- [ ] A ADR-004 sobre ingestão simples via Python foi registrada.

## 4. Tarefas de validação dos arquivos locais

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

- [ ] Conferir quantidade de arquivos CSV em `dados/brutos/`.
- [ ] Conferir nomes dos arquivos.
- [ ] Conferir se os arquivos não estão vazios.
- [ ] Conferir se os arquivos abrem corretamente.
- [ ] Conferir se os CSVs não aparecem no `git status`.

Comando sugerido:

```powershell
Get-ChildItem dados\brutos
```

## 5. Tarefas de preparação do script

Criar estrutura:

```text
ingestao/
├── carregar_bronze_olist.py
└── README.md
```

Tarefas:

- [ ] Criar pasta `ingestao/`.
- [ ] Criar arquivo `ingestao/carregar_bronze_olist.py`.
- [ ] Criar arquivo `ingestao/README.md`.
- [ ] Criar ou atualizar `requirements.txt`.
- [ ] Adicionar dependências necessárias.

Dependências previstas:

```text
pandas
sqlalchemy
psycopg2-binary
python-dotenv
```

## 6. Tarefas de configuração de ambiente

Variáveis esperadas no `.env`:

```env
POSTGRES_HOST=localhost
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=ecommerce_password
POSTGRES_DB=ecommerce_dw
POSTGRES_PORT=5432
```

Tarefas:

- [ ] Adicionar `POSTGRES_HOST` no `.env`.
- [ ] Adicionar `POSTGRES_HOST` no `.env.example`.
- [ ] Confirmar que `.env` não aparece no Git.
- [ ] Confirmar que `.env.example` está versionado.

## 7. Tarefas de implementação do script

O script deve:

- [ ] Ler variáveis de ambiente com `python-dotenv`.
- [ ] Montar string de conexão PostgreSQL com SQLAlchemy.
- [ ] Validar existência da pasta `dados/brutos/`.
- [ ] Validar existência de todos os arquivos esperados.
- [ ] Ler cada CSV com pandas.
- [ ] Preservar os nomes originais das colunas.
- [ ] Criar/carregar tabelas no schema `bronze`.
- [ ] Usar nome do arquivo sem `.csv` como nome da tabela.
- [ ] Usar carga full com substituição da tabela.
- [ ] Exibir logs simples de início, fim e quantidade de registros.
- [ ] Encerrar com erro claro se algum arquivo esperado não existir.

## 8. Tarefas de execução da ingestão

Comando previsto:

```powershell
python ingestao\carregar_bronze_olist.py
```

Tarefas:

- [ ] Criar ambiente virtual, se necessário.
- [ ] Instalar dependências com `pip install -r requirements.txt`.
- [ ] Executar o script de ingestão.
- [ ] Validar logs no terminal.
- [ ] Corrigir erros, se houver.
- [ ] Reexecutar carga, se necessário.

## 9. Tarefas de validação das tabelas bronze

Após a ingestão, validar tabelas criadas.

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

## 10. Tarefas de contagem de registros

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

## 11. Tarefas de amostragem dos dados

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

## 12. Tarefas de preservação da bronze

Confirmar que a bronze foi mantida próxima da origem.

Tarefas:

- [ ] Confirmar que nomes principais das colunas foram preservados.
- [ ] Confirmar que não houve tradução de colunas para português.
- [ ] Confirmar que não houve filtro analítico.
- [ ] Confirmar que não houve agregação.
- [ ] Confirmar que não houve deduplicação intencional.
- [ ] Confirmar que não houve regra de negócio aplicada.

## 13. Tarefas de validação SDD

Criar registro de validação em:

```text
sdd/validacoes/002_ingestao_bronze.md
```

A validação deve conter:

- data da execução;
- script utilizado;
- arquivos carregados;
- tabelas criadas;
- contagens de registros;
- observações sobre nomes e tipos;
- pendências;
- conclusão.

Tarefas:

- [ ] Criar arquivo de validação.
- [ ] Registrar comando executado.
- [ ] Registrar lista de arquivos CSV.
- [ ] Registrar lista de tabelas bronze.
- [ ] Registrar contagens.
- [ ] Registrar divergências.
- [ ] Registrar conclusão da ingestão.

## 14. Tarefas de versionamento

- [ ] Executar `git status`.
- [ ] Confirmar que os CSVs não aparecem no Git.
- [ ] Confirmar que `.env` não aparece no Git.
- [ ] Versionar script, documentação e configurações.
- [ ] Fazer commit dos arquivos criados.
- [ ] Enviar alterações para o GitHub.

Commit sugerido para atualização do planejamento:

```powershell
git add sdd/planos/002_ingestao_bronze.md sdd/tarefas/002_ingestao_bronze.md
git commit -m "docs: atualiza planejamento da ingestao bronze via python"
git push
```

## 15. Critérios de conclusão

Esta lista de tarefas será considerada concluída quando:

- [ ] os arquivos CSV da Olist estiverem em `dados/brutos/`;
- [ ] os CSVs estiverem ignorados pelo Git;
- [ ] o PostgreSQL estiver em execução;
- [ ] o schema `bronze` existir;
- [ ] o script Python de ingestão existir;
- [ ] as tabelas bronze forem criadas;
- [ ] as contagens forem registradas;
- [ ] amostras forem validadas;
- [ ] a bronze preservar os dados próximos da origem;
- [ ] a validação `sdd/validacoes/002_ingestao_bronze.md` existir;
- [ ] as alterações estiverem versionadas no GitHub.

## 16. Pendências

- [ ] Criar script de ingestão.
- [ ] Executar ingestão.
- [ ] Registrar validação.
- [ ] Iniciar configuração do dbt após carga bronze.

## 17. Observações

A ingestão bronze deve ser simples e rastreável.

A decisão de substituir Airbyte por Python foi tomada para evitar complexidade desnecessária nesta fase e manter o foco do projeto em dbt e SDD.
