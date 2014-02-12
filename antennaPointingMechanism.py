
import math

class apme:

    def __init__(self):
        pass

    def compute_angles(self, earthDirection, attitudeQuarternion):

        elevation = 0
        azimuth = 0

        earthDirection = earthDirection.normalize()
        print earthDirection.Y()
        earthDirection.negate()
        print earthDirection.Y()
        spacecraftEarthDirection = attitudeQuarternion.rotate_vector(earthDirection)
        print earthDirection.Y()

        if spacecraftEarthDirection.X() == 0.0:
             elevation = - math.pi / 2
             if spacecraftEarthDirection.Z() < 0:
                 elevation *= -1

        else:
            elevation = -1 * math.atan(spacecraftEarthDirection.Z()/spacecraftEarthDirection.X())


        if spacecraftEarthDirection.X() >= 0.0:
            print spacecraftEarthDirection.Y()
            azimuth = math.asin(spacecraftEarthDirection.Y())
        else:
            azimuth = - .0 * math.pi -  math.asin(spacecraftEarthDirection.Y())


        return elevation * 180 / math.pi, azimuth * 180 / math.pi
