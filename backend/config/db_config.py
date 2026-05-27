import mysql.connector as database
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())

def conectar_db():

    banco = database.connect(
        host=f"{os.getenv("DB_HOST")}",
        user=f"{os.getenv("DB_USER")}",
        password=f"{os.getenv("DB_PASSWORD")}",
        database="todo-database",
    )

    return banco

