from coverage import coverage
import os
import unittest

from app import app, db

from config import basedir
from async import *
from email import *
from functions import *
from models import *
from views import *

# Initialize coverage
cov = coverage(branch = True, omit = ['env/*', 'tests.py'])
cov.start()

class LoggedOutResourceTests(unittest.TestCase):
    '''Tests run with a logged out user'''
    def setUp(self):
        '''Pre-test setup.'''
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tmp/test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        '''Post-test teardown.'''
        db.session.remove()
        db.drop_all()

    def assert_get_status_code(self, route, code):
        rv = self.app.get(route)
        assert rv.status_code == code

    # Test access to resources when not logged in
    def test_index(self):
        self.assert_get_status_code('/', 200)

    def test_login(self):
        self.assert_get_status_code('/login', 200)

    # Test redirects to resources that require a logged-in user
    def test_logout(self):
        self.assert_get_status_code('/logout', 302)

    def test_resetpassword(self):
        self.assert_get_status_code('/resetpassword', 200)

    def test_setpassword(self):
        self.assert_get_status_code('/setpassword', 405)

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

    def test_newevent(self):
        self.assert_get_status_code('/newevent', 302)

    def test_editevent(self):
        self.assert_get_status_code('/editevent', 302)

    def test_confirm(self):
        self.assert_get_status_code('/confirm', 302)


class LoggedInResourceTests(unittest.TestCase):
    '''Tests run with a logged in user but no context'''
    def setUp(self):
        '''Pre-test setup.'''
        app.config['TESTING'] = True
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
        assert 'View Requests' in rv.data

    def tearDown(self):
        '''Post-test teardown.'''
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        '''Login a user by posting to /login.'''
        return self.app.post('/login', data=dict(
                username=username,
                password=password
            ), follow_redirects=True)

    def assert_get_status_code(self, route, code):
        rv = self.app.get(route)
        assert rv.status_code == code

    # Test access to resources when logged in
    def test_index(self):
        self.assert_get_status_code('/', 200)

    def test_login(self):
        self.assert_get_status_code('/login', 302)

    # Test redirects to resources that require a logged-in user
    def test_logout(self):
        self.assert_get_status_code('/logout', 200)

    def test_resetpassword(self):
        self.assert_get_status_code('/resetpassword', 200)

    def test_setpassword(self):
        self.assert_get_status_code('/setpassword', 405)

    def test_users(self):
        self.assert_get_status_code('/users', 301)
        self.assert_get_status_code('/users/', 200)

    def test_user(self):
        self.assert_get_status_code('/users/user', 200)

    def test_newuser(self):
        self.assert_get_status_code('/newuser', 200)

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

    def test_newevent(self):
        self.assert_get_status_code('/newevent', 404)

    def test_editevent(self):
        self.assert_get_status_code('/editevent', 404)

    def test_confirm(self):
        self.assert_get_status_code('/confirm', 302)

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print('\n\nCoverage Report:\n')
    cov.report()
    print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
