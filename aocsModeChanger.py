from fdr_parser import *
import math

class AocsModeChanger:

    def __init__(self):
        pass

    def gsep_gsp_sequence(self, execTime):
        s = Sequence('AACF210A')
        s.set_executionTime( datetime.datetime.fromtimestamp(execTime).strftime('%Y-%jT%H:%M:%S.%f')[0:21] + 'Z')
        s.generate_uniqueID('F')
        s.set_insertOrDeleteFlag('I')
        return s

    def gsp_fpap_sequence(self, execTime):
        s = Sequence('AACF211A')
        s.set_executionTime( datetime.datetime.fromtimestamp(execTime).strftime('%Y-%jT%H:%M:%S.%f')[0:21] + 'Z')
        s.generate_uniqueID('F')
        s.set_insertOrDeleteFlag('I')
        return s
