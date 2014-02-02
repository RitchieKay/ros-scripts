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

    e = EphemeridesParser(sys.argv[1]).ephemerides()

    t = calendar.timegm(datetime.datetime.utcnow().timetuple())

    print 'Earth Spacecraft Vector = ', e.earthScDirection(t)
    print 'Sun Spacecraft Vector   = ', e.sunScDirection(t)

    print 'Earth - Sun - Spacecraft angle =', e.sunScEarthAngle(t)

    print 'Earth Spacecraft Distance = ', e.earthScDistance(t), '=', e.earthScDistanceAU(t), 'AU'
    print 'Sun Spacecraft Distance   = ', e.sunScDistance(t), '=', e.sunScDistanceAU(t), 'AU'

    print 'OWLT =', e.OWLTstr(t)

if __name__ == '__main__':
    main()
