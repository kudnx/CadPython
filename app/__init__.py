from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.entrar'
login.login_message = 'Por Favor, Faça login para acessar a aplicação!'

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.register import bp as register_bp
app.register_blueprint(register_bp)

from app.main import bp as main_bp
app.register_blueprint(main_bp)
