from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, login_required, login_user,
                         current_user, logout_user, UserMixin)
from flask.ext.bcrypt import Bcrypt
from urllib import unquote
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'Shhhh, this is a secret'
# app.config['SERVER_NAME'] = '127.0.0.1:5000' Seems to break login/logout, maybe due to localhost?
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.debug = True

# Define Database entities
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text, unique=True)
  email = db.Column(db.Text, unique=True)
  pw_hash = db.Column(db.Text)
  requests = db.relationship('Request', backref='User', lazy='dynamic')
  enabled = db.Column(db.Boolean)
  
  # Self functions
  def __init__(self, username, email, password, requests=None, enabled=True):
    self.username = username
    self.email = email
    self.pw_hash = bcrypt.generate_password_hash(password)
    if requests:
      self.requests = requests
    self.enabled = enabled
  
  def __repr__(self):
    return '<User %r>' % self.username

# Wraps User object for Flask-login
class DbUser(object):
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

class Request(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  poster = db.relationship('User', backref=db.backref('posted_requests', lazy='dynamic'))
  poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  sub = db.relationship('User', backref=db.backref('filled_requests', lazy='dynamic'))
  band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
  event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
  instrument_id = db.Column(db.Integer, db.ForeignKey('instrument.id'))
  part = db.Column(db.Text)
  
  def __init__(self, poster, sub=None, band_id=None, event_id=None, instrument_id=None, part=""):
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
    return '<Request Event: %r Posted by: %r>' % Event.query.get(self.event_id), self.poster

class Band(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text)
  requests = db.relationship('Request', backref='band', lazy='dynamic')
  
  def __init__(self, name, members=None, requests=None):
    self.name = name
    if requests:
      self.requests = requests
  
  def __repr__(self):
    return '<Band Name: %r>' % self.name

class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  event_type_id = db.Column(db.Integer, db.ForeignKey('eventtype.id', schema='dbo'))
  date = db.Column(db.DateTime)
  requests = db.relationship('Request', backref='event', lazy='dynamic')
  
  def __init__(self, event_type_id, date, requests=None):
    self.event_type_id = event_type_id
    self.date = date
    if requests:
      self.requests = requests
    
  def __repr__(self):
    return '<Event Type: %r Date: %r Time %r>' % self.event_type, self.date, self.time

class EventType(db.Model):
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
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text)
  requests = db.relationship('Request', backref='instrument', lazy='dynamic')
  
  def __init__(self, name, requests=None):
    self.name = name
    if requests:
      self.requests = requests
  
  def __repr__(self):
    return '<Instrument Name: %r>' % self.name

# Define login_manager callback
@login_manager.user_loader
def load_user(user_id):
  user = User.query.get(user_id)
  if user:
    return DbUser(user)
  else:
    return None

# Route Requests
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
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
  logout_user()
  flash('You have logged out')
  session['logged_in'] = False
  return render_template('logout.html')

# Route to users collection
@app.route('/users')
@login_required
def users():
  return render_template('users.html')

# Route to particular user
@app.route('/users/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
  return 'User: %s' % username # render_template('user.html', username=username)

# Add a new user
@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
  error = None
  if request.method == 'POST':
    # Add a new user
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    if not username or not password or not email:
      error = 'Account creation failed: missing username, email, or password'
    else:
      if not add_user(username, email, password):
        error = 'Account creation failed: database errord'
        return redirect(url_for('newuser', error=error))
      return redirect(url_for('index'))
  return render_template('newuser.html')

# Route to Requests Collection
@app.route('/requests')
@login_required
def requests():
  return render_template('requests.html')

# Route to a particular request
@app.route('/requests/<req>', methods=['GET', 'POST'])
@login_required
def req(req):
  return 'Request: %s' % req # render_template('request.html', request=req)

# Add a new request
@app.route('/newrequest', methods=['GET', 'POST'])
def newrequest():
  error = None
  if request.method == 'POST':
    # Add a new request
    username = request.form['username']
    # TODO: Check other args
    if not username: # or not ...other params...:
      error = 'Request creation failed: missing information'
    else:
      add_request(username)
      return redirect(url_for('requests'))
  return render_template('newRequest.html', error=error)

# Helper functions
def authenticate_user(username, password):
  user = User.query.filter_by(username=username).first()
  if user:
    return bcrypt.check_password_hash(user.pw_hash, password)
  return False

# Add a new user to the database
def add_user(username, email, password):
  user = User(username, email, password)
  try:
    db.session.add(user)
    db.session.commit()
  except IntegrityError: 
    return False
  return True

# Add a new request to the database
def add_request(username):
  user = User.query.filter_by(username=username).first()
  if user:
    req = Request(user)
    try:
      db.session.add(req)
      db.session.commit()
    except IntegrityError:
      return False
    return True # Not graceful logic
  return False

if __name__ == '__main__':
    app.run()
