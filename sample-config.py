'''
Contains configuration directives for Flask and its plugins
'''

# Flask.session
SECRET_KEY='Shhhh, this is a secret'

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db'

# Flask-Mail
MAIL_SERVER = 'smtp.example.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'noreply@example.com'
MAIL_PASSWORD = 'examplePassword'

# administrator list
ADMINS = ['admin@example.com']

# Development
DEBUG=True
