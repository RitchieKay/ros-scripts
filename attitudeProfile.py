###################################################
# convert_por_to_pdor.py
# This script takes a set of POR files as input and
# creates a single PDOR based on them.
#
# Ritchie Kay - 10/01/2013
###################################################
from fdr_parser import *
import re
import sys
from quaternion import *
from chebyshev import *

class AttitudeProfileError(Exception):
    def __init__(self):
        pass

class AttitudeProfile:

    def __init__(self, sequence):
        if sequence.sequence_name() != 'AACF105A':
	  raise AttitudeProfileError
        self.sequence = sequence

        p = sequence.get_parameter_map()

        self.q0_cheb = Chebyshev(p[3].get_value())
        self.q1_cheb = Chebyshev(p[3].get_value())
        self.q2_cheb = Chebyshev(p[3].get_value())
        self.q3_cheb = Chebyshev(p[3].get_value())

        self.q0_cheb.add_coefficient(0, p[4].get_value())
        self.q0_cheb.add_coefficient(1, p[5].get_value())
        self.q0_cheb.add_coefficient(2, p[6].get_value())
        self.q0_cheb.add_coefficient(3, p[7].get_value())
        self.q0_cheb.add_coefficient(4, p[8].get_value())
        self.q0_cheb.add_coefficient(5, p[9].get_value())
        self.q0_cheb.add_coefficient(6, p[10].get_value())
        self.q0_cheb.add_coefficient(7, p[11].get_value())

        self.q1_cheb.add_coefficient(0, p[12].get_value())
        self.q1_cheb.add_coefficient(1, p[13].get_value())
        self.q1_cheb.add_coefficient(2, p[14].get_value())
        self.q1_cheb.add_coefficient(3, p[15].get_value())
        self.q1_cheb.add_coefficient(4, p[16].get_value())
        self.q1_cheb.add_coefficient(5, p[17].get_value())
        self.q1_cheb.add_coefficient(6, p[18].get_value())
        self.q1_cheb.add_coefficient(7, p[19].get_value())

        self.q2_cheb.add_coefficient(0, p[20].get_value())
        self.q2_cheb.add_coefficient(1, p[21].get_value())
        self.q2_cheb.add_coefficient(2, p[22].get_value())
        self.q2_cheb.add_coefficient(3, p[23].get_value())
        self.q2_cheb.add_coefficient(4, p[24].get_value())
        self.q2_cheb.add_coefficient(5, p[25].get_value())
        self.q2_cheb.add_coefficient(6, p[26].get_value())
        self.q2_cheb.add_coefficient(7, p[27].get_value())

        self.q3_cheb.add_coefficient(0, p[28].get_value())
        self.q3_cheb.add_coefficient(1, p[29].get_value())
        self.q3_cheb.add_coefficient(2, p[30].get_value())
        self.q3_cheb.add_coefficient(3, p[31].get_value())
        self.q3_cheb.add_coefficient(4, p[32].get_value())
        self.q3_cheb.add_coefficient(5, p[33].get_value())
        self.q3_cheb.add_coefficient(6, p[34].get_value())
        self.q3_cheb.add_coefficient(7, p[35].get_value())

    def initial_quaternion(self):
      return Quaternion(self.q0_cheb.value(-1), self.q1_cheb.value(-1), self.q2_cheb.value(-1), self.q3_cheb.value(-1)).normalize()

    def final_quaternion(self):
      return Quaternion(self.q0_cheb.value(1), self.q1_cheb.value(1), self.q2_cheb.value(1), self.q3_cheb.value(1)).normalize()

