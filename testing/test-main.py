'''
Main test harness for ummbNet
'''

from coverage import coverage
import os
import sys
import unittest

# Add parent directory to import path
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from config import basedir

from logged_out_resource_tests import LoggedOutResourceTests
from logged_in_resource_tests import LoggedInResourceTests
from new_user_tests import NewUserTests
from password_reset_tests import PasswordResetTests
from event_tests import EventTests

if __name__ == '__main__':
    # Initialize coverage
    cov = coverage(branch=True, omit=['env/*', 'testing/*', 'migrations/*'])
    cov.start()

    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print('\n\nCoverage Report:\n')
    cov.report()
    print("\nHTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
