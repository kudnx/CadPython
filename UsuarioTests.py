import unittest
from app import app, db
from app.models import Usuario

class UsuarioModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_CarregaUsuarioPeloEmail(self):
        #cria um usuário
        usuario = Usuario(
            nome='kud',
            email='kud@gmail.com',
            CPF='46894451095',
            PIS='08821234035'
        )
        usuario.set_password('cat')
        usuario2 = Usuario(
            nome='kud',
            email='kud@gmail.com',
            CPF='46894451095',
            PIS='08821234035'
        )
        usuario.set_password('dog')
        db.session.add(usuario)
        db.session.commit

        #carrega o usuario
        usuarioBanco = usuario.carregaUsuarioPeloEmail('kud@gmail.com')

        #verifica o usuário
        self.assertEqual(usuario2.nome, usuarioBanco.nome, 'O NOME do Usuário Não é igual!')
        self.assertEqual(usuario2.email, usuarioBanco.email, 'O EMAIL do Usuário Não é igual!')
        self.assertEqual(usuario2.CPF, usuarioBanco.CPF, 'O CPF do Usuário Não é igual!')
        self.assertEqual(usuario2.PIS, usuarioBanco.PIS, 'O PIS do Usuário Não é igual!')

    def test_CarregaUsuarioPeloCPF(self):
        #cria um usuário
        usuario = Usuario(
            nome='kud',
            email='kud@gmail.com',
            CPF='46894451095',
            PIS='08821234035'
        )
        usuario.set_password('cat')
        usuario2 = Usuario(
            nome='kud',
            email='kud@gmail.com',
            CPF='46894451095',
            PIS='08821234035'
        )
        usuario.set_password('dog')
        db.session.add(usuario)
        db.session.commit

        #carrega o usuario
        usuarioBanco = usuario.carregaUsuarioPeloCPF('46894451095')

        #verifica o usuário
        self.assertEqual(usuario2.nome, usuarioBanco.nome, 'O NOME do Usuário Não é igual!')
        self.assertEqual(usuario2.email, usuarioBanco.email, 'O EMAIL do Usuário Não é igual!')
        self.assertEqual(usuario2.CPF, usuarioBanco.CPF, 'O CPF do Usuário Não é igual!')
        self.assertEqual(usuario2.PIS, usuarioBanco.PIS, 'O PIS do Usuário Não é igual!')

    def test_CarregaUsuarioPeloPIS(self):
        #cria um usuário
        usuario = Usuario(
            nome='kud',
            email='kud@gmail.com',
            CPF='46894451095',
            PIS='08821234035'
        )
        usuario.set_password('cat')
        usuario2 = Usuario(
            nome='kud',
            email='kud@gmail.com',
            CPF='46894451095',
            PIS='08821234035'
        )
        usuario.set_password('dog')
        db.session.add(usuario)
        db.session.commit

        #carrega o usuario
        usuarioBanco = usuario.carregaUsuarioPeloPIS('08821234035')

        #verifica o usuário
        self.assertEqual(usuario2.nome, usuarioBanco.nome, 'O NOME do Usuário Não é igual!')
        self.assertEqual(usuario2.email, usuarioBanco.email, 'O EMAIL do Usuário Não é igual!')
        self.assertEqual(usuario2.CPF, usuarioBanco.CPF, 'O CPF do Usuário Não é igual!')
        self.assertEqual(usuario2.PIS, usuarioBanco.PIS, 'O PIS do Usuário Não é igual!')

if __name__ == '__main__':
    unittest.main(verbosity=2)