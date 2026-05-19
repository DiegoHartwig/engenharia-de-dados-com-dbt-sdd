# Plano Técnico 001 — Configuração Inicial do Projeto

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome do plano | Configuração inicial do projeto |
| Tipo | Configuração |
| Relacionado à spec | `sdd/especificacoes/000_visao_geral.md` |
| Status | Rascunho |
| Responsável | Diego Hartwig |

## 2. Objetivo do plano

Este plano define as etapas técnicas iniciais para preparar o projeto de Engenharia de Dados com dbt e SDD.

O objetivo é criar uma base local funcional para desenvolvimento, contendo:

- estrutura organizada do repositório;
- documentação SDD inicial;
- PostgreSQL via Docker;
- schemas principais do projeto;
- organização dos dados brutos;
- preparação para ingestão com Airbyte;
- preparação para configuração futura do dbt.

## 3. Escopo

Este plano cobre:

- validação da estrutura inicial do repositório;
- criação ou revisão do `docker-compose.yml`;
- criação do `.env.example`;
- configuração do PostgreSQL local;
- criação dos schemas `bronze`, `silver` e `gold`;
- organização da pasta de dados;
- definição da estratégia inicial de ingestão;
- preparação para configuração do dbt.

## 4. Fora de escopo

Este plano não cobre:

- criação dos modelos dbt;
- implementação de testes dbt;
- criação de modelos incrementais;
- criação de dashboards;
- orquestração com Airflow;
- uso de Spark;
- uso de Trino;
- uso de IA ou RAG;
- configuração de CI/CD.

## 5. Dependências

| Tipo | Nome | Descrição |
|---|---|---|
| Ferramenta | Docker | Necessário para executar PostgreSQL localmente |
| Ferramenta | Docker Compose | Necessário para subir os serviços locais |
| Banco | PostgreSQL | Banco de dados usado para bronze, silver e gold |
| Dataset | Olist | Base pública usada como cenário do projeto |
| Ferramenta | Airbyte | Ferramenta prevista para ingestão dos arquivos na bronze |
| Ferramenta | Git | Controle de versão |
| Ferramenta | GitHub | Repositório remoto do projeto |

## 6. Estrutura esperada do repositório

A estrutura inicial esperada é:

```text
engenharia-de-dados-com-dbt-sdd/
├── dados/
│   └── brutos/
├── dbt/
├── documentacao/
├── sdd/
│   ├── decisoes/
│   ├── especificacoes/
│   ├── planos/
│   ├── tarefas/
│   ├── templates/
│   ├── validacoes/
│   ├── constituicao.md
│   └── fluxo_sdd.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── LICENSE
└── README.md
```

## 7. Arquivos que serão criados ou alterados

| Arquivo | Ação | Descrição |
|---|---|---|
| `docker-compose.yml` | criar ou revisar | Configuração do PostgreSQL local |
| `.env` | criar ou revisar | Exemplo de variáveis de ambiente |
| `.gitignore` | criar ou revisar | Arquivos e pastas ignorados pelo Git |
| `README.md` | revisar | Documentação inicial do projeto |
| `dados/brutos/` | criar | Pasta local para armazenar arquivos CSV da Olist |
| `sdd/tarefas/001_configuracao_inicial.md` | criar | Lista de tarefas deste plano |

## 8. Estratégia de infraestrutura local

A infraestrutura local da primeira fase será simples.

Serviços previstos:

```text
PostgreSQL
```

O PostgreSQL será usado para armazenar os schemas:

```text
bronze
silver
gold
```

A ingestão será feita posteriormente com Airbyte, carregando os arquivos da Olist diretamente no schema `bronze`.

## 9. Estratégia do PostgreSQL

O PostgreSQL deverá ser executado via Docker Compose.

Configurações esperadas:

| Item | Valor sugerido |
|---|---|
| Container | `engenharia_dados_dbt_postgres` |
| Banco | `ecommerce_dw` |
| Usuário | `ecommerce_user` |
| Porta | `5432` |
| Schemas | `bronze`, `silver`, `gold` |

Os dados do PostgreSQL devem ser persistidos em volume Docker.

## 10. Estratégia de schemas

Os schemas do banco serão:

```sql
create schema if not exists bronze;
create schema if not exists silver;
create schema if not exists gold;
```

Responsabilidades:

- `bronze`: dados ingeridos próximos da origem;
- `silver`: dados tratados pelo dbt;
- `gold`: dados analíticos gerados pelo dbt.

## 11. Estratégia dos dados brutos

Os arquivos da Olist deverão ser armazenados localmente em:

```text
dados/brutos/
```

A pasta deve ser ignorada pelo Git para evitar versionar arquivos CSV grandes ou sujeitos a licença externa.

Exemplo esperado no `.gitignore`:

```text
dados/brutos/*.csv
dados/brutos/*.zip
```

## 12. Estratégia de ingestão

A ingestão será feita com Airbyte em uma etapa posterior.

Decisão inicial:

```text
CSV Olist → Airbyte → PostgreSQL schema bronze
```

A camada `bronze` deve receber os dados o mais próximo possível da origem.

Não devem ser aplicadas transformações analíticas na ingestão.

## 13. Estratégia inicial do dbt

O projeto dbt será configurado após a validação do PostgreSQL e da ingestão.

Na configuração inicial do dbt, deverão ser criados:

- `dbt_project.yml`;
- profile para PostgreSQL;
- estrutura de modelos;
- sources apontando para o schema `bronze`;
- pastas `models/sources`, `models/silver`, `models/gold`, `tests`, `macros`, `seeds` e `snapshots`.

## 14. Critérios de aceite

Este plano será considerado concluído quando:

- [ ] a estrutura inicial de pastas estiver organizada;
- [ ] a pasta duplicada `especificacoes/` fora de `sdd/` não existir;
- [ ] o `docker-compose.yml` existir;
- [ ] o `.env.example` existir;
- [ ] o `.gitignore` ignorar os arquivos de dados brutos;
- [ ] o PostgreSQL subir localmente via Docker Compose;
- [ ] for possível conectar no banco `ecommerce_dw`;
- [ ] os schemas `bronze`, `silver` e `gold` forem criados;
- [ ] a pasta `dados/brutos/` estiver pronta para receber os CSVs da Olist;
- [ ] a lista de tarefas correspondente existir;
- [ ] as alterações estiverem versionadas no GitHub.

## 15. Riscos e cuidados

Principais riscos:

- conflito de porta local `5432`;
- Docker Desktop não estar ativo no Windows;
- credenciais divergentes entre `.env`, Docker e ferramentas externas;
- arquivos CSV serem versionados por engano;
- Airbyte não conseguir acessar o PostgreSQL por configuração de rede;
- misturar responsabilidades de ingestão e transformação.

Cuidados:

- manter `.env` fora do Git;
- manter `.env.example` versionado;
- validar conexão com PostgreSQL antes de configurar Airbyte;
- documentar qualquer mudança relevante;
- manter a bronze sem transformação analítica.

## 16. Pendências

- [ ] Validar se o Docker Desktop está funcionando no Windows.
- [ ] Confirmar se a porta `5432` está livre.
- [ ] Baixar a base pública da Olist.
- [ ] Definir forma final de execução do Airbyte local.
- [ ] Criar tarefas detalhadas da configuração inicial.

## 17. Observações

Este plano representa a ponte entre a fase de documentação SDD e a fase prática de infraestrutura local.

Após sua conclusão, o projeto estará pronto para iniciar a ingestão dos dados e a configuração do dbt.
