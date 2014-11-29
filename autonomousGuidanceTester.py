#!/usr/bin/python
import sys
import math
import datetime
from ephemeridesParser import *
from autonomousGuidance import *

AU = 149597870.700
C  = 299792.458

def main():

    if len(sys.argv) < 2:
        print 'Usage:', sys.argv[0], '<fdr file>'
        sys.exit(-1)

    autoGuid = AutonomousGuidance(EphemeridesParser(sys.argv[1]).ephemerides())
    autoGuid.setSunPointing()
    autoGuid.setPerpendicularToSunSpacecraft()
    autoGuid.setNorthPointing()
    autoGuid.setPointedAxis(Vector(math.cos(0.0),0,math.sin(0.0)))
    nowTime = calendar.timegm(datetime.datetime.now().timetuple())

    q = autoGuid.quaternion(nowTime)

    print q
    q.print_rotated_axis()

if __name__ == '__main__':
    main()
