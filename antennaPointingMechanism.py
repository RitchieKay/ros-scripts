
import math
from ephemerides import *

APME_VALIDITY_RANGE_MIN = {'X1': -2.827433, 'X2':-4.485496}
APME_VALIDITY_RANGE_MAX = {'X1':0.471239, 'X2': 1.343903}

class apme:

    def __init__(self):
        self.set = 'SET_1' 
        self.position = {'X1':0.0, 'X2':0.0}
        self.ephemerides = Ephemerides.makeEphemerides()

    def select_set_1(self):
        self.set_1 = 'SET_1'

    def select_set_2(self):
        self.set_2 = 'SET_2'

    def elevation(self):
        return self.position['X1']

    def azimuth(self):
        return self.position['X2']

    def current_set(self):
        return self.set

    def compute_position(self, t, attitudeQuarternion):

        earthDirection = self.ephemerides.earthScVector(t).normalize()
        earthDirection.negate()
        spacecraftEarthDirection = attitudeQuarternion.rotate_vector(earthDirection)

        if spacecraftEarthDirection.X() == 0.0:
             elevation = - math.pi / 2
             if spacecraftEarthDirection.Z() < 0:
                 elevation *= -1

        else:
            elevation = -1 * math.atan(spacecraftEarthDirection.Z()/spacecraftEarthDirection.X())


        if spacecraftEarthDirection.X() >= 0.0:
            azimuth = math.asin(spacecraftEarthDirection.Y())
        else:
            azimuth = -1 * math.pi -  math.asin(spacecraftEarthDirection.Y())

        ang_pos_1 = {}
        ang_pos_2 = {}

        ang_pos_1['X1'] = elevation
        ang_pos_1['X2'] = azimuth
        ang_pos_2['X1'] = elevation - math.pi
        ang_pos_2['X2'] = azimuth - math.pi

        angle1_valid = (ang_pos_1['X1'] > APME_VALIDITY_RANGE_MIN['X1']) and (ang_pos_1['X1'] < APME_VALIDITY_RANGE_MAX['X1']) and (ang_pos_1['X2'] > APME_VALIDITY_RANGE_MIN['X2']) and (ang_pos_1['X2'] < APME_VALIDITY_RANGE_MAX['X2'])
        angle2_valid = (ang_pos_2['X1'] > APME_VALIDITY_RANGE_MIN['X1']) and (ang_pos_2['X1'] < APME_VALIDITY_RANGE_MAX['X1']) and (ang_pos_2['X2'] > APME_VALIDITY_RANGE_MIN['X2']) and (ang_pos_2['X2'] < APME_VALIDITY_RANGE_MAX['X2'])

        if self.set == 'SET_1':
            if angle1_valid: 
                self.position = ang_pos_1
            else:
                self.position = ang_pos_2
                self.set = 'SET_2'
        else:
            if angle2_valid: 
                self.position = ang_pos_2
            else:
                self.position = ang_pos_1
                self.set = 'SET_1'

