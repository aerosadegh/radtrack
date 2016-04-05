#
#Test executable #04 for the ParticleBeam6D class.
#
# Copyright (c) 2016 RadiaBeam Technologies. All rights reserved
#
# RadiaBeam imports
import radtrack.bunch.RbParticleBeam6D as beam

# Specify the desired number of particles
numpoints = 4000

# Specify the average beam energy [eV]
energy = 2.5e+6

# Exercise some of the class methods
print ' '
print ' About to instantiate a particle beam --'

myBunch = beam.RbParticleBeam6D(numpoints)

alphaX = 0.0
betaX = 15.
emitX = 3.3e-06
myBunch.setTwissParamsByName2D(alphaX, betaX, emitX, 'twissX')

alpha = 4.6
betaY = 0.0012
emitY = 1.7e-06
myBunch.setTwissParamsByName2D(alpha, betaY, emitY, 'twissY')

alfaZT = -3.3
beta   = 9.9
emittance = 0.58e-06
myBunch.setTwissParamsByName2D(alfaZT, beta, emittance, 'twissZ')

myDist = myBunch.getDistribution6D()
myDist.setDistributionType('gaussian')
myDist.setMaxRmsFactor(3.)

myBunch.makeParticlePhaseSpace6D()
myDistribution = myBunch.getDistribution6D()

print ' '
print ' Some info regarding the beam distribution --'
print ' numParticles = ', myDistribution.getPhaseSpace6D().getNumParticles()

myAverages = myDistribution.calcAverages6D()

print ' '
print 'Here are the average values of the distribution:'
print '<x> :  ', myAverages[0]
print '<xp>:  ', myAverages[1]
print '<y> :  ', myAverages[2]
print '<yp>:  ', myAverages[3]
print '<t> :  ', myAverages[4]
print '<dp>:  ', myAverages[5]

myRmsValues = myDistribution.calcRmsValues6D()

print ' '
print 'Here are the RMS values of the distribution:'
print '<x> :  ', myRmsValues[0]
print '<xp>:  ', myRmsValues[1]
print '<y> :  ', myRmsValues[2]
print '<yp>:  ', myRmsValues[3]
print '<t> :  ', myRmsValues[4]
print '<dp>:  ', myRmsValues[5]
