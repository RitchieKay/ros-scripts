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
    ephemerides = Ephemerides.makeEphemerides()

    nowTime = calendar.timegm(datetime.datetime.now().utctimetuple())
    nowTime = calendar.timegm(datetime.datetime.strptime(config.getItem('START_TIME'), '%Y-%jT%H:%M:%SZ').utctimetuple())

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
