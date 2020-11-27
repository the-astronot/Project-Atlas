"""
Functions for all of the calculations required to aim the telescope
"""
import math
import positions as pos

# Global Variables
Pi = 3.14159265358979323846


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
    geo = False
    if data[0][6] == "true":
        geo = True
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
    x = a * (math.cos(math.radians(E)) - e)
    y = a * math.sqrt(1 - e**2) * math.sin(math.radians(E))
    r = math.sqrt(x * x + y * y)
    vRad = math.atan2(y, x)
    v = rev(math.degrees(vRad))
    #print(r,v)
    #xeclip = r * (math.cos(NRad) * math.cos(vRad+ wRad) - math.sin(NRad) * math.sin(vRad + wRad) * math.cos(iRad))
    #yeclip = r * (math.sin(NRad) * math.cos(vRad + wRad) + math.cos(NRad) * math.sin(vRad + wRad) * math.cos(iRad))
    #zeclip = r * math.sin(vRad + wRad) * math.sin(iRad)
    #print(xeclip,yeclip,zeclip)
    #coords = pos.XYZtoLatLongR(xeclip,yeclip,zeclip)
    coords = pos.RVtoLatLong(r, vRad, NRad, wRad, iRad)
    if object_name == "moon":
        coord_mods = addMoonPerturbations(d,N+w+M,M,w+M)
        for x in range(2):
            coords[x] += coord_mods[x]
    RA, Decl = pos.EcliptoRA(coords[0], coords[1], r, d)
    print("RA h, Decl deg: ",RA/15,Decl)
    topRA, topDecl = converttoTopo(geo,r,coords[0],RA,Decl,d)
    print("RA h,Decl deg:",topRA/15,topDecl)
    pos.RAtoAzimuth(topRA,topDecl,d)


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
    """
    Returns the value of a given variable between 0 and 360 degrees
    :param deg:
    :return: deg
    """
    return deg - math.floor(deg/360.0)*360


def converttoTopo(geo, r, lat, RA, Decl, d):
    if geo:
        par = math.degrees(math.asin(1 / r))
    else:
        par = (8.794 / 3600)/r  # deg/A.U.

    gclat = lat - 0.1924 * math.sin(2 * math.radians(lat))
    rho = 0.99833 + 0.00167 * math.cos(2 * math.radians(lat))
    # simplifying
    #gclat = lat
    #rho = 1.0
    pos.RAtoAzimuth(RA, Decl, d)
    LST = findLST(d)
    HA = LST - RA
    DeclRad = math.radians(Decl)
    HARad = math.radians(HA)
    gclatRad = math.radians(gclat)
    g = rev(math.degrees(math.atan(math.tan(gclatRad) / math.cos(HARad))))
    print("g:",g)
    topRA = RA - par * rho * math.cos(gclatRad) * math.sin(HARad) / math.cos(DeclRad)
    topDecl = Decl - par * rho * math.sin(gclatRad) * math.sin(g - DeclRad) / math.sin(math.radians(g))
    return topRA, topDecl


def findLST(d):
    UT = (d - math.floor(d)) * 24
    ws = 282.9404 + 4.70935*(10**-5) * d
    Ms = 356.0470 + 0.9856002585 * d
    L = rev(Ms + ws)
    print("L:", L)
    GMST0 = L/15 + 12
    print("GMST0", GMST0)
    TLong = pos.getTelescopeCoords()[1]
    LST = GMST0 + UT + TLong / 15
    LST = rev(LST*15)
    print("LST:", LST)
    return LST  # degrees


def addMoonPerturbations(d, Lm, Mm, F):
    Ms = 356.0470 + 0.9856002585 * d
    Ls = 282.9404 + 4.70935*(10**-5) * d + Ms
    D = Lm - Ls
    LsRad = math.radians(Ls)
    LmRad = math.radians(Lm)
    MsRad = math.radians(Ms)
    MmRad = math.radians(Mm)
    DRad = math.radians(D)
    FRad = math.radians(F)
    # Longitude Perturbations
    long = 0
    long += -1.274* math.sin(MmRad - 2 * DRad)  # (Evection)
    long += 0.658* math.sin(2 * DRad)  # (Variation)
    long += -0.186* math.sin(MsRad)  # (Yearly equation)
    long += -0.059* math.sin(2 * MmRad - 2 * DRad)
    long += -0.057* math.sin(MmRad - 2 * DRad + MsRad)
    long += 0.053* math.sin(MmRad + 2 * DRad)
    long += 0.046* math.sin(2 * DRad - MsRad)
    long += 0.041* math.sin(MmRad - MsRad)
    long += -0.035* math.sin(DRad)
    long += -0.031* math.sin(MmRad + MsRad)
    long += -0.015* math.sin(2 * FRad - 2 * DRad)
    long += 0.011* math.sin(MmRad - 4 * DRad)

    lat = 0
    r = 0

    return long, lat, r
