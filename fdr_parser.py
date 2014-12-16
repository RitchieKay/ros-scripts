#!/usr/bin/python
###################################################
# convert_por_to_pdor.py
# This script takes a set of POR files as input and
# creates a single PDOR based on them.
#
# Ritchie Kay - 10/01/2013
###################################################
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import datetime
import re
import random
import sys

class SequenceParameter:

    def __init__(self, name):
        self.name = name
        self.value = 0
        self.representation = 'Raw'
        self.radix = 'Decimal'

    def set_radix(self, radix):
        self.radix = radix
        return self

    def get_radix(self):
        return self.radix

    def set_representation(self, representation):
        self.representation = representation
        return self

    def get_representation(self):
        return self.representation

    def set_value(self, value):
        self.value = value
        return self

    def get_value(self):
        return self.value

    def parameter_name(self):
        return self.name

class Sequence:

    def __init__(self, name):
        self.name = name
        self.parameters = {}

    def __lt__(self, other):
        return self.executionTime < other.executionTime

    def generate_uniqueID(self, char):
        self.uniqueID = char[0] + str(random.random() * 100000000000)[0:9]

    def set_uniqueID(self, uniqueID):
        self.uniqueID = uniqueID

    def get_uniqueID(self):
        return self.uniqueID

    def set_insertOrDeleteFlag(self, insertOrDeleteFlag):
        self.insertOrDeleteFlag = insertOrDeleteFlag

    def get_insertOrDeleteFlag(self):
        return self.insertOrDeleteFlag

    def set_executionTime(self, executionTime):
        if len(executionTime) == 22:
            self.executionTime = datetime.datetime.strptime(executionTime, "%Y-%jT%H:%M:%S.%fZ")
        elif len(executionTime) == 18:
            self.executionTime = datetime.datetime.strptime(executionTime, "%Y-%jT%H:%M:%SZ")
        else:
            print 'Error:', executionTime, 'has incorrect format'

    def get_executionTime(self):
        return self.executionTime

    def sequence_name(self):
        return self.name

    def add_parameter(self, position, parameter):
        self.parameters[position] = parameter
    def update_parameter_value(self, position, value):
        self.parameters[position].set_value(value)
    def get_parameter_value(self, position):
        return self.parameters[position].get_value()

    def get_parameter_map(self):
        return self.parameters

class EventHandler(ContentHandler):

   def __init__ (self):
       self.in_sequence = False
       self.in_uniqueID = False
       self.in_insertOrDeleteFlag = False
       self.in_executionTime = False
       self.in_actionTime = False
       self.in_parameterList = False
       self.in_parameter = False
       self.current_parameter_position = 0
       self.in_value = False

       self.sequences = []


   def get_sequences(self):
      return self.sequences

   def startElement(self, name, attrs):
       xtraAttrs = attrs.getNames()

       if name == 'sequence':
           self.in_sequence = True
           self.current_sequence = Sequence(attrs.get('name'))

       if self.in_sequence:
           if name == 'uniqueID':
               self.in_uniqueID = True

           elif name == 'insertOrDeleteFlag':
               self.in_insertOrDeleteFlag = True

           elif name == 'executionTime':
               self.in_executionTime = True

           elif name == 'actionTime' and self.in_executionTime:
               self.in_actionTime = True

           elif name == 'parameterList':
               self.in_parameterList = True

           elif name == 'parameter' and self.in_parameterList:
               self.in_parameter = True
               self.current_parameter = SequenceParameter(attrs.get('name'))
               self.current_parameter_position = int(attrs.get('position'))

           elif name == 'value' and self.in_parameter:
               self.current_parameter.set_radix(attrs.get('radix'))
               self.current_parameter.set_representation(attrs.get('representation'))
               self.in_value = True

   def characters(self, data):
      if self.in_value:
          self.current_parameter.set_value(data.strip())
      elif self.in_uniqueID:
          self.current_sequence.set_uniqueID(data.strip())
      elif self.in_insertOrDeleteFlag:
          self.current_sequence.set_insertOrDeleteFlag(data)
      elif self.in_actionTime:
          self.current_sequence.set_executionTime(data);


   def endElement(self, name):
       if name == 'sequence':
           self.in_sequence = False
           self.sequences.append(self.current_sequence)
       if self.in_sequence:
           if name == 'executionTime':
               self.in_executionTime = False
           if name == 'parameterList':
               self.in_parameterList = False
               self.in_parameter = False
           if self.in_parameterList and name == 'parameter':
               self.in_parameter = False
               self.current_sequence.add_parameter(self.current_parameter_position, self.current_parameter)
           if self.in_value and name == 'value':
               self.in_value = False
           if self.in_insertOrDeleteFlag and name == 'insertOrDeleteFlag':
               self.in_insertOrDeleteFlag = False
           if self.in_uniqueID and name == 'uniqueID':
               self.in_uniqueID = False
           if self.in_actionTime and name == 'actionTime':
               self.in_actionTime = False

#
#
