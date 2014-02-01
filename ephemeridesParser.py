###################################################
# convert_por_to_pdor.py
# This script takes a set of POR files as input and
# creates a single PDOR based on them.
#
# Ritchie Kay - 10/01/2013
###################################################
import re
import sys
from ephemerides import *



class EphemeridesParser:

    def __init__(self, por_file):

        self.sequences = []
 
        parser = make_parser()   
        curHandler = EventHandler()
        parser.setContentHandler(curHandler)
        fh = open(por_file)
        parser.parse(fh)

        self.sequences += curHandler.get_sequences()
        fh.close()

    def ephemerides(self):
        return Ephemerides(self.sequences[0])

