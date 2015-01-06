# 
# Test executable to explore the use of complex numbers
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#
# python imports
import cmath

# try a few things

arg1 = -17.1 + 0.2j
arg2 =  -1.
arg3 =  11.  + 0j

print 'arg1 = ', arg1
print 'arg2 = ', arg2
print 'arg3 = ', arg3

z1 = cmath.sqrt(arg1)
z2 = cmath.sqrt(arg2)
z3 = cmath.sqrt(arg3)

print 'z1 = ', z1
print 'z2 = ', z2
print 'z3 = ', z1

y1 = arg1**2
y2 = z2**(1./4.)
y3 = y2**(4.)

print 'y1 = ', y1
print 'y2 = ', y2
print 'y3 = ', y3


