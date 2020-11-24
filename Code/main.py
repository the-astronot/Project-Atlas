import calculations as calc
import time

if __name__ == "__main__":
    print("Welcome to Project Atlas")
    time.sleep(1)
    location = calc.getTelescopeCoords()
    print("Location: {0}N, {1}E".format(location[0], location[1]))
