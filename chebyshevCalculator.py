#!/usr/bin/python
import math
from chebyshev import *

def cheb_0_f(x):
    return 1.0
def cheb_1_f(x):
    return x
def cheb_2_f(x):
    return 2*x*x -1
def cheb_3_f(x):
    return 4*x*x*x - 3*x
def cheb_4_f(x):
    return 8*x*x*x*x - 8*x*x +1
def cheb_5_f(x):
    return 16 * x*x*x*x*x -20 *x*x*x + 5*x
def cheb_6_f(x):
    return 32*x*x*x*x*x*x -48 * x*x*x*x + 18*x*x - 1
def cheb_7_f(x):
    return 64 *x*x*x*x*x*x*x -112 * x*x*x*x*x + 56 * x*x *x -7*x


class ChebyshevCalculator:

    def __init__(self, f):
        self.f = f

    def computeQuaternionCoefficients(self, steps):


        coefficients = [0] * 4
        coefficients[0] = [0] * 8
        coefficients[1] = [0] * 8
        coefficients[2] = [0] * 8
        coefficients[3] = [0] * 8

        for i in range(steps):
            xi = math.cos(math.pi*(2*i-1)/steps)
            a = self.f(xi)
            coefficients[0][0] += math.pi/steps*a[0]*cheb_0_f(xi)/math.pi
            coefficients[0][1] += math.pi/steps*a[0]*cheb_1_f(xi)*2.0/math.pi
            coefficients[0][2] += math.pi/steps*a[0]*cheb_2_f(xi)*2.0/math.pi
            coefficients[0][3] += math.pi/steps*a[0]*cheb_3_f(xi)*2.0/math.pi
            coefficients[0][4] += math.pi/steps*a[0]*cheb_4_f(xi)*2.0/math.pi
            coefficients[0][5] += math.pi/steps*a[0]*cheb_5_f(xi)*2.0/math.pi
            coefficients[0][6] += math.pi/steps*a[0]*cheb_6_f(xi)*2.0/math.pi
            coefficients[0][7] += math.pi/steps*a[0]*cheb_7_f(xi)*2.0/math.pi

            coefficients[1][0] += math.pi/steps*a[1]*cheb_0_f(xi)/math.pi
            coefficients[1][1] += math.pi/steps*a[1]*cheb_1_f(xi)*2.0/math.pi
            coefficients[1][2] += math.pi/steps*a[1]*cheb_2_f(xi)*2.0/math.pi
            coefficients[1][3] += math.pi/steps*a[1]*cheb_3_f(xi)*2.0/math.pi
            coefficients[1][4] += math.pi/steps*a[1]*cheb_4_f(xi)*2.0/math.pi
            coefficients[1][5] += math.pi/steps*a[1]*cheb_5_f(xi)*2.0/math.pi
            coefficients[1][6] += math.pi/steps*a[1]*cheb_6_f(xi)*2.0/math.pi
            coefficients[1][7] += math.pi/steps*a[1]*cheb_7_f(xi)*2.0/math.pi

            coefficients[2][0] += math.pi/steps*a[2]*cheb_0_f(xi)/math.pi
            coefficients[2][1] += math.pi/steps*a[2]*cheb_1_f(xi)*2.0/math.pi
            coefficients[2][2] += math.pi/steps*a[2]*cheb_2_f(xi)*2.0/math.pi
            coefficients[2][3] += math.pi/steps*a[2]*cheb_3_f(xi)*2.0/math.pi
            coefficients[2][4] += math.pi/steps*a[2]*cheb_4_f(xi)*2.0/math.pi
            coefficients[2][5] += math.pi/steps*a[2]*cheb_5_f(xi)*2.0/math.pi
            coefficients[2][6] += math.pi/steps*a[2]*cheb_6_f(xi)*2.0/math.pi
            coefficients[2][7] += math.pi/steps*a[2]*cheb_7_f(xi)*2.0/math.pi

            coefficients[3][0] += math.pi/steps*a[3]*cheb_0_f(xi)/math.pi
            coefficients[3][1] += math.pi/steps*a[3]*cheb_1_f(xi)*2.0/math.pi
            coefficients[3][2] += math.pi/steps*a[3]*cheb_2_f(xi)*2.0/math.pi
            coefficients[3][3] += math.pi/steps*a[3]*cheb_3_f(xi)*2.0/math.pi
            coefficients[3][4] += math.pi/steps*a[3]*cheb_4_f(xi)*2.0/math.pi
            coefficients[3][5] += math.pi/steps*a[3]*cheb_5_f(xi)*2.0/math.pi
            coefficients[3][6] += math.pi/steps*a[3]*cheb_6_f(xi)*2.0/math.pi
            coefficients[3][7] += math.pi/steps*a[3]*cheb_7_f(xi)*2.0/math.pi

        c = [Chebyshev(7), Chebyshev(7), Chebyshev(7), Chebyshev(7)]
        for i in range(4):
            for j in range(8):
                c[i].add_coefficient(j, coefficients[i][j])

        return c

def main():
    c = ChebyshevCalculator(cheb_1_f)
    print c.computeCoefficients() 


if __name__ == '__main__':
    main()
