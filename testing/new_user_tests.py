'''
New user tests.
'''

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
# Nuke the db and create new tables
db.drop_all()
db.create_all()
from views import *
from create_db import *

class NewUserTests(unittest.TestCase):
    '''Create new users.'''
    def setUp(self):
        '''Pre-test setup.'''
        app.config['MAIL_SUPPRESS_SEND'] = True
        self.app = app.test_client()
        db.create_all()
        db_insert_all()

    def tearDown(self):
        '''Post-test teardown.'''
        db.session.remove()
        db.drop_all()

    def test_user_new_all_instrs(self):
        rv = self.app.post('/users/new', data=dict({
                        'username'   : 'user',
                        'email'      : 'user@example.com',
                        'password'   : 'password',
                        'confirm'    : 'password',
                        'first_name' : 'User',
                        'last_name'  : 'Name',
                        'nickname'   : 'nickname',
                        'Piccolo'    : 'True',
                        'Flute'      : 'True',
                        'Clarinet'   : 'True',
                        'Alto Sax'   : 'True',
                        'Tenor Sax'  : 'True',
                        'Trumpet'    : 'True',
                        'Mellophone' : 'True',
                        'Trombone'   : 'True',
                        'Baritone'   : 'True',
                        'Tuba'       : 'True',
                        'Drumline'   : 'True'
                    }), follow_redirects=True)
        self.assertIn('Registration Complete', rv.data)

    def test_user_new_no_instrs(self):
        rv = self.app.post('/users/new', data=dict({
                        'username'   : 'user',
                        'email'      : 'user@example.com',
                        'password'   : 'password',
                        'confirm'    : 'password',
                        'first_name' : 'User',
                        'last_name'  : 'Name',
                        'nickname'   : 'nickname'
                    }), follow_redirects=True)
        self.assertIn('Registration Complete', rv.data)

    def test_user_new_dupl_username(self):
        self.test_user_new_no_instrs()
        rv = self.app.post('/users/new', data=dict({
                        'username'   : 'user',
                        'email'      : 'user@example.com',
                        'password'   : 'password',
                        'confirm'    : 'password',
                        'first_name' : 'User',
                        'last_name'  : 'Name',
                        'nickname'   : 'nickname'
                    }), follow_redirects=True)
        self.assertIn('This username is taken.', rv.data)

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
