from app import app
from app.main import bp
from flask import render_template
from flask_login import current_user, login_required
from app.auth.forms import FormularioLogin
from app.models import Endereco

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    CEndereco = Endereco()
    if not current_user.is_authenticated:
        formulario = FormularioLogin()
        return render_template('main/index.html', titulo='Página Inicial', formulario=formulario)
    endereco = CEndereco.carregaEnderecoUsuario(current_user.id)
    return render_template('main/index.html', titulo='Página Inicial', endereco=endereco is None)
