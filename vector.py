import math
from decimal import Decimal

class Book(object):
      def __init__(self,title,author):
          self.title = title
          self.author = author

      def __iter__(self):
          for each in self.__dict__.keys():
              yield self.__getattribute__(each)
            
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

    # http://stackoverflow.com/questions/5434400/python-is-it-possible-to-make-a-class-iterable-using-the-standard-syntax        
    def __iter__(self):
          for each in self.__dict__.keys():
              yield self.__getattribute__(each)
            
    def __getitem__(self,index):
        if index <5:
            return self.coordinates[index]
        else:
            raise IndexError('this is high enough')
                    
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

    def __mul__(self, scalar_n):
        total = [x * scalar_n for x in self.coordinates]
        return Vector(total)

    def mag(self):
        sqmagnitude = Decimal(0.0)
        for n in range(0, self.dimension):
            sqmagnitude += Decimal(self.coordinates[n]**2)
        return float(math.sqrt(sqmagnitude))

    def normalize(self):
        mag = self.mag()
        n_vector = []
        for n in range(0, self.dimension):
            n_vector.append(self.coordinates[n]/mag)
        return Vector(n_vector)

    def dp(self, v):
        total = [x*y for x, y in zip(self.coordinates, v.coordinates)]
        return sum(total)

    def angle(self, v, is_degrees=False):
        dptot = Decimal(self.dp(v))
        return_angle = math.acos(dptot/(Decimal(self.mag())*Decimal(v.mag())))
        if is_degrees:
            return return_angle * Decimal(180/math.pi)
        else:
            return return_angle

    def is_parallel(self, v):
        tolerance = Decimal(1e-9)
        if abs(Decimal(self.angle(v))) < tolerance:
            return True
        elif abs(Decimal(self.angle(v))-Decimal(math.pi)) < tolerance:
            return True
        else:
            return False

    def is_orthogonal(self, v):
        tolerance = 1e-9
        return abs(self.dp(v)) < tolerance

    def proj(self, b):
        return self.parallel(b)

    def perp(self, b):
        pc = self.sub(self.parallel(b))
        return pc

    def parallel(self, b):
        bn = b.normalize()
        return bn*self.dp(bn)

    def components(self, b):
        return self.parallel(b), self.perp(b)

    def cp(self, v, dim=3):
        cp = []
        try:
            if self.dimension == 3 and v.dimension == 3 and dim == 3:
                cp.append(self.coordinates[1]*v.coordinates[2]-self.coordinates[2]*v.coordinates[1])
                cp.append(self.coordinates[2]*v.coordinates[0]-self.coordinates[0]*v.coordinates[2])
                cp.append(self.coordinates[0]*v.coordinates[1]-self.coordinates[1]*v.coordinates[0])
                return Vector(cp)
            elif self.dimension == 2 and v.dimension == 2 and dim == 2:
                self.coordinates[2] = 0
                v.coordinates[2] = 0
                cp[0] = self.coordinates[1]*v.coordinates[2]-self.coordinates[2]*v.coordinates[1]
                cp[1] = self.coordinates[2]*v.coordinates[0]-self.coordinates[0]*v.coordinates[2]
                cp[2] = self.coordinates[0]*v.coordinates[1]-self.coordinates[1]*v.coordinates[0]
                return Vector(cp)
        except ValueError:
            raise ValueError('The vectors must both be 2 or 3 dimensions')

    def area_para(self, v):
        dim = self.dimension
        cp = self.cp(v, dim)
        return cp.mag()

    def area_tri(self, v):
        return 0.5*self.area_para(v)



    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates