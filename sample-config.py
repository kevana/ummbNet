'''
Contains configuration directives for Flask and its plugins
'''

import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Flask.session, CSRF
SECRET_KEY = 'Shhhh, this is a secret'
CSRF_ENABLED = True

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tmp/app.db')

# Flask-Mail
MAIL_SERVER = 'smtp.example.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'noreply@example.com'
MAIL_PASSWORD = 'examplePassword'
MAIL_DEFAULT_SENDER = 'noreply@example.com'

# administrator list
ADMINS = ['admin@example.com']
LOGGING_SENDER = 'server-error@example.com'

# Development
MAIL_SUPPRESS_SEND = True
DEBUG = True
