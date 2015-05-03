'''
Initialize app, db, login_manager, and bcrypt objects
'''

from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from raven.contrib.flask import Sentry


app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)

sentry = Sentry(app, dsn=app.config.get('SENTRY_DSN', None))
