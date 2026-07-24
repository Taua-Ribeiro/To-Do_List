"""Módulo responsável por conter as funções, models e schemas utilizados para a criação do banco de dados.
"""
from sqlalchemy import create_engine, Engine, Connection, text
from sqlalchemy.orm import Session

from flask import g, current_app, Flask

import click

from contextlib import contextmanager
from typing import Iterator

def get_engine() -> Engine:
    """Função responsável por obter a engine do `SQLAlchemy`. Caso :obj:`g` não tenha a instância do objeto :class:`Engine` ela será adicionada ao `g`.
    Essa função não deve ser usada diretamente. Somente através de :func:`get_session` e :func:`get_connection`.

    Returns:
        engine (Engine): Instância do objeto `Engine` que permite criar o objeto de Session para comunicação com o banco de dados.
    """
    if 'engine' not in g:
        g.engine = create_engine(f'sqlite+pysqlite:///{current_app.config["DATABASE"]}', echo=True)

    return g.engine

def remove_engine(e: Exception|None= None):
    """Função que remove a instância do objeto `Engine` do `g`.

    Parameters:
        e (Exception, optional): Não é utilizado pela funcão em si. Só está nela por razões de compatibilidade com o 
        `current_app.teardown_appcontext` do flask.
    """

    g.pop("engine", None)

@contextmanager
def get_session() -> Iterator[Session]:
    """Função responsável por obter a conexão da ORM do `SQLAlchemy`. Sua forma de uso segue a seguinte forma 
    ```python
        with get_session() as session:
            # Código
    ```.

    Yields:
        session (Iterator[Session]): Iterador a ser utilizado com o `with` para ter uma conexão com banco de dados.
    """
    try:
        yield Session(get_engine())
    finally:
        pass

@contextmanager
def get_connection() -> Iterator[Connection]:
    """Função responsável por obter a conexão do `SQLAlchemy`. Ele é utilizado para execcutar scripts SQL direito e sua forma de uso é:
    ```python
    with get_connection() as conn:
        # Código
    
    ```
    """
    try:
        engine = get_engine()

        yield engine.connect()

    except:
        pass

def init_database():
    """Função responsável por inicializar o banco de dados da aplicação. Ela não deve ser usada diretamente,
    ela será utilizada através da função :func:`init_db_cli`
    """
    with current_app.open_resource("./database/schema.sql", "r", "utf-8") as schema:
        with get_connection() as conn:
            conn.execute(text(schema.read()))

@click.command('init-database')
def init_database_cli():
    """Função responsável por criar um comando CLI que será registrado no flask para inicializar o banco de dados.
    
    Forma de utilização do comando via prompt de comando:
        `flask init-database`
    """
    init_database()

    click.echo("Banco de dados inicializado.")
    pass

def init_app(app: Flask):
    """Função responsável por inicializar o app. Ela adiciona o :func:`remove_engine` como comando de destruidor de contexto
    (teardown context) e por registrar o comando de CLI :func:`init_database_cli` ao CLI do flask.

    Params:
        app (:class:`Flask`): Instância da aplicação flask.
    """
    app.teardown_appcontext(remove_engine)

    app.cli.add_command(init_database_cli)