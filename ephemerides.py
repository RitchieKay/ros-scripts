#!/usr/bin/python
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
import datetime
import calendar
from quarternion import *
from chebyshev import *
from vector import *


class EphemeridesError(Exception):
    def __init__(self):
        pass

class Ephemerides:

    def __init__(self, sequence):
        if sequence.sequence_name() != 'AACF103A':
	  raise EphemeridesError
        self.sequence = sequence

        p = sequence.get_parameter_map()
        self._starttime = calendar.timegm(datetime.datetime.strptime(p[1].get_value()[0:17], '%Y-%jT%H:%M:%S').timetuple())
        self._starttime += int(p[1].get_value()[18:21]) * 1.0 / 1000
        self._endtime = calendar.timegm(datetime.datetime.strptime(p[2].get_value()[0:17], '%Y-%jT%H:%M:%S').timetuple())
        self._endtime += int(p[2].get_value()[18:21]) * 1.0 / 1000


        self.earthScX_cheb = Chebyshev(p[3].get_value())
        self.earthScY_cheb = Chebyshev(p[3].get_value())
        self.earthScZ_cheb = Chebyshev(p[3].get_value())

        self.sunScX_cheb = Chebyshev(p[4].get_value())
        self.sunScY_cheb = Chebyshev(p[4].get_value())
        self.sunScZ_cheb = Chebyshev(p[4].get_value())

        self.earthScX_cheb.add_coefficient(0, p[5].get_value())
        self.earthScX_cheb.add_coefficient(1, p[6].get_value())
        self.earthScX_cheb.add_coefficient(2, p[7].get_value())
        self.earthScX_cheb.add_coefficient(3, p[8].get_value())
        self.earthScX_cheb.add_coefficient(4, p[9].get_value())
        self.earthScX_cheb.add_coefficient(5, p[10].get_value())
        self.earthScX_cheb.add_coefficient(6, p[11].get_value())
        self.earthScX_cheb.add_coefficient(7, p[12].get_value())

        self.earthScY_cheb.add_coefficient(0, p[13].get_value())
        self.earthScY_cheb.add_coefficient(1, p[14].get_value())
        self.earthScY_cheb.add_coefficient(2, p[15].get_value())
        self.earthScY_cheb.add_coefficient(3, p[16].get_value())
        self.earthScY_cheb.add_coefficient(4, p[17].get_value())
        self.earthScY_cheb.add_coefficient(5, p[18].get_value())
        self.earthScY_cheb.add_coefficient(6, p[19].get_value())
        self.earthScY_cheb.add_coefficient(7, p[20].get_value())

        self.earthScZ_cheb.add_coefficient(0, p[21].get_value())
        self.earthScZ_cheb.add_coefficient(1, p[22].get_value())
        self.earthScZ_cheb.add_coefficient(2, p[23].get_value())
        self.earthScZ_cheb.add_coefficient(3, p[24].get_value())
        self.earthScZ_cheb.add_coefficient(4, p[25].get_value())
        self.earthScZ_cheb.add_coefficient(5, p[26].get_value())
        self.earthScZ_cheb.add_coefficient(6, p[27].get_value())
        self.earthScZ_cheb.add_coefficient(7, p[28].get_value())

        self.sunScX_cheb.add_coefficient(0, p[29].get_value())
        self.sunScX_cheb.add_coefficient(1, p[30].get_value())
        self.sunScX_cheb.add_coefficient(2, p[31].get_value())
        self.sunScX_cheb.add_coefficient(3, p[32].get_value())
        self.sunScX_cheb.add_coefficient(4, p[33].get_value())
        self.sunScX_cheb.add_coefficient(5, p[34].get_value())
        self.sunScX_cheb.add_coefficient(6, p[35].get_value())
        self.sunScX_cheb.add_coefficient(7, p[36].get_value())

        self.sunScY_cheb.add_coefficient(0, p[37].get_value())
        self.sunScY_cheb.add_coefficient(1, p[38].get_value())
        self.sunScY_cheb.add_coefficient(2, p[39].get_value())
        self.sunScY_cheb.add_coefficient(3, p[40].get_value())
        self.sunScY_cheb.add_coefficient(4, p[41].get_value())
        self.sunScY_cheb.add_coefficient(5, p[42].get_value())
        self.sunScY_cheb.add_coefficient(6, p[43].get_value())
        self.sunScY_cheb.add_coefficient(7, p[44].get_value())

        self.sunScZ_cheb.add_coefficient(0, p[45].get_value())
        self.sunScZ_cheb.add_coefficient(1, p[46].get_value())
        self.sunScZ_cheb.add_coefficient(2, p[47].get_value())
        self.sunScZ_cheb.add_coefficient(3, p[48].get_value())
        self.sunScZ_cheb.add_coefficient(4, p[49].get_value())
        self.sunScZ_cheb.add_coefficient(5, p[50].get_value())
        self.sunScZ_cheb.add_coefficient(6, p[51].get_value())
        self.sunScZ_cheb.add_coefficient(7, p[52].get_value())

    def starttime(self):
        return self._starttime
    def endtime(self):
        return self._endtime

    def getT(self, t):
        if t < self._starttime or t > self._endtime:
            raise EphemeridesError

        return 2.0*(t - self._starttime)/(self._endtime - self._starttime)  - 1


    def sunScVector(self, t):
        T = self.getT(t)
        return Vector(self.sunScX_cheb.value(T), self.sunScY_cheb.value(T), self.sunScZ_cheb.value(T))

     
    def earthScVector(self, t):
        T = self.getT(t)
        return Vector(self.earthScX_cheb.value(T), self.earthScY_cheb.value(T), self.earthScZ_cheb.value(T))
