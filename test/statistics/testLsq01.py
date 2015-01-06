# 
# Test executable #1 to exercise the SciPy least squares method.
# 
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#

# SciPy imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

# number of data points
nPoints = 300

# Calculate residuals for the least squares analysis
# params - array of fitting parameters
# coords - array of coordinates
# efield - resulting electric field
def residuals(params, efield, coords):
    eCalc = np.zeros(nPoints)
    eCalc = params[0] + params[1] * coords + params[2] * coords**2 
    err = np.zeros(nPoints)
    err = efield-eCalc
    return err

# choose initial guesses for all fitting parameters
p0 = np.zeros(3)

# create positions and values
x = np.zeros(nPoints)
E = np.zeros(nPoints)
for iLoop in range(nPoints):
    x[iLoop] = iLoop
    E[iLoop] = 3.1 - 2.9*x[iLoop] + 0.01*x[iLoop]**2

# invoke the least squares algorithm
par_lsq = leastsq(residuals, p0, args=(E, x))
print par_lsq

plt.show()
