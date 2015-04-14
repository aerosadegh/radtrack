#
#Test executable #03 for the ParticleBeam6D class.
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
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
mySpace = myBunch.getDistribution6D()

print ' '
print ' Some info regarding the beam distribution --'
print ' numParticles = ', mySpace.getPhaseSpace6D().getNumParticles()

print ' '
print ' The specified Twiss parameters are:'
print 'X: a/b/e = ', alphaX, betaX, emitX
print 'Y: a/b/e = ', alpha,  betaY, emitY
print 'Z: a/b/e = ', alfaZT, beta, emittance

myBunch.calcTwissParams6D()
twissX = myBunch.getTwissParamsByName2D('twissX')
twissY = myBunch.getTwissParamsByName2D('twissY')
twissZ = myBunch.getTwissParamsByName2D('twissZ')

print ' '
print 'Here are the resulting x, y & z Twiss parameters:'
print 'x:  ', twissX.getAlphaRMS(), twissX.getBetaRMS(), twissX.getEmitRMS()
print 'y:  ', twissY.getAlphaRMS(), twissY.getBetaRMS(), twissY.getEmitRMS()
print 'z:  ', twissZ.getAlphaRMS(), twissZ.getBetaRMS(), twissZ.getEmitRMS()
