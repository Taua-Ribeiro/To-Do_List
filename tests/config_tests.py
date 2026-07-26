import os
import tempfile

import pytest

from src import create_app
from src.database import get_connection, init_database

from flask import Flask, FlaskClient
from sqlalchemy import text

diretorio = os.path.dirname(__file__)
with open(os.path.join(diretorio, "test_data.sql"), mode="r", encoding='utf-8') as f:
    _script_sql = f.read()

@pytest.fixture
def app() -> Flask:
    """Cria uma fixture da aplicação para testes. Criando juntamente o arquivo temporário do banco de dados 
    para testes que é sempre encerrado independentemento do resultado desses testes.

    Yiealds:
        app(:class:`Flask`): Instância da aplicação utilizada para testes.
    """

    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        "TESTING": True,
        "DATABASE": db_path 
    })

    with app.app_context():
        with get_connection() as conn:
            init_database()
            conn.execute(text(_script_sql))

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Cria um cliente de testes para realizar requisições para a aplicação sem a necessidade de rodar ela
    usando `flask run`.

    Returns:
        client (:class:`FlaskClient`): Cliente utilizado para realizar as requisições flask
    """

    return app.test_client()

@pytest.fixture
def runner(app: Flask):

    return app.test_cli_runner()