from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
app.config['SECRET_KEY'] = '1786f0c45b7a2c10b359fbed5c0bb4f0'
app.config['UPLOAD_FOLDER'] = 'static/postpics'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# login_manager.login_view = 'homepage'
bootstrap = Bootstrap(app);

from instagram import routes
