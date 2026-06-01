import sqlite3

class ConexaoTeste:
    """
    Classe responsável por realizar a conexão com o banco de dados de testes.
    """

    @staticmethod
    def conectar() -> sqlite3.Connection:
        """
        Retorna um objeto do tipo Connection do banco de dados criado em memória para testes.
        """

        try:

            conexao = sqlite3.connect(":memory:")

            conexao.cursor().execute("PRAGMA foreign_keys = ON")

            return conexao
        except Exception as e:
            print("Erro ao conectar ao banco de testes: ", e)