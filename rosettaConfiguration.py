import re

defaultConfigFile = 'ROSETTA-CONFIG.dat'

class RosettaConfiguration:

    def __init__(self, configFile=defaultConfigFile):

        self.keys = {}
        self.cfg = configFile
        self.readConfig()

    def readConfig(self):

        p = re.compile('([A-z0-9_\-]*)\s+=\s+([A-z0-9_\-/\.,: ]*)')
        f = open(self.cfg)
        for line in f:

            m = p.match(line.strip())
            if m:
                self.keys[m.groups()[0]] = m.groups()[1]

    def getItem(self, item):
        return self.keys[item]
