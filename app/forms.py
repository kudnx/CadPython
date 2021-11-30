from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Usuario
from validate_docbr import CPF, PIS
from flask_login import current_user

class FormularioCadastro(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    cpf = StringField("CPF", validators=[DataRequired()])
    pis = StringField("PIS", validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    senha2 = PasswordField(
        'Repita a Senha', validators=[DataRequired(), EqualTo('senha')])
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
    pais = StringField("País", validators=[DataRequired()])
    estado = StringField("Estado", validators=[DataRequired()])
    municipio = StringField("Municipio", validators=[DataRequired()])
    cep = StringField("CEP", validators=[DataRequired()])
    rua = StringField("Rua", validators=[DataRequired()])
    numero = StringField("Número", validators=[DataRequired()])
    complemento = StringField("Complemento")
    cadastrar = SubmitField('Cadastrar')