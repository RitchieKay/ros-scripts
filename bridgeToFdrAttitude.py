#!/usr/bin/python
import sys
import math
import datetime
from slewCommandGenerator import *
from slewAttitudeGenerator import *
from rosettaConfiguration import *
from attitudeProfiles import *
from aocsModeChanger import *


def main():

    config = RosettaConfiguration()
    q1 = config.getItem('INITIAL_QUARTERNION').strip().split(',') 
    starttime = datetime.datetime.strptime(config.getItem('START_TIME'), '%Y-%jT%H:%M:%SZ')
    attitudeI = Quaternion(float(q1[0]), float(q1[1]), float(q1[2]), float(q1[3]))

    a = AttitudeProfiles()
    a.addFromFDR(config.getItem('PROFILES'))

    attitudeE = a.getFirstQuaternion()

    scg = SlewCommandGenerator()
    scg.generateSlewCommands(starttime, attitudeI, attitudeE)
    scg.addAntennaCommanding()
    scg.addModeChanges()
    scg.writeDorFile('DOR__TEST.ROS')

    print 'Final error =', (attitudeE.conjugate() * scg.attitude(scg.end_time())).normalize()

if __name__ == '__main__':
    main()
