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

    ephemerides = EphemeridesParser(sys.argv[1]).ephemerides()

    nowTime = calendar.timegm(datetime.datetime.now().utctimetuple())

    eV = ephemerides.earthScVector(nowTime)
    sV = ephemerides.sunScVector(nowTime)

    print 'Earth Spacecraft Vector = ', eV, eV.norm()
    print 'Sun Spacecraft Vector   = ', sV, sV.norm()

    print 'Earth - Sun - Spacecraft angle =', math.degrees(eV.anglebetween(sV))

    print 'Earth Spacecraft Distance = ', eV.magnitude(), '=', eV.magnitude()/AU, 'AU'
    print 'Sun Spacecraft Distance   = ', sV.magnitude(), '=', sV.magnitude()/AU, 'AU'

    print 'OWLT =', str(datetime.timedelta(seconds = eV.magnitude() / C))

if __name__ == '__main__':
    main()
