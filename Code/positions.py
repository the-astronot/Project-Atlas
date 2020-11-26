import math
import calculations as calc


# Gets Telescope's Coordinates
def getTelescopeCoords():
    lat = 42.4793  # Replace with real values from gps sensor
    long = -71.1523  # Replace with real values from gps sensor
    #long = 15
    coords = [lat,  long]
    return coords


def getPositionData(object_name):
    try:
        obj_file = open("../Data/{}.csv".format(object_name))
        obj_data = obj_file.read()
        obj_lists = obj_data.split("\n")
        primary_list = obj_lists[0].split(",")
        secondary_list = obj_lists[1].split(",")
        obj_data = [primary_list, secondary_list]
        for x in range(2):
            for y in range(6):
                obj_data[x][y] = float(obj_data[x][y])
        #print(obj_data)
        obj_file.close()
        return obj_data
    except FileNotFoundError:
        print("No such object found")


def XYZtoLatLongR(x,y,z):
    lat = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))
    long = math.degrees(math.atan2(y,x))
    r = math.sqrt(x**2 + y**2 + z**2)
    coords = [lat, long, r]
    return coords


def EcliptoRA(lat, long, r, d):
    latRad = math.radians(lat)
    longRad = math.radians(long)
    xeclip = r * math.cos(longRad) * math.cos(latRad)
    yeclip = r * math.sin(longRad) * math.cos(latRad)
    zeclip = r * math.sin(latRad)
    oblecl = math.radians(23.4393 - 3.563*(10**-7) * d)
    xequat = xeclip
    yequat = yeclip * math.cos(oblecl) - zeclip * math.sin(oblecl)
    zequat = yeclip * math.sin(oblecl) + zeclip * math.cos(oblecl)
    RA = calc.rev(math.degrees(math.atan2(yequat, xequat)))
    Decl = math.degrees(math.atan2(zequat, math.sqrt(xequat**2 + yequat**2)))
    return RA, Decl


def RAtoAzimuth(RA, Decl, d):
    LST = calc.findLST(d)
    TLat = getTelescopeCoords()[0]
    HA = calc.rev(LST - RA)
    print("HA:", HA)
    x = math.cos(math.radians(HA)) * math.cos(math.radians(Decl))
    y = math.sin(math.radians(HA)) * math.cos(math.radians(Decl))
    z = math.sin(math.radians(Decl))
    xhor = x * math.sin(math.radians(TLat)) - z * math.cos(math.radians(TLat))
    yhor = y
    zhor = x * math.cos(math.radians(TLat)) + z * math.sin(math.radians(TLat))
    azimuth = math.degrees(math.atan2(yhor, xhor)) + 180
    altitude = math.degrees(math.asin(zhor))
    print(azimuth, altitude)

