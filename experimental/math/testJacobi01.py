#
# Test executable #01 for the Jacobi eigenvalue solver
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#
# SciPy imports
import scipy as sp

# RadiaBeam imports
import radtrack.statistics.RbStatistics6D as st6d
import radtrack.bunch.RbPhaseSpace6D as ps6d

# Exercise some of the class methods
myPS6D = ps6d.RbPhaseSpace6D(27)
sigmaM = sp.mat('[1.10  0.20 -0.10  0.30  0.15 -0.20; -0.10  0.95  0.30 -0.22  0.11  0.25; -0.10 -0.31  1.01  0.00 -0.01  0.23; 0.10  0.00 -0.30  1.22 -0.17 -0.05; -0.10 -0.19  0.10 -0.31  0.99  0.02; 0.12 -0.11  0.31 -0.01  0.00  1.17]')

eigVals, eigVecs = st6d.jacobiEigenSolver6D(sigmaM)

print ' '
print 'eigVals = ', eigVals
for iLoop in range(6):
	print 'eigVecs[', iLoop, ',:] = ', eigVecs[iLoop,:]
