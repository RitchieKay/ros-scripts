###################################################
from fdr_parser import *
import re
import sys
import datetime
from quaternion import *
from chebyshev import *

class AttitudeProfileParser:

    def __init__(self, por_file):

        self.sequences = []

        parser = make_parser()
        curHandler = EventHandler()
        parser.setContentHandler(curHandler)
        fh = open(f)
        parser.parse(fh)

        sequences += curHandler.get_sequences()
        fh.close()

    def sequences(self):
        return sequences

class AttitudeProfileError(Exception):
    def __init__(self):
        pass

class AttitudeProfile:

    def __init__(self, q0_cheb, q1_cheb, q2_cheb, q3_cheb):
        self.q0_cheb = q0_cheb
        self.q1_cheb = q1_cheb
        self.q2_cheb = q2_cheb
        self.q3_cheb = q3_cheb

    @staticmethod
    def make_from_sequence(sequence):
        if sequence.sequence_name() != 'AACF105A':
	  raise AttitudeProfileError
        self.sequence = sequence

        p = sequence.get_parameter_map()

        q0_cheb = Chebyshev(p[3].get_value())
        q1_cheb = Chebyshev(p[3].get_value())
        q2_cheb = Chebyshev(p[3].get_value())
        q3_cheb = Chebyshev(p[3].get_value())

        q0_cheb.add_coefficient(0, p[4].get_value())
        q0_cheb.add_coefficient(1, p[5].get_value())
        q0_cheb.add_coefficient(2, p[6].get_value())
        q0_cheb.add_coefficient(3, p[7].get_value())
        q0_cheb.add_coefficient(4, p[8].get_value())
        q0_cheb.add_coefficient(5, p[9].get_value())
        q0_cheb.add_coefficient(6, p[10].get_value())
        q0_cheb.add_coefficient(7, p[11].get_value())

        q1_cheb.add_coefficient(0, p[12].get_value())
        q1_cheb.add_coefficient(1, p[13].get_value())
        q1_cheb.add_coefficient(2, p[14].get_value())
        q1_cheb.add_coefficient(3, p[15].get_value())
        q1_cheb.add_coefficient(4, p[16].get_value())
        q1_cheb.add_coefficient(5, p[17].get_value())
        q1_cheb.add_coefficient(6, p[18].get_value())
        q1_cheb.add_coefficient(7, p[19].get_value())

        q2_cheb.add_coefficient(0, p[20].get_value())
        q2_cheb.add_coefficient(1, p[21].get_value())
        q2_cheb.add_coefficient(2, p[22].get_value())
        q2_cheb.add_coefficient(3, p[23].get_value())
        q2_cheb.add_coefficient(4, p[24].get_value())
        q2_cheb.add_coefficient(5, p[25].get_value())
        q2_cheb.add_coefficient(6, p[26].get_value())
        q2_cheb.add_coefficient(7, p[27].get_value())

        q3_cheb.add_coefficient(0, p[28].get_value())
        q3_cheb.add_coefficient(1, p[29].get_value())
        q3_cheb.add_coefficient(2, p[30].get_value())
        q3_cheb.add_coefficient(3, p[31].get_value())
        q3_cheb.add_coefficient(4, p[32].get_value())
        q3_cheb.add_coefficient(5, p[33].get_value())
        q3_cheb.add_coefficient(6, p[34].get_value())
        q3_cheb.add_coefficient(7, p[35].get_value())

        return AttitudeProfile(q0_cheb, q1_cheb, q2_cheb, q3_cheb)

    @staticmethod
    def make_from_quaternion(q):
        q0_cheb = Chebyshev(0)
        q1_cheb = Chebyshev(0)
        q2_cheb = Chebyshev(0)
        q3_cheb = Chebyshev(0)
        q0_cheb.add_coefficient(0, q[0])
        q1_cheb.add_coefficient(0, q[1])
        q2_cheb.add_coefficient(0, q[2])
        q3_cheb.add_coefficient(0, q[3])
        return AttitudeProfile(q0_cheb, q1_cheb, q2_cheb, q3_cheb)

    def initial_quaternion(self):
        return intermediate_quaternion(-1)

    def final_quaternion(self):
        return intermediate_quaternion(1)

    def intermediate_quaternion(self, t):
      return Quaternion(self.q0_cheb.value(t), self.q1_cheb.value(t), self.q2_cheb.value(t), self.q3_cheb.value(t)).normalize()

    def sequence(self):
        s = Sequence('AACF105A')
        s.set_executionTime('2014-001T00:00:00.000Z')
        s.generate_uniqueID('F')
        s.set_insertOrDeleteFlag('I')
        s.add_parameter(1, SequenceParameter('VAC10501').set_value('2014.001.00.00.00.000'))
        s.add_parameter(2, SequenceParameter('VAC10502').set_value('2014.001.00.00.00.000'))
        s.add_parameter(3, SequenceParameter('VAC10503').set_value(self.q0_cheb.get_degree()))
        s.add_parameter(4, SequenceParameter('VAC10504').set_value(self.q0_cheb.get_coefficient(0)))
        s.add_parameter(5, SequenceParameter('VAC10505').set_value(self.q0_cheb.get_coefficient(1)))
        s.add_parameter(6, SequenceParameter('VAC10506').set_value(self.q0_cheb.get_coefficient(2)))
        s.add_parameter(7, SequenceParameter('VAC10507').set_value(self.q0_cheb.get_coefficient(3)))
        s.add_parameter(8, SequenceParameter('VAC10508').set_value(self.q0_cheb.get_coefficient(4)))
        s.add_parameter(9, SequenceParameter('VAC10509').set_value(self.q0_cheb.get_coefficient(5)))
        s.add_parameter(10, SequenceParameter('VAC10510').set_value(self.q0_cheb.get_coefficient(6)))
        s.add_parameter(11, SequenceParameter('VAC10511').set_value(self.q0_cheb.get_coefficient(7)))
        s.add_parameter(12, SequenceParameter('VAC10512').set_value(self.q1_cheb.get_coefficient(0)))
        s.add_parameter(13, SequenceParameter('VAC10513').set_value(self.q1_cheb.get_coefficient(1)))
        s.add_parameter(14, SequenceParameter('VAC10514').set_value(self.q1_cheb.get_coefficient(2)))
        s.add_parameter(15, SequenceParameter('VAC10515').set_value(self.q1_cheb.get_coefficient(3)))
        s.add_parameter(16, SequenceParameter('VAC10516').set_value(self.q1_cheb.get_coefficient(4)))
        s.add_parameter(17, SequenceParameter('VAC10517').set_value(self.q1_cheb.get_coefficient(5)))
        s.add_parameter(18, SequenceParameter('VAC10518').set_value(self.q1_cheb.get_coefficient(6)))
        s.add_parameter(19, SequenceParameter('VAC10519').set_value(self.q1_cheb.get_coefficient(7)))
        s.add_parameter(20, SequenceParameter('VAC10520').set_value(self.q2_cheb.get_coefficient(0)))
        s.add_parameter(21, SequenceParameter('VAC10521').set_value(self.q2_cheb.get_coefficient(1)))
        s.add_parameter(22, SequenceParameter('VAC10522').set_value(self.q2_cheb.get_coefficient(2)))
        s.add_parameter(23, SequenceParameter('VAC10523').set_value(self.q2_cheb.get_coefficient(3)))
        s.add_parameter(24, SequenceParameter('VAC10524').set_value(self.q2_cheb.get_coefficient(4)))
        s.add_parameter(25, SequenceParameter('VAC10525').set_value(self.q2_cheb.get_coefficient(5)))
        s.add_parameter(26, SequenceParameter('VAC10526').set_value(self.q2_cheb.get_coefficient(6)))
        s.add_parameter(27, SequenceParameter('VAC10527').set_value(self.q2_cheb.get_coefficient(7)))
        s.add_parameter(28, SequenceParameter('VAC10528').set_value(self.q3_cheb.get_coefficient(0)))
        s.add_parameter(29, SequenceParameter('VAC10529').set_value(self.q3_cheb.get_coefficient(1)))
        s.add_parameter(30, SequenceParameter('VAC10530').set_value(self.q3_cheb.get_coefficient(2)))
        s.add_parameter(31, SequenceParameter('VAC10531').set_value(self.q3_cheb.get_coefficient(3)))
        s.add_parameter(32, SequenceParameter('VAC10532').set_value(self.q3_cheb.get_coefficient(4)))
        s.add_parameter(33, SequenceParameter('VAC10533').set_value(self.q3_cheb.get_coefficient(5)))
        s.add_parameter(34, SequenceParameter('VAC10534').set_value(self.q3_cheb.get_coefficient(6)))
        s.add_parameter(35, SequenceParameter('VAC10535').set_value(self.q3_cheb.get_coefficient(7)))
        s.add_parameter(36, SequenceParameter('VAC10536').set_value(1))

        return s
