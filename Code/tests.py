import positions as pos
import calculations as calc
import datetime as dt

RA = 1.4824*15  # degrees
Decl = 5.5354  # degrees

date = dt.datetime.utcnow()
d = calc.getDayTime(date)

pos.RAtoAzimuth(RA, Decl, d)