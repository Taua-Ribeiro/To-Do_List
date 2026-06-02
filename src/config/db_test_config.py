import sqlite3
from src.config.tables_config import TABLES_SCRIPTS
class ConexaoTeste:
    """
    Classe responsável por realizar a conexão com o banco de dados de testes.
    """

    @staticmethod
    def conectar() -> sqlite3.Connection:
        """
        Retorna um objeto do tipo Connection do banco de dados criado em memória para testes.
        """

        conexao = sqlite3.connect(":memory:")

        conexao.execute("PRAGMA foreign_keys = ON")

        for SCRIPT in TABLES_SCRIPTS:
            conexao.execute(SCRIPT)

        return conexao