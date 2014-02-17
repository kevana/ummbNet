'''
Event tests for a logged in user.
'''

import os
import re
import sys
import unittest
from datetime import datetime, timedelta

# Add parent directory to import path
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from app import app, db
from async import *
from email import *
from functions import *
from models import *
# Nuke the db and create new tables
db.drop_all()
db.create_all()
from views import *
from create_db import *


class EventTests(unittest.TestCase):
    '''Test route access for a logged in user.'''
    def setUp(self):
        '''Pre-test setup.'''
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False

        self.app = app.test_client()
        db.create_all()
        db_insert_all(db)
        user = User(username='user',
                    email='admin@example.com',
                    password='password',
                    is_admin=True,
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

    def test_create_event(self):
        rv = self.app.get('/events/new')
        self.assertIn('Create a new event', rv.data)
        # Creata a new event
        one_hour = timedelta(hours=1)
        one_week = timedelta(days=7)
        date = datetime.utcnow() + one_week
        calltime = date - one_hour
        #print(rv.data)
        # Post event
        rv = self.app.post('/events/new', data=dict(
            date=date.strftime('%Y-%m-%dT%H:%M'),
            calltime=calltime.strftime('%H:%M'),
            band_id=1,
            event_type_id=1
        ), follow_redirects=True)
        self.assertNotIn('Create a new event', rv.data)
        self.assertIn(calltime.strftime('%H:%M'), rv.data)

    def test_edit_event(self):
        # Create a new event
        one_hour = timedelta(hours=1)
        one_week = timedelta(days=7)
        date = datetime.utcnow() + one_week
        calltime = date - one_hour
        # Post event
        rv = self.app.post('/events/new', data=dict(
            date=date.strftime('%Y-%m-%dT%H:%M'),
            calltime=calltime.strftime('%H:%M'),
            band_id=1,
            event_type_id=1
        ), follow_redirects=True)
        self.assertNotIn('Create a new event', rv.data)
        self.assertIn(calltime.strftime('%H:%M'), rv.data)
        p = re.compile(ur'.*/events/([0-9]+)/edit.*', re.DOTALL)
        m = p.match(rv.data)
        event_id = int(m.group(1))
        # Edit the event
        rv = self.app.get('/events/' + str(event_id) + '/edit')
        self.assertIn('Update event', rv.data)
        date = datetime.utcnow() + one_week + one_week
        calltime = date - one_hour - one_hour
        # Post edits
        rv = self.app.post('/events/1/edit', data=dict(
            event_id=1,
            date=date.strftime('%Y-%m-%dT%H:%M'),
            calltime=calltime.strftime('%H:%M'),
            band_id=1,
            event_type_id=1
        ), follow_redirects=True)
        self.assertIn(calltime.strftime('%H:%M'), rv.data)
    
    @unittest.skip('Unimplemented feature')
    def test_delete_event(self):
        '''Unimplemented feature.'''
        #self.test_create_event()
        

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
