from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired,Length
from wtforms import SubmitField

class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(message= 'Login é obrigatório!')])
    senha = PasswordField('Senha', validators=[DataRequired(message='A senha é obrigatória'), 
                            Length(min=4, message='A senha precisa ter pelo menos 4 dígitos')])

    submit = SubmitField('Entrar')