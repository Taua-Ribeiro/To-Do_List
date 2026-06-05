from src.model.Usuario import Usuario
from src.config.db_config import conectar
from datetime import datetime
from uuid import uuid4

class UsuarioRepository:
    _eTeste = False
    
    @classmethod
    def utilizar_conexao_teste(cls):
        cls._eTeste = True

    @classmethod
    def cadastrar_usuario(cls, usuario: Usuario) -> None:
        try:
            with conectar(cls._eTeste) as con:
                cursor = con.cursor()

                
                cursor.execute("INSERT INTO Usuario(id, nome, email, senha) VALUES(?,?,?,?)", (str(usuario.id), usuario.nome, usuario.email, usuario.senha))
                
                con.commit()
        except Exception as erro:
            con.rollback()
            raise(erro)

    @classmethod
    def find_usuario(cls, email: str|None= None):
        with conectar(cls._eTeste) as con:
            try:
                cursor = con.cursor()
                if email:
                    res = cursor.execute("SELECT id, nome, senha FROM Usuario WHERE (email = ?);", (email,))
                    id, nome, senha = res.fetchone()

                    return Usuario(nome, email, senha, id= id)
                
                res = cursor.execute("SELECT id, nome, email, senha FROM Usuario")

                # cursor.execute("DELETE FROM Usuario;")
                print(cursor.execute("SELECT count(*) AS numero_linhas FROM Usuario;").fetchall())
                
                resultado = list(map(lambda tuple: Usuario(tuple[1], tuple[2], tuple[3], id= tuple[0]), res.fetchall()))

                return resultado
            except Exception as erro:
                con.rollback()
                raise(erro)

    @classmethod
    def editar_usuario(cls, usuario_editado: Usuario) -> None:
        with conectar(cls._eTeste) as con:
            try:
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
                    cursor.execute("INSERT INTO Senhas_Usuario(id, id_usuario, ultima_senha) VALUES(?,?,?)", (str(uuid4()), str(usuario_editado.id), senha_antiga))

                con.commit()
            except Exception as erro:
                con.rollback()
                raise(erro)
    
    @classmethod
    def remover_usuario(cls, usuario: Usuario) -> None:
        with conectar(cls._eTeste) as con:
            try:
                cursor = con.cursor()

                cursor.execute("DELETE FROM Usuario WHERE (id = ?)", (usuario.id))

                con.commit()
            except Exception as erro:
                con.rollback()
                raise(erro)

    
        