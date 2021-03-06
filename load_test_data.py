'''
A set of sample users, events, and requests for ummbNet.
'''

from datetime import datetime, timedelta

from app import db
from models import Band, Event, EventType, Instrument, Request, User


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


# Get bands
gold_band = Band.query.filter_by(name='Gold Band').first()
maroon_band = Band.query.filter_by(name='Maroon Band').first()
gopher_band = Band.query.filter_by(name='Gopher Band').first()

# Create Dates
now = datetime.now()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute

one_hour = timedelta(minutes=60)
one_day = timedelta(days=1)
one_week = timedelta(days=7)
one_month = timedelta(days=30)

yesterday = now - one_day
yesterday_call = now - one_day - one_hour
tomorrow = now + one_day
tomorrow_call = now + one_day - one_hour
last_week = now - one_week
last_week_call = now - one_week - one_hour
next_week = now + one_week
next_week_call = now + one_week - one_hour
last_month = now - one_month
last_month_call = now - one_month - one_hour
next_month = now + one_month
next_month_call = now + one_month - one_hour

# Create Users
admin = User(username='admin', email='kevan@ummb.net', password='password',
             first_name='Kevan', last_name='Ahlquist', nickname='Krevan',
             instruments=[trumpet], req_add_notify_instrs=[trumpet],
             is_admin=True, is_director=True, enabled=True)

director = User(username='director', email='kevan+skeeter@ummb.net',
                password='password', first_name='Skeeter', last_name='Boroughs',
                nickname='Skeeter', instruments=[], req_add_notify_instrs=[],
                is_director=True, enabled=True)

user_1 = User(username='user_1', email='kevan+user_1@ummb.net',
              password='password', first_name='Mitch', last_name='Gulbransen',
              nickname='Gulbie', instruments=[piccolo, flute],
              req_add_notify_instrs=[piccolo, flute, trumpet], enabled=True)

user_2 = User(username='user_2', email='kevan+user_2@ummb.net',
              password='password', first_name='Phillip', last_name='Homen',
              nickname='Phil', instruments=[clarinet],
              req_add_notify_instrs=[clarinet], enabled=True)

user_3 = User(username='user_3', email='kevan+user_3@ummb.net',
              password='password', first_name='Raoul', last_name='Shah',
              nickname='Batman', instruments=[alto_sax],
              req_add_notify_instrs=[alto_sax], enabled=True)

user_4 = User(username='user_4', email='kevan+user_4@ummb.net',
              password='password', first_name='Joe', last_name='Walsh',
              nickname='', instruments=[mellophone, drumline],
              req_add_notify_instrs=[mellophone, drumline], enabled=True)

user_5 = User(username='user_5', email='kevan+user_5@ummb.net',
              password='password', first_name='Colin', last_name='Campbell',
              nickname='', instruments=[trombone],
              req_add_notify_instrs=[trombone], enabled=True)

user_6 = User(username='user_6', email='kevan+user_6@ummb.net',
              password='password', first_name='Jeff', last_name='Korum',
              nickname='Twitch', instruments=[baritone, trumpet],
              req_add_notify_instrs=[baritone, trumpet], enabled=True)

user_7 = User(username='user_7', email='kevan+user_7@ummb.net',
              password='password', first_name='Tyler', last_name='Hoffman',
              nickname='Ty', instruments=[tuba],
              req_add_notify_instrs=[tuba], enabled=True)

user_8 = User(username='user_8', email='kevan+user_8@ummb.net',
              password='password', first_name='Brad', last_name='Billstein',
              nickname='Colin2', instruments=[drumline, flute, trumpet],
              req_add_notify_instrs=[drumline, flute, trumpet], enabled=True)

user_9 = User(username='user_9', email='kevan+user_9@ummb.net',
              password='password', first_name='Tomas', last_name='Icenogle',
              nickname='Iceman', instruments=[trumpet],
              req_add_notify_instrs=[trumpet], enabled=True)

db.session.add_all([admin, user_1, user_2, user_3, user_4,
                    user_5, user_6, user_7, user_8, user_9])
db.session.commit()


# Create Events
event_1 = Event(event_type_id=mens_basketball.id, date=tomorrow,
                calltime=tomorrow_call, band_id=gold_band.id,
                opponent='Purdue')

