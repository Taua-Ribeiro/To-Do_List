from src.repositorios.UsuarioRepository import UsuarioRepository
from src.model.Usuario import Usuario
import pytest
from faker import Faker
from src.config.db_config import conectar
from src.scripts.clear_scripts import CLEAR_SCRIPTS

    
moker = Faker()

def edit_func(u: Usuario) -> Usuario:
    u.nome = moker.name()
    u.email = moker.email()
    u.senha = moker.password()


TEST_CASE = [Usuario(moker.name(), moker.email(), moker.password()) for _ in range(10)]
EDIT_CASE = map(edit_func, TEST_CASE)

@pytest.mark.parametrize("usuario", TEST_CASE)
def test_cadastro(usuario: Usuario):
    UsuarioRepository.utilizar_conexao_teste()
    UsuarioRepository.cadastrar_usuario(usuario)

def test_find_all():
    UsuarioRepository.utilizar_conexao_teste()

    resultado = UsuarioRepository.find_usuario()

    def filtro(item: Usuario):
        for linha in resultado:
            if linha == item:
                return True
            
        return False
    


    for linha in resultado:
        resultado = list(filter(filtro, TEST_CASE))

        assert len(resultado) > 0

@pytest.mark.parametrize("email", [u.email for u in TEST_CASE])
def test_find_one(email): 
    UsuarioRepository.utilizar_conexao_teste()

    resultado = UsuarioRepository.find_usuario(email)

    assert resultado in TEST_CASE

def test_clear_data():
    with conectar(True) as con:
        for SCRIPT in CLEAR_SCRIPTS:
            con.cursor().execute(SCRIPT)
            con.commit()