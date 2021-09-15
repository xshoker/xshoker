class Point:
    is_parent = True

    def __init__(self, x=0):
        print('Point init called')
        self.x = x

    def who_am_i(self):
        print('I am a parent point')

    def __str__(self):
        return f'Point: x = {self.x}'


class TwoDimensionalPoint(Point):

    def __init__(self, x=0, y=0):
        print('TwoDimensionalPoint init is called')
        super(TwoDimensionalPoint, self).__init__(x)
        self.y = y

    def who_am_i(self):
        print('I am a TwoDimensionalPoint point')


class ThreeDimensionalPoint(TwoDimensionalPoint):
    is_parent = False

    def __init__(self, z=0):
        super(ThreeDimensionalPoint, self).__init__()
        self.z = z

    def who_am_i(self):
        print('I am a ThreeDimensionalPoint point')

    def __str__(self):
        return f'ThreeDimensionalPoint: x={self.x}, y={self.y}, z={self.z}'

parent = Point()
print(parent)

point_2d = TwoDimensionalPoint(3, 4)
print(point_2d)

point_3d = ThreeDimensionalPoint(6)
print(point_3d)
