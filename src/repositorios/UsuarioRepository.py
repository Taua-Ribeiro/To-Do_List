from src.model.Usuario import Usuario
from src.config.db_config import conectar
from datetime import datetime
from uuid import uuid4
from sqlite3 import DataError

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
                    resultado = res.fetchone()
                    if resultado:
                        id, nome, senha = resultado

                        #print(repr(Usuario(nome, email, senha, id)))
                        return Usuario(nome, email, senha, id)
                    else: 
                        raise DataError("Usuário não encontrado")
                
                res = cursor.execute("SELECT id, nome, email, senha FROM Usuario")
                
                resultado = list(map(lambda tuple: Usuario(tuple[1], tuple[2], tuple[3], tuple[0]), res.fetchall()))

                return resultado
            except Exception as erro:
                con.rollback()
                raise(erro)

    @classmethod
    def editar_usuario(cls, usuario_editado: Usuario) -> None:
        with conectar(cls._eTeste) as con:
            try:
                cursor = con.cursor()

                # print(len(usuario_editado.id))
                res = cursor.execute("SELECT senha FROM Usuario WHERE (id = ?);",(usuario_editado.id,))

                senha_antiga = res.fetchone()[0]

                # print(senha_antiga)
                cursor.execute("""
                            UPDATE Usuario SET
                            nome = ?,
                            email = ?, 
                            senha = ?, 
                            atualizado_em = ?
                            WHERE (id = ?);
                            """, (usuario_editado.nome, usuario_editado.email, usuario_editado.senha, datetime.now().isoformat(sep=" "), usuario_editado.id))
                
                if senha_antiga != usuario_editado.senha:
                    cursor.execute("INSERT INTO Senhas_Usuario(id, id_usuario, ultima_senha) VALUES(?,?,?)", (str(uuid4()), usuario_editado.id, senha_antiga))

                con.commit()
            except Exception as erro:
                con.rollback()
                raise(erro)
    
    @classmethod
    def remover_usuario(cls, usuario: Usuario) -> None:
        with conectar(cls._eTeste) as con:
            try:
                cursor = con.cursor()

                res = cursor.execute("DELETE FROM Usuario WHERE (id = ?)", (usuario.id,))

                if len(res.fetchall()) == 0:
                    raise DataError("Usuário não encontrado")
                con.commit()
            except Exception as erro:
                con.rollback()
                raise(erro)

    @classmethod
    def find_ultimas_senhas(cls, usuario: Usuario) -> list:
        with conectar(cls._eTeste) as con:
            cursor = con.cursor()

            res = cursor.execute("""
                                 SELECT ultima_senha FROM Senhas_Usuario 
                                 WHERE(id_usuario = ?)  
                                 ORDER BY ultima_senha DESC
                                 LIMIT 5;""", (usuario.id,))

            return list(map(lambda i: i[0], res.fetchall()))
        