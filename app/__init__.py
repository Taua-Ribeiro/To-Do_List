from flask import Flask
import os

def create_app(config_test= None):
    """Função responsável por criar a aplicação flask e aplicar as configurações necessárias.

    Args:
        config_test(dict, optional): Dicionário com as configurações de teste a serem utilizadas, geralmente 
        irá conter o {"TESTING": True}. Caso não seja passado será utilizado as configurações padrões.

    """
    app = Flask(__name__, instance_relative_config= True)

    app.config.from_mapping({
        "DATABASE": os.path.join(app.instance_path, "database.sqlite"),
        "SECRET": "DEV"
    })

    if config_test is None:
        app.config.from_pyfile("config.py", silent= True)
    else:
        app.config.from_mapping(config_test)

    os.makedirs('instance', exist_ok= True)
    
    @app.route('/')
    def ola_mundo():
        return 'Olá Mundo'

    return app
