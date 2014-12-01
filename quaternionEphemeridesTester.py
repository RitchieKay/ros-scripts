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

def main():

    ephemerides = Ephemerides.makeEphemerides()
    attitudeProfiles = AttitudeProfiles()

    startTime = calendar.timegm(datetime.datetime.now().timetuple())
    currentTime = startTime

    attitudeI = Quaternion(0.151, -0.429, -0.864, -0.216)

    rx = Rotation(20 * math.pi/180, Vector(0,1,0))
    ry = Rotation(20 * math.pi/180, Vector(1,0,0))

    attitudeE = attitudeI * rx.quaternion() * ry.quaternion()

    rp = RotationPlanner()
    rp.generate_rotations(attitudeI, attitudeE, startTime)

    print 'Rotation 1 =', rp[0]
    print 'Rotation 2 =', rp[1]
    print 'Rotation 3 =', rp[2]
    print attitudeI * rp[0].quaternion() * rp[1].quaternion() * rp[2].quaternion()


    # Create a static profile for the first 10 seconds
    attitudeProfiles.addProfile(currentTime, currentTime + 10, AttitudeProfile.make_from_quaternion(attitudeI))
    currentTime += 10

    # 1st slew

    attitude = attitudeI
    print attitudeI
    sa = SlewAttitudeGenerator()
    for slewNo in range(3):

        sa.set_rotation(attitude, rp[slewNo])
        attitude = sa.finalAttitude()
        print attitude
        T = sa.slewTimes()
  
        c = ChebyshevCalculator(sa.get_intermediate_attitude_normalized_t).computeQuaternionCoefficients(1000)

        attitudeProfiles.addProfile(currentTime, currentTime + T[0], AttitudeProfile(c[0], c[1], c[2], c[3]))
        currentTime += T[0]

        qi = Quaternion(c[0].value(-1), c[1].value(-1), c[2].value(-1), c[3].value(-1))
        qe = Quaternion(c[0].value(1), c[1].value(1), c[2].value(1), c[3].value(1))

        # Create a static profile for the first 10 seconds
        attitudeProfiles.addProfile(currentTime, currentTime + 10, AttitudeProfile.make_from_quaternion(qe))
        currentTime += 10
      
    antenna = apme() 
    solar_array = sade() 
    print '--------------------------------'
    for t in range(int(startTime), int(currentTime)):
        antenna.compute_position(t, attitudeProfiles.getQuaternion(t))
        solar_array.compute_position(t, attitudeProfiles.getQuaternion(t))
#        print t - startTime, antenna.current_set(), antenna.elevation(), antenna.azimuth()
        print t - startTime, solar_array.yp(), solar_array.ym()

    print '--------------------------------'

if __name__ == '__main__':
    main()
