import re

configFile = 'ROSETTA-CONFIG.dat'

class RosettaConfiguration:

    def __init__(self):
        self.keys = {}
        self.readConfig()

    def readConfig(self):

        p = re.compile('([A-z0-9_\-]*)\s+=\s+([A-z0-9_\-/\.]*)')
        f = open(configFile)
        for line in f:

            m = p.match(line.strip())
            if m:
                self.keys[m.groups()[0]] = m.groups()[1]

    def getItem(self, item):
        return self.keys[item]
