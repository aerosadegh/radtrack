#
# Test executable to exercise the Gauss-Hermite class
#
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#
# python imports
import math

# SciPy imports
import numpy as np
import matplotlib.pyplot as plt

# RadiaBeam imports
from radtrack.fields import RbGaussHermiteMN
from radtrack.util import plotTools
from radtrack.plot import RbPlotImageSequence

# Specify the desired grid size
numX = 30
numZ = 160
nCells = numX * numZ

# Specify the laser beam parameters
wavelength = 10.e-06       # central wavelength [m]
freq0 = 299792458. / wavelength
w0x = 4.*wavelength    # w0 at z=zRx
w0y = w0x

zR_x = math.pi*w0x**2/wavelength  # horiz. Rayleigh range [m]

# load up the x,z locations of the mesh [m]
xMin = -3.*w0x
xMax = 3.*w0x

zMin = -10.*wavelength
zMax = 10.*wavelength

xArray = np.zeros(numX)
yArray = np.zeros(numX)
zArray = np.zeros(numZ)

yLoc = 0.
dx = (xMax-xMin) / (numX-1)
for iLoop in range(numX):
    xArray[iLoop] = xMin + iLoop * dx
    yArray[iLoop] = yLoc

dz = (zMax-zMin) / (numZ-1)
for iLoop in range(numZ):
    zArray[iLoop] = zMin + iLoop * dz

xGrid = np.zeros((numZ, numX))
yGrid = np.zeros((numZ, numX))
zGrid = np.zeros((numZ, numX))

for iLoop in range(numZ):
    for jLoop in range(numX):
        xGrid[iLoop, jLoop] = xMin + jLoop * dx
        yGrid[iLoop, jLoop] = yLoc
        zGrid[iLoop, jLoop] = zMin + iLoop * dz

# Create a class instance for mode 0,0 (Gaussian)
xMode = 0
yMode = 0
gh = RbGaussHermiteMN.RbGaussHermiteMN(wavelength,w0x,w0y,0.)
gh.setCoeffSingleModeX(xMode, 1.)
gh.setCoeffSingleModeY(yMode, 1.)

# Create scaled values, so plot can show [mm], not [m]
xMM  = xGrid*1.e3

# first, evaluate Ex at the waist, to set the contour levels
Ex = np.zeros((numZ, numX))
Ex = np.reshape(gh.evaluateEx(np.reshape(xGrid,nCells),
                np.reshape(yGrid,nCells), 0., 0.),
                (numZ, numX) )
vLevels = plotTools.generateContourLevels(Ex)

# Instead of x,y cross-sections, sliding along the z-axis,
#   we plot an x-z cross-section, which we slide along the z-axis.

# create the 'axes' object for scrolling through images
axes = RbPlotImageSequence.RbPlotImageSequence()

nPlots = 11
zShift_i = -3.* zR_x
zShift_f =  3.* zR_x
deltaZ = (zShift_f - zShift_i) / (nPlots-1)
for nLoop in range(nPlots):
    zShift = zShift_i + nLoop*deltaZ

    # load up the shifted array of longitudinal positions
    for iLoop in range(numZ):
        zArray[iLoop] = zShift + zMin + iLoop * dz
        for jLoop in range(numX):
            zGrid[iLoop, jLoop] = zShift + zMin + iLoop * dz

    # Calculate Ex at the 1D array of x,y values, for a range of z-values
    for iLoop in range(numZ):
        Ex[iLoop:iLoop+1] = gh.evaluateEx(xArray, yArray, zArray[iLoop], 0.)

    ax = axes.new()

    zMM  = zGrid*1.e3
    csN = ax.contourf(zMM, xMM, Ex, vLevels, extent='none', aspect='equal')
    plt.gcf().colorbar(csN, format='%3.2e')

    ax.set_xlabel('z [mm]')
    ax.set_ylabel('x [mm]')
    ax.set_title('Ex - modes({0} {1}): X-Z slice #{2}'.format(xMode, yMode, nLoop))

axes.show()
