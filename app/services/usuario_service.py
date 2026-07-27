from sqlalchemy import MetaData, Table

from flask import current_app

from app.database import get_session, load_tables
from werkzeug.security import generate_password_hash, check_password_hash

@load_tables
def create_usuario(nome: str, senha: str):
    with get_session() as session:
        hash_senha = generate_password_hash(senha)

        novo_usuario = Usuarios(nome= nome, hash_senha= hash_senha)

        session.add(novo_usuario)

        session.commit()
    

def get_all_usuarios():
    pass

def get_one_usuario(id: Int):
    pass

def update_usuario():
    pass

def delete_usuario():
    pass