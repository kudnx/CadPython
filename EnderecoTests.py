import unittest
from app import create_app, db
from app.models import Endereco
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class EnderecoModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_CarregaEndereco(self):
        #cria um endereço
        endereco = Endereco(
            pais = 'BR',
            estado = 'MG',
            municipio = 'São João Evangelista',
            CEP = '39705000',
            rua = 'da Copasa',
            numero = '577',
            complemento = 'nenhum',
            id_usuario = 1
        )

        endereco2 = Endereco(
            pais = 'BR',
            estado = 'MG',
            municipio = 'São João Evangelista',
            CEP = '39705000',
            rua = 'da Copasa',
            numero = '577',
            complemento = 'nenhum',
            id_usuario = 1
        )

        db.session.add(endereco)
        db.session.commit

        #carrega endereco usuario
        enderecoBanco = endereco.carregaEnderecoUsuario(1)

        self.assertEqual(endereco2.pais, enderecoBanco.pais, 'O PAIS não é igual!')
        self.assertEqual(endereco2.estado, enderecoBanco.estado, 'O ESTADO não é igual!')
        self.assertEqual(endereco2.municipio, enderecoBanco.municipio, 'O MUNICÍPIO não é igual!')
        self.assertEqual(endereco2.CEP, enderecoBanco.CEP, 'O CEP não é igual!')
        self.assertEqual(endereco2.rua, enderecoBanco.rua, 'O RUA não é igual!')
        self.assertEqual(endereco2.numero, enderecoBanco.numero, 'O NÚMERO não é igual!')
        self.assertEqual(endereco2.complemento, enderecoBanco.complemento, 'O COMPLEMENTO não é igual!')

if __name__ == '__main__':
    unittest.main(verbosity=2)