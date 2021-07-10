#/usr/bin/python3

from PlaneShift import *

def run():
    vec1 = Vec2(13, 5)
    vec2 = Vec2(4.9191, 3.1301)
    vec3 = Vec2(19, 14)
    vec4 = Vec2(14.3101, 8.4960)
    ps = PlaneShift(vec1, vec2, vec3, vec4)
    test_c = Vec2(7, 6)
    test_d = Vec2(-2, 10)
    answer_c = ps.calculate_shifted(test_c)
    answer_d = ps.calculate_shifted(test_d)
    print("Point C: ( {0}, {1} )".format(answer_c.x, answer_c.y))
    print("Point D: ( {0}, {1} )".format(answer_d.x, answer_d.y))


if __name__ == '__main__':
    run()
