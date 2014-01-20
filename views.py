'''
Views for ummbNet
'''

from flask import (flash, redirect, render_template,
                   request, session, url_for, abort)
from flask_login import (login_required, login_user, \
                         logout_user, current_user)
from datetime import datetime

from app import app
from emails import *
from functions import *
from models import *


@app.route('/')
def index():
    '''Return the ummbNet homepage.'''
    if session.get('logged_in') == True:
        user = current_user.get_user()
        return render_template('index.html', user=user)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Log in a user with their credentials.'''
    error = None
    next = request.args.get('next')
    if session.get('logged_in') == True:
        user = current_user.get_user()
        return redirect(next or url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if authenticate_user(username, password):
            user = User.query.filter_by(username=username).first()
            if login_user(DbUser(user)):
                flash("You have logged in")
                session['logged_in'] = True
                return redirect(next or url_for('index', error=error))
        if user.email_verify_key:
            error = 'Please verify your email address before logging in.'
        else:
            error = 'Your account has been disabled.'
    return render_template('login.html', login=True, next=next, error=error)

@app.route('/logout')
@login_required
def logout():
    '''Log out the currently logged-in user.'''
    logout_user()
    flash('You have logged out')
    session['logged_in'] = False
    return render_template('logout.html')

@app.route('/resetpassword', methods=['GET', 'POST'])
def reset_pw():
    username = request.args.get('username')
    key = request.args.get('k')
    email = request.form.get('email')
    user = User.query.filter_by(username=username).first()

    if request.method == 'GET':
        if user and user.pw_reset_key != None and user.pw_reset_key == key:
            key = get_hash_key()
            user.pw_reset_key = key
            db.session.commit()
            return render_template('setpassword.html', user=user, key=key)
        return render_template('resetpassword.html', user=None, key=None)
    
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user and user.email == email:
        reset_password_start(user=user)
        return render_template('resetpassword.html', sent=True, user=None)
    error = 'No account with that username/email combination found.'
    return render_template('resetpassword.html', error=error, user=None)

@app.route('/setpassword', methods=['POST'])
def set_pw():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    key = request.form.get('k')
    if user and user.pw_reset_key != None and user.pw_reset_key == key and \
                        password1 != None and password1 == password2:
            user.set_pw(password2)
            return redirect(url_for('user', username=user.username))
    elif password1 == None or password1 != password2:
        error = 'Both passwords must match.'
    else:
        error = 'Unable to reset password'
    return render_template('setpassword.html', user=user, key=key, error=error)

@app.route('/users')
@login_required
def users():
    '''Route to users collection.'''
    users = User.query.all()
    user = current_user.get_user()
    return render_template('users.html', users=users, user=user)

@app.route('/users/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    '''Route to a particular user.'''
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('user.html', user=user, \
                                requests=user.posted_requests.all(), \
                                instruments=user.instruments, \
                                filled_reqs=user.filled_requests.all())
    return render_template('404.html')

@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    '''Add a new user.'''
    error = None
    if request.method == 'POST':
        # Add a new user
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        nickname = request.form['nickname']
        instruments = get_form_instr()
        if not username or not password or not email:
            error = ('Account creation failed: '
                     'missing username, email, or password')
        else:
            user = User(username=username, email=email, password=password, \
                        first_name=first_name, last_name=last_name, \
                        nickname=nickname, instruments=instruments)
            if not add_user(user):
                error = 'Account creation failed: database error'
                return render_template('newuser.html', error=error, \
                                        instruments=instruments)
            verify_email_start(user)
            if session.get('logged_in') == True:
                user = current_user.get_user()
            return render_template('postreg.html', user=user)
    instruments = Instrument.query.all()
    if session.get('logged_in') == True:
        user = current_user.get_user()
        return render_template('newuser.html', user=user, \
                                instruments=instruments)
    return render_template('newuser.html', instruments=instruments)

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
            user = current_user.get_user()
            return render_template('verified.html', success=True, user=user)
        return render_template('verified.html', success=True)
    if session.get('logged_in') == True:
        user = current_user.get_user()
        return render_template('verified.html', success=False, user=user)
    return render_template('verified.html', success=False)

@app.route('/requests')
@login_required
def requests():
    '''Route to Requests Collection.'''
    requests = Request.query.filter(Request.sub == None).all()
    user = current_user.get_user()
    return render_template('requests.html', requests=requests, user=user)

@app.route('/requests/<request_id>', methods=['GET', 'POST'])
@login_required
def req(request_id):
    '''Route to a particular request.'''
    user = current_user.get_user()
    if request.method == 'GET':
        req = Request.query.get(request_id)
        if req:
            return render_template('request.html', req=req, user=user)
        return render_template('404.html', user=user)
    req = Request.query.filter_by(id=request_id).first()
    if req:
        req.sub = current_user.get_user()
        db.session.commit()
        send_req_pickup_emails(req)
        return redirect(url_for('index', message='Success'))
    return render_template('404.html', user=user)

@app.route('/newrequest', methods=['GET', 'POST'])
@login_required
def newrequest():
    '''Add a new request.'''
    error = None
    if request.method == 'POST':
        # Add a new request
        band_id = request.form['band']
        event_id = request.form['event']
        instrument_id = request.form['instrument']
        part = request.form['part']
        if part == None:
            part = ""
        if not band_id or not event_id or not instrument_id:
            error = 'Request creation failed: missing information'
        else:
            add_request(band_id=band_id, event_id=event_id, \
                        instrument_id=instrument_id, part=part)
            return redirect(url_for('requests'))
    bands = Band.query.all()
    events = Event.query.all()
    instruments = Instrument.query.all()
    user = current_user.get_user()
    return render_template('newRequest.html', bands=bands, \
                            events=events, instruments=instruments, user=user)

@app.route('/events/')
@login_required
def events():
    '''Route to Events collection.'''
    user = current_user.get_user()
    if user.is_director or user.is_admin:
        events = Event.query.all()
        return render_template('events.html', events=events, user=user)
    abort(404)

@app.route('/events/<event_id>')
@login_required
def event(event_id):
    '''Route to a particular event.'''
    user = current_user.get_user()
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
    user = current_user.get_user()
    if user.is_director or user.is_admin:
        error = None
        if request.method == 'POST':
            date = request.form['date']
            band_id = request.form['band']
            event_type_id = request.form['event_type']
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
            add_event(date=date, band_id=band_id, event_type_id=event_type_id)
            return redirect(url_for('events'))
        bands = Band.query.all()
        event_types = EventType.query.all()
        return render_template('newevent.html', bands=bands, \
                        event_types=event_types, user=user)
    abort(404)

@app.route('/editevent', methods=['GET', 'POST'])
@login_required
def editevent():
    '''Edit an existing Event.'''
    user = current_user.get_user()
    error = None
    if user.is_director or user.is_admin:
        if request.method == 'GET':
            event_id = request.args['event_id']
            event = Event.query.get(event_id)
            bands = Band.query.all()
            event_types = EventType.query.all()
            if not event:
                return redirect(url_for('events'))
            return render_template('editevent.html', event=event, user=user, \
                                    event_types=event_types, bands=bands)
        if request.method == 'POST':
            event_id = request.form['event_id']
            date = request.form['date']
            band_id = request.form['band']
            event_type_id = request.form['event_type']
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
            event = Event.query.get(event_id)
            event.date = date
            event.band_id = band_id
            event.event_type_id = event_type_id
            if not event:
                error = 'Unable to find event.'
            try:
                db.session.commit()
                return redirect(url_for('event', event_id=event_id))
            except:
                error = 'Unable to update event.'
            return render_template('editevent.html', event=event, \
                                    bands=bands, event_types=event_types, \
                                    user=user, error=error)


    abort(404)

@app.route('/confirm')
@login_required
def confirm():
    '''Confirm an action.'''
    user = current_user.get_user()
    if request.args.get('action') == 'pickup':
        req_id = request.args['request_id']
        req = Request.query.get(req_id)
        if not req or req.sub:
            return redirect(url_for('requests'))
        return render_template('pickup-req-confirm.html', req=req, user=user)
    error = 'Nothing to confirm'
    return redirect(url_for('index', error=error))
