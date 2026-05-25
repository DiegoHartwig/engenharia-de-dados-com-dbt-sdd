# dbt — Engenharia de Dados com dbt e SDD

Esta pasta contém o projeto dbt responsável pelas transformações das camadas `silver` e `gold`.

## Objetivo

O projeto dbt transforma os dados brutos carregados na camada `bronze` em entidades qualificadas (`silver`) e marts analíticos (`gold`), aplicando regras de negócio, padronização, testes e documentação técnica.

## Arquitetura

```text
PostgreSQL - bronze (ingestão Python)
    ↓
dbt - silver (limpeza, padronização, tipagem)
    ↓
dbt - gold (fatos, dimensões, marts analíticos)
```

## Estrutura de diretórios

```text
dbt/
├── dbt_project.yml         # Configuração principal do projeto dbt
├── README.md               # Este arquivo
├── models/
│   ├── sources/
│   │   └── sources.yml     # Declaração das tabelas bronze como sources
│   ├── silver/
│   │   └── schema.yml      # Documentação dos modelos silver
│   └── gold/
│       └── schema.yml      # Documentação dos modelos gold
├── macros/                 # Macros reutilizáveis
├── seeds/                  # Arquivos CSV para seeds dbt
├── snapshots/              # Snapshots SCD tipo 2
└── tests/                  # Testes singulares
```

## Configuração do ambiente

### 1. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 2. Criar o arquivo profiles.yml

O arquivo `profiles.yml` **não deve ser versionado** no repositório, pois contém credenciais de acesso.

Crie o arquivo manualmente em `~/.dbt/profiles.yml` (caminho padrão do dbt) ou na pasta `dbt/` sem adicioná-lo ao Git.

**Exemplo de conteúdo do profiles.yml** (substitua com suas credenciais reais):

```yaml
engenharia_de_dados_com_dbt_sdd:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: seu_usuario
      password: sua_senha
      port: 5432
      dbname: ecommerce_dw
      schema: silver
      threads: 4
```

Para este projeto local com Docker, os valores esperados são:

```yaml
engenharia_de_dados_com_dbt_sdd:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: ecommerce_user
      password: ecommerce_password
      port: 5432
      dbname: ecommerce_dw
      schema: silver
      threads: 4
```

> As credenciais acima são do ambiente Docker local documentado no `docker-compose.yml`.
> Não utilize essas credenciais em ambientes de produção.

### 3. Validar a configuração

Execute dentro da pasta `dbt/`:

```powershell
dbt debug
```

O comando deve confirmar que a conexão com o PostgreSQL está funcionando.

## Comandos úteis

```powershell
# Validar configuração e conexão
dbt debug

# Parsear o projeto sem executar
dbt parse

# Listar modelos e sources
dbt ls

# Executar todos os modelos
dbt run

# Executar todos os testes
dbt test

# Executar modelos e testes juntos
dbt build

# Executar um modelo específico
dbt run --select nome_do_modelo

# Executar um modelo e seus dependentes
dbt run --select +nome_do_modelo+

# Gerar documentação
dbt docs generate

# Servir documentação no navegador
dbt docs serve
```

## Camada bronze

As tabelas bronze são carregadas via script Python e declaradas como sources em:

```text
dbt/models/sources/sources.yml
```

Tabelas disponíveis:

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

Para referenciar uma tabela bronze em um modelo dbt, use:

```sql
select *
from {{ source('bronze', 'olist_orders_dataset') }}
```

## Convenções do projeto

- Modelos em português do Brasil.
- Nomenclatura: `camada_entidade` ou `tipo_entidade`.
- Silver: limpeza, padronização e qualificação dos dados.
- Gold: fatos, dimensões e marts analíticos.
- Toda implementação relevante deve ter especificação SDD correspondente.

Consulte `sdd/constituicao.md` para os princípios completos do projeto.
