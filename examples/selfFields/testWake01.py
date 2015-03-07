# 
# Test executable #1 to exercise the beam space charge calculations.
# Here, we calculate the free-space wakefield of a relativistic beam.
# 
# Copyright (c) 2013 UCLA and RadiaBeam Technologies. All rights reserved

# SciPy imports
import numpy as np
import matplotlib.pyplot as plt

# RadiaBeam imports
import RadTrack.spacecharge.RbGaussBunchSpaceCharge as spacecharge

# Specify the beam parameters
# rmsPerp = 25.e-06                      # [m], transverse beam size (rms)
# tauFWHM = 8.996e-14                    # 1 ps FWHM
rmsPerp = 10.e-06
tauFWHM = 7.197e-14
rmsLong = 2.9979e8 * tauFWHM / 2.355   # [m], assumes Gaussian
xInit   = 0.                           # [m], initial position (beam center)
charge  = -3.0e-9                      # [C], total charge
myKE    = 23.e9                     # [eV], average kinetic energy

# create an instance of the space charge class
mySC = spacecharge.RbGaussBunchSpaceCharge(charge,myKE,xInit,rmsLong,rmsPerp)

# Specify the desired grid size
numX   = 40
numY   = 160

# load up the x,y locations of the mesh
# xyMaxH = 4.*rmsLong
xMax = 1.e-04
xMin = -xMax
# xyMaxV = 20.*rmsPerp
yMax = 0.6e-03
yMin = -yMax

xArr  = np.zeros(numX)
for iLoop in range(numX):
    xArr[iLoop] = xMin + iLoop * (xMax-xMin) / (numX-1)

yArr  = np.zeros(numY)
for jLoop in range(numY):
    yArr[jLoop] = yMin + jLoop * (yMax-yMin) / (numY-1)

xGrid = np.zeros((numX, numY))
yGrid = np.zeros((numX, numY))
for iLoop in range(numX):
    for jLoop in range(numY):
        xGrid[iLoop,jLoop] = xMin + iLoop * (xMax-xMin) / (numX-1)
        yGrid[iLoop,jLoop] = yMin + jLoop * (yMax-yMin) / (numY-1)

# Create field profile
Efield = np.zeros((numX, numY))
for iLoop in range(numX):
    for jLoop in range(numY):
        Efield[iLoop, jLoop] = mySC.calcEz3D(xGrid[iLoop,jLoop],yGrid[iLoop,jLoop],0.,0.)

ncLevels = 20
# plot contours of 3D transverse E-field
plt.figure(1)
cs1 = plt.contourf(xGrid, yGrid, Efield, ncLevels)
plt.colorbar(cs1)
plt.axis([xMin, xMax, yMin, yMax])
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('Ez [V/m] for 3D Gaussian e- beam')

# Create field profile
for iLoop in range(numX):
    for jLoop in range(numY):
        Efield[iLoop, jLoop] = mySC.calcEx3D(xGrid[iLoop,jLoop],yGrid[iLoop,jLoop],0.,0.)

# plot contours of 2D transverse E-field
plt.figure(2)
cs2 = plt.contourf(xGrid, yGrid, Efield, ncLevels)
plt.colorbar(cs2)
plt.axis([xMin, xMax, yMin, yMax])
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('Ex [V/m] for 3D Gaussian e- beam')

plt.show()
