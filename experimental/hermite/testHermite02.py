#
# Test executable #2 to exercise the Gauss-Hermite class
# Here, we fit a Gauss-Hermite expansion to an arbitrary profile.
# The SciPy least squares method is used.
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

# SciPy imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

# ---------------------------------------------------------
# Make sure the residual() method has access to necessary
#   'global' data:
global mMax, nMax, numFuncCalls, hermiteSeries

# Specify the central laser wavelength
lambda0 = 10.e-06

# Need a place holder for the waist size
w0 = 10.*lambda0

# Define the maximum order(s) of the Hermite expansion
mMax = 0    # horizontal
nMax = 0    # vertical

# Create an instance of the Hermite expansion class
hermiteSeries = RbGaussHermiteMN.RbGaussHermiteMN(lambda0,w0,w0,0.)

# Specify the desired grid size
numX   = 50
numY   = 50
nCells = numX * numY

# load up the x,y locations of the mesh
xMin = -4.*w0
xMax =  4.*w0
yMin = xMin
yMax = xMax

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

# Create transverse field profile (#1 simple Gaussian)
ExGrid = np.zeros((numX, numY))
exMax  = 1.0e+09     # this gets scaled out before plotting/fitting
phi1   = math.pi/17.5
xs1    =  1.07 * w0
ys1    = -0.98 * w0
waistx = 0.9 * w0
waisty = 1.8 * w0
maxValue = 0.
for iLoop in range(numX):
    for jLoop in range(numY):
        xArg =  (xArr[iLoop]-xs1)*math.cos(phi1) + (yArr[jLoop]-ys1)*math.sin(phi1)
        yArg = -(xArr[iLoop]-xs1)*math.sin(phi1) + (yArr[jLoop]-ys1)*math.cos(phi1)
        ExGrid[iLoop, jLoop] = exMax*math.exp(-(xArg/waistx)**2)*math.exp(-(yArg/waisty)**2)
        maxValue = max(ExGrid[iLoop, jLoop], maxValue)

# Divide out the maximum value
ExGrid /= maxValue

# Calculate residuals for the least squares analysis
# params - array of fitting parameters
numFuncCalls = 0
def residuals(params, e, x, y):
    global mMax, nMax, numFuncCalls, hermiteSeries

    hermiteSeries.setWaistX(params[0])
    hermiteSeries.setWaistY(params[1])
    hermiteSeries.setWRotAngle(params[2])
    hermiteSeries.setXShift(params[3])
    hermiteSeries.setYShift(params[4])
    hermiteSeries.setMCoef(params[5:mMax+6])
    hermiteSeries.setNCoef(params[mMax+6:mMax+nMax+7])

# let the user know what's going on if many function calls are required
    if numFuncCalls == 0:
        print ' '
        print 'Number of calls to method residual():'
    numFuncCalls += 1
    if 10*int(numFuncCalls/10.) == numFuncCalls:
        print '  ', numFuncCalls

    return e-hermiteSeries.evaluateEx(x,y,0.,0.)

# plot the transverse field profile
ncLevels = 12
vLevels = [0.001, 0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.05]
plt.figure(1)
cs1 = plt.contourf(xGrid, yGrid, ExGrid, vLevels)
plt.colorbar(cs1)
plt.axis([xMin, xMax, yMin, yMax])
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('x-section #1: Gaussian w/ slight asymmetry & rotation')

# choose initial guesses for all fitting parameters
# also, specify the scale of variations for each
paramGuess = np.zeros(mMax+nMax+7)
paramGuess[0] = 1.2*w0              # horizontal waist
paramGuess[1] = 0.9*w0              #   vertical waist
paramGuess[2] = 0.0                 # rotation angle
paramGuess[3] = 0.0                 # horizontal shift
paramGuess[4] = 0.0                 #   vertical shift
paramGuess[5] = 1.0                 # 0th horiz. coeff
for iLoop in range(6,mMax+6):
    paramGuess[iLoop] = 0.0         # other horiz. coeff's
paramGuess[mMax+6] = 1.0            # 0th vertical coeff
for iLoop in range(mMax+7,mMax+nMax+7):
    paramGuess[iLoop] = 0.0         # other vertical coeff's

# invoke the least squares algorithm
result = leastsq(residuals, paramGuess,             \
                 args=(np.reshape(ExGrid,nCells),   \
                       np.reshape(xGrid,nCells),    \
                       np.reshape(yGrid,nCells)),   \
                 full_output=True, ftol=1e-6,       \
                 maxfev=200)

parFit  = result[0]
nEvals  = result[2]['nfev']
resVals = result[2]['fvec']
message = result[3]
iError  = result[4]

print ' '
print ' iError  = ', iError
print ' message = ', message
print ' nEvals  = ', nEvals
print ' resVals = ', resVals

# load the results into named variables (for clarity)
wxFit  = parFit[0]
wyFit  = parFit[1]
tmpPhi = parFit[2]
phiFit = tmpPhi - 2.*math.pi*int(0.5*tmpPhi/math.pi)
if phiFit > 2.*math.pi: phiFit -= 2.*math.pi
if phiFit < 0.: phiFit += 2.*math.pi
xsFit  = parFit[3]
ysFit  = parFit[4]
mCFit  = np.zeros(mMax+1)
mCFit[0:mMax+1] = parFit[5:mMax+6]
nCFit  = np.zeros(nMax+1)
nCFit[0:nMax+1] = parFit[mMax+6:mMax+nMax+7]

# check the results
print ' '
print 'The least squares minimimization has completed:'
print '  wx  = ', waistx,           '; ', wxFit
print '  wy  = ', waisty,           '; ', wyFit
print '  phi = ', phi1,             '; ', phiFit
print '  xS  = ', xs1,              '; ', xsFit
print '  yS  = ', ys1,              '; ', ysFit
print '  C0x * C0y = 1.0; ', mCFit[0]*nCFit[0]
# print '  C1x =  0.0 ; ', mCFit[1]
# print '  C2x =  0.0 ; ', mCFit[2]
# print '  C3x =  0.0 ; ', mCFit[3]
# print '  C4x =  0.0 ; ', mCFit[4]
# print '  C1y =  0.0 ; ', nCFit[1]
# print '  C2y =  0.0 ; ', nCFit[2]
# print '  C3y =  0.0 ; ', nCFit[3]
# print '  C4y =  0.0 ; ', nCFit[4]

# load up the fitted electric field at all grid points
hermiteSeries.setWaistX(wxFit)
hermiteSeries.setWaistY(wyFit)
hermiteSeries.setWRotAngle(phiFit)
hermiteSeries.setXShift(xsFit)
hermiteSeries.setYShift(ysFit)
hermiteSeries.setMCoef(mCFit)
hermiteSeries.setNCoef(nCFit)

ExFit = np.reshape(hermiteSeries.evaluateEx(
                       np.reshape(xGrid,nCells),          \
                       np.reshape(yGrid,nCells), 0., 0.), \
                       (numX, numY))

# plot the fitted transverse field profile
plt.figure(2)
cs2 = plt.contourf(xGrid, yGrid, ExFit, vLevels)
plt.colorbar(cs2)
plt.axis([xMin, xMax, yMin, yMax])
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('x-section #1: Result of the least squares fit')

# plot the transverse profile of the difference
plt.figure(3)
cs3 = plt.contourf(xGrid, yGrid, ExFit-ExGrid, ncLevels)
plt.colorbar(cs3)
plt.axis([xMin, xMax, yMin, yMax])
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('x-section #1: Absolute differences in Ex')

plt.show()
