"""
Carga dos arquivos CSV da Olist para a camada bronze do PostgreSQL.

Este script faz uma carga simples e reproduzível dos arquivos localizados em
`dados/brutos/` para o schema `bronze`.

Regras da camada bronze:
- preservar os nomes originais das colunas sempre que possível;
- não aplicar regras de negócio;
- não traduzir colunas;
- não deduplicar registros;
- não criar métricas;
- carregar os dados próximos da origem.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


ARQUIVOS_ESPERADOS = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]

SCHEMA_DESTINO = "bronze"


def obter_raiz_projeto() -> Path:
    return Path(__file__).resolve().parents[1]


def carregar_variaveis_ambiente(raiz_projeto: Path) -> None:
    caminho_env = raiz_projeto / ".env"
    load_dotenv(caminho_env)


def obter_variavel_obrigatoria(nome: str) -> str:
    valor = os.getenv(nome)

    if not valor:
        raise ValueError(f"Variável de ambiente obrigatória não encontrada: {nome}")

    return valor


def criar_engine_postgres() -> Engine:
    host = obter_variavel_obrigatoria("POSTGRES_HOST")
    port = obter_variavel_obrigatoria("POSTGRES_PORT")
    database = obter_variavel_obrigatoria("POSTGRES_DB")
    user = obter_variavel_obrigatoria("POSTGRES_USER")
    password = obter_variavel_obrigatoria("POSTGRES_PASSWORD")

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    return create_engine(url)


def validar_arquivos(diretorio_dados: Path) -> None:
    if not diretorio_dados.exists():
        raise FileNotFoundError(f"Diretório de dados não encontrado: {diretorio_dados}")

    arquivos_ausentes = [
        arquivo for arquivo in ARQUIVOS_ESPERADOS
        if not (diretorio_dados / arquivo).exists()
    ]

    if arquivos_ausentes:
        mensagem = "\n".join(f"- {arquivo}" for arquivo in arquivos_ausentes)
        raise FileNotFoundError(
            "Arquivos esperados não encontrados em dados/brutos:\n"
            f"{mensagem}"
        )


def criar_schema_bronze(engine: Engine) -> None:
    with engine.begin() as conexao:
        conexao.execute(text(f"create schema if not exists {SCHEMA_DESTINO};"))


def obter_nome_tabela(nome_arquivo: str) -> str:
    return Path(nome_arquivo).stem


def carregar_csv_para_bronze(engine: Engine, caminho_csv: Path, nome_tabela: str) -> int:
    df = pd.read_csv(caminho_csv)

    df.to_sql(
        name=nome_tabela,
        con=engine,
        schema=SCHEMA_DESTINO,
        if_exists="replace",
        index=False,
        chunksize=10_000,
        method="multi",
    )

    return len(df)


def executar_carga() -> None:
    raiz_projeto = obter_raiz_projeto()
    carregar_variaveis_ambiente(raiz_projeto)

    diretorio_dados = raiz_projeto / "dados" / "brutos"

    print("Iniciando carga da camada bronze.")
    print(f"Diretório de dados: {diretorio_dados}")

    validar_arquivos(diretorio_dados)

    engine = criar_engine_postgres()
    criar_schema_bronze(engine)

    total_tabelas = 0
    total_registros = 0

    for nome_arquivo in ARQUIVOS_ESPERADOS:
        caminho_csv = diretorio_dados / nome_arquivo
        nome_tabela = obter_nome_tabela(nome_arquivo)

        print(f"Carregando {nome_arquivo} em {SCHEMA_DESTINO}.{nome_tabela}...")

        quantidade_registros = carregar_csv_para_bronze(
            engine=engine,
            caminho_csv=caminho_csv,
            nome_tabela=nome_tabela,
        )

        total_tabelas += 1
        total_registros += quantidade_registros

        print(
            f"Tabela {SCHEMA_DESTINO}.{nome_tabela} carregada "
            f"com {quantidade_registros} registros."
        )

    print("Carga da camada bronze finalizada com sucesso.")
    print(f"Total de tabelas carregadas: {total_tabelas}")
    print(f"Total de registros carregados: {total_registros}")


if __name__ == "__main__":
    try:
        executar_carga()
    except Exception as erro:
        print("Erro durante a carga da camada bronze.", file=sys.stderr)
        print(str(erro), file=sys.stderr)
        sys.exit(1)
