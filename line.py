from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            all_zeros = [Decimal(n) for n in all_zeros]
            normal_vector = Vector(all_zeros)
        else:
            nv = [Decimal(n) for n in normal_vector]
            normal_vector = Vector(nv)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector.coordinates
            c = self.constant_term
            bc = ['0']*self.dimension
            basepoint_coords = [Decimal(num) for num in bc]

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = Decimal(c)/Decimal(initial_coefficient)
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n.coordinates)
            terms = [write_coefficient(n.coordinates[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n.coordinates[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    def is_parallel(self, line2):
        na = self.normal_vector
        nb = line2.normal_vector
        return na.is_parallel(nb)

    def is_same(self, line2):
        if not self.is_parallel(line2):
            return False

        x0 = self.basepoint
        y0 = line2.basepoint
        basepoint_difference = x0 - y0

        n = self.normal_vector
        return basepoint_difference.is_orthogonal(n)

    def __eq__(self, other):

        if not self.is_parallel(other):
            return False

        x0 = self.basepoint
        y0 = other.basepoint
        basepoint_difference = x0 - y0

        n = self.normal_vector
        return basepoint_difference.is_orthogonal(n)

    def intersect(self, line2):
        if not self.is_same(line2):
            y_int_top = (line2.normal_vector.coordinates[0]*self.constant_term-self.normal_vector.coordinates[0]*line2.constant_term)
            int_bottom = (self.normal_vector.coordinates[0]*line2.normal_vector.coordinates[1]-self.normal_vector.coordinates[1]*line2.normal_vector.coordinates[0])
            y_int = Decimal(y_int_top)/Decimal(int_bottom)
            x_int_top = (line2.normal_vector.coordinates[1]*self.constant_term-self.normal_vector.coordinates[1]*line2.constant_term)
            x_int = Decimal(x_int_top)/Decimal(int_bottom)
            return x_int, -1*y_int
        else:
            return "infinite intersections"

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps