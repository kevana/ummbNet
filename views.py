'''
Views for ummbNet
'''

from flask import (flash, redirect, render_template,
                   request, session, url_for, abort, g)
from flask_login import (login_required, login_user,
                         logout_user, current_user)
from datetime import datetime

from app import app, db
from emails import send_req_pickup_emails
from functions import (add_event, add_request, add_user, authenticate_user, 
                    get_form_instr, reset_password_start, verify_email_start)
from forms import (LoginForm, PasswordResetForm, SetPasswordForm,
                    UserForm, NewRequestForm, EventForm)
from models import Band, Event, EventType, Instrument, Request, User


@app.before_request
def before_request():
    '''Load the current user into g before every request.'''
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
    '''Route to reset a user's password.'''
    form = PasswordResetForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        reset_password_start(user=user)
        return render_template('user/reset_password.html', sent=True, user=None)
    return render_template('user/reset_password.html', form=form, user=None)

@app.route('/setpassword', methods=['GET', 'POST'])
def set_pw():
    '''Route to set a user's password'''
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
        return render_template('user/set_password.html',
                            form=form, user=None, error=error)

    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    key = request.args.get('k')
    if user and user.pw_reset_key != None and user.pw_reset_key == key:
        form = SetPasswordForm(username=user.username)
        form.validate()
        return render_template('user/set_password.html',
                            form=form, user=None, error=error)

    form = PasswordResetForm()
    error = 'Invalid link, please complete this form to receive a new link'
    return render_template('user/reset_password.html', form=form,
                            user=None, error=error)

@app.route('/users/')
@login_required
def users():
    '''Route to users collection.'''
    user = g.user
    if user.is_director or user.is_admin:
        users = User.query.all()
        return render_template('user/users.html', users=users, user=user)
    abort(404)

@app.route('/users/new', methods=['GET', 'POST'])
def user_new():
    '''Route to add a new user.'''
    user = g.user
    if user is not None and user.is_authenticated():
        return redirect(url_for('index'))

    form = UserForm()
    instrs = [(instr.name, instr.name) for instr in Instrument.query.all()]
    form.instruments.choices = instrs

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
        user = User(username=username, email=email, password=password,
                    first_name=first_name, last_name=last_name,
                    nickname=nickname, instruments=instruments, 
                    req_add_notify_instrs=instruments)
        if username_avail and email_avail and add_user(user):
            verify_email_start(user)
            return render_template('user/reg_complete.html', user=None)

        if not username_avail:
            form.errors['username'] = ['This username is taken.']
        if not email_avail:
            form.errors['email'] = ['This email address is taken.']
    return render_template('user/create_update.html', user=None, form=form)

