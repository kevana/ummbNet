from datetime import datetime, timedelta
from ummbNet import *


# Create Users
admin = User(username='admin', email='admin@example.com', password='password')
user_1 = User(username='user_1', email='user_1@example.com', password='password')
user_2 = User(username='user_2', email='user_2@example.com', password='password')
user_3 = User(username='user_3', email='user_3@example.com', password='password')
user_4 = User(username='user_4', email='user_4@example.com', password='password')
user_5 = User(username='user_5', email='user_5@example.com', password='password')
user_6 = User(username='user_6', email='user_6@example.com', password='password')
user_7 = User(username='user_7', email='user_7@example.com', password='password')
user_8 = User(username='user_8', email='user_8@example.com', password='password')
user_9 = User(username='user_9', email='user_9@example.com', password='password')


# Get event_types
mens_basketball = EventType.query.filter_by(name="Men's Basketball").first()
womens_basketball = EventType.query.filter_by(name="Women's Basketball").first()
mens_hockey = EventType.query.filter_by(name="Men's Hockey").first()
womens_hockey = EventType.query.filter_by(name="Women's Hockey").first()
volleyball = EventType.query.filter_by(name="Volleyball").first()

# Get Instruments
piccolo = Instrument.query.filter_by(name='Piccolo').first()
flute = Instrument.query.filter_by(name='Flute').first()
clarinet = Instrument.query.filter_by(name='Clarinet').first()
alto_sax = Instrument.query.filter_by(name='Alto Sax').first()
tenor_sax = Instrument.query.filter_by(name='Tenor Sax').first()
trumpet = Instrument.query.filter_by(name='Trumpet').first()
mellophone = Instrument.query.filter_by(name='Mellophone').first()
trombone = Instrument.query.filter_by(name='Trombone').first()
baritone = Instrument.query.filter_by(name='Baritone').first()
tuba = Instrument.query.filter_by(name='Tuba').first()
drumline = Instrument.query.filter_by(name='Drumline').first()

# Create Dates
now = datetime.utcnow()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute

one_day = timedelta(days=1)
one_week = timedelta(days=7)
one_month = timedelta(days=30)

yesterday = now - one_day
tomorrow = now + one_day
last_week = now - one_week
next_week = now + one_week
last_month = now - one_month
next_month = now + one_month


# Create Events
event_1 = Event(event_type_id=mens_basketball.id, date=tomorrow)
event_2 = Event(event_type_id=mens_basketball.id, date=next_week)
event_3 = Event(event_type_id=mens_basketball.id, date=next_month)
event_4 = Event(event_type_id=womens_basketball.id, date=tomorrow)
event_5 = Event(event_type_id=womens_basketball.id, date=next_week)
event_6 = Event(event_type_id=womens_basketball.id, date=next_month)
event_7 = Event(event_type_id=mens_hockey.id, date=tomorrow)
event_8 = Event(event_type_id=mens_hockey.id, date=next_week)
event_9 = Event(event_type_id=mens_hockey.id, date=next_month)
event_10 = Event(event_type_id=womens_hockey.id, date=tomorrow)
event_11 = Event(event_type_id=womens_hockey.id, date=next_week)
event_12 = Event(event_type_id=womens_hockey.id, date=next_month)
event_13 = Event(event_type_id=volleyball.id, date=tomorrow)
event_14 = Event(event_type_id=volleyball.id, date=next_week)
event_15 = Event(event_type_id=volleyball.id, date=next_month)


# Create Requests
request_1 = Request(poster=user_1, instrument_id=piccolo.id)
request_1 = Request(poster=user_1, instrument_id=piccolo.id)
request_1 = Request(poster=user_2, instrument_id=flute.id)
request_1 = Request(poster=user_2, instrument_id=flute.id)
request_1 = Request(poster=user_3, instrument_id=trumpet.id)
request_1 = Request(poster=user_3, instrument_id=trumpet.id)
request_1 = Request(poster=user_4, instrument_id=alto_sax.id)
request_1 = Request(poster=user_4, instrument_id=alto_sax.id)
request_1 = Request(poster=user_4, instrument_id=alto_sax.id)
request_1 = Request(poster=user_5, instrument_id=drumline.id)
