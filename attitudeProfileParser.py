#!/usr/bin/python
###################################################
# convert_por_to_pdor.py
# This script takes a set of POR files as input and
# creates a single PDOR based on them.
#
# Ritchie Kay - 10/01/2013
###################################################
import re
import sys
from attitudeProfile import *


#
#
#
#

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

