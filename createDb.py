from ummbNet import *
 
db.drop_all()
db.create_all()


# Create bands
gold_band = Band('Gold Band')
maroon_band = Band('Maroon Band')
gopher_band = Band('Gopher Band')

db.session.add_all([gold_band, maroon_band, gopher_band])
db.session.commit()

# Create EventTypes
mens_basketball = EventType("Men's Basketball")
womens_basketball = EventType("Women's Basketball")
mens_hockey = EventType("Men's Hockey")
womens_hockey = EventType("Women's Hockey")
volleyball = EventType("Volleyball")

db.session.add_all([mens_basketball, womens_basketball, mens_hockey, \
                    womens_hockey, volleyball])
db.session.commit()

# Create Instruments
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

db.session.add_all([piccolo, flute, clarinet, alto_sax, tenor_sax, \
                    trumpet, mellophone, trombone, baritone, tuba, drumline])
db.session.commit()
