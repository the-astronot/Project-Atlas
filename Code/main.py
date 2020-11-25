import calculations as calc
import positions as pos
import time
import datetime as dt

if __name__ == "__main__":
    print("Welcome to Project Atlas")
    time.sleep(1)
    location = calc.getTelescopeCoords()
    print("Location: {0}N, {1}W".format(location[0], location[1]))
    current_time = dt.datetime.utcnow()
    d = calc.getDayTime(current_time)
    test_time = dt.datetime(1990, 4,19,0,0,0,0)
    print("Current Time: {} days since 31 Dec 1999".format(d))

    calc.calculatePosition("moon", current_time)
