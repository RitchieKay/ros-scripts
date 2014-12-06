from quaternion import *
from inertiaParser import *
from rosettaConfiguration import *
from inertia import *

sc_to_rw_mat_1off = ( ( 0.000000e+00, 0.000000e+00, 0.000000e+00 ), \
                      ( 8.193392e-01, 2.279204e-03, 8.122086e-01 ), \
                      ( 8.134810e-01, 1.000018e+00,-3.967129e-03 ), \
                      ( 4.381397e-03,-9.973330e-01,-8.125231e-01 ))

sc_to_rw_mat_2off = ( ( 8.192168e-01, 2.278864e-03, 8.120873e-01 ), \
		      ( 0.000000e+00, 0.000000e+00, 0.000000e+00 ), \
                      (-1.222211e-03, 9.977516e-01,-8.115800e-01 ), \
                      ( 8.194772e-01,-9.950656e-01,-4.520987e-03 ))

sc_to_rw_mat_3off = ( ( 8.179878e-01, 1.005558e+00,-3.989107e-03 ), \
                      ( 1.229166e-03,-1.003429e+00, 8.161983e-01 ), \
                      ( 0.000000e+00, 0.000000e+00, 0.000000e+00 ), \
                      ( 8.182544e-01, 3.166868e-03,-8.164921e-01 ))

sc_to_rw_mat_4off = ( (-4.403549e-03, 1.002375e+00, 8.166311e-01 ), \
                      ( 8.237434e-01,-1.000246e+00,-4.544524e-03 ), \
                      ( 8.178603e-01, 3.165342e-03,-8.160989e-01 ), \
                      ( 0.000000e+00, 0.000000e+00, 0.000000e+00 ))

sc_to_rw_mat_all  = ( ( 4.081401e-01, 4.998659e-01, 4.063104e-01 ), \
                      ( 4.111382e-01,-4.976614e-01, 4.058375e-01 ), \
                      ( 4.075897e-01, 5.029061e-01,-4.080389e-01 ), \
                      ( 4.104683e-01,-4.999816e-01,-4.082566e-01 ))

rw_to_sc_mat      = ( ( 6.106860e-01, 6.139091e-01, 6.076657e-01, 6.107046e-01), \
                      ( 5.001355e-01,-4.969614e-01, 5.032291e-01,-4.992260e-01), \
                      ( 6.139439e-01, 6.133066e-01,-6.144127e-01,-6.146652e-01))


