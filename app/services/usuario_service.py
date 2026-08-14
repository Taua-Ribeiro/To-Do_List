from flask import current_app

from app.database import get_session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.models import Usuarios

from app.utils.app_exceptions import ServiceException

import sqlalchemy as db
from sqlalchemy.exc import IntegrityError, NoResultFound

def create_usuario(nome: str, senha: str):
    try:
        with current_app.app_context():
            with get_session() as session:
                hash_senha = generate_password_hash(senha)

                novo_usuario = Usuarios(nome= nome, hash_senha= hash_senha)

                session.add(novo_usuario)

                session.commit()
    except IntegrityError as e:
        raise ServiceException("Usuário já existe!", e)    
def get_one_usuario(nome: str) -> Usuarios:
    try:
        with current_app.app_context():
            with get_session() as session:
                stmt = db.Select(Usuarios).where(Usuarios.nome == nome)

                usuario = session.scalars(stmt).one()

            return usuario
    except NoResultFound as e:
        raise ServiceException("Usuário e/ou senha inválidos!", e)

def update_usuario():
    pass

def delete_usuario():
    pass