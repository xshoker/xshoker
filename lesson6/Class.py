# camelCase
class Point:
    class_attribute = True

    # dunder - double underscore
    def __init__(self, x, y):
        self.x = 4
        self.y = 5

    def __str__(self):
        return f"{self.__class__.__name__} (x = {self.x}, y = {self.y})"

point = Point(4, 6)
point_2 = Point(4, 6)
print(point, point.x, point.y)


print(point.class_attribute)
Point.class_attribute = False
print(point.class_attribute)
print(point_2.class_attribute)