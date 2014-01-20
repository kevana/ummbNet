import os
import unittest

from app import app, db
from config import basedir
from async import *
from email import *
from functions import *
from models import *
from views import *

class NewUserTests(unittest.TestCase):
    def setUp(self):
        '''Pre-test setup.'''
        #app.testing = True
        #app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tmp/test.db')
        #app.config['MAIL_SUPPRESS_SEND'] = True
        self.app = app.test_client()
        #self.app.testing = True
        db.create_all()

    def tearDown(self):
        '''Post-test teardown.'''
        self.logout()
        db.session.remove()
        db.drop_all()

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_newuser(self):
        tpt = Instrument.query.filter_by(name='Trumpet').first()
        rv = self.app.post('/newuser', data=dict(
                        username='user',
                        email='user@example.com',
                        password='password',
                        first_name='User',
                        last_name='Name',
                        nickname='nickname',
                        instruments=[tpt]
                    ), follow_redirects=True)
        self.assertIn('Registration Complete', rv.data)
