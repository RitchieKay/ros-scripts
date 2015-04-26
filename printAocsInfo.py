#!/usr/bin/python
import sys
import math
import datetime
from autonomousGuidance import *
from rosettaConfiguration import *
from antennaPointingMechanism import *
from solarArrayDriveElectronics import *
from attitudeProfiles import *
from starTrackers import *
from optparse import OptionParser

AU = 149597870.700
C  = 299792.458

def main():

    parser = OptionParser()
    parser.add_option("-a", "--attitude", dest="attitude", help="Specify attitude quarternion (q0, q1, q2, q3)")
    parser.add_option("-t", "--start-time", dest="time_str", help="Specify time YYYY-DDDTHH:MM:SSZ")
    parser.add_option("-f", "--fdr-file", dest="fdr_str", help="Specify path to FDR")
    parser.add_option("-g", "--auto-guid", action="store_true", dest="aut_guid", help="Use autonomous guidance")

    (options, args) = parser.parse_args()

    config = RosettaConfiguration()
    ephemerides = Ephemerides.makeEphemerides()

    starttime = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
    starttime_dt = (datetime.datetime.utcnow() - datetime.timedelta(seconds = ephemerides.earthScVector(starttime).magnitude() / C))
    starttime = calendar.timegm((starttime_dt).utctimetuple())

    if options.fdr_str:
	attitudeProfiles = AttitudeProfiles.makeAttitudeProfiles(options.fdr_str)
    else: 
	attitudeProfiles = AttitudeProfiles.makeAttitudeProfiles()

    if options.time_str:
	starttime_dt = datetime.datetime.strptime(options.time_str, '%Y-%jT%H:%M:%SZ')
	starttime = calendar.timegm(starttime_dt.utctimetuple())
    attitudeQuaternion = attitudeProfiles.quaternion(starttime)
    if options.attitude:
        attitudeQuaternion = Quaternion.createFromString(options.attitude).normalize()
    if options.aut_guid:
        attitudeQuaternion = AutonomousGuidance(ephemerides).quaternion(starttime_dt)

    eS = ephemerides.earthScVector(starttime)
    sS = ephemerides.sunScVector(starttime)
    earthSun = eS - sS

    spacecraftEarthDirection =  -attitudeQuaternion.conjugate().rotate_vector(eS.norm()).norm()
    spacecraftSunDirection   =  -attitudeQuaternion.conjugate().rotate_vector(sS.norm()).norm()

    print '------------------------------------------------------'
    print 'Information valid at:', datetime.datetime.utcfromtimestamp(starttime).strftime('%Y-%jT%H:%M:%SZ')
    print '------------------------------------------------------'
    print 'One Way Light Time  :', str(datetime.timedelta(seconds = ephemerides.earthScVector(starttime).magnitude() / C))
    print '------------------------------------------------------'

    print ''
    print 'Earth/Sun Vectors in Spacecraft Frame'
    print '------------------------------------------------------'
    print 'Earth direction = ', spacecraftEarthDirection
    print 'Sun direction   = ', spacecraftSunDirection

    print ''
    print 'Earth/Sun Distances'
    print '------------------------------------------------------'
    print 'Earth Spacecraft Distance = ', eS.magnitude(), '=', eS.magnitude()/AU, 'AU'
    print 'Sun Spacecraft Distance   = ', sS.magnitude(), '=', sS.magnitude()/AU, 'AU'

    print ''
    print 'Earth/Sun Angles'
    print '------------------------------------------------------'
    print 'Sun-Spacecraft-Earth angle = ', math.degrees(eS.anglebetween(sS)), 'degrees'
    print 'Spacecraft-Earth-Sun angle = ', math.degrees(eS.anglebetween(earthSun)), 'degrees'

    print ''
    print 'Attitude Quaternion'
    print '------------------------------------------------------'
    print attitudeQuaternion

    print ''
    print 'STR-A Attitude Quaternion'
    print '------------------------------------------------------'
    print starTracker().str_attitude(attitudeQuaternion)[0]
    #print starTracker().str_attitude(attitudeQuaternion)[0].rotate_vector(Vector(1,0,0))
    #print starTracker().fieldOfView(attitudeQuaternion)[0]
    

    print ''
    print 'STR-B Attitude Quaternion'
    print '------------------------------------------------------'
    print starTracker().str_attitude(attitudeQuaternion)[1]
    #print starTracker().str_attitude(attitudeQuaternion)[1].rotate_vector(Vector(1,0,0))
    #print starTracker().fieldOfView(attitudeQuaternion)[1]

    print ''
    print 'Solar Angles with S/C Axes'
    print '------------------------------------------------------'

    print '%(X)02.2f   %(Y)02.2f   %(Z)02.2f' % {'X':math.degrees(math.acos(spacecraftSunDirection[0])), 'Y':math.degrees(math.acos(spacecraftSunDirection[1])), 'Z':math.degrees(math.acos(spacecraftSunDirection[2]))}

    print ''
    print 'Earth Angles with S/C Axes'
    print '------------------------------------------------------'

    print '%(X)02.2f   %(Y)02.2f   %(Z)02.2f' % {'X':math.degrees(math.acos(spacecraftEarthDirection[0])), 'Y':math.degrees(math.acos(spacecraftEarthDirection[1])), 'Z':math.degrees(math.acos(spacecraftEarthDirection[2]))}

    print ''
    print 'Solar Array Angles'
    print '------------------------------------------------------'
    
    solarArrayDriveElectronics = sade()
    solarArrayDriveElectronics.compute_position(starttime, attitudeQuaternion)
    print 'YP = %(yp)01.3f, YM = %(ym)01.3f (radians)' % {'yp':solarArrayDriveElectronics.yp(), 'ym':solarArrayDriveElectronics.ym()}
    print 'YP = %(yp)01.3f, YM = %(ym)01.3f (degrees)' % {'yp':math.degrees(solarArrayDriveElectronics.yp()), 'ym':math.degrees(solarArrayDriveElectronics.ym())}


    antennaPointingMechanism = apme()
    antennaPointingMechanism.select_set_1()
    antennaPointingMechanism.compute_position(starttime, attitudeQuaternion)

    print ''
    print 'HGA Angles (Shows all Valid Options)'
    print '------------------------------------------------------'
    print 'Set     = ', antennaPointingMechanism.current_set()
    print 'Azimuth = %(az)01.3f, Elevation = %(el)01.3f (radians)' % {'az':antennaPointingMechanism.azimuth(), 'el':antennaPointingMechanism.elevation()}
    print 'Azimuth = %(az)01.3f, Elevation = %(el)01.3f (degrees)' % {'az':math.degrees(antennaPointingMechanism.azimuth()), 'el':math.degrees(antennaPointingMechanism.elevation())}


    if antennaPointingMechanism.current_set() == 'SET_1':
      antennaPointingMechanism.select_set_2()
      antennaPointingMechanism.compute_position(starttime, attitudeQuaternion)
      if antennaPointingMechanism.current_set() == 'SET_2':
        print ''
        print '------------------------------------------------------'
        print 'Set     = ', antennaPointingMechanism.current_set()
        print 'Azimuth = %(az)01.3f, Elevation = %(el)01.3f (radians)' % {'az':antennaPointingMechanism.azimuth(), 'el':antennaPointingMechanism.elevation()}
        print 'Azimuth = %(az)01.3f, Elevation = %(el)01.3f (degrees)' % {'az':math.degrees(antennaPointingMechanism.azimuth()), 'el':math.degrees(antennaPointingMechanism.elevation())}

if __name__ == '__main__':
    main()
