from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, login_required, login_user,
                         current_user, logout_user, UserMixin)
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'Shhhh, this is a secret'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.debug = True

# Define Database entities
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)
  pw_hash = db.Column(db.String(60))
  requests = db.relationship('Request', backref='User', lazy='dynamic')
  enabled = db.Column(db.Boolean)
  
  # Self functions
  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.pw_hash = bcrypt.generate_password_hash(password)
    self.enabled = True
  
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
  poster = db.relationship('User', backref=db.backref('requests1', lazy='dynamic'))
  poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  sub = db.relationship('User', backref=db.backref('requests2', lazy='dynamic'))
  
  def __init__(self, poster, sub=None):
    self.poster = poster
  
  def __repr__(self):
    return '<Request Posted by:%r Filled by: %r>' % self.poster, self.sub

# Define login_manager callback
@login_manager.user_loader
def load_user(user_id):
  user = User.query.get(user_id)
  if user:
    return DbUser(user)
  else:
    return None

# Route Requests
@app.route('/', defaults={'dummy': ''})
@app.route("/<path:dummy>")
def catchAll(dummy):
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
        return redirect(next or url_for('catchAll', error=error))
    error = "Login failed"
  return render_template('login.html', login=True, next=next, error=error)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You have logged out')
  session['logged_in'] = False
  return(redirect(url_for('catchAll')))

# Route to users collection
@app.route('/users', methods=['GET', 'POST', 'PUT'])
@login_required
def users():
  error = None
  if request.method == 'POST':
    # Add a new user
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    if not username or not password or not email:
      error = 'Account creation failed: missing username, email, or password'
    return 'Unimplemented' # url_for('users', username=username)
  return 'unimplemented' # render_template('users.html')

# Route to particular user
@app.route('/users/<username>')
@login_required
def user(username):
  return 'User: %s' % username # render_template('user.html', username=username)

# Route to Requests Collection
@app.route('/requests', methods=['GET', 'POST', 'PUT'])
@login_required
def requests():
  return 'unimplemented' # render_template('requests.html')

# Route to a particular request
@app.route('/requests/<request>')
@login_required
def request(request):
  return 'unimplemented' # render_template('request.html', request=request)

# Helper functions
def authenticate_user(username, password):
  user = User.query.filter_by(username=username).first()
  if user:
    return bcrypt.check_password_hash(user.pw_hash, password)
  return False

if __name__ == '__main__':
    app.run()
