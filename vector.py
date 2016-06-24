# class Vector(object):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def __add__(self, other):
#         x_total = self.x + other.x
#         y_total = self.y + other.y
#         return x_total, y_total
#
#     def __str__(self):
#         return self.x, self.y


class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __add__(self, other):
        try:
            if not self.dimension == other.dimension:
                raise ValueError
            total = []
            for n in range(0, self.dimension):
                total.append(self.coordinates[n]+other.coordinates[n])
            return Vector(total)

        except ValueError:
            raise ValueError('The vectors must have the same number of dimensions')

    def __sub__(self, other):
        try:
            if not self.dimension == other.dimension:
                raise ValueError
            total = []
            for n in range(0, self.dimension):
                total.append(self.coordinates[n]-other.coordinates[n])
            return Vector(total)

        except ValueError:
            raise ValueError('The vectors must have the same number of dimensions')

    def __mul__(self, other):
        total = []
        for n in range(0, self.dimension):
            total.append(self.coordinates[n]*other)
        return Vector(total)


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates