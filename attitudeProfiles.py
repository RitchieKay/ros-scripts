from attitudeProfile import *

class AttitudeProfiles:

    def __init__(self):
        self.profiles = []

    def addProfile(self, starttime, endtime, attitudeProfile):
        self.profiles.append({'starttime':starttime, 'endtime':endtime, 'profile':attitudeProfile})

    def __getitem__(self, i):
        return self.profiles[i]

    def __len__(self):
        return len(self.profiles)

    def getQuaternion(self, t):
        for profile in self.profiles:
            
            if t >= profile['starttime'] and t < profile['endtime']:
                span = profile['endtime'] - profile['starttime']
                pos  = t - profile['starttime']
                nt = 2.0 * pos / span - 1
                return profile['profile'].intermediate_quaternion(nt)
