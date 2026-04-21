"""Script de migração simples do SensoriPlay.

Uso:
    DATABASE_URL=sqlite:///sensoriplay.db python -m backend.migrate
    # ou, estando em backend/:
    DATABASE_URL=sqlite:///sensoriplay.db python migrate.py

- Cria todas as tabelas declaradas em database.Base (idempotente).
- Para bancos pré-existentes: adiciona colunas faltantes em `orders`
  (`shipping_cost`, `shipping_address`) via ALTER TABLE quando necessário.
"""
from __future__ import annotations

import logging
import os
import sys

# Permitir rodar tanto como módulo (`python -m backend.migrate`) quanto como script
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import inspect, text

import database  # noqa: E402

logger = logging.getLogger("sensoriplay.migrate")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def ensure_order_columns() -> None:
    """Adiciona colunas que podem faltar em instalações antigas."""
    if database.engine is None:
        raise RuntimeError("DATABASE_URL não configurada")

    inspector = inspect(database.engine)
    if "orders" not in inspector.get_table_names():
        # Ainda será criada por create_all — nada a fazer
        return

    existing_cols = {c["name"] for c in inspector.get_columns("orders")}
    dialect = database.engine.dialect.name  # 'sqlite', 'postgresql', etc.

    alter_stmts: list[str] = []
    if "shipping_cost" not in existing_cols:
        alter_stmts.append(
            "ALTER TABLE orders ADD COLUMN shipping_cost NUMERIC(10,2) DEFAULT 0"
        )
    if "shipping_address" not in existing_cols:
        # PostgreSQL aceita TEXT; SQLite também. Usamos TEXT para compatibilidade.
        alter_stmts.append("ALTER TABLE orders ADD COLUMN shipping_address TEXT")

    if not alter_stmts:
        logger.info("Tabela orders já contém todas as colunas esperadas.")
        return

    with database.engine.begin() as conn:
        for stmt in alter_stmts:
            logger.info("Executando: %s", stmt)
            conn.execute(text(stmt))

    logger.info("Migração de colunas em `orders` concluída (dialect=%s).", dialect)


def run() -> None:
    if database.engine is None:
        raise SystemExit(
            "DATABASE_URL não configurada. Defina ex: "
            "DATABASE_URL=sqlite:///sensoriplay.db"
        )

    logger.info("Criando tabelas faltantes (create_all)...")
    database.Base.metadata.create_all(bind=database.engine)

    logger.info("Verificando colunas de orders...")
    ensure_order_columns()

    logger.info("Migração concluída com sucesso. URL=%s", database.DATABASE_URL)


if __name__ == "__main__":
    run()
