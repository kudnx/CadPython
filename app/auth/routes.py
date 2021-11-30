from app import app
from app import db
from app.auth import bp
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.auth.forms import FormularioLogin
from app.models import Usuario, Endereco
from email_validator import validate_email, EmailNotValidError
from validate_docbr import CPF, PIS
from werkzeug.security import generate_password_hash

@bp.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    formulario = FormularioLogin()
    CUsuario = Usuario()
    if formulario.validate_on_submit():
        try:
            validate_email(formulario.usuario.data)
            usuario = CUsuario.carregaUsuarioPeloEmail(formulario.usuario.data)
        except EmailNotValidError:
            CPFValidate = CPF()
            PISValidate = PIS()
            if CPFValidate.validate(formulario.usuario.data):
                usuario = CUsuario.carregaUsuarioPeloCPF(formulario.usuario.data) 
            elif PISValidate.validate(formulario.usuario.data): 
                usuario = CUsuario.carregaUsuarioPeloPIS(formulario.usuario.data)
            else:
                usuario = None       
        if usuario is None or not usuario.check_password(formulario.senha.data):
            flash('Usuário ou senha inválidos!!')
            return redirect(url_for('auth.entrar'))
        login_user(usuario, remember=formulario.lembreMe.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', titulo='Login', formulario=formulario)

@bp.route('/sair')
def sair():
    logout_user()
    return redirect(url_for('main.index'))