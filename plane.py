from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Plane(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 3

        if not normal_vector:
            all_zeros = ['0']*self.dimension
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

            initial_index = Plane.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = Decimal(c)/Decimal(initial_coefficient)
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
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
            initial_index = Plane.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
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

    def is_parallel(self, other):
        nv1 = self.normal_vector
        print(nv1.coordinates)
        nv2 = other.normal_vector
        print(nv2.coordinates)

        return nv1.is_parallel(nv2)

    def is_equal(self, other):
        if not self.is_parallel(other):
            return False

        x0 = self.basepoint
        y0 = other.basepoint
        basepoint_difference = x0 - y0

        return basepoint_difference.is_orthogonal(self.normal_vector)
    
    def intersect(self, plane2, plane3):
        p1D = [Decimal(n) for n in self.normal_vector.coordinates]
        k1D = Decimal(self.constant_term)
        p2D = [Decimal(n) for n in plane2.normal_vector.coordinates]
        k2D = plane2.constant_term
        p3D = [Decimal(n) for n in plane3.normal_vector.coordinates]
        k3D = plane3.constant_term
        
        factor12 = -p1D[0]/p2D[0]
        mul_p2 = [factor12*n for n in p2D]
        new_p2 = [sum(x) for x in zip(mul_p2, p1D)]
        new_k2 = factor12*k2D + k1D
        print "new_k2 = " + str(new_k2)
        
        factor13 = -p1D[0]/p3D[0]
        print "factor13 = "  + str(factor13)
        mul_p13 = [factor13*n for n in p3D]
        print "mul_p13 = " + str(mul_p13)
        new_p13 = [sum(x) for x in zip(mul_p13, p1D)]
        print "new plane13 = " + str(new_p13)
        new_k13 = (factor13*k3D) + k1D
        print "new_k13 = " + str(new_k13)
        
        factor23 = -new_p2[1]/new_p13[1]
        print "factor23 = "  + str(factor23)
        mul_p3 = [factor23*n for n in new_p13]
        print "mul_p3 = " + str(mul_p3)
        new_p3 = [sum(x) for x in zip(mul_p3, new_p2)]
        print "new plane3 = " + str(new_p3)
        new_k3 = (factor23*new_k13) + new_k2
        print "new_k3 = " + str(new_k3)
        
        z = new_k3/new_p3[2]
        y = (new_k2-z*new_p2[2])/new_p2[1]
        x = (k1D - y*p1D[1] - z*p1D[2])/p1D[0]
        
        return x,y,z


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps