from flask import current_app

from app.database import get_session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.models import Usuarios

from app.utils.app_exceptions import ServiceException

import sqlalchemy as db

def create_usuario(nome: str, senha: str):
    with current_app.app_context():
        with get_session() as session:
            hash_senha = generate_password_hash(senha)

            novo_usuario = Usuarios(nome= nome, hash_senha= hash_senha)

            session.add(novo_usuario)

            session.commit()
    
def get_one_usuario(nome: str) -> Usuarios:
    with current_app.app_context():
        with get_session() as session:
            stmt = db.Select(Usuarios).where(Usuarios.nome == nome)

            usuario = session.scalars(stmt).one()

        if usuario is None:
            raise ServiceException('Usuário não encontrado.')
        

def update_usuario():
    pass

def delete_usuario():
    pass