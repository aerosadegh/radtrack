# 
# Test executable to exercise some matplotlib syntax
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#
# python imports
import math

# SciPy imports
import matplotlib.pyplot as plt

# RadiaBeam imports
import RadTrack.bunch.RbParticleBeam6D as beam

# class PlotPhaseSpace6D:
#     def __init__(self, phaseSpace6D):
#         self.phaseSpace6D = phaseSpace6D
#         self.phaseSpace6D.checkArray()
#        return

# Specify the desired number of particles 
numpoints = 4000 

# Specify the average beam energy [eV] 
energy = 2.5e+6 
 
myBunch = beam.RbParticleBeam6D(numpoints) 

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
mySpace = myBunch.getDistribution6D()
myArray = mySpace.getPhaseSpace6D().getArray6D()

x  = myArray[0,:] * 1000.   # [m] -> [mm]

xmin = min(x)
xmax = max(x)
if -xmin > xmax:
    xmax = math.fabs(xmin)
else:
    xmin = -xmax

px = myArray[1,:]
pxmin = min(px)
pxmax = max(px)
if -pxmin > pxmax:
    pxmax = math.fabs(pxmin)
else:
    pxmin = -pxmax

y  = myArray[2,:] * 1000.   # [m] -> [mm]
ymin = min(y)
ymax = max(y)
if -ymin > ymax:
    ymax = math.fabs(ymin)
else:
    ymin = -ymax

py = myArray[3,:]
pymin = min(py)
pymax = max(py)
if -pymin > pymax:
    pymax = math.fabs(pymin)
else:
    pymin = -pymax

z  = myArray[4,:]
pz = myArray[5,:]

plt.figure(1)  
plt.scatter(x, px, marker=',',s=1, c='k')
plt.axis([xmin, xmax, pxmin, pxmax])
plt.xlabel('x [mm]')
plt.ylabel('px')
plt.title('x - px phase space projection')

plt.figure(2)  
plt.scatter(y, py, marker=',',s=1, c='k')
plt.axis([ymin, ymax, pymin, pymax])
plt.xlabel('y [mm]')
plt.ylabel('py')
plt.title('y - py phase space projection')

plt.figure(3)  
plt.scatter(x, y, marker=',',s=1, c='k')
plt.axis([xmin, xmax, ymin, ymax])
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
plt.title('x - y phase space projection')

plt.figure(4)  
plt.scatter(px, py, marker=',',s=1, c='k')
plt.axis([pxmin, pxmax, pymin, pymax])
plt.xlabel('px')
plt.ylabel('py')
plt.title('px - py phase space projection')

plt.show()

