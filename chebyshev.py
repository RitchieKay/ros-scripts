#!/usr/bin/python
import datetime
import time
import time
import sys

class Chebyshev:

    def __init__(self, degree):
        self.degree = int(degree)
        self.coefficients = [0.0] * (self.degree + 1)

    def get_degree(self):
        return self.degree

    def add_coefficient(self, index, value):
        if index <= self.degree:
            self.coefficients[index] = value

    def get_coefficient(self, index):
        return self.coefficients[index]

    def get_coefficients(self):
        return self.coefficients

    def get_polynomials(self, t):

        poly = []
        poly.append(1)

        if self.degree == 0:
            return poly

        poly.append(t)

        if self.degree == 1:
            return poly

        for i in range(2,self.degree+1):
            poly.append(2 * t * poly[i-1] - poly[i-2] )

        return poly

    def get_polynomial(self, index, t):
        return self.get_polynomials(t)[index]

    def value(self, t):
        
        value = 0.0
        for i in range(self.degree + 1):
            value = value + float(self.get_coefficient(i)) * float(self.get_polynomial(i, t))
        return value

class Cheb_Coefficients:

    def __init__(self, number):
        self.number = number
        self.coefficients = [0.0] * number

    def get_number(self):
        return self.number

    def set_coefficient(self, index, value):
        self.coefficients[index] = value

    def get_coefficient(self, index):
        return self.coefficients[index]

    def get_coefficients(self):
        return self.coefficients


class Cheb_Normalized_time:

    def __init__(self, start_time, end_time):
        self.start_time = time.mktime(datetime.datetime.strptime(start_time, '%Y.%j.%H.%M.%S').utctimetuple())
        self.end_time = time.mktime(datetime.datetime.strptime(end_time, '%Y.%j.%H.%M.%S').utctimetuple())


    def get_t(self, time_str):
        t = time.mktime(datetime.datetime.strptime(time_str, '%Y.%j.%H.%M.%S').utctimetuple())

        t1 = 2 * (t - self.start_time) / (self.end_time - self.start_time) - 1

        return t1
   
    def get_time(self, t):
        m = (1.0 + t)/2
        s = self.start_time + m * (self.end_time - self.start_time)
        return datetime.datetime.utcfromtimestamp(s).strftime('%Y.%j.%H.%M.%S')
        
 
class Chebyshev_calculator:

    def  __init__(self, coeff):
        self.chebyshev = Chebyshev(len(coeff) - 1 )
        self.coefficients = coeff

    def value(self, t):
        number = self.chebyshev.get_degree() + 1
        if self.coefficients.get_number() < number:
            number = self.coefficients.get_number()
        
        value = 0
        for i in range(number):
            value = value + self.coefficients.get_coefficient(i) * self.chebyshev.get_polynomial(i, t)

        return value        

def main():

    sys.stdout.write('Enter degree of polynomial: ') 
    degree = int(sys.stdin.readline().strip())

    cheb = Chebyshev(degree)

    coeff = Cheb_Coefficients(degree + 1)

    sys.stdout.write('Enter Coefficients:\n') 
    for i in range(degree + 1):
        sys.stdout.write(str(i) + ': ')
        coeff.set_coefficient(i,  float(sys.stdin.readline().strip()))


    sys.stdout.write('Enter segment start time: ') 
    start = sys.stdin.readline().strip()
    sys.stdout.write('Enter segment end time: ') 
    end = sys.stdin.readline().strip()

    norm = Cheb_Normalized_time(start, end)

    calc = Chebyshev_calculator(cheb, coeff)

    sys.stdout.write('Enter number of points to display: ')
    points = int(sys.stdin.readline().strip())

    for i in range(points + 1):
        f = -1.0 + 2.0 * i / points

        print norm.get_time(f), calc.value(f)


if __name__ == '__main__':
    main()
