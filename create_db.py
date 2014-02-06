'''
Script to load static database objects like
bands, event types, and instruments
'''

from alembic.config import Config
from alembic import command

from models import Band, EventType, Instrument


def db_insert_bands(db):
    '''Create Bands and insert into the database.'''
    gold_band = Band('Gold Band')
    maroon_band = Band('Maroon Band')
    gopher_band = Band('Gopher Band')

    db.session.add_all([gold_band, maroon_band, gopher_band])
    db.session.commit()
    print('Added bands')

def db_insert_event_types(db):
    '''Create EventTypes and insert into the database.'''
    mens_basketball = EventType("Men's Basketball")
    womens_basketball = EventType("Women's Basketball")
    mens_hockey = EventType("Men's Hockey")
    womens_hockey = EventType("Women's Hockey")
    volleyball = EventType("Volleyball")

    db.session.add_all([mens_basketball, womens_basketball,
                        mens_hockey, womens_hockey, volleyball])
    db.session.commit()
    print('Added event types')

def db_insert_instruments(db):
    '''Create Instruments and insert into the database.'''
    piccolo = Instrument('Piccolo')
    flute = Instrument('Flute')
    clarinet = Instrument('Clarinet')
    alto_sax = Instrument('Alto Sax')
    tenor_sax = Instrument('Tenor Sax')
    trumpet = Instrument('Trumpet')
    mellophone = Instrument('Mellophone')
    trombone = Instrument('Trombone')
    baritone = Instrument('Baritone')
    tuba = Instrument('Tuba')
    drumline = Instrument('Drumline')

    db.session.add_all([piccolo, flute, clarinet, alto_sax, tenor_sax,
                        trumpet, mellophone, trombone, baritone, tuba,
                        drumline])
    db.session.commit()
    print('Added instruments')

def db_insert_all(db):
    '''Create Bands, EventTypes, Instruments.'''
    db_insert_bands(db)
    db_insert_event_types(db)
    db_insert_instruments(db)


if __name__ == '__main__':
    from app import app, db
    db.drop_all()
    db.create_all()

    with app.app_context():
        alembic_cfg = Config('migrations/alembic.ini')
        command.stamp(alembic_cfg, 'head')

    db_insert_all(db)
