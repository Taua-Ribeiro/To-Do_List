from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

from sqlalchemy import (
    ForeignKey,
    func
)

from typing_extensions import Annotated

from datetime import datetime

pk = Annotated[int, mapped_column(primary_key= True, autoincrement= True)]
timestamp = Annotated[datetime, mapped_column(nullable= False, server_default= func.current_timestamp())]

class Base(DeclarativeBase):
    pass

class Usuarios(Base):
    __tablename__ = "Usuarios"

    id: Mapped[pk]
    nome: Mapped[str] = mapped_column(unique= True, nullable= False)
    hash_senha: Mapped[str] = mapped_column(nullable= False)

class Tarefas(Base):
    __tablename__ = "Tarefas"

    id: Mapped[pk]
    id_usuario: Mapped[int] = mapped_column(ForeignKey("Usuarios.id"), nullable= False)
    titulo: Mapped[str] = mapped_column(nullable= False)
    descricao: Mapped[str | None] = mapped_column(nullable= True)
    concluido_em: Mapped[timestamp | None]

