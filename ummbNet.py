from flask import Flask, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, login_required, login_user,
                         current_user, logout_user, UserMixin)
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.debug = True

# Define Database entities
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)
  pw_hash = db.Column(db.String(60))
  requests = db.relationship('Request', backref='User', lazy='dynamic')
  
  # Self functions
  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.pw_hash = bcrypt.generate_password_hash(password)
  
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
      if login_user(DbUser()):
        flash("You have logged in")
        return redirect(next or url_for('/', error=error))
    error = "Login failed"
  return render_template('login.html', login=True, next=next, error=error)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You have logged out')
  return(redirect(url_for('catchAll')))

# Helper functions
def authenticate_user(username, password):
  user = User.query.filter_by(username=username).first()
  if user:
    return bcrypt.check_password_hash(user.pw_hash, password)
  return False

if __name__ == '__main__':
    app.run()
