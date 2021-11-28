from app import login, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    CPF = db.Column(db.String(11), index=True, unique=True)
    PIS = db.Column(db.String(11), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self) -> str:
        return '<usuário {}>'.format(self.nome)

    def set_password(self, usuario_password):
        self.password = generate_password_hash(usuario_password)

    def check_password(self, usuario_password):
        return check_password_hash(self.password, usuario_password)

    def carregaUsuarioPeloEmail(self, usuarioData):
        usuario = Usuario.query.filter_by(email=usuarioData).first()
        return usuario

    def carregaUsuarioPeloCPF(self, usuarioData):
        usuario = Usuario.query.filter_by(CPF=usuarioData).first()
        return usuario

    def carregaUsuarioPeloPIS(self, usuarioData):
        usuario = Usuario.query.filter_by(PIS=usuarioData).first()
        return usuario

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pais = db.Column(db.String(2), index=True)
    estado = db.Column(db.String(2), index=True)
    municipio = db.Column(db.String(64), index=True)
    CEP = db.Column(db.String(8), index=True)
    rua = db.Column(db.String(64), index=True)
    numero = db.Column(db.String(64), index=True)
    complemento = db.Column(db.String(64), index=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    def __repr__(self):
        return '<endereco {}>'.format(self.rua)

    def carregaEnderecoUsuario(self, id):
        endereco = Endereco.query.filter_by(id_usuario=id).first()
        return endereco

@login.user_loader
def load_user(id):
    return Usuario.query.get(int(id))