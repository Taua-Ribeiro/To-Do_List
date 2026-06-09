from src.repositorios.UsuarioRepository import UsuarioRepository
from src.model.Usuario import Usuario
from src.model.LoginError import LoginError
from src.model.DataError import DataError

class UsuarioService:

    @staticmethod
    def cadastrar(nome: str, email: str, senha: str):
        novo_usuario = Usuario(nome, email, senha)

        UsuarioRepository.cadastrar_usuario(novo_usuario)

    
    @staticmethod
    def login(senha: str, email: str) -> Usuario:
        try:
            usuario = UsuarioRepository.find_usuario(email)

            if usuario.senha == senha.strip():
                return usuario
            else: 
                raise LoginError("Email ou senha inválidas.")
        
        except DataError:
            raise LoginError("Email ou senha inválidas.")

    @staticmethod
    def editar(id_usuario: str, nome: str, email: str, senha: str):
        usuario_editado = Usuario(nome, email, senha, id_usuario)

        UsuarioRepository.editar_usuario(usuario_editado)
    
    @staticmethod
    def deletar(email: str):
        usuario_para_deletar = UsuarioRepository.find_usuario(email)

        UsuarioRepository.remover_usuario(usuario_para_deletar)


