# Test executable #5 to exercise the Gauss-Hermite class
# Here, we fit two Gauss-Hermite expansions to a donut shaped profile
# (Each one forces one of the zero'th order coefficients to be zero)
# The SciPy least squares method is used.
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

# python imports
import math

# SciPy imports
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

# RadiaBeam imports
import RadTrack.fields.RbGaussHermiteMN as hermite

# ---------------------------------------------------------
# Make sure the residual() method has access to necessary
#   'global' data:
global mMax, numFuncCalls, hS1, hS2, zGrid, tGrid, nCells

# Specify the central laser wavelength
lambda0 = 10.e-06

# Need a place holder for the waist size
w0 = 10.*lambda0

# Define the maximum order(s) of the Hermite expansion
mMax = 24    # horizontal and vertical

# Create two instances of the Hermite expansion class
hS1 = hermite.RbGaussHermiteMN(lambda0,w0,w0,0.)
hS2 = hermite.RbGaussHermiteMN(lambda0,w0,w0,0.)

# Specify the desired grid size
numPts = 50
nCells = numPts**2

# load up the x,y locations of the mesh
xMin = -4.*w0
xMax =  4.*w0

yMin = xMin
yMax = xMax

xArr  = np.zeros(numPts)
for iLoop in range(numPts):
    xArr[iLoop] = xMin + iLoop * (xMax-xMin) / (numPts-1)

yArr  = np.zeros(numPts)
for jLoop in range(numPts):
    yArr[jLoop] = yMin + jLoop * (yMax-yMin) / (numPts-1)

xGrid = np.zeros((numPts, numPts))
yGrid = np.zeros((numPts, numPts))

for iLoop in range(numPts):
    for jLoop in range(numPts):
        xGrid[iLoop,jLoop] = xMin + iLoop * (xMax-xMin) / (numPts-1)
        yGrid[iLoop,jLoop] = yMin + jLoop * (yMax-yMin) / (numPts-1)

# Create transverse field profile (#3 elliptical Gaussian donut)
ExGrid = np.zeros((numPts, numPts))
wx3  =  2.0 * w0
rad1 =  1.0 * w0
rad2 =  2.0 * w0
mVal =  0.0
for iLoop in range(numPts):
    for jLoop in range(numPts):
        xArg = xArr[iLoop]
        yArg = yArr[jLoop]
        rArg = math.sqrt(xArg**2 + yArg**2)
        rFactor = 1.0 
        if rArg <= rad2:
            rFactor = 0.5 + 0.5*math.cos(math.pi*((rArg-rad1)/(rad2-rad1) - 1.))
        if rArg <= rad1:
            rFactor = 0.0
        ExGrid[iLoop, jLoop] = rFactor*math.exp(-(xArg/wx3)**2)*math.exp(-(yArg/wx3)**2)
        mVal = max(ExGrid[iLoop, jLoop], mVal)

# Divide out the maximum value
ExGrid /= mVal

# Calculate residuals for the least squares analysis
# params - array of fitting parameters
numFuncCalls = 0
def residuals(params, e, x, y):
    global mMax, numFuncCalls, hS1, hS2, zGrid, tGrid, nCells

    hS1.setWaistX(params[0])
    hS1.setWaistY(params[0])
    hS2.setWaistX(params[0])
    hS2.setWaistY(params[0])

    hCoefs = np.zeros(mMax+1)
    for ii in range(mMax):
        hCoefs[ii+1] = params[1+ii]
    hS1.setMCoef(hCoefs)
    hS2.setNCoef(hCoefs)

    vCoefs = np.zeros(mMax+1)
    for ii in range(mMax+1):
        vCoefs[ii] = params[mMax+1+ii]
    hS1.setNCoef(vCoefs)
    hS2.setMCoef(vCoefs)

# let the user know what's going on if many function calls are required    
    if numFuncCalls == 0:
        print ' '
        print 'Number of calls to method residual():'        
    numFuncCalls += 1
    if 100*int(numFuncCalls/100.) == numFuncCalls:
        print '  ', numFuncCalls

    return e-hS1.evaluateEx(x,y,0.,0.)  \
            -hS2.evaluateEx(x,y,0.,0.)

