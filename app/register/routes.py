from app import app
from app import db
from app.register import bp
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.register.forms import FormularioCadastro, FormularioEdicao, FormularioCadastroEndereco
from app.auth.forms import FormularioLogin
from app.models import Usuario, Endereco
from email_validator import validate_email, EmailNotValidError
from validate_docbr import CPF, PIS
from werkzeug.security import generate_password_hash

@bp.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    formulario = FormularioCadastro()
    if formulario.validate_on_submit():
        usuario = Usuario(nome=formulario.nome.data, email=formulario.email.data, CPF=formulario.cpf.data, PIS=formulario.pis.data)
        usuario.set_password(formulario.senha.data)
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('register/cadastro.html', titulo='Cadastro', formulario=formulario)

@bp.route('/editar', methods=['GET', 'POST'])
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
                return redirect(url_for('registereditar'))
        current_user.nome = formulario.nome.data
        current_user.email = formulario.email.data
        current_user.senha = usuario.set_password(formulario.senha.data)
        db.session.commit()
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        formulario.nome.data = current_user.nome
        formulario.email.data = current_user.email
    return render_template('register/editar.html', titulo='Edição de dados', formulario=formulario, endereco=endereco2 is None)

@bp.route('/cadastrar_endereco', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    return render_template('register/cadastro_endereco.html', titulo='Cadastro de Endereço', formulario=formulario, endereco=endereco2 is None)

@bp.route('/editar_endereco', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        endereco = CEndereco.carregaEnderecoUsuario(current_user.id)
        formulario.pais.data = endereco.pais
        formulario.estado.data = endereco.estado
        formulario.municipio.data = endereco.municipio
        formulario.cep.data = endereco.CEP
        formulario.rua.data = endereco.rua
        formulario.numero.data = endereco.numero
        formulario.complemento.data = endereco.complemento
    return render_template('register/cadastro_endereco.html', titulo='Cadastro de Endereço', formulario=formulario, endereco=None)