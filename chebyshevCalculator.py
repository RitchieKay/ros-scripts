#!/usr/bin/python
import math

def cheb_0_f(x):
    return 1.0/math.sqrt(2)
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

    def computeCoefficients(self):

        coefficients = [0] * 8

        steps = 2000000
        dx = 2.0 / steps
        x = -1.0  + dx
        for j in range (steps-1):
            s = self.f(x)/math.sqrt(1-x*x)*dx*2.0/math.pi
            coefficients[0] += s*cheb_0_f(x)
            coefficients[1] += s*cheb_1_f(x)
            coefficients[2] += s*cheb_2_f(x)
            coefficients[3] += s*cheb_3_f(x)
            coefficients[4] += s*cheb_4_f(x)
            coefficients[5] += s*cheb_5_f(x)
            coefficients[6] += s*cheb_6_f(x)
            coefficients[7] += s*cheb_7_f(x)
            x += dx

        return coefficients

def main():
    c = ChebyshevCalculator(cheb_1_f)
    print c.computeCoefficients() 


if __name__ == '__main__':
    main()
