import sqlite3
from src.config.tables_config import TABLES_SCRIPTS
import os
class ConexaoProducao:
    """
    Classe resposável por fazer a conexão com o banco de dados de produção.
    """


    @staticmethod
    def conectar() -> sqlite3.Connection:
        """
        Conecta ao banco de dados e retorna um objeto do tipo Connection
        """


        conexao = sqlite3.connect("database.db")

        conexao.execute("PRAGMA foreign_keys = ON")


        for SCRIPT in TABLES_SCRIPTS:
            conexao.executemany(SCRIPT)

        conexao.commit()

        return conexao