from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import Usuario
from validate_docbr import CPF, PIS
from flask_login import current_user

class FormularioCadastro(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(message='Por Favor preencha o Nome!')])
    email = StringField("Email", validators=[DataRequired(message='Por Favor preencha o Email!'), Email()])
    cpf = StringField("CPF", validators=[DataRequired(), Length(min=11, max=11, message='O CPF deve contém 11 dígitos!')], render_kw={"placeholder": "Somente números!"})
    pis = StringField("PIS", validators=[DataRequired(), Length(min=11, max=11, message='O PIS deve contém 11 dígitos!')], render_kw={"placeholder": "Somente números!"})
    senha = PasswordField('Senha', validators=[DataRequired(message='Por Favor preencha a Senha!')])
    senha2 = PasswordField(
        'Repita a Senha', validators=[DataRequired(message='Por Favor preencha a Senha Novamente!'), EqualTo('senha')])
    cadastrar = SubmitField('Cadastrar')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email já cadastrado!!')

    def validate_cpf(self, cpf):
        CPFValidate = CPF()
        if not CPFValidate.validate(cpf.data):
            raise ValidationError('CPF Inválido!!')
        user = Usuario.query.filter_by(CPF=cpf.data).first()
        if user is not None:
            raise ValidationError('CPF já cadastrado!!')

    def validate_pis(self, pis):
        PISValidate = PIS()
        if not PISValidate.validate(pis.data):
            raise ValidationError('PIS Inválido!!')
        user = Usuario.query.filter_by(PIS=pis.data).first()
        if user is not None:
            raise ValidationError('PIS já cadastrado!!')

class FormularioEdicao(FlaskForm):
    nome = StringField("Nome")
    email = StringField("Email", validators=[Email()])
    senhaAntiga = PasswordField('Senha Atual')
    senha = PasswordField('Nova Senha')
    senha2 = PasswordField(
        'Repita a Senha', validators=[EqualTo('senha')])
    atualizar = SubmitField('Atualizar Dados')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user is not None and current_user != user:
            raise ValidationError('Email já cadastrado!!')

class FormularioCadastroEndereco(FlaskForm):
    pais = StringField("País", validators=[DataRequired(message='Por Favor preencha o País!'), Length(min=2, max=2, message='O País deve ser uma SIGLA!')], render_kw={"placeholder": "ex: BR"})
    estado = StringField("Estado", validators=[DataRequired(message='Por Favor preencha o Estado!'), Length(min=2, max=2, message='O Estado deve ser uma SIGLA!')], render_kw={"placeholder": "ex: MG"})
    municipio = StringField("Municipio", validators=[DataRequired(message='Por Favor preencha o Município!')])
    cep = StringField("CEP", validators=[DataRequired(message='Por Favor preencha o CEP!')])
    rua = StringField("Rua", validators=[DataRequired(message='Por Favor preencha o RUA!')])
    numero = StringField("Número", validators=[DataRequired(message='Por Favor preencha o Número!')])
    complemento = StringField("Complemento")
    cadastrar = SubmitField('Cadastrar')