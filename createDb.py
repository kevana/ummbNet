from ummbNet import *

db.drop_all()
db.create_all()


# Create bands
goldband = Band('Gold Band')
maroonband = Band('Maroon Band')
gopherband = Band('Gopher Band')

db.session.add_all([goldband, maroonband, gopherband])
db.session.commit()

# Create EventTypes
mbb = EventType("Men's Basketball")
wbb = EventType("Women's Basketball")
mh = EventType("Men's Hockey")
wh = EventType("Women's Hockey")
vb = EventType("Volleyball")

db.session.add_all([mbb, wbb, mh, wh, vb])
db.session.commit()

# Create Instruments
pic = Instrument('Piccolo')
flt = Instrument('Flute')
clar = Instrument('Clarinet')
altsax = Instrument('Alto Sax')
tensax = Instrument('Tenor Sax')
tpt = Instrument('Trumpet')
melo = Instrument('Mellophone')
tbone = Instrument('Trombone')
bari = Instrument('Baritone')
tuba = Instrument('Tuba')
dline = Instrument('Drumline')

db.session.add_all([pic, flt, clar, altsax, tensax, \
                    tpt, melo, tbone, bari, tuba, dline])
db.session.commit()
