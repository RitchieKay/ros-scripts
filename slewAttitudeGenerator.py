from quaternion import *

class SlewAttitudeGenerator:

    def __init__(self):
        self.rotation = None

    def set_rotation(self, r):
        self.angle = r.angle
        self.vector = r.vector

    def set_initial_attitude(self, a):
        self.attitudeI = a

    def get_intermediate_attitude(self, p):
        
        rQ = Rotation(self.angle * p, self.vector).quaternion()
        return (self.attitudeI * rQ).normalize()