# plot the transverse field profile
ncLevels = 12
vLevels = [0.001, 0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.05] 
plt.figure(1)
cs1 = plt.contourf(xGrid, yGrid, ExGrid, vLevels)
plt.colorbar(cs1)
plt.axis([xMin, xMax, yMin, yMax])
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('x-section #2: quadratic square (sharp cut-off)')

# choose initial guesses for all fitting parameters
# also, specify the scale of variations for each
paramGuess = np.zeros(2*mMax+2)
paramGuess[0] = w0                  # horizontal waist
paramGuess[1] = 1.0
for ii in range(mMax-1):
    paramGuess[ii+2] = 1.e-5        # horiz. coeff's
paramGuess[mMax+1] = 1.0
for ii in range(mMax):
    paramGuess[mMax+1+ii] = 1.e-5    # vertical coeff's

# invoke the least squares algorithm
result = leastsq(residuals, paramGuess,             \
                 args=(np.reshape(ExGrid,nCells),   \
                       np.reshape(xGrid,nCells),    \
                       np.reshape(yGrid,nCells)),   \
                 full_output=True, ftol=1e-4,       \
                 maxfev=1200)

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
wxFit = parFit[0]
mCFit = np.zeros(mMax+1)
for ii in range(mMax):
    mCFit[ii+1] = parFit[1+ii]
nCFit = np.zeros(mMax+1)
for ii in range(mMax+1):
    nCFit[ii] = parFit[mMax+1+ii]

# check the results
print ' '
print 'The least squares minimimization has completed:'
print '  wx  = ', wx3, '; ', wxFit
print '  C0x =  0.; ', mCFit[0]
print '  C0y =  NA; ', nCFit[0]
if mMax >= 1:
    print '  C1x =  NA; ', mCFit[1]
    print '  C1y =  NA; ', nCFit[1]
if mMax >= 2:
    print '  C2x =  NA; ', mCFit[2]
    print '  C2y =  NA; ', nCFit[2]
if mMax >= 3:
    print '  C3x =  NA; ', mCFit[3]
    print '  C3y =  NA; ', nCFit[3]
if mMax >= 4:
    print '  C4x =  NA; ', mCFit[4]
    print '  C4y =  NA; ', nCFit[4]
if mMax >= 5:
    print '  C5x =  NA; ', mCFit[5]
    print '  C5y =  NA; ', nCFit[5]
if mMax >= 6:
    print '  C6x =  NA; ', mCFit[6]
    print '  C6y =  NA; ', nCFit[6]
if mMax >= 7:
    print '  C7x =  NA; ', mCFit[7]
    print '  C7y =  NA; ', nCFit[7]
if mMax >= 8:
    print '  C8x =  NA; ', mCFit[8]
    print '  C8y =  NA; ', nCFit[8]
if mMax >= 9:
    print '  C9x =  NA; ', mCFit[9]
    print '  C9y =  NA; ', nCFit[9]
if mMax >= 10:
    print '  C10x=  NA; ', mCFit[10]
    print '  C10y=  NA; ', nCFit[10]
if mMax >= 11:
    print '  C11x=  NA; ', mCFit[11]
    print '  C11y=  NA; ', nCFit[11]
if mMax >= 12:
    print '  C12x=  NA; ', mCFit[12]
    print '  C12y=  NA; ', nCFit[12]
if mMax >= 13:
    print '  C13x=  NA; ', mCFit[13]
    print '  C13y=  NA; ', nCFit[13]
if mMax >= 14:
    print '  C14x=  NA; ', mCFit[14]
    print '  C14y=  NA; ', nCFit[14]
if mMax >= 15:
    print '  C15x=  NA; ', mCFit[15]
    print '  C15y=  NA; ', nCFit[15]
if mMax >= 16:
    print '  C16x=  NA; ', mCFit[16]
    print '  C16y=  NA; ', nCFit[16]
if mMax >= 17:
    print '  C17x=  NA; ', mCFit[17]
    print '  C17y=  NA; ', nCFit[17]
if mMax >= 18:
    print '  C18x=  NA; ', mCFit[18]
    print '  C18y=  NA; ', nCFit[18]
if mMax >= 19:
    print '  C19x=  NA; ', mCFit[19]
    print '  C19y=  NA; ', nCFit[19]
