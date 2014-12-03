from quaternion import *
from inertiaParser import *
from rosettaConfiguration import *

K_INERTIA_TOL = 1.0
MAX_RATE = 0.00087
TRQ_CAPACITY = 0.05

class SlewAttitudeGenerator:

    def __init__(self):
        self.rotation = None
        self.inertia = InertiaParser(RosettaConfiguration().getItem('INERTIA')).inertia()
        self.legs = 0

    def set_rotation(self, a0, r):
        self.angle = r.angle
        self.vector = r.vector

        rot_axis_inertia = self.inertia.Iw(self.vector).magnitude()

        if rot_axis_inertia > K_INERTIA_TOL and self.angle > 0:
            self.max_rate = MAX_RATE
            self.accel  = TRQ_CAPACITY / rot_axis_inertia 

            K = math.sqrt(self.angle / self.accel)

            if K <= self.max_rate / self.accel:
                self.t1 = K
                self.t2 = K
                self.legs = 2
            else:
                self.t1 = self.max_rate / self.accel
                self.t2 = self.angle / self.max_rate
                self.legs = 3

            self.T = self.t1 + self.t2

        else:
            self.max_rate = 0
            self.accel = 0 
            self.t1 = 0
            self.t2 = 0
            self.T = 0

        self.a0 = a0
        self.a1 = a0 * Rotation(self.accel * self.t1 * self.t1 / 2, self.vector).quaternion()
        self.a2 = a0 * Rotation(self.angle - self.accel * self.t1 * self.t1 / 2, self.vector).quaternion()
        self.a3 = a0 * Rotation(self.angle, self.vector).quaternion() 

    def legs(self):
        return self.legs

    def slewTimes(self):
        return (self.T, self.t1, self.t2)

    def initialAttitude(self):
        return self.a0

    def finalAttitude(self):
        return self.a3

    def attitudeAtLegs(self):
        return (self.a0, self.a1, self.a2, self.a3)

    def get_intermediate_attitude_leg_1_normalized_t(self, t):
        return self.get_intermediate_attitude((t + 1) * self.t1 / 2)

    def get_intermediate_attitude_leg_2_normalized_t(self, t):
        return self.get_intermediate_attitude(self.t1 + (t + 1) * (self.t2 - self.t1) / 2)

    def get_intermediate_attitude_leg_3_normalized_t(self, t):
        return self.get_intermediate_attitude(self.t2 + (t + 1) * (self.T - self.t2) / 2)

    def get_intermediate_attitude_normalized_t(self, t):
        return self.get_intermediate_attitude((t + 1) * self.T / 2)

    def get_intermediate_attitude(self, t):

        if t < self.t1:
            angle = self.accel * t * t / 2
        elif t < self.t2:
            angle = self.accel * self.t1 * self.t1 / 2 + (t - self.t1) * self.max_rate
        else:
            angle = self.angle - self.accel * (self.T - t) * (self.T - t) / 2

        rQ = Rotation(angle, self.vector).quaternion()
        return (self.a0 * rQ).normalize()
