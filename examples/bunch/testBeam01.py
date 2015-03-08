#
# Test executable #01 for the RbParticleBeam6D class.
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#
# SciPy imports
import numpy as np
import sys
sys.path.append("..")

# RadiaBeam imports
import radtrack.bunch.RbParticleBeam6D as beam
#from radtrack.bunch import RbParticleBeam6D as beam
# Exercise some of the class methods
print ' '
print ' About to instantiate a particle beam --'
numpoints = 250
energy = 100.
myBunch = beam.RbParticleBeam6D(numpoints)

# Define the Twiss parameters
print ' '
print ' About to set the Twiss parameters --'

alphaX = 0.0
betaX = 2.0
emitX = 0.99e-06
myBunch.setTwissParamsByName2D(alphaX, betaX, emitX, 'twissX')

alpha = 0.0
betaY = 1.0
emitY = 1.2e-06
myBunch.setTwissParamsByName2D(alpha, betaY, emitY, 'twissY')

alfaZT = 0.0
beta   = 0.5
emittance = 1.05e-06
myBunch.setTwissParamsByName2D(alfaZT, beta, emittance, 'twissZ')

myBunch.makeParticlePhaseSpace6D()

mySpace = myBunch.getDistribution6D()
xxArray = mySpace.getPhaseSpace6D().getArrayX()

print ' '
print ' Some info regarding the x array --'
print ' numParticles = ', mySpace.getPhaseSpace6D().getNumParticles()

for nLoop in range(numpoints):
    print ' xArray[', nLoop, '] = ', xxArray[nLoop]

print ' '
print ' Writing all arrays to a file: '
fileName = 'testBeam01'
mySpace.getPhaseSpace6D().setFileName(fileName)
mySpace.getPhaseSpace6D().writeArray()

print ' '
print ' Loading the data file: '
dataObject = np.load(fileName + '.npz')
dataObject.files
testArray6D = dataObject['a']

for nLoop in range(numpoints):
    print ' xArray[', nLoop, '] = ', testArray6D[0,nLoop]

