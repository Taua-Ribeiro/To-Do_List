import sqlite3

def conectar() -> sqlite3.Connection:
    """
    Conecta ao banco de dados e retorna um objeto do tipo Connection
    """

    try:

        conexao = sqlite3.connect("../database.db")

        conexao.cursor().execute("PRAGMA foreign_keys = ON")

        return conexao
    except Exception as e:
        print("Um erro ocorreu: ", e)