
import math
from quaternion import *


class starTracker:

    def __init__(self):
        self.STR_A_QUATERNION = Quaternion( 5.615766e-01,
                                            5.604697e-01,
                                            4.304900e-01,
                                           -4.303298e-01)
        self.STR_B_QUATERNION = Quaternion( 5.098050e-01,
                                           -6.095483e-01,
                                           4.659036e-01,
                                           3.892090e-01)

    def quaternions(self):
        return (self.STR_A_QUATERNION, self.STR_B_QUATERNION)

    def str_attitude(self, spacecraftAttitude):

        return (spacecraftAttitude * self.STR_A_QUATERNION.conjugate(), spacecraftAttitude * self.STR_B_QUATERNION.conjugate())


    def fieldOfView(self, spacecraftAttitude):
       
        (str_a_att, str_b_att) = self.str_attitude(spacecraftAttitude)

        return (str_a_att.celestialCoordinates(), str_b_att.celestialCoordinates())
