class AppException(Exception):
    """Classe base para os erros relacionados à aplicação.
    """
    def __init__(self, message: str, original_error: Exception):
            self.original_error = original_error
            self.message = message
            super().__init__(message)
    
class DatabaseException(AppException):
    """Erros relacionados ao banco de dados
    """
    pass

class ServiceException(AppException):
    """Erros relacionados aos services do sistema.
    """
    pass