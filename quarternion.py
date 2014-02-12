#!/usr/bin/python

import math
from vector import *

class Rotation:

    def __init__(self, angle, vector):

        self.angle = 1.0 * angle
        self.vector = vector

    def __str__(self):

        return str(self.angle) + ', ' + '(' + str(self.vector[0]) + ', ' + str(self.vector[1]) + ', ' + str(self.vector[2]) + ')'

    def __repr__(self):
        return str(self)

    def quarternion(self):

        mod = self.vector[0] ** 2 + self.vector[1] ** 2 + self.vector[2] ** 2
        v = [ math.sin(self.angle/2) * x / mod for x in self.vector ]
        s = math.cos(self.angle/2)

        return Quarternion(s, v[0], v[1], v[2])

class Quarternion:

    def __init__(self, s, v1, v2, v3):

        self.s  = 1.0 * s
        self.v1 = 1.0 * v1
        self.v2 = 1.0 * v2
        self.v3 = 1.0 * v3

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
             

        return Quarternion(q0, q1, q2, q3).normalize()

    def rotation(self):

        q = self
        q.normalize()

        angle = 2 * math.acos(q.scalar())
        vector = [1.0 * x / math.sin(1.0 * angle / 2) for x in q.vector()]

        return Rotation(angle, vector)

    def conjugate(self):
        return Quarternion(self.s, -self.v1, -self.v2, -self.v3)

    def norm(self):
        return math.sqrt((self * self.conjugate()).scalar())

    def normalize(self):
  
        n = self.norm()
        self.s = self.s / n
        self.v1 = self.v1 / n
        self.v2 = self.v2 / n
        self.v3 = self.v3 / n

        return self

    def rotate_vector(self, v):

        q0_2 = self.s * self.s
        q1_2 = self.v1 * self.v1
        q2_2 = self.v2 * self.v2
        q3_2 = self.v3 * self.v3


#      -- compute first element
#      VECT(X1) :=       T_FLOAT_EP(P_V(X1)) * (Q0_2 + Q1_2 - Q2_2 - Q3_2)
#                + 2.0 * T_FLOAT_EP(P_V(X2)) * (P_Q.VECT(X1)*P_Q.VECT(X2) + P_Q.SCAL*P_Q.VECT(X3))
#                + 2.0 * T_FLOAT_EP(P_V(X3)) * (P_Q.VECT(X1)*P_Q.VECT(X3) - P_Q.SCAL*P_Q.VECT(X2))

        v_x1 = v.X() * (q0_2 + q1_2 - q2_2 -q3_2) + 2.0 * v.Y() * (self.v1*self.v2 + self.s*self.v3) + 2.0 * v.Y() * (self.v1*self.v3 - self.s*self.v2)

#      -- compute second element
#      VECT(X2) := 2.0 * T_FLOAT_EP(P_V(X1)) * (P_Q.VECT(X1)*P_Q.VECT(X2) - P_Q.SCAL*P_Q.VECT(X3))
#                +       T_FLOAT_EP(P_V(X2)) * (Q0_2 - Q1_2 + Q2_2 - Q3_2)
#                + 2.0 * T_FLOAT_EP(P_V(X3)) * (P_Q.VECT(X2)*P_Q.VECT(X3) + P_Q.SCAL*P_Q.VECT(X1))

        v_x2 = 2.0 * v.X() * (self.v1*self.v2 - self.s*self.v3) + v.Y() * (q0_2 - q1_2 + q2_2 - q3_2) + 2.0 * v.Z() * (self.v2*self.v3 + self.s*self.v1)

#      -- compute third element
#      VECT(X3) := 2.0 * T_FLOAT_EP(P_V(X1)) * (P_Q.VECT(X1)*P_Q.VECT(X3) + P_Q.SCAL*P_Q.VECT(X2))
#                + 2.0 * T_FLOAT_EP(P_V(X2)) * (P_Q.VECT(X2)*P_Q.VECT(X3) - P_Q.SCAL*P_Q.VECT(X1))
#                +       T_FLOAT_EP(P_V(X3)) * (Q0_2 - Q1_2 - Q2_2 + Q3_2)

        v_x3 = 2.0 * v.X() * (self.v1*self.v3 + self.s*self.v2) + 2.0 * v.Y() * (self.v2*self.v3 - self.s*self.v1) + v.Z() * (q0_2 - q1_2 - q2_2 + q3_2)

        return Vector(v_x1, v_x2, v_x3)

    def print_rotated_axis(self):

        q = self.normalize()
        qp = q.conjugate()

        x = q * Quarternion(0,1,0,0) * qp
        y = q * Quarternion(0,0,1,0) * qp
        z = q * Quarternion(0,0,0,1) * qp

        print 'x: ', x.vector()
        print 'y: ', y.vector()
        print 'z: ', z.vector()

    def scalar(self):
        return self.s 

    def vector(self):
        return [self.v1, self.v2, self.v3]

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

        return Quarternion(q0, q1, q2, q3)

    def __str__(self):
  
        return '(' + str(self.s) + ', ' + str(self.v1) + ', ' + str(self.v2) + ', ' + str(self.v3) + ')'

    def __repr__(self):
        return str(self)

