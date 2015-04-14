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
# matplotlib.rcParams['backend.qt4']='PyQt4'
import matplotlib.pyplot as plt

# RadiaBeam imports
import radtrack.fields.RbGaussHermiteMN as hermite
import radtrack.plot.RbPlotUtils as plotutils
import radtrack.plot.RbPlotImageSequence as imageseq

# instance of the plot utility class
myPlotUtils = plotutils.RbPlotUtils()

# Specify the desired grid size
numPts = 40
numCells = numPts**2

# Specify the laser beam parameters
wavelength = 10.e-06       # central wavelength [m]
w0x  =   20.*wavelength    # w0 at z=zRx
w0y  =  w0x

zR_x = math.pi*w0x**2/wavelength  # horiz. Rayleigh range [m]

# load up the x,y locations of the mesh [m]
xMin = -4.*w0x
xMax =  4.*w0x

yMin = xMin
yMax = xMax

zMin = -2000.*wavelength
zMax =  2000.*wavelength

xGrid = np.zeros((numPts, numPts))
yGrid = np.zeros((numPts, numPts))

for iLoop in range(numPts):
    for jLoop in range(numPts):
        xGrid[iLoop,jLoop] = xMin + iLoop * (xMax-xMin) / (numPts-1)
        yGrid[iLoop,jLoop] = yMin + jLoop * (yMax-yMin) / (numPts-1)

# Create a class instance for mode 0,0 (Gaussian)
xMode = 0
yMode = 4
gh = hermite.RbGaussHermiteMN(wavelength,w0x,w0y,0.)
gh.setCoeffSingleModeX(xMode, 1.)
gh.setCoeffSingleModeY(yMode, 1.)

# Create scaled values, so plot can show [mm], not [m]
x_mm  = xGrid*1.e3
y_mm  = yGrid*1.e3

# first, evaluate Ex at t=0, to set the contour levels
Ex = np.reshape(gh.evaluateEx(np.reshape(xGrid,numCells),
                             np.reshape(yGrid,numCells),
                             0.,
                             0.),
                (numPts,numPts) )
vLevels = myPlotUtils.generateContourLevels(Ex)

# create the 'axes' object for scrolling through images
axes = imageseq.RbPlotImageSequence()

nPlots = 11
dz = (zMax-zMin) / (nPlots-1)
for nLoop in range(nPlots):
    
# Calculate Ex at the 2D array of x,y values
    zLoc = zMin + nLoop*dz
    zMM = 1000.*zLoc

    Ex = np.reshape(gh.evaluateEx(np.reshape(xGrid,numCells),
                                  np.reshape(yGrid,numCells),
                                  zLoc,
                                  0.),
                    (numPts, numPts) )

    ax = axes.new()
    csN = ax.contourf(x_mm, y_mm, Ex, vLevels, extent='none', aspect='equal')
    plt.gcf().colorbar(csN, format='%3.2e')

    ax.set_xlabel('x [mm]')
    ax.set_ylabel('y [mm]')
    ax.set_title('Ex - modes({0} {1}): slice #{2} at z = {3:2.3f} [mm]'.format(xMode, yMode, nLoop, zMM))

axes.show()
