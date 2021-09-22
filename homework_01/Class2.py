# camelCase
class Point:
    is_parent = True

    # dunder - double underscore
    def __init__(self, x = 0):
        print('Point init called')
        self.x = x

    def who_am_i(self):
        print('I am parent')

    def __str__(self):
        return f'Point: x = {self.x}'

class TwoDimensionalPoint(Point):

    def __init__(self, x = 0, y = 0):
        print('Two init is called')
        super(TwoDimensionalPoint, self).__init__(x)
        self.y = y

    def who_am_i(self):
        print('I am two')

class ThreeDimensionalPoint(TwoDimensionalPoint):
    is_parent = False

    def __init__(self, x = 0, y = 0, z = 0):
        print('Three init is called')
        super(TwoDimensionalPoint, self).__init__()
        self.x = x
        self.y = y
        self.z = z

    def who_am_i(self):
        print('I am three')

    def __str__(self):
        return f'I am three and x = {self.x}, y = {self.y}, z = {self.z}'

# parent = Point()
# print(parent)
#
point_2d = TwoDimensionalPoint(3, 4)
# print(point_2d)

point_3d = ThreeDimensionalPoint(2, 5, 6)
# print(point_3d)

parent = Point()

parent.who_am_i()
point_2d.who_am_i()
point_3d.who_am_i()