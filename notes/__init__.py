from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gwyn'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MyDatabase.db'
db = SQLAlchemy(app)

from notes.models import User

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load(id):
    return User.query.get(int(id))


from notes import routes