import pytest

def test_cli_command(runner, monkeypatch):
    class Gravador(object):
        foiChamado = False

    def mock_init():
        Gravador.foiChamado = True

    monkeypatch.setattr("app.database.init_database", mock_init)

    result = runner.invoke(args=["init-database"])


    assert "inicializado" in result.output

    assert Gravador.foiChamado

def test_loaded_data(app):
    from app.database import get_connection
    from sqlalchemy import text

    with app.app_context():
        with get_connection() as conn:
            result_usuarios = conn.execute(text("""
            SELECT * FROM Usuarios;
            """)).fetchone()

            assert "test" in result_usuarios

            qtd_tarefas = conn.execute(text("""
            SELECT COUNT(id) FROM Tarefas;
            """)).fetchone()

            assert qtd_tarefas == 2
