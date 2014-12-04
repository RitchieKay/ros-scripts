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
    autoGuid = AutonomousGuidance(EphemeridesParser(config.getItem('EPHEMERIDES')).ephemerides())
    autoGuid.setEarthPointing()
    autoGuid.setPerpendicularToEcliptic()
    autoGuid.setNorthPointing()
    autoGuid.setPointedAxis(Vector(0.81899989,0,0.57399988))
#    autoGuid.setPointedAxis(Vector(1,0,0))
    nowTime = calendar.timegm(datetime.datetime.now().utctimetuple())
    config = RosettaConfiguration()
    nowTime = calendar.timegm(datetime.datetime.strptime(config.getItem('START_TIME'), '%Y-%jT%H:%M:%SZ').utctimetuple())

    q = autoGuid.quaternion(nowTime)

    print q
    q.print_rotated_axis()

if __name__ == '__main__':
    main()
