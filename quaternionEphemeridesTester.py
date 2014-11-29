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


def main():

    if len(sys.argv) < 2:
        print 'Usage:', sys.argv[0], '<fdr file>'
        sys.exit(-1)

    ephemerides = EphemeridesParser(sys.argv[1]).ephemerides()

    nowTime = calendar.timegm(datetime.datetime.now().timetuple())


    attitudeI = Quaternion(0.143, 0.266, 0.494, 0.815)

    rx = Rotation(20, Vector(0,1,0))

    attitudeE = attitudeI * rx.quaternion()

    rp = RotationPlanner()
    rp.set_ephemerides(ephemerides)
    rp.generate_rotations(attitudeI, attitudeE, nowTime)
   

    print 'Initial  :', attitudeI
    print 'Rotation 1:', attitudeI * rp[0].quaternion(), rp[0]
    print 'Rotation 2:', attitudeI * rp[0].quaternion() * rp[1].quaternion(), rp[1]
    print 'Rotation 3:', attitudeI * rp[0].quaternion() * rp[1].quaternion() * rp[2].quaternion(), rp[2]
    print 'Final     :', attitudeE

    # 1st slew

    sa = SlewAttitudeGenerator()
    sa.set_initial_attitude(attitudeI)
    sa.set_rotation(rp[0])

    coefficients = [0] * 4
    coefficients[0] = [0] * 8
    coefficients[1] = [0] * 8
    coefficients[2] = [0] * 8
    coefficients[3] = [0] * 8

    s = [0] * 4
    steps = 20000000
    dt = 2.0 / steps
    t = -1.0  + dt
    for j in range (steps-1):
        a = sa.get_intermediate_attitude((t + 1)/2)
        s[0] = a[0]/math.sqrt(1-t*t)*dt
        s[1] = a[1]/math.sqrt(1-t*t)*dt
        s[2] = a[2]/math.sqrt(1-t*t)*dt
        s[3] = a[3]/math.sqrt(1-t*t)*dt
#        s[0] = 1/math.sqrt(1-t*t)*dt
#        s[1] = t/math.sqrt(1-t*t)*dt
#        s[2] = (2*t*t -1)/math.sqrt(1-t*t)*dt
#        s[3] = (4*t*t*t - 3*t) /math.sqrt(1-t*t)*dt
        coefficients[0][0] += s[0]*cheb_0_f(t)/math.pi
        coefficients[0][1] += s[0]*cheb_1_f(t)*2.0/math.pi
        coefficients[0][2] += s[0]*cheb_2_f(t)*2.0/math.pi
        coefficients[0][3] += s[0]*cheb_3_f(t)*2.0/math.pi
        coefficients[0][4] += s[0]*cheb_4_f(t)*2.0/math.pi
        coefficients[0][5] += s[0]*cheb_5_f(t)*2.0/math.pi
        coefficients[0][6] += s[0]*cheb_6_f(t)*2.0/math.pi
        coefficients[0][7] += s[0]*cheb_7_f(t)*2.0/math.pi
        coefficients[1][0] += s[1]*cheb_0_f(t)/math.pi
        coefficients[1][1] += s[1]*cheb_1_f(t)*2.0/math.pi
        coefficients[1][2] += s[1]*cheb_2_f(t)*2.0/math.pi
        coefficients[1][3] += s[1]*cheb_3_f(t)*2.0/math.pi
        coefficients[1][4] += s[1]*cheb_4_f(t)*2.0/math.pi
        coefficients[1][5] += s[1]*cheb_5_f(t)*2.0/math.pi
        coefficients[1][6] += s[1]*cheb_6_f(t)*2.0/math.pi
        coefficients[1][7] += s[1]*cheb_7_f(t)*2.0/math.pi
        coefficients[2][0] += s[2]*cheb_0_f(t)/math.pi
        coefficients[2][1] += s[2]*cheb_1_f(t)*2.0/math.pi
        coefficients[2][2] += s[2]*cheb_2_f(t)*2.0/math.pi
        coefficients[2][3] += s[2]*cheb_3_f(t)*2.0/math.pi
        coefficients[2][4] += s[2]*cheb_4_f(t)*2.0/math.pi
        coefficients[2][5] += s[2]*cheb_5_f(t)*2.0/math.pi
        coefficients[2][6] += s[2]*cheb_6_f(t)*2.0/math.pi
        coefficients[2][7] += s[2]*cheb_7_f(t)*2.0/math.pi
        coefficients[3][0] += s[3]*cheb_0_f(t)/math.pi
        coefficients[3][1] += s[3]*cheb_1_f(t)*2.0/math.pi
        coefficients[3][2] += s[3]*cheb_2_f(t)*2.0/math.pi
        coefficients[3][3] += s[3]*cheb_3_f(t)*2.0/math.pi
        coefficients[3][4] += s[3]*cheb_4_f(t)*2.0/math.pi
        coefficients[3][5] += s[3]*cheb_5_f(t)*2.0/math.pi
        coefficients[3][6] += s[3]*cheb_6_f(t)*2.0/math.pi
        coefficients[3][7] += s[3]*cheb_7_f(t)*2.0/math.pi
        t += dt

    print coefficients[0]
    print coefficients[1]
    print coefficients[2]
    print coefficients[3]

    c = [Chebyshev(7), Chebyshev(7), Chebyshev(7), Chebyshev(7)] 
    for i in range(4):
        for j in range(8):
            c[i].add_coefficient(j, coefficients[i][j])

    print c[0].value(-1), c[0].value(1)
    print c[1].value(-1), c[1].value(1)
    print c[2].value(-1), c[2].value(1)
    print c[3].value(-1), c[3].value(1)

if __name__ == '__main__':
    main()