if mMax >= 20:
    print '  C20x=  NA; ', mCFit[20]
    print '  C20y=  NA; ', nCFit[20]
if mMax >= 21:
    print '  C21x=  NA; ', mCFit[21]
    print '  C21y=  NA; ', nCFit[21]
if mMax >= 22:
    print '  C22x=  NA; ', mCFit[22]
    print '  C22y=  NA; ', nCFit[22]
if mMax >= 23:
    print '  C23x=  NA; ', mCFit[23]
    print '  C23y=  NA; ', nCFit[23]
if mMax >= 24:
    print '  C24x=  NA; ', mCFit[24]
    print '  C24y=  NA; ', nCFit[24]
if mMax >= 25:
    print '  C25x=  NA; ', mCFit[25]
    print '  C25y=  NA; ', nCFit[25]
if mMax >= 26:
    print '  C26x=  NA; ', mCFit[26]
    print '  C26y=  NA; ', nCFit[26]
if mMax >= 27:
    print '  C27x=  NA; ', mCFit[27]
    print '  C27y=  NA; ', nCFit[27]
if mMax >= 28:
    print '  C28x=  NA; ', mCFit[28]
    print '  C28y=  NA; ', nCFit[28]
if mMax >= 29:
    print '  C29x=  NA; ', mCFit[29]
    print '  C29y=  NA; ', nCFit[29]
if mMax >= 30:
    print '  C30x=  NA; ', mCFit[30]
    print '  C30y=  NA; ', nCFit[30]
if mMax >= 31:
    print '  C31x=  NA; ', mCFit[31]
    print '  C31y=  NA; ', nCFit[31]
if mMax >= 32:
    print '  C32x=  NA; ', mCFit[32]
    print '  C32y=  NA; ', nCFit[32]
if mMax >= 33:
    print '  C33x=  NA; ', mCFit[33]
    print '  C33y=  NA; ', nCFit[33]
if mMax >= 34:
    print '  C34x=  NA; ', mCFit[34]
    print '  C34y=  NA; ', nCFit[34]
if mMax >= 35:
    print '  C35x=  NA; ', mCFit[35]
    print '  C35y=  NA; ', nCFit[35]
if mMax >= 36:
    print '  C36x=  NA; ', mCFit[36]
    print '  C36y=  NA; ', nCFit[36]
if mMax >= 37:
    print '  C37x=  NA; ', mCFit[37]
    print '  C37y=  NA; ', nCFit[37]
if mMax >= 38:
    print '  C38x=  NA; ', mCFit[38]
    print '  C38y=  NA; ', nCFit[38]
if mMax >= 39:
    print '  C39x=  NA; ', mCFit[39]
    print '  C39y=  NA; ', nCFit[39]
if mMax >= 40:
    print '  C40x=  NA; ', mCFit[40]
    print '  C40y=  NA; ', nCFit[40]

# load up the fitted electric field at all grid points
hS1.setWaistX(wxFit)
hS1.setWaistY(wxFit)
hS1.setMCoef(mCFit)
hS1.setNCoef(nCFit)

Ex1 = np.reshape(hS1.evaluateEx(
                 np.reshape(xGrid,nCells),
                 np.reshape(yGrid,nCells), 0., 0.),
                 (numPts, numPts))

hS2.setWaistX(wxFit)
hS2.setWaistY(wxFit)
hS2.setMCoef(nCFit)
hS2.setNCoef(mCFit)

Ex2 = np.reshape(hS2.evaluateEx(
                 np.reshape(xGrid,nCells),
                 np.reshape(yGrid,nCells), 0., 0.),
                 (numPts, numPts))

ExFit = Ex1 + Ex2

# plot the fitted transverse field profile
plt.figure(2)
cs2 = plt.contourf(xGrid, yGrid, ExFit, vLevels)
plt.colorbar(cs2)
plt.axis([xMin, xMax, yMin, yMax])
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('x-section #2: Result of the least squares fit')

# plot the transverse profile of the difference
plt.figure(3)
cs3 = plt.contourf(xGrid, yGrid, ExFit-ExGrid, ncLevels)
plt.colorbar(cs3)
plt.axis([xMin, xMax, yMin, yMax])
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('x-section #2: Absolute differences in Ex')

plt.show()
