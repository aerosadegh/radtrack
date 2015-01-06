#
# Test executable #02 for the ParticleBeam6D class.
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

#import sys
#sys.path.append("..")

# RadiaBeam imports
import RadTrack.bunch.RbPhaseSpace6D as ps6d
import RadTrack.bunch.RbDistribution6D as dist6d
import RadTrack.statistics.RbStatistics6D as st6d

# Specify the desired number of particles
numpoints = 50
myArray6D = ps6d.RbPhaseSpace6D(numpoints)

# Exercise some of the class methods
myDist = dist6d.RbDistribution6D(myArray6D)
myDist.setMaxRmsFactor(3.)
myStatObj = st6d.RbStatistics6D(myDist.getPhaseSpace6D())

# Let's generate an initial (noisy) particle distribution...
print ' '
print ' Generating the distribution...'
myDist.initialPhaseSpace6D()
print ' numParticles = ', myArray6D.getNumParticles()

# Calculate the averages before cleaning
if 1:
    averages = myStatObj.calcAverages6D()
    print ' '
    for nLoop in range(6):
        print ' averages[', nLoop, '] = ', averages[nLoop]

# Calculate the RMS values before cleaning
if 1:
    rmsArray = myStatObj.calcRmsValues6D()
    print ' '
    for nLoop in range(6):
        print ' rmsArray[', nLoop, '] = ', rmsArray[nLoop]

# Calculate the phase space correlations before cleaning
if 1:
    corr6d = myStatObj.calcCorrelations6D()
    print ' '
    for nLoop in range(6):
        print ' corr6d[', nLoop, '] = ', corr6d[nLoop]

# Now cleanup the distribution
if 1:
    print ' '
    print 'Cleaning up the distribution...'
    if 1:
        myDist.cleanPhaseSpace6D()
    if 0:
        myStatObj.subtractAverages6D()
        myStatObj.normalizeRmsValues6D()
        myStatObj.eraseCorrelations6D()
        myStatObj.subtractAverages6D()
        myStatObj.normalizeRmsValues6D()
    
# Calculate the averages after cleaning
if 1:
    averages = myStatObj.calcAverages6D()
    print ' '
    for nLoop in range(6):
        print ' averages[', nLoop, '] = ', averages[nLoop]

# Calculate the RMS values after cleaning
if 1:
    rmsArray = myStatObj.calcRmsValues6D()
    print ' '
    for nLoop in range(6):
        print ' rmsArray[', nLoop, '] = ', rmsArray[nLoop]

# Calculate the phase space correlations after cleaning
if 1:
    corr6d = myStatObj.calcCorrelations6D()
    print ' '
    for nLoop in range(6):
        print ' corr6d[', nLoop, '] = ', corr6d[nLoop]


