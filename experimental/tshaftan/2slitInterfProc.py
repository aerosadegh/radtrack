# -*- coding: utf-8 -*-
#cd C:\d from old\RadiaBeam\RadSoft\SRW\2dipoleInterf
# python GaussBeamDiffr.py
from __future__ import print_function #Python 2.7 compatibility
from numpy import size
import pylab as py
from scipy.special import jv
from math import sin, cos

#Defining paramet		 ers for analytic calculation
Aperture= 0.00005#float(OutSRWdata[8])
SlitSeparation=0.0002 #
lam=2.4796e-6 #1.2398/0.5 eV
NptsIn=1000 #size(InSRW)
NptsOut=1000 #size(OutSRW)
Siz=0.05 #float(OutSRWdata[5])
DriftLength=1.0 #float(InSRWdata[8])

# Computing intensity distribution as per Born & Wolf, Principles of Optics
th=[]
Inte=[]
sOut=[]
sIn=[]
for i in range(NptsOut):
	thx=2.0*(i-NptsOut/2.0+0.5)*Siz/NptsOut/DriftLength
	th.append(thx)
	sOut.append(thx*DriftLength*1)
#	print('angles:',[thx, thx*DriftLength*1])
	xA=3.1415*Aperture*sin(thx)/lam
	xS=3.1415*SlitSeparation*sin(thx)/lam
	Inte.append((sin(xA)/(xA+0.00001)*cos(xS))**2)

#for i in range(NptsIn):
#	sIn.append(2000.0*(i-NptsIn/2.0)*float(InSRWdata[5])/NptsIn)

py.plot(sOut, Inte, '-b.')
#py.plot(sIn, InSRW, '--g.')
#py.plot(sOut, OutSRW, '-r.')
py.xlabel('$x$')
py.ylabel('Normalized Intensity, a.u.')
py.title('Intensity distribution')                                
py.grid(True)
#py.savefig('besseln0to6.eps', format = 'eps')                                      
py.show()