"""
Calculates the angle and azimuth required to view an astral body
"""
import math

# Global Variables


# Gets Telescope's Coordinates
def getTelescopeCoords():
    lat = 32.454545  # Replace with real values from gps sensor
    long = 45.323232  # Replace with real values from gps sensor
    height_above_sea_level = 42  # You know the drill
    coords = [lat,  long, height_above_sea_level]
    return coords


def getObjectCoords(obj_name):
    obj_file = open("../Data/{}.csv".format(obj_name))
    obj_data = obj_file.read()
