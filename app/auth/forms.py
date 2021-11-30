from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Usuario
from validate_docbr import CPF, PIS
from flask_login import current_user

class FormularioLogin(FlaskForm):
    usuario  = StringField("Usuario", validators=[DataRequired()])
    senha    = PasswordField("Senha", validators=[DataRequired()])
    lembreMe = BooleanField("Lembre me")
    entrar   = SubmitField("Entrar")