from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
class FormularioLogin(FlaskForm):
    usuario  = StringField("Usuario", validators=[DataRequired(message='Por Favor, preencha o Campo!')], render_kw={"placeholder": "Usuário, CPF ou PIS"})
    senha    = PasswordField("Senha", validators=[DataRequired(message='Por Favor digite a senha!')])
    lembreMe = BooleanField("Lembre me")
    entrar   = SubmitField("Entrar")