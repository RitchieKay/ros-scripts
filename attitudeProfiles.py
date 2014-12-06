from attitudeProfile import *
from rosettaConfiguration import *

class AttitudeProfiles:

    def __init__(self):
        self.profiles = []

    def addProfile(self, starttime, endtime, attitudeProfile):
        self.profiles.append({'starttime':starttime, 'endtime':endtime, 'profile':attitudeProfile})

    @staticmethod
    def makeAttitudeProfiles():
        a = AttitudeProfileParser(RosettaConfiguration().getItem('PROFILES'))
        sequences = a.get_sequences()
        profiles = AttitudeProfiles()
        for sequence in sequences:
            try:
                p = AttitudeProfile.make_from_sequence(sequence)
                starttime = calendar.timegm(datetime.datetime.strptime(sequence.get_parameter_value(1), "%Y-%jT%H:%M:%S.%fZ").utctimetuple())
                endtime =  calendar.timegm(datetime.datetime.strptime(sequence.get_parameter_value(2), "%Y-%jT%H:%M:%S.%fZ").utctimetuple())
                profiles.addProfile(starttime, endtime, p)
            except AttitudeProfileError:
                pass
        return profiles

    def __getitem__(self, i):
        return self.profiles[i]

    def __len__(self):
        return len(self.profiles)

    def first_quaternion(self):
        return self.quaternion(self.profiles[0]['starttime'])
    def last_quaternion(self):
        return self.quaternion(self.profiles[-1]['endtime'])

    def start_time(self):
        return self.profiles[0]['starttime']
    def end_time(self):
        return self.profiles[-1]['endtime']

    def quaternion(self, t):
        for profile in self.profiles:
            
            if t >= profile['starttime'] and t < profile['endtime']:
                span = profile['endtime'] - profile['starttime']
                pos  = t - profile['starttime']
                nt = 2.0 * pos / span - 1
                return profile['profile'].intermediate_quaternion(nt)

    def deltaQuaternion(self, t, delta):
        q0 = self.quaternion(t)
        q1 = self.quaternion(t + delta)
        dq = q0.conjugate() * q1
        return dq

    def deltaDeltaQuaternion(self, t, delta):
        q0 = self.deltaQuaternion(t, delta)
        q1 = self.deltaQuaternion(t + delta, delta)
        dq = q0.conjugate() * q1
        return dq


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
