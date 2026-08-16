from app.database import get_connection

from sqlalchemy import text

from werkzeug.security import check_password_hash

import pytest

def test_register(app, client):
    assert client.get("/auth/register").status_code == 200

    response = client.post("/auth/register", data= {
        "login": "usuario_teste",
        "senha": "12345678",
        "confirmacao": "12345678"
    })

    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        with get_connection() as conn:
            result = conn.execute(text("SELECT * FROM Usuarios WHERE id = 2;")).fetchone()

            assert result.nome == "usuario_teste"
            assert check_password_hash(result.hash_senha, "12345678")

@pytest.mark.parametrize(("login", "senha", "confirmacao", "menssagem"), (

    ('', "senha", "senha", "Login é necessário!"),
    ('                 ', "senha", "senha", "Login é necessário!"),
    ("login_test", "", "", "Senha é necessária!" ),
    ("login_test", "             ", "", "Senha é necessária!" ),
    ("login_test", "s", "s", "A senha precisa ter pelo menos 4 caracters!"),
    ("login_test", "s                      ", "s", "A senha precisa ter pelo menos 4 caracters!"),
    ("login_test", "senha", "outra_senha", "A senha não é igual à confirmação da senha!"),
    ("teste", "1234", "1234", "Usuário já existe!")
))
def test_fail_register(client, login, senha, confirmacao, menssagem):
    assert client.get("/auth/register").status_code == 200

    response = client.post("/auth/register", data= {
        "login": login,
        "senha": senha,
        "confirmacao": confirmacao
    })

    assert menssagem in response.data.decode()
