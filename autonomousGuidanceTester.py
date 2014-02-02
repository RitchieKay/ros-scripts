#!/usr/bin/python
import sys
import math
import datetime
import time
from ephemeridesParser import *
from autonomousGuidance import *

AU = 149597870.700
C  = 299792.458

def main():

    if len(sys.argv) < 2:
        print 'Usage:', sys.argv[0], '<fdr file>'
        sys.exit(-1)

    eph = EphemeridesParser(sys.argv[1]).ephemerides()
    autoGuid = AutonomousGuidance(eph)
    autoGuid.setEarthPointing()
    autoGuid.setPerpendicularToEcliptic()
    autoGuid.setNorthPointing()
    autoGuid.setPointedAxis(Vector(0.819,0,0.574))
    t = calendar.timegm(datetime.datetime.utcnow().timetuple())
    t -= eph.OWLT(t)

    print time.gmtime(t)

    q = autoGuid.quarternion(t)

    print q
    q.print_rotated_axis()

if __name__ == '__main__':
    main()
