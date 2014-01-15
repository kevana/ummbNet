'''
Initialize app, db, login_manager, and bcrypt objects
'''

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db',
    SECRET_KEY='Shhhh, this is a secret',
    
    DEBUG=True,
)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)
