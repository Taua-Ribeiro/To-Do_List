from app.services.usuario_service import create_usuario

from app.database import get_connection

from sqlalchemy import text

def test_register_usuario(app):
    with app.app_context():
        create_usuario("novo_usuario", "teste")

        with get_connection() as conn:
            result = conn.execute(text("SELECT * FROM Usuarios WHERE id=2;")).fetchone()

            assert "novo_usuario" == result.nome
            assert "teste" != result.hash_senha




