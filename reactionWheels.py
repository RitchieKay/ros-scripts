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

    def set_ang_mom_vector(self, v):
        self.ang_mom_vector = v

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

    def compute_wheel_speeds(self, qs, qi, qf):

        dQ_i= qs.conjugate() * qi
        angle_i = dQ_i.angle()
        vector_i = dQ_i.vector()

        sc_ang_velocity_i= vector_i * angle_i 
        sc_ang_mom_i     = self.inertia.Iw(sc_ang_velocity_i)
        sc_ang_mom_in_j2000_frame_i = qi.conjugate().rotate_vector(sc_ang_mom_i)

        dQ_f= qi.conjugate() * qf
        angle_f = dQ_f.angle()
        vector_f = dQ_f.vector()

        sc_ang_velocity_f= vector_f * angle_f
        sc_ang_mom_f     = self.inertia.Iw(sc_ang_velocity_f)
        sc_ang_mom_in_j2000_frame_f = qf.conjugate().rotate_vector(sc_ang_mom_f)
 
        d_sc_ang_mom_in_j2000_frame = sc_ang_mom_in_j2000_frame_f - sc_ang_mom_in_j2000_frame_i
        print d_sc_ang_mom_in_j2000_frame

        rwa_ang_mom_in_j2000_frame = self.get_ang_mom_in_j2000_frame(qs) - d_sc_ang_mom_in_j2000_frame


        rwa_ang_mom_in_sc_frame = qf.rotate_vector(rwa_ang_mom_in_j2000_frame)

        self.individual_wheel_speeds(rwa_ang_mom_in_sc_frame)

        return self.ang_mom_vector

    def individual_wheel_speeds(self, rwa_ang_mom_in_sc_frame):

        sc_to_rw_mat = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        if self.isolated_wheel == 1:
            sc_to_rw_mat = sc_to_rw_mat_1off
        elif self.isolated_wheel == 2:
            sc_to_rw_mat = sc_to_rw_mat_2off
        elif self.isolated_wheel == 3:
            sc_to_rw_mat = sc_to_rw_mat_3off
        elif self.isolated_wheel == 4:
            sc_to_rw_mat = sc_to_rw_mat_4off
        elif self.isolated_wheel == 0:
            sc_to_rw_mat = sc_to_rw_mat_all


        self.ang_mom_vector[0] = sc_to_rw_mat[0][0] * rwa_ang_mom_in_sc_frame[0] +\
                                 sc_to_rw_mat[0][1] * rwa_ang_mom_in_sc_frame[1] +\
                                 sc_to_rw_mat[0][2] * rwa_ang_mom_in_sc_frame[2] 
        self.ang_mom_vector[1] = sc_to_rw_mat[1][0] * rwa_ang_mom_in_sc_frame[0] +\
                                 sc_to_rw_mat[1][1] * rwa_ang_mom_in_sc_frame[1] +\
                                 sc_to_rw_mat[1][2] * rwa_ang_mom_in_sc_frame[2] 
        self.ang_mom_vector[2] = sc_to_rw_mat[2][0] * rwa_ang_mom_in_sc_frame[0] +\
                                 sc_to_rw_mat[2][1] * rwa_ang_mom_in_sc_frame[1] +\
                                 sc_to_rw_mat[2][2] * rwa_ang_mom_in_sc_frame[2] 
        self.ang_mom_vector[3] = sc_to_rw_mat[3][0] * rwa_ang_mom_in_sc_frame[0] +\
                                 sc_to_rw_mat[3][1] * rwa_ang_mom_in_sc_frame[1] +\
                                 sc_to_rw_mat[3][2] * rwa_ang_mom_in_sc_frame[2] 

