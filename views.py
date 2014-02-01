'''
Views for ummbNet
'''

from flask import (flash, redirect, render_template,
                   request, session, url_for, abort, g)
from flask_login import (login_required, login_user,
                         logout_user, current_user)
from datetime import datetime

from app import app
from emails import *
from functions import *
from models import *
from forms import (LoginForm, PasswordResetForm, SetPasswordForm, 
                    NewUserForm, NewRequestForm, EventForm)


@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
def index():
    '''Return the ummbNet homepage.'''
    if session.get('logged_in') == True:
        user = g.user
        return render_template('index.html', user=user)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Log in a user with their credentials.'''
    next = request.args.get('next')
    user = g.user
    error = None
    if user is not None and user.is_authenticated():
            return redirect(next or url_for('index'))

    form = LoginForm()
    username = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        if authenticate_user(username, password):
            user = User.query.filter_by(username=username).first()
            login_user(user)
            session['logged_in'] = True
            return redirect(next or url_for('index'))
        error = 'Incorrect username or password.'

    return render_template('login.html', form=form, user=user, error=error)

@app.route('/logout')
def logout():
    '''Log out the currently logged-in user.'''
    logout_user()
    flash('You have logged out')
    session.pop('logged_in', None)
    return render_template('logout.html')

@app.route('/resetpassword', methods=['GET', 'POST'])
def reset_pw():
    form = PasswordResetForm()
    if form.validate_on_submit(): # Checks for post
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        reset_password_start(user=user)
        return render_template('resetpassword.html', sent=True, user=None)
    return render_template('resetpassword.html', form=form, user=None)

@app.route('/setpassword', methods=['GET', 'POST'])
def set_pw():
    error = None
    form = SetPasswordForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            user.set_pw(password)
            return redirect(url_for('user', username=user.username))
        error = 'Unable to reset password.'
        return render_template('setpassword.html',
                            form=form, user=None, error=error)

    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    key = request.args.get('k')
    if user and user.pw_reset_key != None and user.pw_reset_key == key:
        form = SetPasswordForm(username=user.username)
        form.validate()
        return render_template('setpassword.html',
                            form=form, user=None, error=error)
    
    form = PasswordResetForm()
    error = 'Invalid link, please complete this form to receive a new link'
    return render_template('resetpassword.html', form=form, 
                            user=None, error=error)

@app.route('/users')
@login_required
def users():
    '''Route to users collection.'''
    user = g.user
    if user.is_director or user.is_admin:
        users = User.query.all()
        return render_template('users.html', users=users, user=user)
    abort(404)

@app.route('/users/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    '''Route to a particular user.'''
    user = g.user
    if user.is_director or user.is_admin:
        page_user = User.query.filter_by(username=username).first()
        if page_user:
            return render_template('user.html', user=user, page_user=page_user)
    abort(404)

@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    user = g.user
    if user is not None and user.is_authenticated():
            return redirect(url_for('index'))

    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        nickname = form.nickname.data
        instruments = get_form_instr(form)
        
        username_avail = [] == User.query.filter_by(username=username).all()
        email_avail = [] == User.query.filter_by(email=email).all()
        user = User(username=username, email=email, password=password, \
                    first_name=first_name, last_name=last_name, \
                    nickname=nickname, instruments=instruments)
        if username_avail and email_avail and add_user(user):
            verify_email_start(user)
            return render_template('postreg.html', user=None)

        if not username_avail:
            form.errors['username'] = ['This username is taken.']
        if not email_avail:
            form.errors['email'] = ['This email address is taken.']
    return render_template('newuser.html', user=None, form=form)

@app.route('/verify')
def verify_email():
    username = request.args.get('username')
    key = request.args.get('k')
    user = User.query.filter_by(username=username).first()
    
    if user and user.email_verify_key != None and user.email_verify_key == key:
        user.email_verify_key = None
        user.enabled = True
        db.session.commit()
        if session.get('logged_in') == True:
            user = g.user
            return render_template('verified.html', success=True, user=user)
        return render_template('verified.html', success=True)
    if session.get('logged_in') == True:
        user = g.user
        return render_template('verified.html', success=False, user=user)
    return render_template('verified.html', success=False)

@app.route('/requests')
@login_required
def requests():
    '''Route to Requests Collection.'''
    requests = Request.get_open_reqs()
    user = g.user
    return render_template('requests.html', requests=requests, user=user)

@app.route('/requests/<request_id>', methods=['GET', 'POST'])
@login_required
def req(request_id):
    '''Route to a particular request.'''
    user = g.user
    if request.method == 'GET':
        req = Request.query.get(request_id)
        if req:
            return render_template('request.html', req=req, user=user)
        return render_template('404.html', user=user)
    req = Request.query.filter_by(id=request_id).first()
    if req:
        req.sub = g.user
        db.session.commit()
        send_req_pickup_emails(req)
        return redirect(url_for('index', message='Success'))
    return render_template('404.html', user=user)

@app.route('/newrequest', methods=['GET', 'POST'])
@login_required
def newrequest():
    '''Add a new request.'''
    user = g.user
    form = NewRequestForm()
    form.instrument.choices = [(instr.id, instr.name) 
                                for instr in user.instruments]
    events = Event.get_future_events()
    choices = [(event.id, event.event_type.name + ' ' + event.date.strftime('%a %b %d, %I:%M%p')) 
        for event in Event.get_future_events()]
    form.event_id.choices = choices

    if form.validate_on_submit():
        band_id = form.band_id.data
        event_id = form.event_id.data
        instrument_id = form.instrument.data
        part = form.part.data if form.part.data else ''
        req_id = add_request(band_id=band_id, event_id=event_id,
                            instrument_id=instrument_id, part=part)
        if req_id:
            return redirect(url_for('req', request_id=req_id))
        form.errors['event_id'] = ['You have already created a request for this event.']

    return render_template('newRequest.html', form=form, user=user)

@app.route('/events/')
@login_required
def events():
    '''Route to Events collection.'''
    user = g.user
    if user.is_director or user.is_admin:
        events = Event.get_future_events()
        return render_template('events.html', events=events, user=user)
    abort(404)

@app.route('/events/<event_id>')
@login_required
def event(event_id):
    '''Route to a particular event.'''
    user = g.user
    if user.is_director or user.is_admin:
        if request.method == 'GET':
            event = Event.query.get(event_id)
            if event:
                return render_template('event.html', event=event, user=user)
            abort(404)
        return 'POST unimplemented'
    abort(404)

@app.route('/newevent', methods=['GET', 'POST'])
@login_required
def newevent():
    '''Add a new Event.'''
    user = g.user
    if user.is_director or user.is_admin:
        form = EventForm()
        if form.validate_on_submit():
            date = form.date.data
            time = form.calltime.data
            calltime = datetime(year=date.year,
                                 month=date.month, 
                                 day=date.day, 
                                 hour=time.hour, 
                                 minute=time.minute)
            band_id = form.band_id.data
            event_type_id = form.event_type_id.data
            event_id = add_event(date=date, calltime=calltime, band_id=band_id, event_type_id=event_type_id)
            return redirect(url_for('event', event_id=event_id))
        
        return render_template('create_update_event.html', form=form, user=user)
    abort(404)

@app.route('/events/<event_id>/edit', methods=['GET', 'POST'])
@login_required
def event_edit(event_id):
    user = g.user
    if user.is_director or user.is_admin:
        form = EventForm()
        if form.validate_on_submit():
            event = Event.query.get(event_id)
            event.date = form.date.data
            event.band_id = form.band_id.data
            event.event_type_id = form.event_type_id.data
            db.session.commit()
            return redirect(url_for('event', event_id=event_id))

        if event_id:
            event = Event.query.get(event_id)
            form.date.data = event.date
            form.band_id.data = event.band_id
            form.event_type_id.data = event.event_type_id
            return render_template('create_update_event.html', form=form, user=user)
            
    abort(404)

@app.route('/confirm')
@login_required
def confirm():
    '''Confirm an action.'''
    user = g.user
    if request.args.get('action') == 'pickup':
        req_id = request.args['request_id']
        req = Request.query.get(req_id)
        if not req or req.sub:
            return redirect(url_for('requests'))
        return render_template('pickup-req-confirm.html', req=req, user=user)
    error = 'Nothing to confirm'
    return redirect(url_for('index', error=error))
