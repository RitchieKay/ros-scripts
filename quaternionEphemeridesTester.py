#!/usr/bin/python
import sys
import math
import datetime
from ephemeridesParser import *
from autonomousGuidance import *
from quaternion import *
from rotationPlanner import *
from slewAttitudeGenerator import *
from chebyshev import *
from chebyshevCalculator import *
from rosettaConfiguration import *

def main():

    config = RosettaConfiguration()
    ephemerides = EphemeridesParser(config.getItem('EPHEMERIDES')).ephemerides()

    nowTime = calendar.timegm(datetime.datetime.now().timetuple())


    attitudeI = Quaternion(0.143, 0.266, 0.494, 0.815)

    rx = Rotation(20 * math.pi/180, Vector(0,1,0))

    attitudeE = attitudeI * rx.quaternion()

    rp = RotationPlanner()
    rp.set_ephemerides(ephemerides)
    rp.generate_rotations(attitudeI, attitudeE, nowTime)
   

    print 'Initial  :', attitudeI
#    print 'Rotation 1:', attitudeI * rp[0].quaternion(), rp[0]
#    print 'Rotation 2:', attitudeI * rp[0].quaternion() * rp[1].quaternion(), rp[1]
#    print 'Rotation 3:', attitudeI * rp[0].quaternion() * rp[1].quaternion() * rp[2].quaternion(), rp[2]
    print 'Final     :', attitudeE

    # 1st slew

    sa = SlewAttitudeGenerator()
    sa.set_rotation(attitudeI, rp[0])
    T = sa.slewTimes()
    print 'Slew time = ', T
  
    c = ChebyshevCalculator(sa.get_intermediate_attitude_normalized_t).computeQuaternionCoefficients(1000)

    print c[0].value(-1), c[1].value(-1), c[2].value(-1), c[3].value(-1)
    print c[0].value(1), c[1].value(1), c[2].value(1), c[3].value(1)

    q0 = Quaternion(c[0].value(-1), c[1].value(-1), c[2].value(-1), c[3].value(-1))
    q1 = Quaternion(c[0].value(1), c[1].value(1), c[2].value(1), c[3].value(1))

    errorq0 = (q0.conjugate() * attitudeI).normalize()
    errorq3 = (q1.conjugate() * attitudeE).normalize()

    print 'Initial  :', q0
    print 'Final    :', q1
    print 'Initial error =', errorq0, errorq0.angle()
    print 'Final error   =', errorq3, errorq3.angle()


if __name__ == '__main__':
    main()
