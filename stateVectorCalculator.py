#!/usr/bin/python
import sys
import math
import datetime
from vector import *
from autonomousGuidance import *
from rosettaConfiguration import *
from optparse import OptionParser

AU = 149597870.700
C  = 299792.458
inc = 23.4 * math.pi / 180



def main():

    parser = OptionParser()
    config = RosettaConfiguration()
    ephemerides = Ephemerides.makeEphemerides()
    parser.add_option("-t", "--time", dest="time", help="Specify time YYYY-DDDTHH:MM:SSZ")

    (options, args) = parser.parse_args()

    nowTime = calendar.timegm(datetime.datetime.now().utctimetuple())

    if options.time:
        nowTime = calendar.timegm(datetime.datetime.strptime(options.time, '%Y-%jT%H:%M:%SZ').utctimetuple())

    sV = ephemerides.sunScVector(nowTime)
    esV =  Vector.equatorialToEcliptic(sV)
    svV = ephemerides.sunScVector(nowTime + 0.5) -  ephemerides.sunScVector(nowTime - 0.5)
    esvV =  Vector.equatorialToEcliptic(svV)

    print ''
    print 'Earth Equatorial Reference Frame - required by EQM'
    print '-------------------------------------------------------------------------------------------------'
  
    sys.stdout.write('(' + str(sV[0]) + ', ' +  str(sV[1]) + ', ' + str(sV[2]) + ', ' + str(svV[0]) + ', ' + str(svV[1]) + ', ' + str(svV[2]) + ')\n')

    print ''
    print ''
    print 'Ecliptic Reference Frame - required by SIM'
    print '-------------------------------------------------------------------------------------------------'
  
    sys.stdout.write('SET_ORBIT(0, 0, ' + str(esV[0]) + ', ' +  str(esV[1]) + ', ' + str(esV[2]) + ', ' + str(esvV[0]) + ', ' + str(esvV[1]) + ', ' + str(esvV[2]) + ', 0, 10)\n')



if __name__ == '__main__':
    main()
