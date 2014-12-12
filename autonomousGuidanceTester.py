#!/usr/bin/python
import sys
import math
import datetime
from ephemeridesParser import *
from autonomousGuidance import *
from rosettaConfiguration import *

AU = 149597870.700
C  = 299792.458

def main():

    config = RosettaConfiguration()
#    autoGuid.setPointedAxis(Vector(1,0,0))
    nowTime = calendar.timegm(datetime.datetime.now().utctimetuple())
    nowTime = datetime.datetime.strptime(config.getItem('START_TIME'), '%Y-%jT%H:%M:%SZ')

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

    q = aut.quaternion(nowTime)

    print q
    q.print_rotated_axis()

if __name__ == '__main__':
    main()
