import re
from uuid import uuid4, UUID
from dataclasses import dataclass, field

@dataclass()
class Usuario:
    _nome: str
    _email: str
    _senha: str
    _id: UUID = field(default_factory = uuid4)

    def __post_init__(self):
        erros = []

        if len(self._nome.strip()) < 3:
            erros.append(ValueError("Nome não pode ser menor que 3 caractres."))
        
        if not re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",self._email.strip()):
            erros.append(ValueError("Email inválido"))

        if len(self._senha) < 8:
            erros.append(ValueError("A senha deve ter no mínimo 8 caracteres"))
        
        if len(erros):
            raise ExceptionGroup("Erro de validação", erros)

        self._id = UUID(self._id) if isinstance(self._id, str) else self._id
            
    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, nome: str) -> None:
        if len(nome.strip()) < 3:
            raise ValueError("Nome não pode ser menor que 3 caractres.")
        
        self._nome = nome.strip()
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, email: str) -> None:
        if not re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",email.strip()):
            raise ValueError("Email inválido")
        
        self._email = email.strip().lower()
    
    @property
    def senha(self) -> str:
        return self._senha
    
    @senha.setter
    def senha(self, senha: str) -> None:
        if len(senha) < 8:
            raise ValueError("A senha deve ter no mínimo 8 caracteres")

        self._senha = senha
    
    @property
    def id(self) -> UUID:
        return str(self._id)
    
    @id.setter
    def id(self, id: str|UUID) -> None:
        if isinstance(id, str):
            id = UUID(id)

        self._id = UUID(id)
