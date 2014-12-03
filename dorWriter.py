import datetime

class DorWriter:

    def __init__(self):
        self.sequences = []

    def add_sequences(self, sequences):
        self.sequences += sequences
        self.latest_sequence_time = self.sequences[0].get_executionTime()
        self.earliest_sequence_time = self.sequences[0].get_executionTime()
        for sequence in self.sequences:
            if sequence.executionTime < self.earliest_sequence_time:
                self.earliest_sequence_time = sequence.executionTime
            if sequence.executionTime > self.latest_sequence_time:
                self.latest_sequence_time = sequence.executionTime

    def write(self, out):
        self.out = out

        self.write_file_header()

        for sequence in self.sequences:
            self.write_sequence(sequence)

    def write_file_header(self):

        print >> self.out,  '%(type)4s %(version)05d %(time)19s' % {"type" : "DOR_", "version" : 1, "time" : datetime.datetime.now().strftime("%y-%jT%H:%M:%S.%f")[0:19] + 'Z'}

        print >> self.out, '%(et)19s %(lt)19s %(count)04d' % {"et" : self.earliest_sequence_time.strftime("%y-%jT%H:%M:%S.%f")[0:19] + 'Z' ,\
                                                              "lt" : self.latest_sequence_time.strftime("%y-%jT%H:%M:%S.%f")[0:19] + 'Z', \
                                                              "count" : len(self.sequences)}

    def write_sequence(self, sequence):

        self.write_sequence_header(sequence)
        self.write_sequence_sub_header(sequence)

        param_map = sequence.get_parameter_map()

        keys = sorted(param_map.keys())

        for key in keys:
            self.write_parameter_record(param_map[key])

    def write_sequence_header(self, sequence):

        print >> self.out, 'H1%(name)8s %(type)1s' % {"name" : sequence.sequence_name(), "type": "S"}
        print >> self.out, 'H2%(insOrDel)1s %(ref)3s    %(dest)1s %(source)1s %(params)03d' % {"insOrDel": sequence.get_insertOrDeleteFlag()[0], \
                                                                                                 "ref" : "UTC",
                                                                                                 "dest" : "T",
                                                                                                 "source" : "D",
                                                                                                 "params" : len(sequence.get_parameter_map())}
        print >> self.out, 'H3'
        print >> self.out, 'H4%(execTime)19s' % {"execTime": sequence.get_executionTime().strftime("%y-%jT%H:%M:%S.%f")[0:19] + 'Z'}
        print >> self.out, 'H5'

    def write_sequence_sub_header(self, sequence):

        print >> self.out, 'S1%(uniqueID)10s' % {"uniqueID": sequence.get_uniqueID()}
    def write_parameter_record(self, parameter):

        if parameter.get_representation() > 0:
            type = parameter.get_representation()[0]
        else:
            type = 'R'

        if parameter.get_radix() > 0:
            radix = parameter.get_radix()[0]
        else:
            radix = 'D'

        print >> self.out, 'P%(name)8s %(type)1s %(unit)4s %(radix)1s %(value)-20s' % {"name" : parameter.parameter_name(), \
                                                                                       "type" : type, \
                                                                                       "unit" : "", \
                                                                                       "radix" : radix, \
                                                                                       "value" : parameter.get_value()}

