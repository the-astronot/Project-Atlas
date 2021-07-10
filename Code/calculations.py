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
    #print(year,month,day,hours,minutes,seconds)
    d = 367 * year - int((7 * (year + int((month + 9) / 12))) / 4) + int((275 * month) / 9) + day - 730530 + \
        hours/24.0 + minutes/1440.0 + seconds/86400.0
    return d


def readData(object_name, d):
    data = pos.getPositionData(object_name)
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
    geo = False
    offset = False
    if data[0][6] == "true":
        geo = True
    if data[1][6] == "true":
        offset = True
    return N,w,i,a,e,M,geo,offset


def calculatePosition(object_name, date):
    """
    Calculates the position of a given body at a given time
    :param object_name: Name of body
    :param date: current date and time
    :return: position
    """
    d = getDayTime(date)
    N,w,i,a,e,M,geo,offset = readData(object_name,d)
    NRad = math.radians(N)
    wRad = math.radians(w)
    iRad = math.radians(i)
    MRad = math.radians(M)
    E0 = M + (180/Pi) * e * math.sin(MRad) * (1 + e * math.cos(MRad))
    E = getEccVal(E0,e,M)
    x = a * (math.cos(math.radians(E)) - e)
    y = a * math.sqrt(1 - e**2) * math.sin(math.radians(E))
    r = math.sqrt(x * x + y * y)
    v = rev(math.degrees(math.atan2(y, x)))
    vRad = math.radians(v)
    #print("R-V:",r,v)
    coords = pos.RVtoLatLong(r, vRad, NRad, wRad, iRad, d, offset)

    if object_name == "moon":
        coord_mods = addMoonPerturbations(d,N+w+M,M,w+M)
        for x in range(3):
            coords[x] += coord_mods[x]

    RA, Decl = pos.EcliptoRA(coords[0], coords[1], coords[2], d)
    #print("RA h, Decl deg:",RA/15,Decl)
    topRA, topDecl = converttoTopo(geo,coords[2],pos.getTelescopeCoords()[0],RA,Decl,d)
    print("RA h,Decl deg:",topRA/15,topDecl)
    pos.RAtoAzimuth(topRA,topDecl,d)
    showRightAscensionDeclination(topRA,topDecl)


def showRightAscensionDeclination(RA,Decl):
    deg_mod = Decl/abs(Decl)
    ttra = 3600*RA/15
    hours = math.floor(ttra/3600)
    remainder = ttra-(hours*3600)
    minutes = math.floor(remainder/60)
    seconds = remainder - (minutes*60)
    degs = math.floor(abs(Decl))
    ttdecl = 3600*(abs(Decl)-math.floor(abs(Decl)))
    mins = math.floor(ttdecl/60)
    secs = ttdecl - (mins*60)

    print("RA: {0}h {1}m {2}s -- Decl: {3}\u00b0 {4}\' {5}\""
          .format(hours,minutes,int(seconds),int(degs*deg_mod),mins,int(secs)))


def extrapolateInfo(N,w,i,a,e,M,d):

    # Convert to Radians
    NRad = math.radians(N)
    wRad = math.radians(w)
    iRad = math.radians(i)
    MRad = math.radians(M)
    # Calculate secondary orbital elements
    L = M + w + N  # mean longitude




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
    while deg < 0.0:
        deg += 360.0
    while deg >= 360.0:
        deg -= 360.0
    return deg


def converttoTopo(geo, r, lat, RA, Decl, d):
    if geo:
        par = math.degrees(math.asin(1 / r))
    else:
        par = (8.794 / 3600)/r  # deg/A.U.

    gclat = lat - 0.1924 * math.sin(2 * math.radians(lat))
    rho = 0.99833 + 0.00167 * math.cos(2 * math.radians(lat))
    #print("Gclat:", gclat, "Rho:", rho)
    #pos.RAtoAzimuth(RA, Decl, d)
    LST = findLST(d)
    HA = rev(LST - RA+180)-180
    DeclRad = math.radians(Decl)
    HARad = math.radians(HA)
    gclatRad = math.radians(gclat)
    gRad = math.atan(math.tan(gclatRad) / math.cos(HARad))
    #print("g:",math.degrees(gRad)+90)
    topRA = RA - par * rho * math.cos(gclatRad) * math.sin(HARad) / math.cos(DeclRad)
    topDecl = Decl - par * rho * math.sin(gclatRad) * math.sin(gRad - DeclRad) / math.sin(gRad)
    return topRA, topDecl


def findLST(d):
    UT = (d - math.floor(d)) * 24
    ws = 282.9404 + 4.70935*(10**-5) * d
    Ms = 356.0470 + 0.9856002585 * d
    L = rev(Ms + ws)
    #print("L:", L)
    GMST0 = L/15 + 12
    #print("GMST0", GMST0)
    TLong = pos.getTelescopeCoords()[1]
    #TLong = -71.15390
    LST = GMST0 + UT + TLong / 15
    LST = rev(LST*15)
    #print("LST:", LST)
    return LST  # degrees


def offsetSun(d):
    NS,wS,iS,aS,eS,MS,geo,offset = readData("sun", d)
    MSRad = math.radians(MS)
    ES = MS + (180/Pi) * eS * math.sin(MSRad) * (1 + eS * math.cos(MSRad))
    #ES = getEccVal(E0, eS, MS)
    xS = math.cos(math.radians(ES)) - eS
    yS = math.sin(math.radians(ES)) * math.sqrt(1 - eS**2)
    #print("xs-ys:",xS,yS)
    rS = math.sqrt(xS**2 + yS**2)
    vS = math.degrees(math.atan2(yS,xS))
    #print("w,a,e,M:",wS,aS,eS,MS)
    #print("vS, wS", vS, wS)
    longS = rev(vS + wS)
    xs = rS*math.cos(math.radians(longS))
    ys = rS*math.sin(math.radians(longS))
    #print("XS-Y:",xs,ys)
    return xs, ys


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
    # Latitude Perturbations
    lat = 0
    lat += -0.173 * math.sin(FRad - 2 * DRad)
    lat += -0.055 * math.sin(MmRad - FRad - 2 * DRad)
    lat += -0.046 * math.sin(MmRad + FRad - 2 * DRad)
    lat += 0.033 * math.sin(FRad + 2 * DRad)
    lat += 0.017 * math.sin(2 * MmRad + FRad)
    # Radius Perturbations
    r = 0
    r += -0.58 * math.cos(MmRad - 2 * DRad)
    r += -0.46 * math.cos(2 * DRad)
    #print("LatMod:",lat,"LongMod:",long,"RMod:",r)
    return lat, long, r
