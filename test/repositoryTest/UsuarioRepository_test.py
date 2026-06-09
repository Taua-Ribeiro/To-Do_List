from src.repositorios.UsuarioRepository import UsuarioRepository
from src.model.Usuario import Usuario
import pytest
from faker import Faker
from src.config.db_config import conectar
from src.scripts.clear_scripts import CLEAR_SCRIPTS
from src.model.DataError import DataError

    
moker = Faker()

def edit_func(u: Usuario) -> Usuario:
    u.nome = moker.name()
    u.email = moker.email()
    u.senha = moker.password()
    return u

def clear_data():
    with conectar(True) as con:
        for SCRIPT in CLEAR_SCRIPTS:
            con.cursor().execute(SCRIPT)
            con.commit()

TEST_CASE = [Usuario(moker.name(), moker.email(), moker.password()) for _ in range(10)]
EDIT_CASE = list(map(edit_func, TEST_CASE))

@pytest.mark.parametrize("usuario", TEST_CASE)
def test_cadastro(usuario: Usuario):
    UsuarioRepository.utilizar_conexao_teste()
    UsuarioRepository.cadastrar_usuario(usuario)
    clear_data()

@pytest.mark.parametrize("lista_test", [(TEST_CASE)])
def test_find_all(lista_test):
    UsuarioRepository.utilizar_conexao_teste()
    
    for linha in lista_test:
        UsuarioRepository.cadastrar_usuario(linha)


    resultado = UsuarioRepository.find_usuario()

    def filtro(item: Usuario):
        for linha in resultado:
            if linha.id == item.id:
                return True
            
        return False

    resultado_filtro = list(filter(filtro, TEST_CASE))

    # print(resultado)

    clear_data()
    assert len(resultado_filtro) > 0

@pytest.mark.parametrize("lista_test", [(TEST_CASE)])
def test_find_one(lista_test):
    UsuarioRepository.utilizar_conexao_teste()

    for linha in lista_test:
        UsuarioRepository.cadastrar_usuario(linha)
 
    for linha in lista_test:
        resultado = UsuarioRepository.find_usuario(linha.email)

        assert resultado in TEST_CASE
    
    clear_data()

@pytest.mark.parametrize("lista_teste,lista_editada", [(TEST_CASE, EDIT_CASE)])
def test_edit(lista_teste, lista_editada):
    UsuarioRepository.utilizar_conexao_teste()

    for linha_original in lista_teste:
        UsuarioRepository.cadastrar_usuario(linha_original)
    
    for linha_editado in lista_editada:
        UsuarioRepository.editar_usuario(linha_editado)
    
    resultado_banco = UsuarioRepository.find_usuario()

    for linha in resultado_banco:
        assert linha in lista_editada
    
    clear_data()

@pytest.mark.parametrize("lista_teste", [(TEST_CASE[0:i]) for i in range(1, len(TEST_CASE)+1)])
def test_delete(lista_teste):
    try:
        with pytest.raises(DataError):
            UsuarioRepository.utilizar_conexao_teste()

            for linha in lista_teste:
                UsuarioRepository.cadastrar_usuario(linha)

            for linha in lista_teste:
                UsuarioRepository.remover_usuario(linha)

                UsuarioRepository.find_usuario(linha.email)
    finally:
        clear_data()

@pytest.mark.parametrize("lista_cadastro,email_test", [(TEST_CASE, moker.email())])
def test_fail_find_one(lista_cadastro, email_test):
    try:
        with pytest.raises(DataError):
            UsuarioRepository.utilizar_conexao_teste()

            for usuario in lista_cadastro:
                UsuarioRepository.cadastrar_usuario(usuario)
            
            UsuarioRepository.find_usuario(email_test)
    finally:     
        clear_data()

@pytest.mark.parametrize("lista_cadastro, usuario_test", [(TEST_CASE, Usuario(moker.name(), moker.email(), moker.password()))])
def test_fail_delete(lista_cadastro, usuario_test):
    try:
        with pytest.raises(DataError):
            UsuarioRepository.utilizar_conexao_teste()

            for usuario in lista_cadastro:
                UsuarioRepository.cadastrar_usuario(usuario)
            
            UsuarioRepository.remover_usuario(usuario_test)
    finally:
        clear_data()
