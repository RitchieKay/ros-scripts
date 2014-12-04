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
from optparse import OptionParser

def main():

    parser = OptionParser()
    parser.add_option("-i", "--initial-attitude", dest="attitudeI", help="Specify initial attitude quarternion (q0, q1, q2, q3)")
    parser.add_option("-f", "--final-attitude", dest="attitudeE", help="Specify initial attitude quarternion (q0, q1, q2, q3)")
    parser.add_option("-t", "--start-time", dest="time_str", help="Specify time YYYY-DDDTHH:MM:SSZ")
    parser.add_option("-a", "--auto", action="store_true", dest="auto", help="Obtain initial and final attitude from configuration")

    (options, args) = parser.parse_args()
    
    starttime = datetime.datetime.now()
    attitudeI = Quaternion.nullQuaternion()
    attitudeE = Quaternion.nullQuaternion()

    if options.auto:

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
    scg.writeDorFile('DOR__BRIDGE_TO_FDS.ROS')

    print 'Initial Attitude:', attitudeI
    print 'Final   Attitude:', attitudeE
    print 'Final error     :', (attitudeE.conjugate() * scg.attitude(scg.end_time())).normalize()

    for i in range(3):
        print 'SLEW', i, 'times    :', scg.slewTimes(i)

if __name__ == '__main__':
    main()
