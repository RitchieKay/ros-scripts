#!/usr/bin/python
import sys
import math
import datetime
from ephemeridesParser import *
from autonomousGuidance import *
from quaternion import *

TOL = 0.995


class RotationPlanner:

    def __init__(self):
        self.rotations = [0,0,0]
        self.ephemerides = Ephemerides.makeEphemerides()

    def __getitem__(self, i):
        return self.rotations[i]

    def generate_rotations(self, attitudeI, attitudeE, t):

        sV = self.ephemerides.sunScVector(t)

        spacecraftSunVectorI =  -attitudeI.conjugate().rotate_vector(sV.norm()).norm()
        spacecraftSunVectorE =  -attitudeE.conjugate().rotate_vector(sV.norm()).norm()


        # rotation 1
        numerator = spacecraftSunVectorI.X()*spacecraftSunVectorE.X() + spacecraftSunVectorI.Z()*spacecraftSunVectorE.Z()
        denominator = math.sqrt(spacecraftSunVectorI.X()*spacecraftSunVectorI.X() + spacecraftSunVectorI.Z()*spacecraftSunVectorI.Z()) * \
                      math.sqrt(spacecraftSunVectorE.X()*spacecraftSunVectorE.X() + spacecraftSunVectorE.Z()*spacecraftSunVectorE.Z())

        cos_alpha = numerator / denominator
        angle1 = 0
        vector1 = Vector(0,0,0)
        if cos_alpha < -TOL:
            angle1 = math.pi
            vector1 = Vector(0,1,0)
        elif cos_alpha < TOL:
          angle1 = math.acos(cos_alpha)
          sign = spacecraftSunVectorI.Z() * spacecraftSunVectorE.X() - spacecraftSunVectorI.X() * spacecraftSunVectorE.Z()
          Y = 1
          if sign > 0:
              Y = -1
          vector1 = Vector(0, Y, 0)   
        
        self.rotations[0] = Rotation(angle1, vector1)

        # rotation 2
        spacecraftSunVectorXZ = self.rotations[0].quaternion().conjugate().rotate_vector(spacecraftSunVectorI)
   
        cos_alpha = spacecraftSunVectorXZ.scalarproduct(spacecraftSunVectorE)
 
        angle2 = 0
        vector2 = Vector(0,0,0)
        if cos_alpha < -TOL:
            angle2 = math.pi
            vector2 = Vector(1,0,0)
        elif cos_alpha < TOL:
            angle2 = math.acos(cos_alpha)
            vector2 = spacecraftSunVectorE.vectorproduct(spacecraftSunVectorXZ).norm()

        self.rotations[1] = Rotation(angle2, vector2)

        # rotation 3
        deltaQ = self.rotations[1].quaternion().conjugate() * self.rotations[0].quaternion().conjugate() * attitudeI.conjugate() * attitudeE

        angle3 = 0
        vector3 = Vector(0,0,0)

        if math.fabs(deltaQ.scalar()) < 0.995:
            angle3 = 2.0 * math.acos(deltaQ.scalar())
            vector3 = deltaQ.vector().norm()
            if angle3 > math.pi:
                angle3 = 2 * math.pi - angle3
                vector3 = -vector3

        self.rotations[2] = Rotation(angle3, vector3)

