import math

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
            total = [x+y for x,y in zip(self.coordinates,other.coordinates)]
            return Vector(total)

        except ValueError:
            raise ValueError('The vectors must have the same number of dimensions')

    def __sub__(self, other):
        try:
            if not self.dimension == other.dimension:
                raise ValueError
            total = [x-y for x,y in zip(self.coordinates, other.coordinates)]
            return Vector(total)

        except ValueError:
            raise ValueError('The vectors must have the same number of dimensions')

    def sub(self, other):
        try:
            if not self.dimension == other.dimension:
                raise ValueError
            total = [x-y for x,y in zip(self.coordinates, other.coordinates)]
            return Vector(total)

        except ValueError:
            raise ValueError('The vectors must have the same number of dimensions')

    def __mul__(self, other):
        total = [self.coordinates[n]*other for n in self.coordinates]
        return Vector(total)

    def mag(self):
        sqmagnitude = 0.0
        for n in range(0, self.dimension):
            sqmagnitude += self.coordinates[n]**2
        return math.sqrt(sqmagnitude)

    def normal(self):
        mag = self.mag()
        n_vector = []
        for n in range(0, self.dimension):
            n_vector.append(self.coordinates[n]/mag)
        return Vector(n_vector)

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates