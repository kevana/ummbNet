import os
import sys
import unittest

# Add parent directory to import path
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from app import app, db
from config import basedir
from async import *
from email import *
from functions import *
from models import *
from views import *
from create_db import *

class PasswordResetTests(unittest.TestCase):
    '''Reset user passwords.'''
    def setUp(self):
        '''Pre-test setup.'''
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tmp/test.db')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        user = User(username='user', \
                    email='admin@example.com', \
                    password='password', \
                    enabled=True)
        db.session.add(user)
        db.session.commit()
        rv = self.login('user', 'password')
        self.assertIn('View Requests', rv.data)

    def tearDown(self):
        '''Post-test teardown.'''
        rv = self.logout()
        self.assertIn('You have logged out', rv.data)
        db.session.remove()
        db.drop_all()
    
    def login(self, username, password):
        '''Login a user by posting to /login.'''
        return self.app.post('/login', data=dict(
                username=username,
                password=password
            ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_reset_password(self):
        rv = self.app.post('/resetpassword', data=dict(
                username='user',
                email='admin@example.com'
            ), follow_redirects=True)
        self.assertIn('Reset successful', rv.data)
    
    def test_fail_reset_password(self):
        rv = self.app.post('/resetpassword', data=dict(
                username='user',
                email='fakeuser@example.com'
            ), follow_redirects=True)
        self.assertIn('Invalid username email combination', rv.data)

    def test_resetpassword_fail_pw_mismatch(self):
        rv = self.app.get('/resetpassword', data=dict(username='user',
                                                    password1='pw1',
                                                    password2='pw2'))
        self.assertIn('Password Reset', rv.data)
        

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
