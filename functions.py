'''
Functions for ummbNet
'''

from flask import request
from flask_login import current_user
from hashlib import sha1
from os import urandom
from sqlalchemy.exc import IntegrityError

from app import bcrypt, db, login_manager
from models import *
from emails import *

@login_manager.user_loader
def load_user(user_id):
    '''login_manager callback, Return user in DbUser wrapper.'''
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
    user = current_user.get_user()
    if user:
        req = Request(poster=user, band_id=band_id, event_id=event_id, \
                      instrument_id=instrument_id, part=part)
        try:
            db.session.add(req)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return False
        send_new_req_emails(req)
        return True
    return False

def add_event(date, band_id, event_type_id):
    '''Add a new event to the database.'''
    event = Event(date=date, band_id=band_id, event_type_id=event_type_id)
    if event:
        try:
            db.session.add(event)
            db.session.commit()
        except IntegrityError:
            return False
        return True
    return False

def get_form_instr():
    '''Retrieve chosen instruments from form. Return a list containing them.'''
    instr = []
    if request.form.get('Piccolo', None) == 'True':
        instr.append(Instrument.query.filter_by(name='Piccolo').first())
    if request.form.get('Flute', None) == 'True':
        instr.append(Instrument.query.filter_by(name='Flute').first())
    if request.form.get('Clarinet', None) == 'True':
        instr.append(Instrument.query.filter_by(name='Clarinet').first())
    if request.form.get('Alto Sax') == 'True':
        instr.append(Instrument.query.filter_by(name='Alto Sax').first())
    if request.form.get('Tenor Sax') == 'True':
        instr.append(Instrument.query.filter_by(name='Tenor Sax').first())
    if request.form.get('Trumpet') == 'True':
        instr.append(Instrument.query.filter_by(name='Trumpet').first())
    if request.form.get('Mellophone') == 'True':
        instr.append(Instrument.query.filter_by(name='Mellophone').first())
    if request.form.get('Trombone') == 'True':
        instr.append(Instrument.query.filter_by(name='Trombone').first())
    if request.form.get('Baritone') == 'True':
        instr.append(Instrument.query.filter_by(name='Baritone').first())
    if request.form.get('Tuba') == 'True':
        instr.append(Instrument.query.filter_by(name='Tuba').first())
    if request.form.get('Drumline') == 'True':
        instr.append(Instrument.query.filter_by(name='Drumline').first())
    return instr

def get_hash_key():
    m = sha1()
    m.update(urandom(10))
    return m.hexdigest()

def reset_password_start(user):
    key = get_hash_key()
    user.pw_reset_key = key
    db.session.commit()
    send_pw_reset_email(user=user, key=key)

def verify_email_start(user):
    key = get_hash_key()
    user.email_verify_key = key
    db.session.commit()
    send_verify_email(user=user, key=key)
