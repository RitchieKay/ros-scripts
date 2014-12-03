#!/usr/bin/python
import sys
import math
import datetime
from ephemeridesParser import *
from autonomousGuidance import *
from quaternion import *
from rotationPlanner import *
from slewAttitudeGenerator import *
from chebyshev import *
from chebyshevCalculator import *
from rosettaConfiguration import *
from attitudeProfiles import *
from antennaPointingMechanism import * 
from solarArrayDriveElectronics import * 
from dorWriter import *
from aocsModeChanger import *


class SlewCommandGenerator:

    def __init__(self):
        self.attitudeProfiles = AttitudeProfiles()
        self.starttime = 0
        self.endtime = 0
        self.sequences = []
        self.d = DorWriter()

    def end_time(self):
        return self.endtime

    def writeDorFile(self, dor):
       self.d.add_sequences(self.attitudeProfiles.sequences())
       o = open(dor, 'w')
       self.d.write(o)
       o.close()

    def generateSlewCommands(self, starttime, attitudeI, attitudeE):

        
        self.attitudeProfiles = AttitudeProfiles()
        self.starttime = calendar.timegm(starttime.utctimetuple())
        currentTime = self.starttime

        rp = RotationPlanner()
        rp.generate_rotations(attitudeI, attitudeE, self.starttime)

        # Create a static profile for the first 5 minutes
        self.attitudeProfiles.addProfile(currentTime, currentTime + 302, AttitudeProfile.make_from_quaternion(attitudeI))
        currentTime += 300

        attitude = attitudeI
        sa = SlewAttitudeGenerator()
        for slewNo in range(3):

            sa.set_rotation(attitude, rp[slewNo])
            attitude = sa.finalAttitude()
            T = sa.slewTimes()
            print T

            if T[0] > 0:
  
                c = ChebyshevCalculator(sa.get_intermediate_attitude_normalized_t).computeQuaternionCoefficients(1000)
                self.attitudeProfiles.addProfile(currentTime, currentTime + T[0], AttitudeProfile(c[0], c[1], c[2], c[3]))
                currentTime += T[0]

                qs = Quaternion(c[0].value(-1), c[1].value(-1), c[2].value(-1), c[3].value(-1))
                qe = Quaternion(c[0].value(1), c[1].value(1), c[2].value(1), c[3].value(1))

                # Create a static profile for the first 60 seconds
                if slewNo < 2:
                    self.attitudeProfiles.addProfile(currentTime, currentTime + 61, AttitudeProfile.make_from_quaternion(qe))
                    currentTime += 60
                else:
                    self.attitudeProfiles.addProfile(currentTime, currentTime + 86400, AttitudeProfile.make_from_quaternion(qe))

     
        self.endtime = currentTime
 
    def addAntennaCommanding(self):

        antenna = apme() 
        current_set = antenna.current_set()
        current_set_valid = antenna.current_set_valid()
        antenna_flip_required = False
        antenna_off_time = self.endtime + 10

#    solar_array = sade() 
        for t in range(int(self.starttime), int(self.endtime)):
#            print t  - self.starttime, self.attitudeProfiles.getQuaternion(t)
            dQ =  self.attitudeProfiles.getDeltaDeltaQuaternion(t, 1)

#            print t  - self.starttime, dQ.angle(), dQ.vector().normalize()
            antenna.compute_position(t, self.attitudeProfiles.getQuaternion(t))

            if current_set_valid and not antenna.current_set_valid():
                current_set_valid = False
                antenna_flip_required = True 
            elif not current_set_valid:
                current_set_valid = True

            if antenna.current_set() != current_set:
                antenna_flip_required = True 
                current_set = antenna.current_set()

            if antenna_flip_required and t < antenna_off_time:
                antenna_off_time = t

        if antenna_flip_required:

            antenna_on_time = self.endtime
            if antenna_off_time - antenna_on_time < 50 * 60:
                antenna_on_time = antenna_off_time + 50 * 60
            sequences = [antenna.hold_sequence(antenna_off_time - 60 )]
            sequences.append(antenna.command_rotation_sequence(antenna_on_time - 45 * 60, antenna.elevation(), antenna.azimuth()))
            sequences.append(antenna.on_auto_sequence(antenna_on_time))
            sequences.append(antenna.set_flag_sequence(antenna_on_time + 50, antenna.current_set()))
            self.d.add_sequences(sequences)       
#        solar_array.compute_position(t, attitudeProfiles.getQuaternion(t))
#        print t - startTime, antenna.current_set(), antenna.elevation(), antenna.azimuth()
#        print t - startTime, solar_array.yp(), solar_array.ym()

    def addModeChanges(self):
        
        mc = AocsModeChanger()
        sequences = [mc.gsep_gsp_sequence(self.starttime + 5), mc.gsp_fpap_sequence(self.endtime + 5)]
        self.d.add_sequences(sequences)       

    def attitude(self, t):
        return self.attitudeProfiles.getQuaternion(t)