@app.route('/users/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    '''Route to a particular user.'''
    user = g.user
    page_user = User.query.filter_by(username=username).first()
    if user.is_director or user.is_admin or user == page_user:
        if page_user:
            return render_template('user/user.html', user=user, page_user=page_user)
    abort(404)

@app.route('/users/<username>/edit', methods=['GET', 'POST'])
@login_required
def user_edit(username):
    '''Route to edit a user's account information.'''
    user = g.user
    edit_user = User.query.filter_by(username=username).first()
    if user == edit_user or user.is_director or user.is_admin:
        form = UserForm()
        del form.username
        del form.email
        del form.password
        del form.confirm
        instrs = [(instr.name, instr.name) for instr in Instrument.query.all()]
        form.instruments.choices = instrs

        if form.validate_on_submit():
            edit_user.first_name = form.first_name.data
            edit_user.last_name = form.last_name.data
            edit_user.nickname = form.nickname.data
            edit_user.instruments = get_form_instr(form)
            db.session.commit()
            return redirect(url_for('user', username=username))

        form.first_name.data = edit_user.first_name
        form.last_name.data = edit_user.last_name
        form.nickname.data = edit_user.nickname
        form.instruments.data = user.instruments
        return render_template('user/create_update.html', form=form, user=user,
                                edit_user=edit_user)

    abort(404)

@app.route('/requests/')
@login_required
def requests():
    '''Route to Requests Collection.'''
    if ('past' == request.args.get('date')):
        requests = Request.get_past_reqs()
    else:
        requests = Request.get_open_reqs()
    user = g.user
    return render_template('request/requests.html', requests=requests, user=user)

@app.route('/requests/new', methods=['GET', 'POST'])
@login_required
def request_new():
    '''Add a new request.'''
    user = g.user
    form = NewRequestForm()
    form.instrument.choices = [(instr.id, instr.name)
                                for instr in user.instruments]
    choices = [(event.id, event.event_type.name + ' ' + \
                event.date.strftime('%a %b %d, %I:%M%p'))
        for event in Event.get_future_events()]
    form.event_id.choices = choices

    if form.validate_on_submit():
        band_id = form.band_id.data
        event_id = form.event_id.data
        instrument_id = form.instrument.data
        part = form.part.data if form.part.data else ''
        info = form.info.data if form.info.data else ''
        req_id = add_request(band_id=band_id, event_id=event_id,
                            instrument_id=instrument_id, part=part, info=info)
        if req_id:
            return redirect(url_for('req', request_id=req_id))
        form.errors['event_id'] = \
                    ['You have already created a request for this event.']

    return render_template('request/new.html', form=form, user=user)

@app.route('/requests/<request_id>', methods=['GET', 'POST'])
@login_required
def req(request_id):
    '''Route to a particular request.'''
    user = g.user
    if request.method == 'GET':
        req = Request.query.get(request_id)
        if req:
            return render_template('request/request.html', req=req, user=user)
        abort(404)
    req = Request.query.filter_by(id=request_id).first()
    if req:
        if not req.sub:
            req.sub = g.user
            db.session.commit()
            send_req_pickup_emails(req)
        return redirect(url_for('req', request_id=req.id))
    abort(404)

@app.route('/requests/<request_id>/delete', methods=['POST'])
@login_required
def req_delete(request_id):
    '''Route to delete a request.'''
    user = g.user
    req = Request.query.get(request_id)
    if req and (user == req.poster or user.is_admin or user.is_director):
        db.session.delete(req)
        db.session.commit()
        return redirect(url_for('requests'))
    return redirect(url_for('req', request_id=req.id))

@app.route('/requests/<request_id>/pickup/confirm')
@login_required
def req_pickup_confirm(request_id):
    '''Route to confirm pickup of a request.'''
    user = g.user
    req = Request.query.get(request_id)
    if not req or req.sub:
        return redirect(url_for('requests'))
    return render_template('request/pickup_confirm.html', req=req, user=user)

@app.route('/requests/<request_id>/delete/confirm')
@login_required
def req_delete_confirm(request_id):
    '''Route to confirm deletion of a request.'''
    user = g.user
    req = Request.query.get(request_id)
    if req and (user == req.poster or user.is_admin or user.is_director):
        return render_template('request/delete_confirm.html', req=req, user=user)
    if req:
        return redirect(url_for('req', request_id=req.id))
    return redirect(url_for('requests'))

@app.route('/events/')
@login_required
def events():
    '''Route to Events collection.'''
    user = g.user
    if user.is_director or user.is_admin:
        events = Event.get_future_events()
        return render_template('event/events.html', events=events, user=user)
    abort(404)

@app.route('/events/new', methods=['GET', 'POST'])
@login_required
def event_new():
    '''Add a new Event.'''
    user = g.user
    if user.is_director or user.is_admin:
        form = EventForm()
        bands = [(band.id, band.name) for band in Band.query.all()]
        event_types = [(typ.id, typ.name) for typ in EventType.query.all()]
        form.band_id.choices = bands
        form.event_type_id.choices = event_types

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
            opponent = form.opponent.data
            event_id = add_event(date=date, calltime=calltime, band_id=band_id,
                                    event_type_id=event_type_id, opponent=opponent)
            return redirect(url_for('event', event_id=event_id))

        return render_template('event/create_update.html', form=form, user=user)
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
                return render_template('event/event.html', event=event, user=user)
            abort(404)
        return 'POST unimplemented'
    abort(404)

@app.route('/events/<event_id>/edit', methods=['GET', 'POST'])
@login_required
def event_edit(event_id):
    '''Route to edit an event.'''
    user = g.user
    if user.is_director or user.is_admin:
        form = EventForm()
        bands = [(band.id, band.name) for band in Band.query.all()]
        event_types = [(typ.id, typ.name) for typ in EventType.query.all()]
        form.band_id.choices = bands
        form.event_type_id.choices = event_types

        if form.validate_on_submit():
            event = Event.query.get(event_id)
            event.date = form.date.data
            time = form.calltime.data
            event.calltime = datetime(year=event.date.year,
                                 month=event.date.month,
                                 day=event.date.day,
                                 hour=time.hour,
                                 minute=time.minute)
            event.band_id = form.band_id.data
            event.event_type_id = form.event_type_id.data
            event.opponent = form.opponent.data
            db.session.commit()
            return redirect(url_for('event', event_id=event_id))

        event = Event.query.get(event_id)
        if event:
            form.event_id.data = event.id
            form.date.data = event.date
            form.calltime.data = event.calltime
            form.band_id.data = event.band_id
            form.event_type_id.data = event.event_type_id
            form.opponent.data = event.opponent
            return render_template('event/create_update.html', form=form, user=user)

    abort(404)

@app.route('/verify')
def verify_email():
    '''Route to verify a user's email address.'''
    username = request.args.get('username')
    key = request.args.get('k')
    user = User.query.filter_by(username=username).first()

    if user and user.email_verify_key != None and user.email_verify_key == key:
        user.email_verify_key = None
        user.enabled = True
        db.session.commit()
        if session.get('logged_in') == True:
            user = g.user
            return render_template('user/verify.html', success=True, user=user)
        return render_template('user/verify.html', success=True)
    if session.get('logged_in') == True:
        user = g.user
        return render_template('user/verify.html', success=False, user=user)
    return render_template('user/verify.html', success=False)
