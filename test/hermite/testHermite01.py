# 
# Test executable to exercise the Gauss-Hermite class
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#
# python imports
import math

# SciPy imports
import numpy as np
# import matplotlib
# matplotlib.use('Qt4Agg')
# matplotlib.rcParams['backend.qt4']='PySide'
import matplotlib.pyplot as plt

# RadiaBeam imports
import RadTrack.fields.RbGaussHermiteMN as hermite
import RadTrack.plot.RbPlotUtils as plotutils
import RadTrack.plot.RbPlotImageSequence as imageseq

# instance of the plot utility class
myPlotUtils = plotutils.RbPlotUtils()

# Specify the desired grid size
numX = 100 
numY = 100
numCells = numX * numY 

# Specify the laser beam parameters
wavelength = 10.e-06         # central wavelength [m]
w0x = 10.*wavelength         # w0 at z=0.

# Specify z location
zLoc = 20. * w0x

# load up the x,y locations of the mesh [m]
xMin = -4.*w0x
xMax =  4.*w0x
yMin = xMin
yMax = xMax

xArr  = np.zeros(numX)
xGrid = np.zeros((numX, numY))
yArr  = np.zeros(numY)
yGrid = np.zeros((numX, numY))
for iLoop in range(numX):
    xArr[iLoop] = xMin + iLoop * (xMax-xMin) / (numX-1)

for jLoop in range(numY):
    yArr[jLoop] = yMin + jLoop * (yMax-yMin) / (numY-1)

for iLoop in range(numX):
    for jLoop in range(numY):
        xGrid[iLoop,jLoop] = xMin + iLoop * (xMax-xMin) / (numX-1)
        yGrid[iLoop,jLoop] = yMin + jLoop * (yMax-yMin) / (numY-1)

# Create a class instance for mode 0,0 (Gaussian)
exMax = 1.3e+09
xMode = 3
yMode = 0
gh00 = hermite.RbGaussHermiteMN(wavelength,w0x,2.0*w0x,0.)
gh00.setCoeffSingleModeX(xMode, exMax)
gh00.setCoeffSingleModeY(yMode, 1.)

# Calculate Ex at the 2D array of x,y values
Ex = np.reshape(gh00.evaluateEx(np.reshape(xGrid,numCells),
                                np.reshape(yGrid,numCells),
                                zLoc,
                                0.),
                (numX, numY))

# Create scaled values, so the plot can show microns, rather than meters
xMM  = xGrid*1.e3
yMM  = yGrid*1.e3
zMM = zLoc *1.e3 
sliceNumber = 1

# Create a single matplotlib window, with multiple plots
axes = imageseq.RbPlotImageSequence()

# first plot
ax = axes.new()
# ax.axis('equal')
vLevels = myPlotUtils.generateContourLevels(Ex)
cs1 = ax.contourf(xMM, yMM, Ex, vLevels, extent='none', aspect='equal')
# plt.colorbar(cs1, format='%3.2e')
plt.gcf().colorbar(cs1, format='%3.2e')
ax.set_xlabel('x [mm]')
ax.set_ylabel('y [mm]')
ax.set_title('Ex - modes({0} {1}): slice #{2} at z = {3:2.1f} [mm]'.format(xMode, yMode, sliceNumber, zMM))
sliceNumber +=1

# -----------------------------------------------
# Create a class instance for mode 0,1 (Gaussian)
xMode = 0
yMode = 1
gh01 = hermite.RbGaussHermiteMN(wavelength,w0x,0.75*w0x,0.)
gh01.setCoeffSingleModeX(xMode, 1.)
gh01.setCoeffSingleModeY(yMode, exMax)

# Calculate Ex at the 2D array of x,y values
Ex = np.reshape(gh01.evaluateEx(np.reshape(xGrid,numCells),
                                np.reshape(yGrid,numCells),
                                zLoc,
                                0.),
                (numX, numY))

# 2nd plot
ax = axes.new()
# ax.axis('equal')
cs2 = ax.contourf(xMM, yMM, Ex, vLevels, extent='none', aspect='equal')
# plt.colorbar(cs2, format='%3.2e')
plt.gcf().colorbar(cs2, format='%3.2e')
ax.set_xlabel('x [mm]')
ax.set_ylabel('y [mm]')
ax.set_title('Ex - modes({0} {1}): slice #{2} at z = {3:2.1f} [mm]'.format(xMode, yMode, sliceNumber, zMM))
sliceNumber +=1

# -----------------------------------------------
# Create a class instance for mode 2,1 (Gaussian)
xMode = 2
yMode = 1
rot_angle = math.pi/4.
gh21 = hermite.RbGaussHermiteMN(wavelength,w0x,w0x,rot_angle)
gh21.setCoeffSingleModeX(xMode, exMax)
gh21.setCoeffSingleModeY(yMode, 1.)

# Calculate Ex at the 2D array of x,y values
Ex = np.reshape(gh21.evaluateEx(np.reshape(xGrid,numCells),
                                np.reshape(yGrid,numCells),
                                zLoc,
                                0.),
                (numX, numY) )

# 3rd plot
ax = axes.new()
# ax.axis('equal')
cs3 = ax.contourf(xMM, yMM, Ex, vLevels, extent='none', aspect='equal')
# plt.colorbar(cs3, format='%3.2e')
plt.gcf().colorbar(cs3, format='%3.2e')
ax.set_xlabel('x [mm]')
ax.set_ylabel('y [mm]')
ax.set_title('Ex - modes({0} {1}): slice #{2} at z = {3:2.1f} [mm]'.format(xMode, yMode, sliceNumber, zMM))
sliceNumber +=1

# -----------------------------------------------
# Create a class instance for mode 3,3 (Gaussian)
xMode = 3
yMode = 3
rot_angle = -math.pi/10.
gh33 = hermite.RbGaussHermiteMN(wavelength,1.3*w0x,0.6*w0x,rot_angle)
gh33.setCoeffSingleModeX(xMode, 1.)
gh33.setCoeffSingleModeY(yMode, exMax)

# Calculate Ex at the 2D array of x,y values
Ex = np.reshape(gh33.evaluateEx(np.reshape(xGrid,numCells),           \
                                np.reshape(yGrid,numCells), zLoc, 0.),  \
                                (numX, numY) )

# 4th plot
ax = axes.new()
# ax.axis('equal')
cs4 = ax.contourf(xMM, yMM, Ex, vLevels, extent='none', aspect='equal')
# plt.colorbar(cs4, format='%3.2e')
plt.gcf().colorbar(cs4, format='%3.2e')
ax.set_xlabel('x [mm]')
ax.set_ylabel('y [mm]')
ax.set_title('Ex - modes({0} {1}): slice #{2} at z = {3:2.1f} [mm]'.format(xMode, yMode, sliceNumber, zMM))
sliceNumber +=1

# generate the master window, with interactive right/left arrow key responses
axes.show()
