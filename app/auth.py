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
    id_usuario = session.get("id_usuario")

    if id_usuario is None:
        g.usuario = None
    else:
        from app.database.models import Usuarios
        with get_session() as sess:
            stmt = select(Usuarios).where(Usuarios.id == id_usuario)

            g.usuario = sess.scalars(stmt).one()

@bp.route('/register', methods=['GET', 'POST'])
def register():
    method = request.method
    error = []

    if method == 'POST':
        login = request.form["login"].strip()
        senha = request.form["senha"].strip()
        confirmacao = request.form["confirmacao"].strip()

        if not login:
            error.append("Login é necessário!")

        if not senha:
            error.append("Senha é necessária!")

        if len(senha) < 4:
            error.append("A senha precisa ter pelo menos 4 caracters!")

        if senha != confirmacao:
            error.append("A senha não é igual à confirmação da senha!")

        if len(error) == 0:
            create_usuario(login, senha)

            flash("Usuário criado com sucesso!", "sucesso")

            return redirect(url_for('auth.login'))
    elif method != "GET":
        return abort(405, f'Método {method} não é permitido!')

    print(error)
    return render_template('auth/register.html', error=error)

@bp.route("/login", methods=["GET", "POST"])
def login():
    return "Funcionou"