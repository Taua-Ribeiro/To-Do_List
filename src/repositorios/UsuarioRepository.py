from src.model.Usuario import Usuario
from src.config.factorys.db_factory import ConectarFactory
from datetime import datetime
from uuid import uuid4

class UsuarioRepository:
    @staticmethod
    def cadastrar_usuario(usuario: Usuario, eTeste: bool= False) -> None:
        con = ConectarFactory.criarConexao(eTeste).conectar()
        cursor = con.cursor()

        
        cursor.execute("INSERT INTO Usuario(id, nome, email, senha) VALUES(?,?,?,?)", (usuario.id, usuario.nome, usuario.email, usuario.senha))

        con.commit()
        con.close()
    
    @staticmethod
    def find_usuario(usuario: Usuario|None, eTeste: bool= False) -> Usuario|List[Usuario]:
        con = ConectarFactory.criarConexao().conectar(eTeste)
        cursor = con.cursor()

        if usuario:
            res = cursor.execute("SELECT id, nome, email, senha FROM Ususario WHERE (email = ?);", (usuario.email))
            nome, email, senha = res.fetchone()

            return Usuario(nome, email, senha)
        
        res = cursor.execute("SELECT nome, email, senha FROM Usuario")

        return [Usuario(l.nome, l.email, l.senha) for l in res.fetchall()]

    @staticmethod
    def editar_usuario(usuario_editado: Usuario, eTeste: bool= False) -> None:
        con = ConectarFactory.criarConexao(eTeste).conectar()
        cursor = con.cursor()

        res = cursor.execute("SELECT senhaFROM Usuario WHERE (id = ?)",(usuario_editado.id))

        senha_antiga = res.fetchone()[0]

        cursor.execute("""
                       UPDATE USUARIO SET(
                       nome = ?, 
                       email = ?, 
                       senha = ?, 
                       atualizado_em = ?),
                       WHERE (id = ?);
                       """, (usuario_editado.nome, usuario_editado.email, usuario_editado.senha, datetime.now(), usuario_editado.id))
        
        if senha_antiga != usuario_editado.senha:
            cursor.execute("INSERT INTO Senhas_Usuario(id, id_usuario, ultima_senha) VALUES(?,?,?)"(uuid4(), usuario_editado.id, senha_antiga))

        con.commit()
        con.close()

    def remover_usuario(usuario: Usuario, eTeste: bool= False) -> None:
        con = ConectarFactory.criarConexao(eTeste).conectar()
        cursor = con.cursor()

        cursor.execute("DELETE FROM Usuario WHERE (id = ?)", (usuario.id))

        con.commit()
        con.close()

        