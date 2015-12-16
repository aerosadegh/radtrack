#
# Test executable #02 for the ParticleBeam6D class.
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

#import sys
#sys.path.append("..")

# RadiaBeam imports
import radtrack.bunch.RbPhaseSpace6D as ps6d
import radtrack.bunch.RbDistribution6D as dist6d
import radtrack.statistics.RbStatistics6D as st6d

# Specify the desired number of particles
numpoints = 50
myArray6D = ps6d.RbPhaseSpace6D(numpoints)

# Exercise some of the class methods
myDist = dist6d.RbDistribution6D(myArray6D)
myDist.setMaxRmsFactor(3.)

# Let's generate an initial (noisy) particle distribution...
print ' '
print ' Generating the distribution...'
myDist.initialPhaseSpace6D()
print ' numParticles = ', myArray6D.getNumParticles()

# Calculate the averages before cleaning
if 1:
    averages = st6d.calcAverages6D(myDist.getPhaseSpace6D())
    print ' '
    for nLoop in range(6):
        print ' averages[', nLoop, '] = ', averages[nLoop]

# Calculate the RMS values before cleaning
if 1:
    rmsArray = st6d.calcRmsValues6D(myDist.getPhaseSpace6D())
    print ' '
    for nLoop in range(6):
        print ' rmsArray[', nLoop, '] = ', rmsArray[nLoop]

# Calculate the phase space correlations before cleaning
if 1:
    corr6d = st6d.calcCorrelations6D(myDist.getPhaseSpace6D())
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
        st6d.subtractAverages6D(myDist.getPhaseSpace6D())
        st6d.normalizeRmsValues6D(myDist.getPhaseSpace6D())
        st6d.eraseCorrelations6D(myDist.getPhaseSpace6D())
        st6d.subtractAverages6D(myDist.getPhaseSpace6D())
        st6d.normalizeRmsValues6D(myDist.getPhaseSpace6D())
    
# Calculate the averages after cleaning
if 1:
    averages = st6d.calcAverages6D(myDist.getPhaseSpace6D())
    print ' '
    for nLoop in range(6):
        print ' averages[', nLoop, '] = ', averages[nLoop]

# Calculate the RMS values after cleaning
if 1:
    rmsArray = st6d.calcRmsValues6D(myDist.getPhaseSpace6D())
    print ' '
    for nLoop in range(6):
        print ' rmsArray[', nLoop, '] = ', rmsArray[nLoop]

# Calculate the phase space correlations after cleaning
if 1:
    corr6d = st6d.calcCorrelations6D(myDist.getPhaseSpace6D())
    print ' '
    for nLoop in range(6):
        print ' corr6d[', nLoop, '] = ', corr6d[nLoop]


