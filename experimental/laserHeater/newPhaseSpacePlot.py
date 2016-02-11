"""
Based on the file: laserHeaterBenchmark10Mode.py

Added a phase space plot.  D. Bruhwiler, 2015-02-05

moduleauthor:: Stephen Webb <swebb@radiasoft.net>
Copyright (c) 2013-2016 RadiaBeam Technologies LLC and RadiaSoft LLC. All rights reserved
"""

__author__ = 'Stephen Webb, David Bruhwiler'
__copyright__ = "Copyright &copy RadiaBeam Technologies and RadiaSoft 2013-2016, all rights reserved"
__version__ = "1.0"
__email__ = "swebb@radiasoft.net"

print ' '
print 'Testing laser heater numerics... '
print ' '

from radtrack.ptclmovers.RbLaserHeaterIntegrator import RbLaserHeaterIntegrator as integrator
from radtrack.fields.RbIdealPlanarUndulator import RbIdealPlanarUndulator as undulator
from radtrack.fields.RbGaussHermiteMN2 import RbGaussHermiteMN as laser
import radtrack.bunch.RbParticleBeam6D as beam

import numpy as np
from scipy import constants as consts
from scipy import stats
from scipy.special import jn
from matplotlib import pyplot as plt
import matplotlib as mpl
import math

tol = 1.e-8

# Beam parameters
gamma0 = 264.188

# Undulator parameters
lambdaw = 0.05 # [m]
kw = 2.*math.pi/lambdaw
B0      = 0.33 # [T]
interaction_length  = .5  # [m]

# Laser parameters
laserP  = 1.2e6   # [Watts]
lambda0 = 783.3e-9 # [m]
k0 = 2.*math.pi/lambda0
lambdaR = 5.5     # [m]  Rayleigh range...?
pol     = [1., 0., 0.]

Kw = consts.e*B0*lambdaw/(consts.m_e*consts.c*2*consts.pi)
resonantLambda = lambdaw*(1 + Kw**2/2)/(2.*gamma0**2)

print '!------'
print ' Simulating laser heater with laser wavelength', lambda0*10**9, 'nm'
print '    and undulator resonant wavelength', resonantLambda*10**9, 'nm'
print ' '

#
# Derived quantities below this line -- do not modify !!
#

# Laser field
waistX = np.sqrt(lambdaR * lambda0/np.pi)
waistY = waistX
sigmaR = np.sqrt(waistX**2 + waistY**2)
E0 = np.sqrt(laserP/(np.pi*(sigmaR**2)*consts.epsilon_0*consts.c)) #
pol = E0*np.array(pol) #E0 in Volts/meter

wRotAngle = 0.

# Specify the Gauss-Hermite coefficients
hCoeffs = np.array([[0., 1., 1., 1., 0., 1.], [0., 0., 0., 0., 0., 0.]])

# Instantiate the laser field
mylaserfield = laser(pol, lambda0, waistX, waistY, wRotAngle, hCoeffs)

# Undulator field
myundulatorfield = undulator(B0, lambdaw)

# Integrator
myintegrator = integrator(mylaserfield, myundulatorfield)
zInit  = -0.5*interaction_length
zFinal = 0.5*interaction_length

num_ptcls = 100
nAngle = 10
nRadii = num_ptcls
radius = [0.]*num_ptcls
slopeNum = [0.]*num_ptcls
slopeTry = [0.]*num_ptcls
expectedE = [0.]*num_ptcls
radCount = 0
angCount = 0

myBunch = beam.RbParticleBeam6D(num_ptcls)

beta0 = math.sqrt(1.-1./gamma0**2)
massEV = 0.511e+6
pzEV = beta0*gamma0 / massEV
myBunch.setDesignMomentumEV(pzEV)

alphaX = 0.0
betaX = 1.
emitX = 1.e-06
myBunch.setTwissParamsByName2D(alphaX, betaX, emitX, 'twissX')

alphaY = 0.
betaY = 1.
emitY = 1.e-06
myBunch.setTwissParamsByName2D(alphaY, betaY, emitY, 'twissY')

alfaZT = 0.
betaZ  = 10.
emittance = 1.e-06
myBunch.setTwissParamsByName2D(alfaZT, betaZ, emittance, 'twissZ')

myDist = myBunch.getDistribution6D()
myDist.setDistributionType('gaussian')
myDist.setMaxRmsFactor(3.)

myBunch.makeParticlePhaseSpace6D()
mySpace = myBunch.getDistribution6D()
myArray = mySpace.getPhaseSpace6D().getArray6D()

for idx in range(num_ptcls):

    x0  = myArray[0,idx]
    px0 = myArray[1,idx]
#    px0 = 0.
    y0  = myArray[2,idx]
    py0 = myArray[3,idx]
#    py0 = 0.
    phi0 = ((kw + k0)*myArray[4,idx])%(2.*math.pi)
    dp_over_p0 = myArray[4,idx]

    r = np.sqrt(x0**2 + y0**2)
    initPtcl = np.array([x0, px0, y0, py0, phi0, gamma0])
    expectedE[idx]=mylaserfield.getA(initPtcl, zInit)*consts.c*2.*np.pi/lambda0

    soln, zrange = myintegrator.integrate(zInit, zFinal, initPtcl)

    gamma = np.zeros(zrange.shape[0])
    gamma[:] = (soln[:,5]-gamma0)
    theta = np.zeros(zrange.shape[0])
    theta[:] = soln[:,4] #%(2*np.pi)

    slope, intercept, rvalue, pvalue, stderr = stats.linregress(zrange, gamma)

    # Theoretical result from Huang, et al. LCLS laser heater paper (2004)
    P0 = 8.7e9 # I_A m c^2/e = 8.7 GW
    expectedSlope = consts.e/(consts.m_e*consts.c**2)
    expectedSlope *= Kw
    expectedSlope /= gamma0
    A_JJ = jn(0, Kw**2/(4.+2.*Kw**2)) - jn(1, Kw**2/(4.+2.*Kw**2))
    expectedSlope *= A_JJ
    expectedSlope *= expectedE[idx]
    slopeTry[idx] = expectedSlope
    radius[idx] = r
    slopeNum[idx] = slope

    radCount += 1

plt.plot(radius, slopeNum, '-.', linewidth=2, c='b', label='numerical')
plt.plot(radius, slopeTry, 'x', c='r', label='theory', alpha=0.75)
plt.title(r'$u_{1,0}$ Hermite-Gauss Mode')
plt.xlabel(r'$r$ [m]')
plt.ylabel(r'$\Delta \gamma/\ell$ [m${}^{-1}$]')
plt.legend()
plt.tight_layout()
plt.savefig('hermiteGaussBenchmark.png')

plt.plot(radius, slopeNum, '-.', linewidth=2, c='b', label='numerical')
plt.plot(radius, slopeTry, 'x', c='r', label='theory', alpha=0.75)
plt.title(r'$u_{1,0}$ Hermite-Gauss Mode')
plt.xlabel(r'$r$ [m]')
plt.ylabel(r'$\Delta \gamma/\ell$ [m${}^{-1}$]')
plt.legend()
plt.tight_layout()
plt.savefig('hg_InitialPhaseSpace.png')

plt.show()
