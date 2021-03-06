'''
SQLAlchemy db models for ummbNet
'''

from datetime import datetime

from app import db, bcrypt

users_instrs_play = db.Table('users_instrs_play', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('instrument_id', db.Integer, db.ForeignKey('instrument.id')))

users_instrs_notify = db.Table('users_instrs_notify', db.Model.metadata,
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
    email_verify_key = db.Column(db.Text)
    pw_reset_key = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    nickname = db.Column(db.Text)
    instruments = db.relationship('Instrument',
                                  secondary=users_instrs_play, backref='users')
    req_add_notify_instrs = db.relationship('Instrument',
                    secondary=users_instrs_notify, backref='notify_users_add')
    enabled = db.Column(db.Boolean)

    def set_pw(self, password):
        '''Calculate and store a password hash for the user.'''
        self.pw_hash = bcrypt.generate_password_hash(password)
        self.pw_reset_key = None
        db.session.commit()

    def __init__(self, username, email, password, first_name=None,
                 last_name=None, nickname=None, requests=None, enabled=False,
                 instruments=None, is_admin=False, is_director=False,
                 req_add_notify_instrs=None):
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
        if req_add_notify_instrs:
            self.req_add_notify_instrs = req_add_notify_instrs

        self.is_admin = is_admin
        self.is_director = is_director
        self.enabled = enabled

    def is_authenticated(self):
        '''Return true for all users, used by Flask-Login.'''
        return True

    def is_active(self):
        '''Return the account status of a user, used by Flask-Login.'''
        return self.enabled

    def is_anonymous(self):
        '''Return false for all users, used by Flask-Login.'''
        return False

    def get_id(self):
        '''Return the identifying key for a user, used by Flask-Login.'''
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username


class Request(db.Model):
    '''Represent a user's request for a substitute for an event.'''
    id = db.Column(db.Integer, primary_key=True)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    poster = db.relationship('User',
                    backref=db.backref('posted_requests', lazy='dynamic'),
                    foreign_keys=[poster_id])
    sub_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sub = db.relationship('User',
                    backref=db.backref('filled_requests', lazy='dynamic'),
                    foreign_keys=[sub_id])
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    instrument_id = db.Column(db.Integer, db.ForeignKey('instrument.id'))
    part = db.Column(db.Text)
    info = db.Column(db.Text)

    def __init__(self, poster, sub=None, band_id=None,
                 event_id=None, instrument_id=None, part='', info=''):
        self.poster = poster
        if sub:
            self.sub = sub
        if band_id:
            self.band_id = band_id
        if event_id:
            self.event_id = event_id
        if instrument_id:
            self.instrument_id = instrument_id
        if info:
            self.info = info
        self.part = part

    def __repr__(self):
        return '<Request Event: %r Posted by: %r>' % \
               (self.event_id, self.poster)

    @staticmethod
    def get_open_reqs():
        '''Get a list of all open requests for future events.'''
        return Request.query.filter(Request.sub is None).\
                             join(Request.event).\
                             filter(Event.date > datetime.now()).\
                             order_by(Event.date).all()

    @staticmethod
    def get_past_reqs():
        '''Get a list of all requests for past events.'''
        return Request.query.join(Request.event).\
                             filter(Event.date < datetime.now()).\
                             order_by(Event.date).all()


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
                    db.Integer, db.ForeignKey('event_type.id'))
    date = db.Column(db.DateTime)
    calltime = db.Column(db.DateTime)
    requests = db.relationship('Request', backref='event', lazy='dynamic')
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    opponent = db.Column(db.Text)

    def __init__(self, event_type_id, date, calltime=None,
                 requests=None, band_id=None, opponent=None):
        self.event_type_id = event_type_id
        self.date = date
        if requests:
            self.requests = requests
        if band_id:
            self.band_id = band_id
        if calltime:
            self.calltime = calltime
        else:
            self.calltime = date

        if opponent:
            self.opponent = opponent

    def __repr__(self):
        return '<Event Type: %r Date: %r Call: %r>' % \
               (self.event_type_id, self.date, self.date.time())

    @staticmethod
    def get_future_events():
        '''Get a list of all future events.'''
        return Event.query.filter(Event.date > datetime.now()).\
                           order_by(Event.date).all()


class EventType(db.Model):
    '''Represent the type of band event.'''
    __tablename__ = 'event_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    events = db.relationship('Event', backref='event_type', lazy='dynamic')

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

    @staticmethod
    def get_by_name(name):
        '''Get an instrument object by its name.'''
        instr = Instrument.query.filter_by(name=name).first()
        return instr
