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

    def sequences(self):
        seqs = []

        c = 0
        for profile in self.profiles:
            p = profile['profile'].sequence()
            p.update_parameter_value(1, datetime.datetime.fromtimestamp(profile['starttime']).strftime('%y-%jT%H:%M:%S.%f')[0:19] + 'Z')
            p.update_parameter_value(2, datetime.datetime.fromtimestamp(profile['endtime']).strftime('%y-%jT%H:%M:%S.%f')[0:19] + 'Z')

            if c > 0:
                t = datetime.datetime.fromtimestamp(self.profiles[c-1]['starttime']) + datetime.timedelta(2.0/86400)
                p.set_executionTime(t.strftime('%Y-%jT%H:%M:%S.%f')[0:21] + 'Z')

            seqs.append(p)
            c += 1


        t0 = datetime.datetime.fromtimestamp(self.profiles[0]['starttime']) - datetime.timedelta(10.0/86400)
        seqs[0].set_executionTime(t0.strftime('%Y-%jT%H:%M:%S.%f')[0:21] + 'Z')

        return seqs
