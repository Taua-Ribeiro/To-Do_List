"""Módulo responsável por conter as funções, models e schemas utilizados para a criação do banco de dados.
"""
from sqlalchemy import (
    create_engine,
    Engine,
    Connection,
    text,
    MetaData,
    Table
)

from sqlalchemy.orm import Session

from flask import g, current_app, Flask

import click

from contextlib import contextmanager
from typing import Generator, Any, Callable
from functools import wraps

def _get_engine() -> Engine:
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
def get_session() -> Generator[Session, Any, None]:
    """Função responsável por obter a conexão da ORM do `SQLAlchemy`. Sua forma de uso segue a seguinte forma 
    ```python
        with get_session() as session:
            # Código
    ```.

    Yields:
        session (Generator[Connection, Any, None]): Gerador a ser utilizado com o `with` para ter uma conexão com banco de dados.
    """
    try:
        engine = _get_engine()
        
        yield Session(engine)
    finally:
        pass

@contextmanager
def get_connection() -> Generator[Connection, Any, None]:
    """Função responsável por obter a conexão do `SQLAlchemy`. Ele é utilizado para execcutar scripts SQL direito e sua forma de uso é:
    ```python
    with get_connection() as conn:
        # Código
    ```

    Yields:
        connection (Generator[Connection, Any, None]): Gerador a ser utilizado com o `with` para ter uma conexão mais direta com o banco
        de dados.
    
    """
    try:
        engine = _get_engine()

        yield engine.connect()
    except Exception as e:
        raise(e)

def init_database():
    """Função responsável por inicializar o banco de dados da aplicação. Ela não deve ser usada diretamente,
    ela será utilizada através da função :func:`init_db_cli`
    """
    with current_app.open_resource("./database/schema.sql", "r", "utf-8") as schema:
        statements = [stmt.strip() for stmt in schema.read().split(";") if stmt.strip()]

    with get_connection() as conn:
        for statement in statements:
            conn.execute(text(statement))
        conn.commit()

@click.command('init-database')
def init_database_cli():
    """Função responsável por criar um comando CLI que será registrado no flask para inicializar o banco de dados.
    
    Forma de utilização do comando via prompt de comando:
        `flask init-database`
    """
    init_database()

    click.echo("Banco de dados inicializado.")

def load_tables(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        engine = _get_engine()

        Table("Usuarios", MetaData(), autoload_with= engine)
        Table("Tarefas", MetaData(), autoload_with=engine)

        return engine


    return wrapper


def init_app(app: Flask):
    """Função responsável por inicializar o app. Ela adiciona o :func:`remove_engine` como comando de destruidor de contexto
    (teardown context) e por registrar o comando de CLI :func:`init_database_cli` ao CLI do flask.

    Params:
        app (:class:`Flask`): Instância da aplicação flask.
    """

    app.teardown_appcontext(remove_engine)
    app.cli.add_command(init_database_cli)

