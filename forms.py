'''
Form classes for ummbNet
'''

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, HiddenField
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
