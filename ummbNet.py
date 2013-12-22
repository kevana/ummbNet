from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, login_required, login_user,
                         current_user, logout_user, UserMixin)
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.debug = True

# Define Database entities
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)
  
  # For login_manager
  def is_authenticated():
    return False
  
  def is_active():
    return False
  
  def is_anonymous():
    return True
  
  def get_id():
    return unicode(current_user.id)
  
  # Self functions
  def __init__(self, username, email):
    self.username = username
    self.email = email
  
  def __repr__(self):
    return '<User %r>' % self.username

class Request(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  poster = db.relationship('User', backref=db.backref('requests', lazy='dynamic'))
  sub_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  sub = db.relationship('User', backref=db.backref('requests', lazy='dynamic'))
  
  def __init__(self, poster, sub=None):
    self.poster = poster
  
  def __repr__(self):
    return '<Request Posted by:%r Filled by: %r>' % self.poster, self.sub

# Define login_manager callback
@login_manager.user_loader
def load_user(userid):
  return User.get(userid)

# Route Requests
@app.route('/', defaults={'dummy': ''})
@app.route("/<path:dummy>")
def catchAll(dummy):
	return render_template('ummbNet.html')

if __name__ == '__main__':
    app.run()
