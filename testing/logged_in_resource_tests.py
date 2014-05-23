'''
Route access tests for (non-admin) logged-in users.
'''

import os
import sys
import unittest

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


class LoggedInResourceTests(unittest.TestCase):
    '''Test route access for a logged in user.'''
    def setUp(self):
        '''Pre-test setup.'''
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False

        self.app = app.test_client()
        db.create_all()
        user = User(username='user',
                    email='admin@example.com',
                    password='password',
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
        '''Logout the logged in user.'''
        return self.app.get('/logout', follow_redirects=True)

    def assert_get_status_code(self, route, code):
        rv = self.app.get(route)
        self.assertEqual(rv.status_code, code)

    def test_index(self):
        self.assert_get_status_code('/', 200)

    def test_login(self):
        self.assert_get_status_code('/login', 302)

    def test_resetpassword(self):
        self.assert_get_status_code('/resetpassword', 200)

    def test_setpassword(self):
        self.assert_get_status_code('/setpassword', 200)

    def test_users(self):
        self.assert_get_status_code('/users', 301)
        self.assert_get_status_code('/users/', 404)

    def test_user_new(self):
        self.assert_get_status_code('/users/new', 302)

    def test_user(self):
        self.assert_get_status_code('/users/user', 200)

    def test_user_edit(self):
        self.assert_get_status_code('/users/user/edit', 200)

    def test_requests(self):
        self.assert_get_status_code('/requests', 301)
        self.assert_get_status_code('/requests/', 200)

    def test_request_new(self):
        self.assert_get_status_code('/requests/new', 200)

    def test_request(self):
        self.assert_get_status_code('/requests/request_id', 404)

    def test_request_delete(self):
        self.assert_get_status_code('/requests/request_id/delete', 405)

    def test_request_confirm_add(self):
        self.assert_get_status_code('/requests/request_id/pickup/confirm', 302)

    def test_request_delete_confirm(self):
        self.assert_get_status_code('/requests/request_id/delete/confirm', 302)

    def test_events(self):
        self.assert_get_status_code('/events', 301)
        self.assert_get_status_code('/events/', 404)

    def test_event_new(self):
        self.assert_get_status_code('/events/new', 404)

    def test_event(self):
        self.assert_get_status_code('/events/event_id', 404)

    def test_event_edit(self):
        self.assert_get_status_code('/event/event_id/edit', 404)

    def test_verify(self):
        self.assert_get_status_code('/verify', 200)

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
