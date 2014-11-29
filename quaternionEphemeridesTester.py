#!/usr/bin/python
import sys
import math
import datetime
from ephemeridesParser import *
from autonomousGuidance import *
from quaternion import *

TOL = 0.995

def main():

    if len(sys.argv) < 2:
        print 'Usage:', sys.argv[0], '<fdr file>'
        sys.exit(-1)

    ephemerides = EphemeridesParser(sys.argv[1]).ephemerides()

    nowTime = calendar.timegm(datetime.datetime.now().timetuple())

    eV = ephemerides.earthScVector(nowTime)
    sV = ephemerides.sunScVector(nowTime)


    attitudeI = Quaternion(0.143, 0.266, 0.494, 0.815)

    rx = Rotation(20, Vector(0,1,0))
    ry = Rotation(20, Vector(1,0,0))
    rz = Rotation(20, Vector(0,0,1))

    attitudeE = attitudeI * rz.quaternion() * ry.quaternion() * rx.quaternion()

    spacecraftSunVectorI =  -attitudeI.conjugate().rotate_vector(sV.norm()).norm()
    spacecraftSunVectorE =  -attitudeE.conjugate().rotate_vector(sV.norm()).norm()


    # rotation 1
    numerator = spacecraftSunVectorI.X()*spacecraftSunVectorE.X() + spacecraftSunVectorI.Z()*spacecraftSunVectorE.Z()
    denominator = math.sqrt(spacecraftSunVectorI.X()*spacecraftSunVectorI.X() + spacecraftSunVectorI.Z()*spacecraftSunVectorI.Z()) * \
                  math.sqrt(spacecraftSunVectorE.X()*spacecraftSunVectorE.X() + spacecraftSunVectorE.Z()*spacecraftSunVectorE.Z())

    cos_alpha = numerator / denominator
    angle1 = 0
    vector1 = Vector(0,0,0)
    if cos_alpha < -TOL:
        angle1 = math.pi
        vector1 = Vector(0,1,0)
    elif cos_alpha < TOL:
      angle1 = math.acos(cos_alpha)
      sign = spacecraftSunVectorI.Z() * spacecraftSunVectorE.X() - spacecraftSunVectorI.X() * spacecraftSunVectorE.Z()
      Y = 1
      if sign > 0:
          Y = -1
      vector1 = Vector(0, Y, 0)   
        
    r1 = Rotation(angle1 * 180.0 / math.pi, vector1.vector())
    q1 = r1.quaternion()

    # rotation 2
    spacecraftSunVectorXZ = q1.conjugate().rotate_vector(spacecraftSunVectorI)
   
    cos_alpha = spacecraftSunVectorXZ.scalarproduct(spacecraftSunVectorE)
 
    angle2 = 0
    vector2 = Vector(0,0,0)
    if cos_alpha < -TOL:
        angle2 = math.pi
        vector2 = Vector(1,0,0)
    elif cos_alpha < TOL:
        angle2 = math.acos(cos_alpha)
        vector2 = spacecraftSunVectorE.vectorproduct(spacecraftSunVectorXZ).norm()

    r2 = Rotation(angle2 * 180.0 / math.pi, vector2.vector())
    q2 = r2.quaternion()

    # rotation 3
    deltaQ = q2.conjugate() * q1.conjugate() * attitudeI.conjugate() * attitudeE

    angle3 = 0
    vector3 = Vector(0,0,0)

    if math.fabs(deltaQ.scalar()) < 0.995:
        angle3 = 2.0 * math.acos(deltaQ.scalar())
        vector3 = deltaQ.vector().norm()
        if angle3 > math.pi:
            angle3 = 2 * math.pi - angle3
            vector3 = -vector3

    r3 = Rotation(angle3 * 180.0 / math.pi, vector3.vector())
    q3 = r3.quaternion()

    print 'Initial  :', attitudeI
    print 'Rotation 1:', attitudeI * q1, r1
    print 'Rotation 2:', attitudeI * q1 * q2, r2
    print 'Rotation 3:', attitudeI * q1 * q2 * q3, r3
    print 'Final     :', attitudeE

if __name__ == '__main__':
    main()
