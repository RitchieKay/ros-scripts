#!/usr/bin/python

from quaternion import *

# 
# This rotates the y axis up perpendicular to the ecliptic
#
r1 = Rotation(2*math.pi*(90-23.5)/360, [1, 0, 0])
q1 = r1.quaternion()

#
# This rotates the x axis to the earth direction
#

r2 = Rotation(2*math.pi*50.0/360, [0, 1, 0])
q2 = r2.quaternion()

print q1
print q2

print q1 * q2

( q2 * q1).print_rotated_axis()
