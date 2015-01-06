# 
# Test executable to explore the use of complex numbers
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#
# python imports
import math
import cmath

# x,z coordinates at which to evaluate u_m(x,z)
wx0=1.e-4
x = 0.1*wx0
z = 4.7*wx0

# try to build up Ex
lambda0 = 1.e-5
rt2opi = math.sqrt(2./math.pi)
zRx = math.pi*wx0**2/lambda0
wxz = wx0*math.sqrt(1.+(z/zRx)**2)
qx0 = 0. + zRx*1.j
qxz = z + qx0
k0 = 2.*math.pi/lambda0
mm = 1

u_m = math.sqrt(rt2opi/wx0) *                              \
      cmath.sqrt(qx0/qxz)   *                              \
      cmath.exp(-(k0*x**2/2./qxz)*1.j) /                   \
      math.sqrt(math.factorial(mm)*2**mm) *                \
      (qx0*qxz.conjugate()/qx0.conjugate()/qxz)**(0.5*mm)


print '     u_m  = ', u_m
print 'real(u_m) = ', u_m.real



xTemp = qx0*qxz.conjugate()/qx0.conjugate()/qxz
yTemp = xTemp**(0.5*mm)
print ' '
print ' xTemp = ', xTemp
print ' yTemp = ', yTemp




arg1 = -17.1 + 0.2j
arg2 =  -1.
arg3 =  11.  + 0j

z1 = cmath.sqrt(arg1)
z2 = cmath.sqrt(arg2)
z3 = cmath.sqrt(arg3)

y1 = arg1**2
y2 = z2**(1./4.)
y3 = y2**(4.)


