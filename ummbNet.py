from flask import (Flask, flash, redirect, render_template,
                   request, session, url_for, abort)
from flask_login import (LoginManager, login_required, login_user, \
                         logout_user, current_user)
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db',
    SECRET_KEY='Shhhh, this is a secret'
)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.debug = True

# Define Database entities

users_instrs = db.Table('users_instrs', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('instrument_id', db.Integer, db.ForeignKey('instrument.id')))

class User(db.Model):
    '''Represent a user that can log into ummbNet.'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    email = db.Column(db.Text, unique=True)
    pw_hash = db.Column(db.Text)
    is_admin = db.Column(db.Boolean)
    is_director = db.Column(db.Boolean)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    nickname = db.Column(db.Text)
    instruments = db.relationship('Instrument', \
                                secondary=users_instrs, backref='users')
    enabled = db.Column(db.Boolean)

    def __init__(self, username, email, password, first_name=None, \
                last_name=None, nickname=None, requests=None, enabled=True, \
                instruments=None, is_admin=False, is_director=False):
        self.username = username
        self.email = email
        self.pw_hash = bcrypt.generate_password_hash(password)
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if nickname:
            self.nickname = nickname
        if requests:
            self.requests = requests
        if instruments:
            self.instruments = instruments
        self.is_admin = is_admin
        self.is_director = is_director
        self.enabled = enabled

    def __repr__(self):
        return '<User %r>' % self.username

class DbUser(object):
    '''Wrap User object for Flask-Login.'''
    def __init__(self, user):
        self._user = user

    def get_id(self):
        return unicode(self._user.id)

    def is_active(self):
        return self._user.enabled

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_user(self):
        return self._user

class Request(db.Model):
    '''Represent a user's request for a substitute for an event.'''
    id = db.Column(db.Integer, primary_key=True)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    poster = db.relationship('User', \
                    backref=db.backref('posted_requests', lazy='dynamic'), \
                    foreign_keys=[poster_id])
    sub_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sub = db.relationship('User',
                    backref=db.backref('filled_requests', lazy='dynamic'), \
                    foreign_keys=[sub_id])
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    instrument_id = db.Column(db.Integer, db.ForeignKey('instrument.id'))
    part = db.Column(db.Text)

    def __init__(self, poster, sub=None, band_id=None,
                 event_id=None, instrument_id=None, part=''):
        self.poster = poster
        if sub:
            self.sub = sub
        if band_id:
            self.band_id = band_id
        if event_id:
            self.event_id = event_id
        if instrument_id:
            self.instrument_id = instrument_id
        self.part = part

    def __repr__(self):
        return '<Request Event: %r Posted by: %r>' % \
            (self.event_id, self.poster)

class Band(db.Model):
    '''Represent which band the request is for.'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    requests = db.relationship('Request', backref='band', lazy='dynamic')
    events = db.relationship('Event', backref='band', lazy='dynamic')

    def __init__(self, name, members=None, requests=None, events=None):
        self.name = name
        if requests:
            self.requests = requests
        if events:
            self.events = events

    def __repr__(self):
        return '<Band Name: %r>' % self.name

class Event(db.Model):
    '''Represent a specific band event.'''
    id = db.Column(db.Integer, primary_key=True)
    event_type_id = db.Column(
        db.Integer, db.ForeignKey('eventtype.id', schema='dbo'))
    date = db.Column(db.DateTime)
    requests = db.relationship('Request', backref='event', lazy='dynamic')
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))

    def __init__(self, event_type_id, date, requests=None, band_id=None):
        self.event_type_id = event_type_id
        self.date = date
        if requests:
            self.requests = requests
        if band_id:
            self.band_id = band_id

    def __repr__(self):
        return '<Event Type: %r Date: %r Call: %r>' % \
            (self.eventtype, self.date, self.date.time())

class EventType(db.Model):
    '''Represent the type of band event.'''
    __tablename__ = 'eventtype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    events = db.relationship('Event', backref='eventtype', lazy='dynamic')

    def __init__(self, name, events=None):
        self.name = name
        if events:
            self.events = events

    def __repr__(self):
        return '<Event_Type Name: %r>' % self.name

class Instrument(db.Model):
    '''Represent the instrument the requester plays and needs a sub for.'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    requests = db.relationship('Request', backref='instrument', lazy='dynamic')

    def __init__(self, name, requests=None):
        self.name = name
        if requests:
            self.requests = requests

    def __repr__(self):
        return '<Instrument Name: %r>' % self.name


@login_manager.user_loader
def load_user(user_id):
    '''login_manager callback, Return user in DbUser wrapper.'''
    user = User.query.get(user_id)
    if user:
        return DbUser(user)
    else:
        return None

# Route Requests

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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if authenticate_user(username, password):
            user = User.query.filter_by(username=username).first()
            if login_user(DbUser(user)):
                flash("You have logged in")
                session['logged_in'] = True
                return redirect(next or url_for('index', error=error))
        error = "Login failed"
    return render_template('login.html', login=True, next=next, error=error)

@app.route('/logout')
@login_required
def logout():
    '''Log out the currently logged-in user.'''
    logout_user()
    flash('You have logged out')
    session['logged_in'] = False
    return render_template('logout.html')

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
                return redirect(url_for('newuser', error=error))
            return redirect(url_for('index'))
    instruments = Instrument.query.all()
    if session.get('logged_in') == True:
        user = current_user.get_user()
        return render_template('newuser.html', user=user, \
                                instruments=instruments)
    return render_template('newuser.html', instruments=instruments)

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

# Helper functions

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
            return False
        return True # Not graceful logic
    return False

def add_event(date, band_id, event_type_id):
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
    instr = []
    if request.form.get('Piccolo', None) == 'True':
        instr.append(Instrument.query.filter_by(name='Piccolo').first())
    if request.form.get('Piccolo', None) == 'True':
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

if __name__ == '__main__':
    app.run()
