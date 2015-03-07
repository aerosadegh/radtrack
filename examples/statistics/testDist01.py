#
#Test executable #01 for the Distribution6D class.
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#
# scipy imports
import numpy as np

# RadiaBeam imports
import RadTrack.bunch.RbDistribution6D as dist6d
import RadTrack.bunch.RbPhaseSpace6D as ps6d

# Specify the desired number of particles
numpoints = 17
myArray6D = ps6d.RbPhaseSpace6D(numpoints)

# Exercise some of the class methods
myDist = dist6d.RbDistribution6D(myArray6D)
myDist.setDistributionType('uniform')
myDist.roundPhaseSpace6D()
testArray = myArray6D.getArrayX()

print ' '
print ' Some info regarding the x array --'
print ' numpoints    = ', numpoints
print ' numParticles = ', myArray6D.getNumParticles()
print ' array size   = ', testArray.size

for nLoop in range(numpoints):
    print ' testArray[', nLoop, '] = ', testArray[nLoop]
    
print ' '
print ' Writing all arrays to a file: '
myDist.getPhaseSpace6D().setFileName('testData')
myDist.getPhaseSpace6D().writeArray()

print ' '
print ' Loading the data file: '
dataObject = np.load('testData.npz')
dataObject.files
arrayPS = dataObject['a']

for nLoop in range(numpoints):
    print ' arrayPS[0,', nLoop, '] = ', arrayPS[0,nLoop]
