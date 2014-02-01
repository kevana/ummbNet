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

    def assert_get_status_code(self, route, code):
        rv = self.app.get(route)
        self.assertEqual(rv.status_code, code)

    # Test access to resources when logged in
    def test_index(self):
        self.assert_get_status_code('/', 200)

    def test_login(self):
        self.assert_get_status_code('/login', 302)

    # Test redirects to resources that require a logged-in user

    def test_resetpassword(self):
        self.assert_get_status_code('/resetpassword', 200)

    def test_setpassword(self):
        self.assert_get_status_code('/setpassword', 200)

    def test_users(self):
        self.assert_get_status_code('/users', 301)
        self.assert_get_status_code('/users/', 404)

    def test_user(self):
        self.assert_get_status_code('/users/user', 404)

    def test_newuser(self):
        self.assert_get_status_code('/newuser', 302)

    def test_verify(self):
        self.assert_get_status_code('/verify', 200)

    def test_requests(self):
        self.assert_get_status_code('/requests', 301)
        self.assert_get_status_code('/requests/', 200)

    def test_request(self):
        self.assert_get_status_code('/requests/request_id', 200)

    def test_newrequest(self):
        self.assert_get_status_code('/newrequest', 200)

    def test_events(self):
        self.assert_get_status_code('/events', 301)
        self.assert_get_status_code('/events/', 404)

    def test_event(self):
        self.assert_get_status_code('/events/event_id', 404)

    def test_event_new(self):
        self.assert_get_status_code('/events/new', 404)

    def test_event_edit(self):
        self.assert_get_status_code('/event//edit', 404)

    def test_confirm(self):
        self.assert_get_status_code('/confirm', 302)

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
