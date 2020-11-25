"""
Functions for all of the calculations required to aim the telescope
"""
import math
import positions as pos

# Global Variables
Pi = 3.14159265358979323846


# Gets Telescope's Coordinates
def getTelescopeCoords():
    lat = 42.4793  # Replace with real values from gps sensor
    long = 71.1523  # Replace with real values from gps sensor
    height_above_sea_level = 42  # You know the drill
    coords = [lat,  long, height_above_sea_level]
    return coords


def getDayTime(date):
    """
    :type date: datetime.datetime
    Verified Correct
    """
    year = date.year
    month = date.month
    day = date.day
    hours = date.hour
    minutes = date.minute
    seconds = date.second
    print(date.ctime())
    d = 367 * year - int((7 * (year + ((month + 9) / 12))) / 4) + int((275 * month) / 9) + day - 730530 + \
        hours/24.0 + minutes/1440.0 + seconds/86400.0
    return d


def calculatePosition(object_name, date):
    """
    Calculates the position of a given body at a given time
    :param object_name: Name of body
    :param date: current date and time
    :return: position
    """
    data = pos.getPositionData(object_name)
    d = getDayTime(date)
    N = data[0][0] + data[1][0] * d  # deg
    w = data[0][1] + data[1][1] * d  # deg
    i = data[0][2] + data[1][2] * d  # deg
    a = data[0][3] + data[1][3] * d
    e = data[0][4] + data[1][4] * d
    M = data[0][5] + data[1][5] * d  # deg
    N = rev(N)
    w = rev(w)
    i = rev(i)
    M = rev(M)
    NRad = math.radians(N)
    wRad = math.radians(w)
    iRad = math.radians(i)
    MRad = math.radians(M)
    E0 = M + (180/Pi) * e * math.sin(MRad) * (1 + e * math.cos(MRad))
    E = getEccVal(E0,e,M)
    print(d)
    print(N,w,i,a,e,M)
    print(E0,E)
    x = a * (math.cos(math.radians(E)) - e)
    y = a * math.sqrt(1 - e**2) * math.sin(math.radians(E))
    print(x, y)
    r = math.sqrt(x * x + y * y)
    vRad = math.atan2(y, x)
    v = rev(math.degrees(vRad))
    print(r,v)
    xeclip = r * (math.cos(NRad) * math.cos(vRad+ wRad) - math.sin(NRad) * math.sin(vRad + wRad) * math.cos(iRad))
    yeclip = r * (math.sin(NRad) * math.cos(vRad + wRad) + math.cos(NRad) * math.sin(vRad + wRad) * math.cos(iRad))
    zeclip = r * math.sin(vRad + wRad) * math.sin(iRad)
    print(xeclip,yeclip,zeclip)
    coords = pos.XYZtoLatLongR(xeclip,yeclip,zeclip)
    print(coords)
    pos.EcliptoRA(coords[0], coords[1], coords[2], d)


def getEccVal(E0, e, M):
    """
    Recursively finds the eccetricity of a given astral body
    :param E0: First guess at eccentricity, E_0
    :param e: eccentric anomaly
    :param M: mean anomaly
    :return: E, the eccentricity calculated
    """
    E = E0 - ((E0 - (180/Pi) * e * math.sin(math.radians(E0)) - M) / (1 - e * math.cos(math.radians(E0))))
    if abs(E0-E) > .005:
        return getEccVal(E,e,M)
    else:
        return E


def rev(deg):
    '''
    Returns the value of a given variable between 0 and 360 degrees
    :param deg:
    :return: deg
    '''
    return deg - math.floor(deg/360.0)*360
