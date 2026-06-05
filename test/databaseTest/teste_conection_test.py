from src.config.db_config import conectar
from uuid import uuid4
from faker import Faker

fake = Faker()

INSERT_DATA = []

for i in range(0,5):
    INSERT_DATA.append((str(uuid4()), f"Usuario{i}", fake.password(), f"usuario{i}@email.com"))


def test_one():
    with conectar(True) as con:
        cursor = con.cursor()
        cursor.executemany("INSERT INTO Usuario(id, nome, senha, email) VALUES(?, ?, ?, ?);", INSERT_DATA)
        con.commit()

def test_two():
    with conectar(True) as con:

        cursor = con.cursor()
        res = cursor.execute("SELECT id, nome, senha, email FROM Usuario;")

        for linha in res.fetchall():
            assert linha in INSERT_DATA
        
        cursor.execute("DELETE FROM Usuario;")

    