class rwa:

    def __init__(self):
        self.ang_mom_vector = [0,0,0,0]
        self.isolated_wheel = 0
        self.four_wheels = True
        self.inertia = InertiaParser(RosettaConfiguration().getItem('INERTIA')).inertia()
        self.set_four_wheels(RosettaConfiguration().getItem('FOUR_WHEELS') == 'TRUE')
        self.set_isolated_wheel(int(RosettaConfiguration().getItem('ISOLATED_WHEEL')))

    def set_ang_mom_vector(self, v):
        self.ang_mom_vector = v
        if not self.four_wheels:
            self.ang_mom_vector[self.isolated_wheel - 1] = 0

    def set_isolated_wheel(self, wheel):
        self.isolated_wheel = wheel

    def set_four_wheels(self, status):
        self.four_wheels = status

    def get_ang_mom_in_sc_frame(self):

        return Vector( rw_to_sc_mat[0][0] * self.ang_mom_vector[0] + \
                       rw_to_sc_mat[0][1] * self.ang_mom_vector[1] + \
                       rw_to_sc_mat[0][2] * self.ang_mom_vector[2] + \
                       rw_to_sc_mat[0][3] * self.ang_mom_vector[3] , \
                       rw_to_sc_mat[1][0] * self.ang_mom_vector[0] + \
                       rw_to_sc_mat[1][1] * self.ang_mom_vector[1] + \
                       rw_to_sc_mat[1][2] * self.ang_mom_vector[2] + \
                       rw_to_sc_mat[1][3] * self.ang_mom_vector[3], 
                       rw_to_sc_mat[2][0] * self.ang_mom_vector[0] + \
                       rw_to_sc_mat[2][1] * self.ang_mom_vector[1] + \
                       rw_to_sc_mat[2][2] * self.ang_mom_vector[2] + \
                       rw_to_sc_mat[2][3] * self.ang_mom_vector[3] )
                    

    def get_ang_mom_in_j2000_frame(self, q):

        return q.conjugate().rotate_vector(self.get_ang_mom_in_sc_frame())

    # Arguments are the attitude quaternion and delta quaternion @ time s & f 
    # together with the time interval represented by the delta

    def compute_wheel_speeds(self, qs, dQs, qf, dQf, dt):

        # First compute the angular momentum of the spacecraft in the J2000 frame at the time
        # represented by the quaternion qs and the time represented by the quaternion qf
      
        angle_s = dQs.angle()
        vector_s = dQs.vector()

        sc_ang_velocity_s= vector_s.normalize() * (angle_s/dt)
        sc_ang_mom_s     = self.inertia.Iw(sc_ang_velocity_s)
        sc_ang_mom_in_j2000_frame_s = qs.conjugate().rotate_vector(sc_ang_mom_s)

        angle_f = dQf.angle()
        vector_f = dQf.vector()

        sc_ang_velocity_f= vector_f.normalize() * (angle_f/dt)
        sc_ang_mom_f     = self.inertia.Iw(sc_ang_velocity_f)
        sc_ang_mom_in_j2000_frame_f = qf.conjugate().rotate_vector(sc_ang_mom_f)

        # Now we compute the delta in the spacecraft angular momentum in the J2000 frame
        # This is the first component that needs to be applied to the wheels
 
        d_sc_ang_mom_in_j2000_frame = sc_ang_mom_in_j2000_frame_f - sc_ang_mom_in_j2000_frame_s

        # Now we compute the change in the angular momentum of the wheels as a result of the
        # rotation of the spacecraft body from qs to qf

        rwa_ang_mom_in_j2000_frame_s = self.get_ang_mom_in_j2000_frame(qs)
        rwa_ang_mom_in_j2000_frame_f = self.get_ang_mom_in_j2000_frame(qf)

        d_rwa_ang_mom_in_j2000_frame = rwa_ang_mom_in_j2000_frame_f - rwa_ang_mom_in_j2000_frame_s

        # 1: If there is no change in the spacecraft angular momentum then the wheel speeds still
        #    need to change to keep the total reaction wheel angular momentum in the J2000 frame
        #    the same despite the rotation of their orientation.
        #    This difference must be applied to the wheels

        factor_1 = -(rwa_ang_mom_in_j2000_frame_f - rwa_ang_mom_in_j2000_frame_s)

        # 2: Any change in spacecraft angular momentum must be directly compensated by the wheels:

        factor_2 = -d_sc_ang_mom_in_j2000_frame

        # These two things are combined, transferred back into the spacecraft frame and then applied
        # to the wheels

        rwa_ang_mon_delta_in_sc_frame = qf.rotate_vector(factor_1 + factor_2)

        # Project this onto the wheels ...

        ang_mom_vector = self.individual_wheel_speeds(rwa_ang_mon_delta_in_sc_frame)

        # ... and add onto the current wheel speeds

        self.ang_mom_vector = [self.ang_mom_vector[i] + ang_mom_vector[i] for i in range(4)]

        return self.ang_mom_vector

    def individual_wheel_speeds(self, rwa_ang_mom_in_sc_frame):

        sc_to_rw_mat = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

        if self.four_wheels:
            sc_to_rw_mat = sc_to_rw_mat_all
        else:
     
            if self.isolated_wheel == 1:
                sc_to_rw_mat = sc_to_rw_mat_1off
            elif self.isolated_wheel == 2:
                sc_to_rw_mat = sc_to_rw_mat_2off
            elif self.isolated_wheel == 3:
                sc_to_rw_mat = sc_to_rw_mat_3off
            elif self.isolated_wheel == 4:
                sc_to_rw_mat = sc_to_rw_mat_4off

        ang_mom_vector = [0, 0, 0, 0]

        ang_mom_vector[0] = sc_to_rw_mat[0][0] * rwa_ang_mom_in_sc_frame[0] +\
                            sc_to_rw_mat[0][1] * rwa_ang_mom_in_sc_frame[1] +\
                            sc_to_rw_mat[0][2] * rwa_ang_mom_in_sc_frame[2] 
        ang_mom_vector[1] = sc_to_rw_mat[1][0] * rwa_ang_mom_in_sc_frame[0] +\
                            sc_to_rw_mat[1][1] * rwa_ang_mom_in_sc_frame[1] +\
                            sc_to_rw_mat[1][2] * rwa_ang_mom_in_sc_frame[2] 
        ang_mom_vector[2] = sc_to_rw_mat[2][0] * rwa_ang_mom_in_sc_frame[0] +\
                            sc_to_rw_mat[2][1] * rwa_ang_mom_in_sc_frame[1] +\
                            sc_to_rw_mat[2][2] * rwa_ang_mom_in_sc_frame[2] 
        ang_mom_vector[3] = sc_to_rw_mat[3][0] * rwa_ang_mom_in_sc_frame[0] +\
                            sc_to_rw_mat[3][1] * rwa_ang_mom_in_sc_frame[1] +\
                            sc_to_rw_mat[3][2] * rwa_ang_mom_in_sc_frame[2] 

        return ang_mom_vector
