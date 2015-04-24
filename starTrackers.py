
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

    def str_a_spacecraft(self):
        return self.STR_A_QUATERNION
    def str_b_spacecraft(self):
        return self.STR_B_QUATERNION
    def spacecraft_str_a(self):
        return self.STR_A_QUATERNION.conjugate()
    def spacecraft_str_b(self):
        return self.STR_B_QUATERNION.conjugate()
