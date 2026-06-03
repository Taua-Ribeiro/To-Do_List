from src.model.Usuario import Usuario
from faker import Faker
import pytest

moker = Faker()

@pytest.mark.parametrize("nome,email,senha",
                         [(moker.name(), moker.email(), moker.password()) for _ in range(0, 10)])
def test_sucesso(nome, email, senha):
    usuario = Usuario(nome, email, senha)

    assert isinstance(usuario, Usuario)

@pytest.mark.parametrize("nome,email,senha",[
    ("Ab", moker.email(), moker.password()),
    ("            Ab               ", moker.email(), moker.password()),
    ("", moker.email(), moker.password()),
    ("Teste", moker.email(), moker.password()),
])
def test_fail_nome(nome, email, senha):
    with pytest.raises((ExceptionGroup, ValueError)):
        novo_usuario = Usuario(nome, email, senha)

        novo_usuario.nome = nome[0:1]

@pytest.mark.parametrize("nome,email,senha",[
    (moker.name(), "ofdkapf", moker.password()),
    (moker.name(), "ofdkapf@", moker.password()),
    (moker.name(), "off.com", moker.password()),
    (moker.name(), "@", moker.password()),
    (moker.name(), "", moker.password()),
    (moker.name(), "                @ofdkapf              ", moker.password()),
    (moker.name(), "           ofdkapf@              ", moker.password())

])
def test_fail_email(nome, email, senha):
    with pytest.raises((ExceptionGroup, ValueError)):
        novo_usuario = Usuario(nome, email, senha)

        novo_usuario.email = email.replace("@", "")

@pytest.mark.parametrize("nome,email,senha",[
    (moker.name(), moker.email(), "adrscfga"),
    (moker.name(), moker.email(), "adrscfg"),
    (moker.name(), moker.email(), "adrscf"),
    (moker.name(), moker.email(), "adrsc"),
    (moker.name(), moker.email(), "adrs"),
    (moker.name(), moker.email(), "adr"),
    (moker.name(), moker.email(), "ad"),
    (moker.name(), moker.email(), "a"),
    (moker.name(), moker.email(), ""),
])
def test_fail_senha(nome, email, senha):
    with pytest.raises((ExceptionGroup, ValueError)):
        novo_usuario = Usuario(nome, email, senha)

        novo_usuario.senha = senha[0:1]
