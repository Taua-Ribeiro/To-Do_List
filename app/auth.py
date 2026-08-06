import functools

from flask import (
    Blueprint,
    g,
    request,
    session,
    flash,
    redirect,
    render_template,
    url_for,
    abort
)

from app.database import get_session

from sqlalchemy import select

from app.services.usuario_service import create_usuario

bp = Blueprint('auth', __name__, url_prefix='/auth')

def requer_login(view):
    @functools.wraps(view)
    def wrapper(**kwargs):
        return redirect('auth.login') if g.usuario is None else view(**kwargs)

    return wrapper

@bp.before_app_request
def carregar_usuario_logado():
    id_usuario = session.id_usuario

    if id_usuario is None:
        g.usuario = None
    else:
        from app.database.models import Usuarios
        with get_session() as session:
            stmt = select(Usuarios).where(Usuarios.id == id_usuario)

            g.usuario = session.scalars(stmt).one()

@bp.route('/register', methods=['GET', 'POST'])
def resgister():
    method = request.method

    if method == 'POST':
        login = request.form["login"]
        senha = request.form["senha"]
        confirmacao = request.form["confirmacao"]

        error = []

        if login is None:
            error.append("Login é necessário!")

        if senha is None:
            error.append("Senha é necessária!")

        if len(senha) < 4:
            error.append("A senha precisa ter pelo menos 4 caracters!")

        if senha != confirmacao:
            error.append("A senha não é igual à confirmação da senha!")

        if len(error) > 0:
            create_usuario(login, senha)

            flash("Usuário creado com sucesso!", "sucesso")

            return redirect(url_for('auth.login'))
    elif method != "GET":
        return abort(405, f'Método {method} não é permitido!')
    
    return render_template('auth/templates/register.html', error=error)