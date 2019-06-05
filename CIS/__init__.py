from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

app.config['SECRET_KEY'] = '815a75a147ef418a6c19ba63958249a5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

from CIS import routes
