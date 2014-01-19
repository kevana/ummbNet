'''
Email functions for ummbNet
'''

from flask import render_template
from flask.ext.mail import Message

from app import mail
from async import async, Thread

@async
def send_async_email(msg):
    mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    thr = Thread(target = send_async_email, args = [msg])
    thr.start()

def send_pw_reset_email(user, key):
    subject = 'Password reset for %r on ummbNet' % user.username
    msg_from = 'noreply@ummb.net'
    msg_to  = [user.email]
    txt_body = render_template('pw_reset_email.txt', user=user, key=key)
    html_body = render_template('pw_reset_email.html', user=user, key=key)
    send_email(subject=subject, sender=msg_from, recipients=msg_to, \
               text_body=txt_body, html_body=html_body)

def send_verify_email(user, key):
    subject = 'Verify email address for %r on ummbNet' % user.username
    msg_from = 'noreply@ummb.net'
    msg_to  = [user.email]
    txt_body = render_template('verify_email.txt', user=user, key=key)
    html_body = render_template('verify_email.html', user=user, key=key)
    send_email(subject=subject, sender=msg_from, recipients=msg_to, \
               text_body=txt_body, html_body=html_body)
