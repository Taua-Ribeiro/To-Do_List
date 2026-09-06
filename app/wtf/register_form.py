from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired(message="Login é obrigatório!")])
    senha = PasswordField("Senha", validators=[DataRequired(message="Senha é obrigatória!"),
                                             Length(min= 4, message="A senha deve ter no mínimo 4 caracteres!")])
    confirmacao = PasswordField("Confirme a senha", validators=[EqualTo("senha", message="Não é igual a senha definida!")])
    submit = SubmitField("Registrar")
