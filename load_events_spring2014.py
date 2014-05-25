'''
Event data for Spring 2014, TBD and playoffs excluded.
'''

from main import Band, datetime, db, Event, EventType


# Get event_types
mens_basketball = EventType.query.filter_by(name="Men's Basketball").first()
womens_basketball = EventType.query.filter_by(name="Women's Basketball").first()
mens_hockey = EventType.query.filter_by(name="Men's Hockey").first()
womens_hockey = EventType.query.filter_by(name="Women's Hockey").first()
volleyball = EventType.query.filter_by(name="Volleyball").first()

# Get bands
gold_band = Band.query.filter_by(name='Gold Band').first()
maroon_band = Band.query.filter_by(name='Maroon Band').first()
gopher_band = Band.query.filter_by(name='Gopher Band').first()

# 1/22/14	8:00pm	MBB	Gold
dt = datetime(2014, 1, 22, 19, 15)
event_1 = Event(event_type_id=mens_basketball.id,
                date=dt,
                band_id=gold_band.id)
# 1/23/14	8:00pm	WBB	Gopher
dt = datetime(2014, 1, 23, 19, 30)
event_2 = Event(event_type_id=womens_basketball.id,
                date=dt,
                band_id=gopher_band.id)
# 1/24/14	7:00pm	WH  Gold
dt = datetime(2014, 1, 24, 18, 30)
event_3 = Event(event_type_id=womens_hockey.id,
                date=dt,
                band_id=gold_band.id)
# 1/25/14	7:00pm	WH  Gopher
dt = datetime(2014, 1, 25, 18, 30)
event_4 = Event(event_type_id=womens_hockey.id,
                date=dt,
                band_id=gopher_band.id)
# 1/29/14	7:00pm	WBB Gopher
dt = datetime(2014, 1, 29, 18, 30)
event_5 = Event(event_type_id=womens_basketball.id,
                date=dt,
                band_id=gopher_band.id)
# 2/1/14	1:00pm	MBB Gold
dt = datetime(2014, 2, 1, 12, 15)
event_6 = Event(event_type_id=mens_basketball.id,
                date=dt,
                band_id=gold_band.id)
# 2/7/14	7:00pm	WH  Maroon
dt = datetime(2014, 2, 7, 18, 30)
event_7 = Event(event_type_id=womens_hockey.id,
                date=dt,
                band_id=maroon_band.id)
# 2/8/14	4:00pm	WH  Maroon
dt = datetime(2014, 2, 8, 15, 30)
event_8 = Event(event_type_id=womens_hockey.id,
                date=dt,
                band_id=maroon_band.id)
# 2/8/14	7:15pm	MBB Gold
dt = datetime(2014, 2, 8, 18, 30)
event_9 = Event(event_type_id=mens_basketball.id,
                date=dt,
                band_id=gold_band.id)
# 2/9/14	2:00pm	WBB Gopher
dt = datetime(2014, 2, 9, 13, 30)
event_10 = Event(event_type_id=womens_basketball.id,
                 date=dt,
                 band_id=gopher_band.id)
# 2/19/14	8:00pm	MBB Gold
dt = datetime(2014, 2, 19, 19, 15)
event_11 = Event(event_type_id=mens_basketball.id,
                 date=dt,
                 band_id=gold_band.id)
# 2/20/14	7:00pm	WBB Gopher
dt = datetime(2014, 2, 20, 18, 30)
event_12 = Event(event_type_id=womens_basketball.id,
                 date=dt,
                 band_id=gopher_band.id)
# 2/21/14	7:07pm	WH  Maroon
dt = datetime(2014, 2, 21, 18, 30)
event_13 = Event(event_type_id=womens_hockey.id,
                 date=dt,
                 band_id=maroon_band.id)
# 2/22/14	4:07pm	WH  Maroon
dt = datetime(2014, 2, 22, 15, 30)
event_14 = Event(event_type_id=womens_hockey.id,
                 date=dt,
                 band_id=maroon_band.id)
# 2/25/14	6:00pm	MBB Gold
dt = datetime(2014, 2, 25, 17, 15)
event_15 = Event(event_type_id=mens_basketball.id,
                 date=dt,
                 band_id=gold_band.id)
# 2/27/14	7:00 or 9:00pm	WBB Gopher
dt = datetime(2014, 2, 27, 18, 30)
event_16 = Event(event_type_id=womens_basketball.id,
                 date=dt,
                 band_id=gopher_band.id)

db.session.add_all([event_1, event_2, event_3, event_4, event_5, event_6,
                    event_7, event_8, event_9, event_10, event_11, event_12,
                    event_13, event_14, event_15, event_16])
db.session.commit()
