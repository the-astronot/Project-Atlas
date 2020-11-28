import positions as pos
import calculations as calc
import datetime as dt

RA = 2.4021*15  # degrees
Decl = 11.4637  # degrees

date = dt.datetime.utcnow()
d = calc.getDayTime(date)

pos.RAtoAzimuth(RA, Decl, d)