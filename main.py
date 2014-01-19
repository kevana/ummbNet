'''
Entry point for ummbNet. Always run the app from here
'''

from app import app

from async import *
from email import *
from functions import *
from models import *
from views import *

if __name__ == '__main__':
    app.run()
