# 
# Test executable #3 to exercise the Gauss-Hermite class
# Here, we fit a Gauss-Hermite expansion to an arbitrary profile.
# The SciPy least squares method is used.
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#
# python imports
import math

# SciPy imports
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PyQt4'
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

# RadiaBeam imports
import radtrack.fields.RbGaussHermiteMN as hermite

# ---------------------------------------------------------
# Make sure the residual() method has access to necessary
#   'global' data:
global mMax, nMax, numFuncCalls, hermiteSeries

# Specify the central laser wavelength
lambda0 = 10.e-06

# Need a place holder for the waist size
w0 = 10.*lambda0

# Define the maximum order(s) of the Hermite expansion
mMax = 20    # horizontal
nMax = mMax  # vertical

# Create an instance of the Hermite expansion class
hermiteSeries = hermite.RbGaussHermiteMN(lambda0,w0,w0,0.)

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

# Define the rectangular region of non-zero field
xLeft  = 0.8*xMin
xRight = 0.4*xMax
yLeft  = 0.1*yMin
yRight = 0.5*yMax

xMid = 0.5 * (xRight + xLeft)
xDif = 0.5 * (xRight - xLeft)   
yMid = 0.5 * (yRight + yLeft)   
yDif = 0.5 * (yRight - yLeft)   

# Create transverse field profile (#2 quadratic square)
ExGrid = np.zeros((numX, numY))
phi2   = math.pi/4.
maxVal = 0.
for iLoop in range(numX):
    for jLoop in range(numY):
        xArg =  xArr[iLoop]*math.cos(phi2) + yArr[jLoop]*math.sin(phi2)
        yArg = -xArr[iLoop]*math.sin(phi2) + yArr[jLoop]*math.cos(phi2)
        if (xArg>=xLeft) and (xArg<=xRight) and (yArg>=yLeft) and (yArg<=yRight): 
            ExGrid[iLoop, jLoop] = (1.-((xArg-xMid)/xDif)**2) * (1.-((yArg-yMid)/yDif)**2)
            maxVal = max(ExGrid[iLoop, jLoop], maxVal)

# Divide out the maximum value
ExGrid /= maxVal

# Calculate residuals for the least squares analysis
# params - array of fitting parameters
numFuncCalls = 0
def residuals(params, e, x, y):
    global mMax, nMax, numFuncCalls, hermiteSeries

    hermiteSeries.setWaistX(params[0])
    hermiteSeries.setWaistY(params[1])
    hermiteSeries.setXShift(params[2])
    hermiteSeries.setYShift(params[3])
    hermiteSeries.setWRotAngle(params[4])

    hCoefs = np.zeros(mMax+1)
    for ii in range(mMax/2+1):
        hCoefs[2*ii] = params[5+ii]
    hermiteSeries.setMCoef(hCoefs)

    vCoefs = np.zeros(nMax+1)
    for ii in range(nMax/2+1):
        vCoefs[2*ii] = params[6+mMax/2+ii]
    hermiteSeries.setNCoef(vCoefs)

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
plt.title('x-section #2: quadratic square (sharp cut-off)')

# choose initial guesses for all fitting parameters
# also, specify the scale of variations for each
paramGuess = np.zeros(mMax/2+nMax/2+7)
paramGuess[0] = 1.2*w0              # horizontal waist
paramGuess[1] = 0.9*w0              #   vertical waist
paramGuess[2] = 0.                  # horizontal shift
paramGuess[3] = 0.                  #   vertical shift
paramGuess[4] = 0.                  # rotation angle
paramGuess[5] = 1.0                 # 0th horiz. coeff
for ii in range(mMax/2):
    paramGuess[6+ii] = 1.e-5        # other horiz. coeff's
paramGuess[mMax/2+6] = 1.0          # 0th vertical coeff
for ii in range(nMax/2):
    paramGuess[mMax/2+7+ii] = 1.e-5 # other vertical coeff's

# invoke the least squares algorithm
result = leastsq(residuals, paramGuess,             \
                 args=(np.reshape(ExGrid,nCells),   \
                       np.reshape(xGrid,nCells),    \
                       np.reshape(yGrid,nCells)),   \
                 full_output=True, ftol=1e-3,       \
                 maxfev=400)

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
wyFit = parFit[1]
xsFit = parFit[2]
ysFit = parFit[3]
tmpPhi = parFit[4]
phiFit = tmpPhi - 2.*math.pi*int(0.5*tmpPhi/math.pi)
if phiFit > 2.*math.pi: phiFit -= 2.*math.pi
if phiFit < 0.: phiFit += 2.*math.pi
mCFit = np.zeros(mMax+1)
for ii in range(mMax/2+1):
    mCFit[2*ii] = parFit[5+ii]
nCFit = np.zeros(nMax+1)
for ii in range(nMax/2+1):
    nCFit[2*ii] = parFit[mMax/2+6+ii]

# check the results
print ' '
print 'The least squares minimimization has completed:'
print '  wx  =  NA; ', wxFit
print '  wy  =  NA; ', wyFit
print '  xs  =  NA; ', xsFit
print '  ys  =  NA; ', ysFit
print '  phi = ', phi2, '; ', phiFit
print '  C0x =  NA; ', mCFit[0]
print '  C0y =  NA; ', nCFit[0]
if mMax >= 2:
    print '  C2x =  NA; ', mCFit[2]
    print '  C2y =  NA; ', nCFit[2]
if mMax >= 4:
    print '  C4x =  NA; ', mCFit[4]
    print '  C4y =  NA; ', nCFit[4]
if mMax >= 6:
    print '  C6x =  NA; ', mCFit[6]
    print '  C6y =  NA; ', nCFit[6]
if mMax >= 8:
    print '  C8x =  NA; ', mCFit[8]
    print '  C8y =  NA; ', nCFit[8]
if mMax >= 10:
    print '  C10x=  NA; ', mCFit[10]
    print '  C10y=  NA; ', nCFit[10]
if mMax >= 12:
    print '  C12x=  NA; ', mCFit[12]
    print '  C12y=  NA; ', nCFit[12]
if mMax >= 14:
    print '  C14x=  NA; ', mCFit[14]
    print '  C14y=  NA; ', nCFit[14]
if mMax >= 16:
    print '  C16x=  NA; ', mCFit[16]
    print '  C16y=  NA; ', nCFit[16]
if mMax >= 18:
    print '  C18x=  NA; ', mCFit[18]
    print '  C18y=  NA; ', nCFit[18]
if mMax >= 20:
    print '  C20x=  NA; ', mCFit[20]
    print '  C20y=  NA; ', nCFit[20]
if mMax >= 22:
    print '  C22x=  NA; ', mCFit[22]
    print '  C22y=  NA; ', nCFit[22]
if mMax >= 24:
    print '  C24x=  NA; ', mCFit[24]
    print '  C24y=  NA; ', nCFit[24]
if mMax >= 26:
    print '  C26x=  NA; ', mCFit[26]
    print '  C26y=  NA; ', nCFit[26]
if mMax >= 28:
    print '  C28x=  NA; ', mCFit[28]
    print '  C28y=  NA; ', nCFit[28]
if mMax >= 30:
    print '  C30x=  NA; ', mCFit[30]
    print '  C30y=  NA; ', nCFit[30]

# load up the fitted electric field at all grid points
hermiteSeries.setWaistX(wxFit)
hermiteSeries.setWaistY(wyFit)
hermiteSeries.setXShift(xsFit)
hermiteSeries.setYShift(ysFit)
hermiteSeries.setWRotAngle(phiFit)
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
