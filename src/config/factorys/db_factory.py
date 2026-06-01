from src.config.db_test_config import ConexaoTeste
from src.config.db_config import ConexaoProducao
from sqlite3 import Connection

class ConectarFactory:
    """
    Classe responsável por retornar o tipo de conexão desejda através do método criarConexão
    """
    @staticmethod
    def criarConexao(eTeste: bool= False) -> Connection:
        """
        Retorna um objeto do tipo Connection do banco de dados de produção por padrão. Caso o valor do parámetro "eTeste"
        seja True, ele retornará a conexão do banco de dados de teste.
        """
        if eTeste:
            return ConexaoTeste
        else:
            return ConexaoProducao


