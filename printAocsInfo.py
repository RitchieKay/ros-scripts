#!/usr/bin/python
import sys
import math
import datetime
from autonomousGuidance import *
from rosettaConfiguration import *
from antennaPointingMechanism import *
from solarArrayDriveElectronics import *
from optparse import OptionParser

AU = 149597870.700
C  = 299792.458

def main():

    parser = OptionParser()
    parser.add_option("-a", "--attitude", dest="attitude", help="Specify attitude quarternion (q0, q1, q2, q3)")
    parser.add_option("-t", "--start-time", dest="time_str", help="Specify time YYYY-DDDTHH:MM:SSZ")

    (options, args) = parser.parse_args()

    starttime = datetime.datetime.now()
    attitudeQuaternion = Quaternion.nullQuaternion()

    config = RosettaConfiguration()
    ephemerides = Ephemerides.makeEphemerides()

    starttime = calendar.timegm(datetime.datetime.now().utctimetuple())
    attitudeQuaternion = Quaternion(-0.00298, -0.043, -0.973, 0.229)

    if options.time_str:
        starttime = calendar.timegm(datetime.datetime.strptime(options.time_str, '%Y-%jT%H:%M:%SZ').utctimetuple())
    if options.attitude:
        attitudeQuaternion = Quaternion.createFromString(options.attitude).normalize()

    print starttime

    eS = ephemerides.earthScVector(starttime)
    sS = ephemerides.sunScVector(starttime)

    spacecraftEarthDirection =  -attitudeQuaternion.conjugate().rotate_vector(eS.norm()).norm()
    spacecraftSunDirection   =  -attitudeQuaternion.conjugate().rotate_vector(sS.norm()).norm()

    print 'Earth/Sun Vectors in Spacecraft Frame'
    print '------------------------------------------------------'
    print 'Earth direction = ', spacecraftEarthDirection
    print 'Sun direction   = ', spacecraftSunDirection

    print ''
    print 'Solar Angles with S/C Axes'
    print '------------------------------------------------------'

    print '%(X)02.2f   %(Y)02.2f   %(Z)02.2f' % {'X':180*math.acos(spacecraftSunDirection[0])/math.pi, 'Y':180*math.acos(spacecraftSunDirection[1])/math.pi, 'Z':180*math.acos(spacecraftSunDirection[2])/math.pi}

    print ''
    print 'Solar Array Angles'
    print '------------------------------------------------------'
    
    solarArrayDriveElectronics = sade()
    solarArrayDriveElectronics.compute_position(starttime, attitudeQuaternion)
    print 'YP = %(yp)01.3f, YM = %(ym)01.3f (radians)' % {'yp':solarArrayDriveElectronics.yp(), 'ym':solarArrayDriveElectronics.ym()}
    print 'YP = %(yp)01.3f, YM = %(ym)01.3f (degrees)' % {'yp':180/math.pi*solarArrayDriveElectronics.yp(), 'ym':180/math.pi*solarArrayDriveElectronics.ym()}


    antennaPointingMechanism = apme()
    antennaPointingMechanism.select_set_1()
    antennaPointingMechanism.compute_position(starttime, attitudeQuaternion)

    print ''
    print 'HGA Angles (Shows all Valid Options)'
    print '------------------------------------------------------'
    print 'Set = ', antennaPointingMechanism.current_set()
    print 'Azimuth = %(az)01.3f, Elevation = %(el)01.3f (radians)' % {'az':antennaPointingMechanism.azimuth(), 'el':antennaPointingMechanism.elevation()}
    print 'Azimuth = %(az)01.3f, Elevation = %(el)01.3f (degrees)' % {'az':180*antennaPointingMechanism.azimuth()/math.pi, 'el':180*antennaPointingMechanism.elevation()/math.pi}


    if antennaPointingMechanism.current_set() == 'SET_1':
      antennaPointingMechanism.select_set_2()
      antennaPointingMechanism.compute_position(starttime, attitudeQuaternion)
      if antennaPointingMechanism.current_set() == 'SET_2':
        print 'Set     = ', antennaPointingMechanism.current_set()
        print 'Azimuth = %(az)01.3f, Elevation = %(el)01.3f (radians)' % {'az':antennaPointingMechanism.azimuth(), 'el':antennaPointingMechanism.elevation()}
        print 'Azimuth = %(az)01.3f, Elevation = %(el)01.3f (degrees)' % {'az':180*antennaPointingMechanism.azimuth()/math.pi, 'el':180*antennaPointingMechanism.elevation()/math.pi}

if __name__ == '__main__':
    main()
