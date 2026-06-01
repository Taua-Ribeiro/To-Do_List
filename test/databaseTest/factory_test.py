from src.config.factorys.db_factory import ConectarFactory
from src.config.db_test_config import ConexaoTeste
from src.config.db_config import ConexaoProducao

class TestClass:

    def test_conexao_teste(self):
        assert ConectarFactory.criarConexao(True) is ConexaoTeste
    
    def test_conexao_producao(self):
        assert ConectarFactory.criarConexao() is ConexaoProducao
