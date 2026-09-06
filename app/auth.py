import functools

from flask import (
    Blueprint,
    g,
    session,
    flash,
    redirect,
    render_template,
    url_for,
)

from werkzeug.security import check_password_hash

from app.database import get_session
from app.services.usuario_service import create_usuario, get_one_usuario
from app.utils.app_exceptions import ServiceException
from app.wtf.login_form import LoginForm
from app.wtf.register_form import RegisterForm

from sqlalchemy import select

bp = Blueprint('auth', __name__, url_prefix='/auth')

def require_login(view):
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

@bp.route("/auth", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            error = False
            login = form.login.data.strip().lower()
            senha = form.senha.data.strip()
            confirmacao = form.confirmacao.data.strip()

            if login == "" or senha == "":
                error = True
                flash("Login e senha são obrigatórios")
                
            if len(senha) < 4:
                error = True
                flash("A senha deve possuir pelo menos 4 caracteres!", category="error")

            if senha != confirmacao:
                error = True
                flash("A confirmação da senha não é igual a senha inserida!", category="error")
            
            create_usuario(login, senha)

            if not error:
                flash("Usuário registrado com sucesso!", category="success")
                return render_template('auth/login.html')
        except ServiceException as e:
            flash(e.message, category="error")

    return render_template("auth/register.html", form= form)

@bp.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('auth.login'))

@bp.route("/login", methods=["GET", "POST"])
def login():
    form  = LoginForm()

    if form.validate_on_submit():
        try:
            error = False
            login = form.login.data.strip().lower()
            senha = form.senha.data.strip()

            if login == "" or senha == "":
                error = True
                flash("Login e senha são obrigatórios", category="error")

            if len(senha) < 4:
                error = True
                flash("A senha precisa ter no mínimo 4 caracteres!", category="error")

            usuario = get_one_usuario(login)

            if not check_password_hash(usuario.hash_senha, senha):
                error = True
                flash("Usuário e/ou senha inválidos!", category="error")

            if not error:
                # Trocar para renderizar o index
                return render_template('auth/login.html')
        except ServiceException as e:
            flash(e.message, category='error')
    
    return render_template('auth/login.html', form= form)
