import math

class PlaneShift():
    '''
    
    '''
    def __init__(self, pl1_p1, pl2_p1, pl1_p2, pl2_p2):
        self.min_error = 0.1
        self.point_1 = Point(pl1_p1, pl2_p1)
        self.point_2 = Point(pl1_p2, pl2_p2)
        self.theta = self.calculate_theta() #RADIANS
        self.calculate_offset()

    # Find the angle theta between the axis of the two
    # 2D planes with shared Z axis
    def calculate_theta(self):
        x_diff = self.point_2.pl1.x - self.point_1.pl1.x
        y_diff = self.point_2.pl1.y - self.point_1.pl1.y
        x_p_diff = self.point_2.pl2.x - self.point_1.pl2.x
        y_p_diff = self.point_2.pl2.y - self.point_1.pl2.y
        r1 = math.hypot(x_diff, y_diff)
        r2 = math.hypot(x_p_diff, y_p_diff)
        #print(r1)
        #print(r2)
        assert(abs(r2-r1) < self.min_error)
        theta_0 = math.acos(x_diff/r1)
        theta_p = math.acos(x_p_diff/r2)
        return theta_0 - theta_p

    # Takes a point from plane 1 and outputs the coords 
    # for the same point from the POV of plane 2
    def calculate_shifted(self, point0):
        pi_2 = float(math.pi/2.0) # PI/2
        point = Vec2(0,0) # Just initializing
        # Follows the format: p' = x*cos(theta) + y*sin(theta)
        point.x = (point0.x)*math.cos(self.theta) + \
            (point0.y)*math.sin(self.theta) + self.offset.x
        point.y = (point0.x)*math.cos(self.theta+pi_2) + \
            (point0.y)*math.sin(self.theta+pi_2)+self.offset.y
        return point

    # We have the slope, but require an offset in the x and y dimensions
    # to give us some kind of reference for the locations of the centers 
    # of the planes relative to each other
    def calculate_offset(self):
        self.offset = Vec2(0,0)
        point_1_calc = self.calculate_shifted(self.point_1.pl1)
        self.offset.x = self.point_1.pl2.x - point_1_calc.x
        self.offset.y = self.point_1.pl2.y - point_1_calc.y
        print(self.offset.x, self.offset.y)


# Dummy Struct to hold x y coords
class Vec2():
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Dummy Struct to hold same points from both planes
class Point():
    def __init__(self, pl1, pl2):
        self.pl1 = pl1
        self.pl2 = pl2