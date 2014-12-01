
import math
from ephemerides import *

K_SUN_TOL_SQUARE = 3E-06

class sade:

    def __init__(self):
        self.position = {'YP':0.0, 'YM':0.0}
        self.ephemerides = Ephemerides.makeEphemerides()

    def yp(self):
        return self.position['YP']

    def ym(self):
        return self.position['YM']

    def compute_position(self, t, attitudeQuarternion):

        sunDirection = self.ephemerides.sunScVector(t).normalize()
        # Calculate spacecraft sun in reference frame
        spacecraftSunVector =  -attitudeQuarternion.conjugate().rotate_vector(sunDirection.norm()).norm()

        if (spacecraftSunVector.X() * spacecraftSunVector.X() + spacecraftSunVector.Z() * spacecraftSunVector.Z()) > K_SUN_TOL_SQUARE:

            self.position['YP'] = self.atan2(spacecraftSunVector.Z(), spacecraftSunVector.X())
            self.position['YM'] = -self.position['YP']


    def atan2(self, EX, EY):
        if EX > 0.0: 
            return math.atan(EY/EX)
        elif EX < 0.0:
            if (EY < 0.0):
                return math.atan(EY/EX) - math.pi
            else:     
              return math.atan(EY/EX) + math.pi
        else:
            if EY > 0.0:
                return math.pi / 2
            elif EY < 0.0:
                return - math.pi / 2
            else:
                return 0.0

