from app import app
from app import db
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import FormularioCadastro, FormularioEdicao, FormularioCadastroEndereco
from app.auth.forms import FormularioLogin
from app.models import Usuario, Endereco
from email_validator import validate_email, EmailNotValidError
from validate_docbr import CPF, PIS
from werkzeug.security import generate_password_hash

@app.route('/')
@app.route('/index')
@login_required
def index():
    CEndereco = Endereco()
    if not current_user.is_authenticated:
        formulario = FormularioLogin()
        return render_template('index.html', titulo='Página Inicial', formulario=formulario)
    endereco = CEndereco.carregaEnderecoUsuario(current_user.id)
    return render_template('index.html', titulo='Página Inicial', endereco=endereco is None)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    formulario = FormularioCadastro()
    if formulario.validate_on_submit():
        usuario = Usuario(nome=formulario.nome.data, email=formulario.email.data, CPF=formulario.cpf.data, PIS=formulario.pis.data)
        usuario.set_password(formulario.senha.data)
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastro.html', titulo='Sign In', formulario=formulario)

@app.route('/editar', methods=['GET', 'POST'])
@login_required
def editar():
    CEndereco = Endereco()
    CUsuario  = Usuario()
    endereco2 = CEndereco.carregaEnderecoUsuario(current_user.id)
    formulario = FormularioEdicao()
    if formulario.validate_on_submit():
        usuario = CUsuario.carregaUsuarioPeloEmail(current_user.email)
        if formulario.senhaAntiga.data != '':
            if not usuario.check_password(formulario.senhaAntiga.data):
                flash('A senha atual é inválida!!')
                return redirect(url_for('editar'))
        current_user.nome = formulario.nome.data
        current_user.email = formulario.email.data
        current_user.senha = usuario.set_password(formulario.senha.data)
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        formulario.nome.data = current_user.nome
        formulario.email.data = current_user.email
    return render_template('editar.html', titulo='Sign In', formulario=formulario, endereco=endereco2 is None)

@app.route('/cadastrar_endereco', methods=['GET', 'POST'])
def cadastrar_endereco():
    CEndereco = Endereco()
    endereco2 = CEndereco.carregaEnderecoUsuario(current_user.id)
    formulario = FormularioCadastroEndereco()
    if formulario.validate_on_submit():
        endereco = Endereco(pais=formulario.pais.data, estado=formulario.estado.data, municipio=formulario.municipio.data,
        CEP=formulario.cep.data, rua=formulario.rua.data, numero=formulario.numero.data, complemento=formulario.complemento.data,
        id_usuario=current_user.id)
        db.session.add(endereco)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastro_endereco.html', titulo='Sign In', formulario=formulario, endereco=endereco2 is None)

@app.route('/editar_endereco', methods=['GET', 'POST'])
def editar_endereco():
    CEndereco = Endereco()
    formulario = FormularioCadastroEndereco()
    if formulario.validate_on_submit():
        endereco = CEndereco.carregaEnderecoUsuario(current_user.id)
        endereco.pais = formulario.pais.data
        endereco.estado = formulario.estado.data
        endereco.municipio = formulario.municipio.data
        endereco.CEP = formulario.cep.data
        endereco.rua = formulario.rua.data
        endereco.numero = formulario.numero.data
        endereco.complemento = formulario.complemento.data
        endereco.id_usuario = current_user.id
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        CEndereco = Endereco()
        endereco = CEndereco.carregaEnderecoUsuario(current_user.id)
        formulario.pais.data = endereco.pais
        formulario.estado.data = endereco.estado
        formulario.municipio.data = endereco.municipio
        formulario.cep.data = endereco.CEP
        formulario.rua.data = endereco.rua
        formulario.numero.data = endereco.numero
        formulario.complemento.data = endereco.complemento
    return render_template('cadastro_endereco.html', titulo='Sign In', formulario=formulario, endereco=endereco is None)
