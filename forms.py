'''
Form classes for ummbNet
'''

from flask.ext.wtf import Form
from wtforms import (TextField, BooleanField, PasswordField,
                    HiddenField, SelectField, SelectMultipleField)
from wtforms.fields.html5 import DateTimeLocalField
from wtforms_components import TimeField
from wtforms.validators import Required, EqualTo, Email, ValidationError

from app import db
from models import *

# Validators
def Password(length=8):
    '''Validator factory for passwords'''
    message = 'Must be at least %d characters long.' % length

    def _password(form, field):
        l = len(field.data) if field.data else 0
        if l < length:
            raise ValidationError(message)

    return _password

# Forms
class LoginForm(Form):
    '''Form for main login screen.'''
    username = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])

class PasswordResetForm(Form):
    '''Form for password reset screen.'''
    username = TextField('Username:', validators=[Required()])
    email = TextField('Email:', validators=[Required(), Email()])
    
    def validate_email(form, field):
            username = form.username.data
            user = User.query.filter_by(username=username).first()
            if not user or form.email.data != user.email:
                raise ValidationError('Invalid username email combination.')

class SetPasswordForm(Form):
    '''Form for password set screen.'''
    password = PasswordField('Select a new password:', 
                            validators=[Password(8)])
    confirm  = PasswordField('Please re-enter your new password:',
                             validators=[EqualTo('password',
                                    message='Passwords must match')])
    username = HiddenField('username')

class NewUserForm(Form):
    '''Form for new user screen.'''
    username = TextField('Username:', validators=[Required()])
    email = TextField('Email:', validators=[Required(), Email()])
    password = PasswordField('Password:',
                             validators=[Required()])
    confirm = PasswordField('Please re-enter your password:',
                             validators=[EqualTo('password',
                                    message='Passwords must match')])
    first_name = TextField('First Name:', validators=[Required()])
    last_name = TextField('Last Name:')
    nickname = TextField('Nickname:')
    instrs = [(instr.name, instr.name) for instr in Instrument.query.all()]
    instruments = SelectMultipleField(
                'Instruments: (ctrl+click or cmd+click to select multiple)', 
                choices=instrs)

class NewRequestForm(Form):
    '''Form for new request screen.'''
    bands = [(band.id, band.name) for band in Band.query.all()]
    band_id = SelectField('Band:', choices=bands, 
                        validators=[Required()], coerce=int)
    event_id = SelectField('Event:', validators=[Required()], coerce=int)
    instrument = SelectField('Instrument:', validators=[Required()], coerce=int)
    part = TextField('Part:')

class EventForm(Form):
    '''Form for new event screen.'''
    bands = [(band.id, band.name) for band in Band.query.all()]
    event_types = [(typ.id, typ.name) for typ in EventType.query.all()]
    
    event_id = HiddenField('event_id')
    date = DateTimeLocalField('Event Date:', format='%Y-%m-%dT%H:%M')
    calltime = TimeField('Calltime:')
    band_id = SelectField('Band:', choices=bands, 
                        validators=[Required()], coerce=int)
    event_type_id = SelectField('Event Type:', choices=event_types, 
                        validators=[Required()], coerce=int)
    
    def validate_date(form, field):
        if field.data and field.data < datetime.utcnow():
            raise ValidationError('Event date must be in the future.')
