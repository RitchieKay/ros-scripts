#!/usr/bin/python
###################################################
###################################################
import re
import sys
import datetime
import calendar
from vector import *


class InertiaError(Exception):
    def __init__(self):
        pass

class Inertia:

    def __init__(self, sequence):
        if sequence.sequence_name() != 'AACF107A':
	  raise InertiaError
        self.sequence = sequence

        p = sequence.get_parameter_map()
        self.element_XX = float(p[1].get_value())
        self.element_XY = float(p[2].get_value())
        self.element_YX = float(p[2].get_value())
        self.element_XZ = float(p[3].get_value())
        self.element_ZX = float(p[3].get_value())
        self.element_YY = float(p[4].get_value())
        self.element_YZ = float(p[5].get_value())
        self.element_ZY = float(p[5].get_value())
        self.element_ZZ = float(p[6].get_value())

    def Iw(self, v):

        pX = self.element_XX * v.X() + self.element_XY * v.Y() + self.element_XZ * v.Z()
        pY = self.element_YX * v.X() + self.element_YY * v.Y() + self.element_YZ * v.Z()
        pZ = self.element_ZX * v.X() + self.element_ZY * v.Y() + self.element_ZZ * v.Z()

        return Vector(pX, pY, pZ)
