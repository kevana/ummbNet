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

class LoggedOutResourceTests(unittest.TestCase):
    '''Test route access for users that are not logged in.'''
    def setUp(self):
        '''Pre-test setup.'''
        app.config['MAIL_SUPPRESS_SEND'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        '''Post-test teardown.'''
        db.session.remove()
        db.drop_all()

    def assert_get_status_code(self, route, code):
        rv = self.app.get(route)
        self.assertEqual(rv.status_code, code)

    # Test access to resources when not logged in
    def test_index(self):
        self.assert_get_status_code('/', 200)

    def test_login(self):
        self.assert_get_status_code('/login', 200)

    # Test redirects to resources that require a logged-in user
    def test_logout(self):
        self.assert_get_status_code('/logout', 200)

    def test_resetpassword(self):
        self.assert_get_status_code('/resetpassword', 200)

    def test_setpassword(self):
        self.assert_get_status_code('/setpassword', 200)

    def test_users(self):
        self.assert_get_status_code('/users', 301)
        self.assert_get_status_code('/users/', 302)

    def test_user(self):
        self.assert_get_status_code('/users/username', 302)

    def test_newuser(self):
        self.assert_get_status_code('/newuser', 200)

    def test_verify(self):
        self.assert_get_status_code('/verify', 200)

    def test_requests(self):
        self.assert_get_status_code('/requests', 301)
        self.assert_get_status_code('/requests/', 302)

    def test_request(self):
        self.assert_get_status_code('/requests/request_id', 302)

    def test_newrequest(self):
        self.assert_get_status_code('/newrequest', 302)

    def test_events(self):
        self.assert_get_status_code('/events', 301)
        self.assert_get_status_code('/events/', 302)

    def test_event(self):
        self.assert_get_status_code('/events/event_id', 302)

    def test_event_new(self):
        self.assert_get_status_code('/events/new', 302)

    def test_event_edit(self):
        self.assert_get_status_code('/event//edit', 404)

    def test_confirm(self):
        self.assert_get_status_code('/confirm', 302)

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
