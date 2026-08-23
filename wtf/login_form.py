from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=4, message='A senha precisa ter pelo menos 4 dígitos')])