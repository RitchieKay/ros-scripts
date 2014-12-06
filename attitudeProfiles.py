from attitudeProfile import *
from rosettaConfiguration import *

class ProfileElement:
    def __init__(self, starttime, endtime, profile):
        self.starttime = starttime
        self.endtime = endtime
        self.prof = profile

    def __lt__(self, other):
        return self.starttime < other.starttime

    def start_time(self):
        return self.starttime
    def end_time(self):
        return self.endtime
    def profile(self):
        return self.prof 

class AttitudeProfiles:

    def __init__(self):
        self.profiles = []

    def addProfile(self, starttime, endtime, attitudeProfile):
        self.profiles.append(ProfileElement(starttime, endtime, attitudeProfile))

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
        profiles.sort()
        return profiles

    def __getitem__(self, i):
        return self.profiles[i]

    def __len__(self):
        return len(self.profiles)

    def sort(self):
        self.profiles.sort()

    def first_quaternion(self):
        return self.quaternion(self.profiles[0].start_time())
    def last_quaternion(self):
        return self.quaternion(self.profiles[-1].end_time())

    def start_time(self):
        return self.profiles[0].start_time()
    def end_time(self):
        return self.profiles[-1].end_time()

    def quaternion(self, t):
        for profile in self.profiles:
            
            if t >= profile.start_time() and t < profile.end_time():
                span = profile.end_time() - profile.start_time()
                pos  = t - profile.start_time()
                nt = 2.0 * pos / span - 1
                return profile.profile().intermediate_quaternion(nt)

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
            p = profile.profile().sequence()
            p.update_parameter_value(1, datetime.datetime.fromtimestamp(profile.start_time()).strftime('%y-%jT%H:%M:%S.%f')[0:19] + 'Z')
            p.update_parameter_value(2, datetime.datetime.fromtimestamp(profile.end_time()).strftime('%y-%jT%H:%M:%S.%f')[0:19] + 'Z')

            if c > 0:
                t = datetime.datetime.fromtimestamp(self.profiles[c-1].start_time()) + datetime.timedelta(2.0/86400)
                p.set_executionTime(t.strftime('%Y-%jT%H:%M:%S.%f')[0:21] + 'Z')

            seqs.append(p)
            c += 1


        t0 = datetime.datetime.fromtimestamp(self.profiles[0].start_time()) - datetime.timedelta(10.0/86400)
        seqs[0].set_executionTime(t0.strftime('%Y-%jT%H:%M:%S.%f')[0:21] + 'Z')

        return seqs
