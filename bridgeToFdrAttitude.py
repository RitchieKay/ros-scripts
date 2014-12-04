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
    parser.add_option("-i", "--initial-attitude", dest="attitudeI", help="Specify initial attitude quarternion (q0, q1, q2, q3)")
    parser.add_option("-f", "--final-attitude", dest="attitudeE", help="Specify initial attitude quarternion (q0, q1, q2, q3)")
    parser.add_option("-t", "--start-time", dest="time_str", help="Specify time YYYY-DDDTHH:MM:SSZ")
    parser.add_option("-A", "--auto", action="store_true", dest="auto", help="Obtain initial and final attitude from configuration")
    parser.add_option("-d", "--dor-file", default="DOR__BRIDGE_TO_FDS.ROS", dest="dorfile", help="Output DOR file")
    parser.add_option("-s", "--sade-file", dest="sadefile", help="Dump SADE angles to file")
    parser.add_option("-a", "--apme-file", dest="apmefile", help="Dump AMPE angles to file")
    parser.add_option("-w", "--wheel-file", dest="wheelfile", help="Dump wheel speeds to file")

    (options, args) = parser.parse_args()
    
    starttime = datetime.datetime.now()
    attitudeI = Quaternion.nullQuaternion()
    attitudeE = Quaternion.nullQuaternion()

    if options.auto:
        (attitudeI, attitudeE, starttime) = autoAttitude()
    elif options.attitudeI and options.attitudeE and options.time_str:
        attitudeI = Quaternion.createFromString(options.attitudeI).normalize()
        attitudeE = Quaternion.createFromString(options.attitudeE).normalize()
        starttime = datetime.datetime.strptime(options.time_str, '%Y-%jT%H:%M:%SZ')
    else:
        parser.print_help()
        sys.exit(-1)

    scg = SlewCommandGenerator()
    scg.generateSlewCommands(starttime, attitudeI, attitudeE)
    scg.addAntennaCommanding()
    scg.addModeChanges()
    scg.writeDorFile(options.dorfile)

    print 'Initial Attitude:', attitudeI
    print 'Final   Attitude:', attitudeE
    print 'Final error     :', (attitudeE.conjugate() * scg.attitude(scg.end_time())).normalize()

    for i in range(3):
        print 'SLEW', i, 'times    :', scg.slewTimes(i)

    if options.sadefile:
        sade_angles(options.sadefile, scg)
    if options.apmefile:
        apme_angles(options.apmefile, scg)
    if options.wheelfile:
        wheel_speeds(options.wheelfile, scg)

def sade_angles(filename, scg):

    f = open(filename, 'w')
    solar_array = sade()
    for t in range(int(scg.start_time()), int(scg.end_time())):
        solar_array.compute_position(t, scg.attitude_profiles().getQuaternion(t))
#        print t - startTime, antenna.current_set(), antenna.elevation(), antenna.azimuth()
        print >> f, t - scg.start_time(), solar_array.yp(), solar_array.ym()
    f.close()

def apme_angles(filename, scg):

    f = open(filename, 'w')
    antenna = apme()
    for t in range(int(scg.start_time()), int(scg.end_time())):
        antenna.compute_position(t, scg.attitude_profiles().getQuaternion(t))
        print >> f, t - scg.start_time(), antenna.current_set(), antenna.elevation(), antenna.azimuth()
    f.close()

def wheel_speeds(filename, scg):
    config = RosettaConfiguration()
    f = open(filename, 'w')
    wheels = rwa()
    wheels.set_ang_mom_vector([float(config.getItem('RWA_ANG_MON_1')), float(config.getItem('RWA_ANG_MON_2')), float(config.getItem('RWA_ANG_MON_3')), float(config.getItem('RWA_ANG_MON_4'))])

    for i in range(int(scg.end_time() -scg.start_time())*4):
        ts = scg.start_time() + float(i)/4
        tf = scg.start_time() + float(i+1)/4
        ti = (ts + tf)/2
    
        qs = scg.attitude_profiles().getQuaternion(ts)
        qi = scg.attitude_profiles().getQuaternion(ti)
        qf = scg.attitude_profiles().getQuaternion(tf)
        
        ang_mom_vector = wheels.compute_wheel_speeds(qs, qi, qf)
        if i % 4 == 0:
            print >> f, float(i)/4, ang_mom_vector[0], ang_mom_vector[1], ang_mom_vector[2], ang_mom_vector[3]
    f.close()

def autoAttitude():
    config = RosettaConfiguration()
    q1 = config.getItem('INITIAL_QUARTERNION').strip().split(',')
    starttime = datetime.datetime.strptime(config.getItem('START_TIME'), '%Y-%jT%H:%M:%SZ')
    attitudeI = Quaternion(float(q1[0]), float(q1[1]), float(q1[2]), float(q1[3]))

    # Get the attitude at the start of the FDR
    a = AttitudeProfiles()
    a.addFromFDR(config.getItem('PROFILES'))

    attitudeE = a.getFirstQuaternion()

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
