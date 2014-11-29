#!/usr/bin/python

import sys
import math

if len(sys.argv) < 2:
    print 'Usage:', sys.argv[0], '<hex value> or <msw (dec)> <lsw(dec)'
    sys.exit(-1)
hex = ''

if len(sys.argv) == 2:
    hex = sys.argv[1]
else:
  hex = str('{0:X}'.format(int(sys.argv[1])) + '{0:04X}'.format(int(sys.argv[2])))

exponent = int(hex[-2:],16)
mantissa = int(hex[0:-2],16)

if exponent > 0x7F:
    exponent -= 0x100
if mantissa > 0x7FFFFF:
    mantissa -= 0x1000000

mantissa = float(mantissa) / 0x800000

print mantissa * math.pow(2, exponent)
