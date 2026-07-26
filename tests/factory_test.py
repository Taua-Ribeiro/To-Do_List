from src import create_app

def test_creation():
    app = create_app()

    assert not app.testing

    test_app = create_app({"TESTING": True})

    assert test_app.testing

