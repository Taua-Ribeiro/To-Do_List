import sqlite3
from src.scripts.tables_scripts import TABLES_SCRIPTS
from contextlib import contextmanager

@contextmanager
def conectar(eTeste: bool = False):
    database = "test.db" if eTeste else "database.db"

    conexao = sqlite3.connect(database, uri= eTeste)

    conexao.execute("PRAGMA foreign_keys = ON")

    for SCRIPT in TABLES_SCRIPTS:
        conexao.execute(SCRIPT)

    yield conexao

    conexao.close()