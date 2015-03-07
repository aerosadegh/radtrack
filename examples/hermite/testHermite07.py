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
import RadTrack.fields.RbGaussHermiteMN as hermite
import RadTrack.plot.RbPlotUtils as plotutils
import RadTrack.plot.RbPlotImageSequence as imageseq

# instance of the plot utility class
myPlotUtils = plotutils.RbPlotUtils()

# Specify the desired grid size
numPts = 40
nCells = numPts**2 

# Specify the laser beam parameters
wavelength = 10.e-06         # central wavelength [m]
freq0 = 299792458. / wavelength 
w0x  =   20.*wavelength  # w0 at z=zRx
w0y  =   20.*wavelength  # w0 at z=zRy

zR_x = math.pi*w0x**2/wavelength  # horiz. Rayleigh range [m]

# load up the x,y locations of the mesh [m]
xMin = -2.*w0y
xMax =  2.*w0y
yMin = -2.*w0y
yMax =  2.*w0y

xGrid = np.zeros((numPts, numPts))
yGrid = np.zeros((numPts, numPts))

zLoc = zR_x
tLoc = 0.

for iLoop in range(numPts):
    for jLoop in range(numPts):
        xGrid[iLoop,jLoop] = xMin + iLoop * (xMax-xMin) / (numPts-1)
        yGrid[iLoop,jLoop] = yMin + jLoop * (yMax-yMin) / (numPts-1)

# Create a class instance for mode 0,0 (Gaussian)
xMode = 1
yMode = 0
gh = hermite.RbGaussHermiteMN(wavelength,w0x,w0y,0.)
gh.setCoeffSingleModeX(xMode, 1.)
gh.setCoeffSingleModeY(yMode, 1.)

# Create scaled values, so the plot can show microns, rather than meters
x_mm  = xGrid*1.e3
y_mm  = yGrid*1.e3

# first, evaluate Ex at t=0, to set the contour levels
Ex = np.reshape(                                   \
     gh.evaluateEx(np.reshape(xGrid,nCells),       \
                   np.reshape(yGrid,nCells), zLoc, tLoc), (numPts, numPts) )
vLevels = myPlotUtils.generateContourLevels(Ex)

# create the 'axes' object for scrolling through images
axes = imageseq.RbPlotImageSequence()

nPlots = 20
tI = 0.
tF = 1./freq0
dt = (tF-tI) / nPlots
for nLoop in range(nPlots): 
    tLoc = tI + nLoop*dt
    tFS = tLoc * 1.e15

    # Calculate Ex at the 2D array of x,y values
    Ex = np.reshape(                                   \
         gh.evaluateEx(np.reshape(xGrid,nCells),       \
                       np.reshape(yGrid,nCells), zLoc, tLoc), (numPts, numPts) )

    ax = axes.new()
    csN = ax.contourf(x_mm, y_mm, Ex, vLevels, extent='none', aspect='equal')
    plt.gcf().colorbar(csN, format='%3.2e')

    ax.set_xlabel('x [mm]')
    ax.set_ylabel('y [mm]')
    ax.set_title('Ex - modes({0} {1}): slice #{2} at t = {3:2.3f} [fs]'.format(xMode, yMode, nLoop, tFS))

axes.show()
