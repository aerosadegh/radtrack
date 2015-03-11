# 
# Test executable to exercise ODE for drifting beam
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#
# scipy imports
import numpy as np
from scipy.integrate import odeint

# RadiaBeam imports
import radtrack.bunch.RbParticleBeam6D as beam
import radtrack.plot.RbPlotPhaseSpace6D as plotps

# Calculate time-derivatives for a beam in free space
def driftingBeamGradient(ptcl_data, t_data):
    # forces are zero for a drifting beam 
    derivs = np.zeros(ptcl_data.size)

    # derivatives of position are the momentum
    nptcl = ptcl_data.size / 6
    for iLoop in range(nptcl):
        derivs[iLoop        ] = ptcl_data[iLoop+  nptcl]
        derivs[iLoop+2*nptcl] = ptcl_data[iLoop+3*nptcl]
        derivs[iLoop+4*nptcl] = ptcl_data[iLoop+5*nptcl]

    return derivs

# Instantiate the bunch (no particles yet)
numpoints = 200
myBunch = beam.RbParticleBeam6D(numpoints) 

# Specify the Twiss parameters 
alphaX = 0.0 
betaX = 15. 
emitX = 3.3e-07 
myBunch.setTwissParamsByName2D(alphaX, betaX, emitX, 'twissX') 
 
alpha = 4.6 
betaY = 0.012 
emitY = 1.7e-06 
myBunch.setTwissParamsByName2D(alpha, betaY, emitY, 'twissY') 
 
alfaZT = -3.3 
beta   = 0.9 
emittance = 0.58e-06 
myBunch.setTwissParamsByName2D(alfaZT, beta, emittance, 'twissZ') 

# Specify the distribution type 
myDist = myBunch.getDistribution6D() 
myDist.setDistributionType('gaussian') 
myDist.setMaxRmsFactor(3.)

# Generate the particle data 
myBunch.makeParticlePhaseSpace6D()

# Grab a pointer to the phase space object (particle data)
mySpace = myBunch.getPhaseSpace6D()

# Instantiate a bunch plotting object
myPlotter = plotps.RbPlotPhaseSpace6D(mySpace)

# Generate an x-px scatter plot
myPlotter.setTitle('Initial x-px projection')
myPlotter.plotData6D(0,1)

# Drift the particles, using built-in NumPy ODE integrator
myArray = mySpace.getArray6D()
flatArray = np.reshape(myArray, myArray.size)
timeArray = np.array([0., 100.])
trajectoryMatrix = odeint(driftingBeamGradient, flatArray, timeArray, printmessg=True)
newArray = np.reshape(trajectoryMatrix[-1,:], [6,numpoints])

# We have to put the modified particle data into the plotting object
myPlotter.setData6D(newArray)

# Generate an x-px scatter plot (after the drift)
myPlotter.setTitle('Final x-px projection')
myPlotter.plotData6D(0,1)

# Generate a y-pz scatter plot (after the drift)
myPlotter.setTitle('Final y-pz projection')
myPlotter.plotData6D(2,5)

# Render the plots
myPlotter.showPlots()

