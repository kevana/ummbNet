'''
New user tests.
'''

import os
import sys
import unittest
from werkzeug.datastructures import MultiDict
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
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()
        db_insert_all(db)
        db.session.remove()

    def tearDown(self):
        '''Post-test teardown.'''
        db.session.remove()
        db.drop_all()

    def test_user_new_all_instrs(self):
        rv = self.app.get('/users/new')
        self.assertIn('option', rv.data)
        rv = self.app.post('/users/new', data=MultiDict([
                        ('username'    , 'user'),
                        ('email'       , 'user@example.com'),
                        ('password'    , 'password'),
                        ('confirm'     , 'password'),
                        ('first_name'  , 'User'),
                        ('last_name'   , 'Name'),
                        ('nickname'    , 'nickname'),
                        ('instruments' , 'Piccolo'),
                        ('instruments' , 'Flute'),
                        ('instruments' , 'Clarinet'),
                        ('instruments' , 'Alto Sax'),
                        ('instruments' , 'Tenor Sax'),
                        ('instruments' , 'Trumpet'),
                        ('instruments' , 'Mellophone'),
                        ('instruments' , 'Trombone'),
                        ('instruments' , 'Baritone'),
                        ('instruments' , 'Tuba'),
                        ('instruments' , 'Drumline'),
                    ]),
                    follow_redirects=True)
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
