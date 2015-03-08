# 
# Test executable to exercise ODE for drifting beam
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#
# python imports
import math

# scipy imports
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PyQt4'
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# RadiaBeam imports
import radtrack.bunch.RbParticleBeam6D as beam

# Calculate time-derivatives for a beam in free space
def driftingBeamGradient(ptcl_data, t_data):

    # forces are zero for a drifting beam 
    derivs = np.zeros(ptcl_data.size)

    # derivatives of position are the momentum
    nptcl = ptcl_data.size / 6
    for iLoop in range(nptcl):
        derivs[iLoop        ] = ptcl_data[iLoop+  nptcl]
        derivs[iLoop+2*nptcl] = ptcl_data[iLoop+3*nptcl]
        derivs[iLoop+4*nptcl] = ptcl_data[iLoop+5*nptcl]
    return derivs

# Specify the desired number of particles 
numpoints = 1200

# Specify the average beam energy [eV] 
energy = 2.5e+6 
 
myBunch = beam.RbParticleBeam6D(numpoints) 
myBunch.setAvgEnergyEV(energy) 
 
alphaX = 0.0 
betaX = 15. 
emitX = 3.3e-07 
myBunch.setTwissParamsByName2D(alphaX, betaX, emitX, 'twissX') 
 
alpha = 4.6 
betaY = 0.012 
emitY = 1.7e-06 
myBunch.setTwissParamsByName2D(alpha, betaY, emitY, 'twissY') 
 
alfaZT = -3.3 
beta   = 0.9 
emittance = 0.58e-06 
myBunch.setTwissParamsByName2D(alfaZT, beta, emittance, 'twissZ') 
 
myDist = myBunch.getDistribution6D() 
myDist.setDistributionType('gaussian') 
myDist.setMaxRmsFactor(3.)
 
myBunch.makeParticlePhaseSpace6D() 
mySpace = myBunch.getPhaseSpace6D() 
myArray = mySpace.getArray6D()

x  = myArray[0,:]
px = myArray[1,:]

xmin = min(x)
xmax = max(x)
if -xmin > xmax:
    xmax = math.fabs(xmin)
else:
    xmin = -xmax

pxmin = min(px)
pxmax = max(px)
if -pxmin > pxmax:
    pxmax = math.fabs(pxmin)
else:
    pxmin = -pxmax

plt.figure(1)  
plt.scatter(x, px, marker=',',s=1, c='k')
plt.axis([xmin, xmax, pxmin, pxmax])
plt.xlabel('x [mm]')
plt.ylabel('px')
plt.title('Initial x-px projection')

flatArray = np.reshape(myArray, myArray.size)
numPrintPoints = 2
print ''
print ' Before integration --'
for iLoop in range(numPrintPoints):
    for jLoop in range(6):
        print ' myArray[', jLoop, ',', iLoop, '] = ', myArray[jLoop, iLoop]

# print ''
# print ' Before integration --'
# for iLoop in range(numPrintPoints):
#     for jLoop in range(6):
#         print ' flatArray[', iLoop+numpoints*jLoop, '] = ', flatArray[iLoop+numpoints*jLoop]

timeArray = np.array([0., 100.])
trajectoryMatrix = odeint(driftingBeamGradient, flatArray, timeArray, printmessg=True)
newArray = np.reshape(trajectoryMatrix[-1,:], [6,numpoints])

print ''
print ' After integration --'
for iLoop in range(numPrintPoints):
    for jLoop in range(6):
        print ' newArray[', jLoop, ',', iLoop, '] = ', newArray[jLoop, iLoop]

x  = newArray[0,:]
px = newArray[1,:]

xmin = min(x)
xmax = max(x)
if -xmin > xmax:
    xmax = math.fabs(xmin)
else:
    xmin = -xmax

pxmin = min(px)
pxmax = max(px)
if -pxmin > pxmax:
    pxmax = math.fabs(pxmin)
else:
    pxmin = -pxmax

plt.figure(2)  
plt.scatter(x, px, marker=',',s=1, c='k')
plt.axis([xmin, xmax, pxmin, pxmax])
plt.xlabel('x [mm]')
plt.ylabel('px')
plt.title('Final x-px projection')

plt.show()
