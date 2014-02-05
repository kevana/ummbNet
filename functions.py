'''
Functions for ummbNet
'''

from flask import g
from hashlib import sha1
from os import urandom
from sqlalchemy.exc import IntegrityError

from app import bcrypt, db, login_manager
from models import Event, Instrument, Request, User
from emails import send_new_req_emails, send_pw_reset_email, send_verify_email

@login_manager.user_loader
def load_user(user_id):
    '''login_manager callback, Return user for a given user_id.'''
    return User.query.get(int(user_id))

def authenticate_user(username, password):
    '''Authenticate a user. Return True if username and password are valid.'''
    user = User.query.filter_by(username=username).first()
    if user:
        return bcrypt.check_password_hash(user.pw_hash, password)
    return False

def add_user(user):
    '''Add a new user to the database.'''
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return False
    return True

def add_request(band_id, event_id, instrument_id, part):
    '''Add a new request to the database.'''
    user = g.user
    part = '' if part == None else part
    # Check if user has already created a request for this event
    if [] != user.posted_requests.filter(Request.event_id == event_id).all():
        return None

    req = Request(poster=user, band_id=band_id, event_id=event_id, \
                  instrument_id=instrument_id, part=part)
    try:
        db.session.add(req)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    send_new_req_emails(req)
    return req.id

def add_event(date, band_id, event_type_id, calltime=None):
    '''Add a new event to the database.'''
    event = Event(date=date, calltime=calltime,
                band_id=band_id, event_type_id=event_type_id)
    if event:
        try:
            db.session.add(event)
            db.session.commit()
        except IntegrityError:
            return None
        return event.id
    return None

def get_form_instr(form):
    '''Retrieve chosen instruments from form. Return a list containing them.'''
    instrs = []
    for instr in form.instruments:
        if instr.checked:
            instrs.append(Instrument.get_by_name(instr._value()))
    return instrs

def get_hash_key():
    '''Get a pseudorandom hex key for password reset and email verification.'''
    m = sha1()
    m.update(urandom(10))
    return m.hexdigest()

def reset_password_start(user):
    '''Generate a password reset key and send it via email to a user.'''
    key = get_hash_key()
    user.pw_reset_key = key
    db.session.commit()
    send_pw_reset_email(user=user, key=key)

def verify_email_start(user):
    '''Generate a verification key and send it via email to a user.'''
    key = get_hash_key()
    user.email_verify_key = key
    db.session.commit()
    send_verify_email(user=user, key=key)
