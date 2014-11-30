
import math

APME_VALIDITY_RANGE_MIN = [-2.827433, -4.485496]
APME_VALIDITY_RANGE_MAX = [0.471239, 1.343903]

class apme:

    def __init__(self):
        self.set = 1

    def commanded_position(self, earthDirection, attitudeQuarternion):

        elevation = 0
        azimuth = 0

        earthDirection = earthDirection.normalize()
        earthDirection.negate()
        spacecraftEarthDirection = attitudeQuarternion.rotate_vector(earthDirection)

        if spacecraftEarthDirection.X() == 0.0:
             elevation = - math.pi / 2
             if spacecraftEarthDirection.Z() < 0:
                 elevation *= -1

        else:
            elevation = -1 * math.atan(spacecraftEarthDirection.Z()/spacecraftEarthDirection.X())


        if spacecraftEarthDirection.X() >= 0.0:
            azimuth = math.asin(spacecraftEarthDirection.Y())
        else:
            azimuth = -1 * math.pi -  math.asin(spacecraftEarthDirection.Y())

        cur_cmd_ang_pos_1 = []
        cur_cmd_ang_pos_2 = []

        cur_cmd_ang_pos_1[0] = elevation
        cur_cmd_ang_pos_1[1] = azimuth
        cur_cmd_ang_pos_2[0] = elevation - math.pi
        cur_cmd_ang_pos_2[1] = azimuth - math.pi

        angle1_valid = cur_cmd_ang_pos_1


        return elevation * 180 / math.pi, azimuth * 180 / math.pi