event_2 = Event(event_type_id=mens_basketball.id, date=next_week,
                calltime=next_week_call, band_id=maroon_band.id,
                opponent='Illinois')

event_3 = Event(event_type_id=mens_basketball.id, date=next_month,
                calltime=next_month_call, band_id=gopher_band.id,
                opponent='Indiana')

event_4 = Event(event_type_id=womens_basketball.id, date=tomorrow,
                calltime=tomorrow_call, band_id=gold_band.id,
                opponent='Wisconsin')

event_5 = Event(event_type_id=womens_basketball.id, date=next_week,
                calltime=next_week_call, band_id=maroon_band.id,
                opponent='Nebraska')

event_6 = Event(event_type_id=womens_basketball.id, date=next_month,
                calltime=next_month_call, band_id=gopher_band.id,
                opponent='Iowa')

event_7 = Event(event_type_id=mens_hockey.id, date=tomorrow,
                calltime=tomorrow_call, band_id=gold_band.id,
                opponent='Penn State')

event_8 = Event(event_type_id=mens_hockey.id, date=next_week,
                calltime=next_week_call, band_id=maroon_band.id,
                opponent='Michigan')

event_9 = Event(event_type_id=mens_hockey.id, date=next_month,
                calltime=next_month_call, band_id=gopher_band.id,
                opponent='Michigan State')

event_10 = Event(event_type_id=womens_hockey.id, date=tomorrow,
                 calltime=tomorrow_call, band_id=gold_band.id,
                 opponent='Rutgers')

event_11 = Event(event_type_id=womens_hockey.id, date=next_week,
                 calltime=next_week_call, band_id=maroon_band.id,
                 opponent='Maryland')

event_12 = Event(event_type_id=womens_hockey.id, date=next_month,
                 calltime=next_month_call, band_id=gopher_band.id,
                 opponent='Northwestern')

event_13 = Event(event_type_id=volleyball.id, date=tomorrow,
                 calltime=tomorrow_call, band_id=gold_band.id,
                 opponent='Purdue')

event_14 = Event(event_type_id=volleyball.id, date=next_week,
                 calltime=next_week_call, band_id=maroon_band.id,
                 opponent='Illinois')

event_15 = Event(event_type_id=volleyball.id, date=next_month,
                 calltime=next_month_call, band_id=gopher_band.id,
                 opponent='Indiana')

db.session.add_all([event_1, event_2, event_3, event_4, event_5,
                    event_6, event_7, event_8, event_9, event_10,
                    event_11, event_12, event_13, event_14, event_15])
db.session.commit()


# Create Requests
request_0 = Request(poster=user_5, band_id=gold_band.id,
                    event_id=event_1.id, instrument_id=drumline.id, part='Bass')

request_1 = Request(poster=user_1, band_id=maroon_band.id,
                    event_id=event_2.id, instrument_id=piccolo.id, part='1')

request_2 = Request(poster=user_1, band_id=gopher_band.id,
                    event_id=event_3.id, instrument_id=piccolo.id, part='2')

request_3 = Request(poster=user_2, band_id=gold_band.id,
                    event_id=event_4.id, instrument_id=flute.id, part='1')

request_4 = Request(poster=user_2, band_id=maroon_band.id,
                    event_id=event_5.id, instrument_id=flute.id, part='3')

request_5 = Request(poster=user_3, band_id=gopher_band.id,
                    event_id=event_6.id, instrument_id=trumpet.id, part='3')

request_6 = Request(poster=user_3, band_id=gold_band.id,
                    event_id=event_7.id, instrument_id=trumpet.id, part='2')

request_7 = Request(poster=user_4, band_id=maroon_band.id,
                    event_id=event_8.id, instrument_id=alto_sax.id, part='1')

request_8 = Request(poster=user_4, band_id=gopher_band.id,
                    event_id=event_9.id, instrument_id=alto_sax.id, part='2')

request_9 = Request(poster=user_4, band_id=gold_band.id,
                    event_id=event_10.id, instrument_id=alto_sax.id, part='3')

db.session.add_all([request_0, request_1, request_2, request_3, request_4,
                    request_5, request_6, request_7, request_8, request_9])
db.session.commit()
