from src.model.Usuario import Usuario
from src.config.db_config import conectar
from datetime import datetime
from src.model.DataError import DataError

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

                cursor.execute("""
                            UPDATE Usuario SET
                            nome = ?,
                            email = ?, 
                            senha = ?, 
                            atualizado_em = ?
                            WHERE (id = ?);
                            """, (usuario_editado.nome, usuario_editado.email, usuario_editado.senha, datetime.now().isoformat(sep=" "), usuario_editado.id))
                
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
