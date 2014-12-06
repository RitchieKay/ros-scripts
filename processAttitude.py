#!/usr/bin/python
import sys
import math
import datetime
from slewCommandGenerator import *
from slewAttitudeGenerator import *
from rosettaConfiguration import *
from attitudeProfiles import *
from aocsModeChanger import *
from autonomousGuidance import *
from reactionWheels import *
from optparse import OptionParser


def main():

    parser = OptionParser()
    (options, args) = parser.parse_args()
    
    aps = AttitudeProfiles.makeAttitudeProfiles()
    wheel_speeds('fdr_wheels.txt', aps)

def sade_angles(filename, scg):

    f = open(filename, 'w')
    solar_array = sade()
    for t in range(int(scg.start_time()), int(scg.end_time())):
        solar_array.compute_position(t, scg.attitude_profiles().getQuaternion(t))
        print >> f, t - scg.start_time(), solar_array.yp(), solar_array.ym()
    f.close()

def apme_angles(filename, scg):

    f = open(filename, 'w')
    antenna = apme()
    for t in range(int(scg.start_time()), int(scg.end_time())):
        antenna.compute_position(t, scg.attitude_profiles().quaternion(t))
        print >> f, t - scg.start_time(), 2 - int(antenna.current_set()=="SET_1"), antenna.elevation(), antenna.azimuth()
    f.close()

def wheel_speeds(filename, aps):
    config = RosettaConfiguration()
    f = open(filename, 'w')
    wheels = rwa()
    wheels.set_ang_mom_vector([float(config.getItem('RWA_ANG_MON_1')), float(config.getItem('RWA_ANG_MON_2')), float(config.getItem('RWA_ANG_MON_3')), float(config.getItem('RWA_ANG_MON_4'))])

    for i in range(int(aps.end_time() -aps.start_time())):
        ts = aps.start_time() + float(i)
        tf = aps.start_time() + float(i+1)
    
        qs = aps.quaternion(ts)
        qsd = aps.deltaQuaternion(ts, 0.25)
        qf = aps.quaternion(tf)
        qfd = aps.deltaQuaternion(tf, 0.25)
        
        ang_mom_vector = wheels.compute_wheel_speeds(qs, qsd, qf, qfd, 0.25)
        if i % 64 == 0:
            print >> f, float(i), ang_mom_vector[0], ang_mom_vector[1], ang_mom_vector[2], ang_mom_vector[3]
    f.close()

def quaternions(filename, scg):

    f = open(filename, 'w')
    solar_array = sade()
    for t in range(int(scg.start_time()), int(scg.end_time())):
        q = scg.attitude_profiles().quaternion(t)
        print >> f, t - scg.start_time(), q[0], q[1], q[2], q[3]
    f.close()

def autoAttitude():
    config = RosettaConfiguration()
    q1 = config.getItem('INITIAL_QUARTERNION').strip().split(',')
    starttime = datetime.datetime.strptime(config.getItem('START_TIME'), '%Y-%jT%H:%M:%SZ')
    attitudeI = Quaternion(float(q1[0]), float(q1[1]), float(q1[2]), float(q1[3]))

    # Get the attitude at the start of the FDR
    a = AttitudeProfiles.makeAttitudeProfiles()

    attitudeE = a.first_quaternion()

    # Obtain the autonomous guidance attitude
    aut = AutonomousGuidance(EphemeridesParser(config.getItem('EPHEMERIDES')).ephemerides())
    aut.setPointedAxis(Vector(float(config.getItem('AUTO_POINTED_X_AXIS')), float(config.getItem('AUTO_POINTED_Y_AXIS')), float(config.getItem('AUTO_POINTED_Z_AXIS'))))


    if config.getItem('AUTO_EARTH_POINTING') == 'TRUE':
        aut.setEarthPointing()
    else:
        aut.setSunPointing()
    if config.getItem('AUTO_NORTH_POINTING') == 'TRUE':
        aut.setNorthPointing()
    else:
        aut.setSouthPointing()
    if config.getItem('AUTO_PERP_ECLIPTIC') == 'TRUE':
        aut.setPerpendicularToEcliptic()
    else:
        aut.setPerpendicularToSunSpacecraft()
        attitudeI = aut.quaternion(starttime) 

    return (attitudeI, attitudeE, starttime)

if __name__ == '__main__':
    main()
