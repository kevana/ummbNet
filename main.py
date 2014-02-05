'''
Entry point for ummbNet. Always run the app from here
'''

import os

import config
from config import basedir
from app import app
from views import *

if __name__ == '__main__':
    if not app.debug:
        # Email and file log handlers
        import logging
        from logging import Formatter
        from logging.handlers import SMTPHandler, RotatingFileHandler
        mail_handler = SMTPHandler(mailhost=config.MAIL_SERVER,
                                fromaddr=config.LOGGING_SENDER,
                                toaddrs=config.ADMINS,
                                subject='ummbNet Server Error',
                                credentials=(config.MAIL_USERNAME,
                                             config.MAIL_PASSWORD))
        file_handler = RotatingFileHandler(
                            filename=os.path.join(basedir, 'log/app.log'),
                            maxBytes=1048756,
                            backupCount=5)
        mail_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.WARNING)
        mail_handler.setFormatter(Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s
        '''))
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)

    app.run()
