#!/usr/bin/python

import math
import re
from vector import *

class Rotation:

    def __init__(self, angle, vector):

        self.angle = 1.0 * angle
        self.vector = vector

    def angle(self):
        return self.angle

    def vector(self):
        return self.vector

    def __str__(self):

        return str(self.angle) + ', ' + '(' + str(self.vector[0]) + ', ' + str(self.vector[1]) + ', ' + str(self.vector[2]) + ')'

    def __repr__(self):
        return str(self)

    def quaternion(self):

        try:
            mod = self.vector.X() ** 2 + self.vector.Y() ** 2 + self.vector.Z() ** 2
            v = make_vector_from_list([ math.sin(self.angle/2) * x / mod for x in self.vector ])
            
            s = math.cos(self.angle/2)
            return Quaternion(s, v.X(), v.Y(), v.Z())
        except ZeroDivisionError:

            return Quaternion(1, 0, 0, 0)

class Quaternion:

    def __init__(self, s, v1, v2, v3):

        self.s  = 1.0 * s
        self.v1 = 1.0 * v1
        self.v2 = 1.0 * v2
        self.v3 = 1.0 * v3

    @staticmethod
    def nullQuaternion():
        return Quaternion(1,0,0,0)
    @staticmethod
    def createFromString(s):
        q = [float(a) for a in re.findall('\d+', s)]
        return Quaternion(q[0], q[1], q[2], q[3])
    @staticmethod
    def createFromVectors(v1, v2, v3):

        T11 = v1.X()
        T21 = v1.Y()
        T31 = v1.Z()
        T12 = v2.X()
        T22 = v2.Y()
        T32 = v2.Z()
        T13 = v3.X()
        T23 = v3.Y()
        T33 = v3.Z()


        v_pq = [0,0,0,0]

        v_pq[0] = math.fabs(1.0 + T11 + T22 + T33)
        v_pq[1] = math.fabs(1.0 + T11 - T22 - T33)
        v_pq[2] = math.fabs(1.0 - T11 + T22 - T33)
        v_pq[3] = math.fabs(1.0 - T11 - T22 + T33)

        index = 0
        maxVal = -1
        for i in range(4):
            if v_pq[i] > maxVal:
                index = i
                maxVal = v_pq[i]

        q0 = q1 = q2 = q3 = 0

        if index == 0:
            q0 = 0.5 * math.sqrt(v_pq[0])
            v_scal = 0.25 / q0
            q1 =  (T32 - T23) * v_scal
            q2 =  (T13 - T31) * v_scal
            q3 =  (T21 + T12) * v_scal
        elif index == 1:
            q1 = 0.5 * math.sqrt(v_pq[1])
            v_scal = 0.25 / q1
            q0 =  (T32 - T23) * v_scal
            q2 =  (T21 + T12) * v_scal
            q3 =  (T13 + T31) * v_scal
        elif index == 2:
            q2 = 0.5 * math.sqrt(v_pq[2])
            v_scal = 0.25 / q2
            q0 =  (T13 - T31) * v_scal
            q1 =  (T21 + T12) * v_scal
            q3 =  (T32 + T23) * v_scal
        elif index == 3:
            q3 = 0.5 * math.sqrt(v_pq[3])
            v_scal = 0.25 / q3
            q0 =  (T21 - T12) * v_scal
            q1 =  (T31 + T13) * v_scal
            q2 =  (T32 + T23) * v_scal
             
        return Quaternion(q0, q1, q2, q3).normalize()


    def conjugate(self):
        return Quaternion(self.s, -self.v1, -self.v2, -self.v3)

    def norm(self):
        return math.sqrt((self * self.conjugate()).scalar())

    def normalize(self):
  
        n = self.norm()
        self.s = self.s / n
        self.v1 = self.v1 / n
        self.v2 = self.v2 / n
        self.v3 = self.v3 / n

        return self

    def print_rotated_axis(self):

        q = self.normalize()
        qp = q.conjugate()

        x = q * Quaternion(0,1,0,0) * qp
        y = q * Quaternion(0,0,1,0) * qp
        z = q * Quaternion(0,0,0,1) * qp

        print 'x: ', self.rotate_vector(Vector(1,0,0))
        print 'y: ', self.rotate_vector(Vector(0,1,0))
        print 'z: ', self.rotate_vector(Vector(0,0,1))

    def rotate_vector(self, v):

        q = self.normalize()
        qp = q.conjugate()

        x = q * Quaternion(0,v.X(),v.Y(),v.Z()) * qp
        
        return x.vector() 


    def scalar(self):
        return self.s 

    def angle(self):
        s = self.s
        if self.s >= 1.0 or self.s <= -1.0:
            return 0
        return math.acos(self.s) * 2 

    def vector(self):
        return Vector(self.v1, self.v2, self.v3).normalize()

    def print_profile_coefficients(self, q2):

        print 's :', (self.s + q2.s)/2,  (q2.s - self.s)/2
        print 'v1:', (self.v1 + q2.v1)/2, (q2.v1 - self.v1)/2
        print 'v2:', (self.v2 + q2.v2)/2, (q2.v2 - self.v2)/2
        print 'v3:', (self.v3 + q2.v3)/2, (q2.v3 - self.v3)/2


    def __getitem__(self, i):
        if i == 0:
            return self.s
        elif i == 1:
            return self.v1
        elif i == 2:
            return self.v2
        elif i == 3:
            return self.v3

    def __mul__(self, other):

        u0 = self.s
        u1 = self.v1
        u2 = self.v2
        u3 = self.v3

        v0 = other.s
        v1 = other.v1
        v2 = other.v2
        v3 = other.v3

        q0 = u0 * v0 - u1 * v1 - u2 * v2 - u3 * v3

        q1 = u0 * v1 + v0 * u1 + u2 * v3 - u3 * v2
        q2 = u0 * v2 + v0 * u2 + u3 * v1 - u1 * v3
        q3 = u0 * v3 + v0 * u3 + u1 * v2 - u2 * v1 

        return Quaternion(q0, q1, q2, q3)

    def __str__(self):
  
        return '(' + str(self.s) + ', ' + str(self.v1) + ', ' + str(self.v2) + ', ' + str(self.v3) + ')'

    def __repr__(self):
        return str(self)

