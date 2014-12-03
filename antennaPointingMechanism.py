
import math
from ephemerides import *

APME_VALIDITY_RANGE_MIN = {'X1': -2.827433, 'X2':-4.485496}
APME_VALIDITY_RANGE_MAX = {'X1':0.471239, 'X2': 1.343903}

class apme:

    def __init__(self):
        self.set = RosettaConfiguration().getItem('APME_CURRENT_SET')
        self.position = {'X1':0.0, 'X2':0.0}
        self.ephemerides = Ephemerides.makeEphemerides()
        self.set_valid = True

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

    def current_set_valid(self):
        return self.set_valid

    def compute_position(self, t, attitudeQuarternion):

        eS = self.ephemerides.earthScVector(t).normalize()
        spacecraftEarthDirection =  -attitudeQuarternion.conjugate().rotate_vector(eS.norm()).norm()

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
        ang_pos_2['X2'] = - azimuth - math.pi

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


        if (angle1_valid or angle2_valid) and not self.set_valid:
            self.set_valid = True

        elif self.set_valid and not (angle1_valid or angle2_valid):
            self.set_valid = False 

    def hold_sequence(self, execTime):
        s = Sequence('AACF081B')
        s.set_executionTime( datetime.datetime.fromtimestamp(execTime).strftime('%Y-%jT%H:%M:%S.%f')[0:21] + 'Z')
        s.generate_uniqueID('F')
        s.set_insertOrDeleteFlag('I')
        return s

    def command_rotation_sequence(self, execTime, elevation, azimuth):
        s = Sequence('AACF081A')
        s.set_executionTime( datetime.datetime.fromtimestamp(execTime).strftime('%Y-%jT%H:%M:%S.%f')[0:21] + 'Z')
        s.generate_uniqueID('F')
        s.set_insertOrDeleteFlag('I')
        s.add_parameter(1, SequenceParameter('VAC08101').set_value(elevation))
        s.add_parameter(2, SequenceParameter('VAC08102').set_value(azimuth))
        return s

    def on_auto_sequence(self, execTime):
        s = Sequence('AACF083B')
        s.set_executionTime( datetime.datetime.fromtimestamp(execTime).strftime('%Y-%jT%H:%M:%S.%f')[0:21] + 'Z')
        s.generate_uniqueID('F')
        s.set_insertOrDeleteFlag('I')
        return s

    def set_flag_sequence(self, execTime, set):
        s = Sequence('AACF083C')
        s.set_executionTime( datetime.datetime.fromtimestamp(execTime).strftime('%Y-%jT%H:%M:%S.%f')[0:21] + 'Z')
        s.generate_uniqueID('F')
        s.set_insertOrDeleteFlag('I')
        p = 0
        if set == 'SET_2':
            p = 1
        s.add_parameter(1, SequenceParameter('VAC08301').set_value(1))
        return s
