import re
from uuid import uuid4, UUID

class Usuario:
    def __init__(self, nome: str, email: str, senha: str, id: str| UUID= None):
        erros = []

        if len(nome.strip()) < 3:
            erros.append(ValueError("Nome não pode ser menor que 3 caractres."))
        
        if not re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",email.strip()):
            erros.append(ValueError("Email inválido"))

        if len(senha) < 8:
            erros.append(ValueError("A senha deve ter no mínimo 8 caracteres"))
        
        if len(erros):
            raise ExceptionGroup("Erro de validação", erros)

        if id:
            self._id = UUID(id)
        else:
            self._id = uuid4()

        self._nome = nome.strip()
        self._email = email.strip().lower()
        self._senha = senha
    
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
    
    @property
    def id(self) -> UUID:
        return self._id      

    def __eq__(self, other):
        return self._id == other._id
    
    def __repr__(self):
        return f'(id: {str(self._id)}, nome: {self._nome}, email: {self.email})'

    
