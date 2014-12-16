#!/usr/bin/python
import sys
import math
import datetime
import re
from autonomousGuidance import *
from rosettaConfiguration import *
from optparse import OptionParser

AU = 149597870.700
C  = 299792.458

def main():

    parser = OptionParser()
    parser.add_option("-f", "--pointing-flags", dest="pointing_flags", help="Specify Pointing Flags i.e. EES/ESN")
    parser.add_option("-p", "--pointed-axis", dest="pointed_axis", help="Specify Pointed Axis (v0, v1, v2)")
    parser.add_option("-t", "--time", dest="time", help="Specify time YYYY-DDDTHH:MM:SSZ")

    (options, args) = parser.parse_args()

    config = RosettaConfiguration()
    nowTime = datetime.datetime.utcnow()

    if options.time:
        nowTime = datetime.datetime.strptime(options.time, '%Y-%jT%H:%M:%SZ')

    aut = AutonomousGuidance(Ephemerides.makeEphemerides())

    if options.pointed_axis:
        aut.setPointedAxis(Vector.createFromString(options.pointed_axis))
    else:
        aut.setPointedAxis(Vector(float(config.getItem('AUTO_POINTED_X_AXIS')), float(config.getItem('AUTO_POINTED_Y_AXIS')), float(config.getItem('AUTO_POINTED_Z_AXIS'))))

    valid = False
    if options.pointing_flags:
        valid = True
        if options.pointing_flags[0].upper() == 'E':
            aut.setEarthPointing()
        elif options.pointing_flags[0].upper() == 'S':
            aut.setSunPointing()
        else:
           valid = False
        if options.pointing_flags[1].upper() == 'E':
            aut.setPerpendicularToEcliptic()
        elif options.pointing_flags[1].upper() == 'S':
            aut.setPerpendicularToSunSpacecraft()
        else:
           valid = False
        if options.pointing_flags[2].upper() == 'N':
            aut.setNorthPointing()
        if options.pointing_flags[2].upper() == 'S':
            aut.setSouthPointing()
        else:
           valid = False
           print 'Specified pointing options not valid. Using defaults specified in configuration file'

    if not valid:

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

    q = aut.quaternion(nowTime)

    print 'Autonomous Attitude Quaternion:', q

if __name__ == '__main__':
    main()
