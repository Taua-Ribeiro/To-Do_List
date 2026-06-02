from src.config.factorys.db_factory import ConectarFactory
from uuid import uuid4
from faker import Faker

con = ConectarFactory.criarConexao(eTeste=True).conectar()
cursor = con.cursor()
fake = Faker()

INSERT_DATA = []

for i in range(0,5):
    INSERT_DATA.append((str(uuid4()), f"Usuario{i}", fake.password(), f"usuario{i}@email.com"))

def test_one():
    cursor.executemany("INSERT INTO Usuario(id, nome, senha, email) VALUES(?, ?, ?, ?)", INSERT_DATA)

def test_two():
    res = cursor.execute("SELECT id, nome, senha, email FROM USUARIO")

    for linha in res.fetchall():
        print(INSERT_DATA)
        print(linha)
        assert linha in INSERT_DATA

    