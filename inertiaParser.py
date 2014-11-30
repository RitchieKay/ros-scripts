###################################################
import re
import sys
from fdr_parser import *
from inertia import *



class InertiaParser:

    def __init__(self, por_file):

        self.sequences = []
 
        parser = make_parser()   
        curHandler = EventHandler()
        parser.setContentHandler(curHandler)
        fh = open(por_file)
        parser.parse(fh)

        self.sequences += curHandler.get_sequences()
        fh.close()

    def inertia(self):
        return Inertia(self.sequences[0])

