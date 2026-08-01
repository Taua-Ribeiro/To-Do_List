class DatabaseException(Exception):
    """Erros relacionados ao banco de dados
    """
    def __init__(self, message, original_error):
        self.original_error = original_error
        super().__init__(message)
