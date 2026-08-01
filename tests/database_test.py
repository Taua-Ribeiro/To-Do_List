from app.database import get_session, get_connection
from app.database.models import Usuarios

from flask import g

import sqlalchemy as db
from sqlalchemy.orm import Session
from sqlalchemy import text, select
from sqlalchemy.exc import OperationalError

from app import create_app

import pytest

from app.utils.app_exceptions import DatabaseException

def test_cli_command(runner, monkeypatch):
    class Gravador(object):
        foiChamado = False

    def mock_init():
        Gravador.foiChamado = True

    monkeypatch.setattr("app.database.init_database", mock_init)

    result = runner.invoke(args=["init-database"])


    assert "inicializado" in result.output

    assert Gravador.foiChamado

def test_loaded_data(app):
    with app.app_context():
        with get_connection() as conn:
            result_usuarios = conn.execute(text("""
            SELECT * FROM Usuarios;
            """)).fetchone()

            assert "teste" in result_usuarios

            qtd_tarefas = conn.execute(text("""
            SELECT COUNT(id) FROM Tarefas;
            """)).fetchone()

            assert qtd_tarefas == (2,)

def test_get_session(app):
    with app.app_context():
        with get_session() as session:
            assert type(g.engine) is db.Engine

            assert type(session) is  Session

def test_get_connection(app):
    with app.app_context():
        with get_connection() as conn:
            assert type(g.engine) is db.Engine

            assert type(conn) is db.Connection

def test_database_not_initicialized():
    test_app = create_app({"TESTING": True})

    with pytest.raises(DatabaseException, check= lambda e: type(e.original_error) == OperationalError) as info:
        with test_app.app_context():
            with get_session():

                print("Código qualquer")

    assert info.type is DatabaseException
    assert "Banco de dados não inicializado!" in info.value.args[0]