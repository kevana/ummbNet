'''
Email functions for ummbNet
'''

from flask import render_template
from flask.ext.mail import Message

from app import app, mail
from async import async, Thread

@async
def send_async_email(app, msg):
    '''Send a message asynchronously.'''
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body, html_body, sender=None):
    '''Construct and send an email message.'''
    if sender:
        msg = Message(subject, sender=sender, recipients=recipients)
    else:
        msg = Message(subject, recipients=recipients)

    msg.body = text_body
    msg.html = html_body

    if app.config.get('TESTING'):
        mail.send(msg)
    else:
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()

def send_pw_reset_email(user, key):
    '''Send a password reset email to a user.'''
    subject = 'Password reset for %s on ummbNet' % user.username
    msg_to = [user.email]
    txt_body = render_template('email/pw_reset_email.txt', user=user, key=key)
    html_body = render_template('email/pw_reset_email.html', user=user, key=key)
    send_email(subject=subject, recipients=msg_to,
               text_body=txt_body, html_body=html_body)

def send_verify_email(user, key):
    '''Send an email verification message to a user.'''
    subject = 'Verify email address for %s on ummbNet' % user.username
    msg_to = [user.email]
    txt_body = render_template('email/verify_email.txt', user=user, key=key)
    html_body = render_template('email/verify_email.html', user=user, key=key)
    send_email(subject=subject, recipients=msg_to,
               text_body=txt_body, html_body=html_body)

def send_new_req_emails(req):
    '''Send creation notifications to request poster and subscribed users.'''
    # Send confirmation to poster
    subject = 'Request created'
    msg_to = [req.poster.email]
    txt_body = render_template('email/req_add_conf_email.txt', req=req)
    html_body = render_template('email/req_add_conf_email.html', req=req)
    send_email(subject=subject, recipients=msg_to,
               text_body=txt_body, html_body=html_body)
    # Send notification to subscribed users if list is not empty
    if req.instrument.notify_users_add:
        subject = 'New %s sub request posted' % req.instrument.name
        msg_to = [user.email for user in req.instrument.notify_users_add]
        txt_body = render_template('email/req_add_notify_email.txt', req=req)
        html_body = render_template('email/req_add_notify_email.html', req=req)
        send_email(subject=subject, recipients=msg_to,
                   text_body=txt_body, html_body=html_body)

def send_req_pickup_emails(req):
    '''Send pickup notifications to the poster and sub of a request.'''
    # Send notification to poster
    subject = 'Your request has been picked up'
    msg_to = [req.poster.email]
    txt_body = render_template('email/req_pickup_notify_email.txt', req=req)
    html_body = render_template('email/req_pickup_notify_email.html', req=req)
    send_email(subject=subject, recipients=msg_to,
               text_body=txt_body, html_body=html_body)
    # Send confirmation to sub
    subject = 'You have picked up a request'
    msg_to = [req.sub.email]
    txt_body = render_template('email/req_pickup_conf_email.txt', req=req)
    html_body = render_template('email/req_pickup_conf_email.html', req=req)
    send_email(subject=subject, recipients=msg_to,
               text_body=txt_body, html_body=html_body)
