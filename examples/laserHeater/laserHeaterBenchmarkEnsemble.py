"""
Test for the laser heater infrastructure using the Gauss-Hermite laser mode
and a planar undulator. This test just checks a gaussian mode with the
parameters of the LCLS laser heater.

moduleauthor:: Stephen Webb <swebb@radiasoft.net>
Copyright (c) 2014 RadiaBeam Technologies. All rights reserved
"""

__author__ = 'Stephen Webb, David Bruhwiler'
__copyright__ = "Copyright &copy RadiaBeam Technologies 2013, all rights " \
                "reserved"
__version__ = "1.0"
__email__ = "swebb@radiasoft.net"

import time

t0 = time.time()

print 'testing laser heater system... '

from radtrack.ptclmovers.RbLaserHeaterIntegrator\
    import RbLaserHeaterIntegrator as integrator
from radtrack.fields.RbIdealPlanarUndulator\
    import RbIdealPlanarUndulator as undulator
from radtrack.fields.RbGaussHermiteMN2\
    import RbGaussHermiteMN as laser

import random
import numpy as np
from scipy import constants as consts
from scipy import stats
from scipy.special import jn
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rc('text', usetex=True)

tol = 1.e-8

# Beam parameters
gamma0 = 264.188
sigmaGamma = 3/510.998 #3 keV energy spread

# Undulator parameters
lambdaw = 0.05 # [m]
B0      = 0.33 # [T]
length  = .5  # [m]

# Laser parameters
laserP  = 1.2e6   # [Watts]
lambda0 = 783.3e-9 # [m]
lambdaR = .5     # [m]
pol     = [1., 0., 0.]

Kw = consts.e*B0*lambdaw/(consts.m_e*consts.c*2*consts.pi)
resonantLambda = lambdaw*(1 + Kw**2/2)/(2.*gamma0**2)

#
# Derived quantities below this line
# Do not modify!
#


# Laser field
waistX = np.sqrt(lambdaR * lambda0/np.pi)
waistY = waistX
sigmaR = np.sqrt(waistX**2 + waistY**2)
E0 = np.sqrt(laserP/(np.pi*(sigmaR**2)*consts.epsilon_0*consts.c)) #
pol = E0*np.array(pol) #E0 in Volts/meter

wRotAngle = 0.
# Pure Gaussian beam
hCoeffs = np.array([[0., 1.], [0., 0.]])
mylaserfield = laser(pol, lambda0, waistX, waistY, wRotAngle, hCoeffs)

# Undulator field
myundulatorfield = undulator(B0, lambdaw)

print '!------'
print ' Simulating laser heater with laser wavelength', lambda0*10**9, 'nm'
print 'and undulator resonant wavelength', resonantLambda*10**9, 'nm'
print 'Laser has Rayleigh range', lambdaR, 'm and waist size', waistX, 'm'

# Integrator
myintegrator = integrator(mylaserfield, myundulatorfield)
zInit  = -0.5*length
zFinal = 0.5*length

# Test the for-loop

nTests = 25000
gammasf = []
gammasi = []
ys = []
xs = []

# perfectly matched bunch
sigmaX = 0.00019 #190 microns
sigmaY = sigmaX

print 'gamma0 =', gamma0
print 'sigma =', sigmaGamma
# Uniform distribution in the initial angle

# Test the particles and bin up a histogram in the energy modulation
for idx in range(nTests):
    gammai = random.gauss(gamma0,sigmaGamma)
 #   gammasi.append((gammai-gamma0)*510.998)
    initPtcl = np.array([random.gauss(0., sigmaX), 0.,
                         random.gauss(0., sigmaY), 0.,
                         (1.-2.*random.random()*consts.pi), gammai])
    soln, zrange = myintegrator.integrate(zInit, zFinal, initPtcl)

    xf, pxf, yf, pyf, thetaf, gammaf = soln[-1]

  #  gammasf.append((gammaf-gamma0)*510.998)
   # ys.append(yf)
    #xs.append(xf)

#n, bins, patches = plt.hist(gammasi, 20, label='initial', normed=1)
#n, bins, patches = plt.hist(gammasf, 50, label='final', alpha=0.5, normed=1)
#plt.xlabel(r'$\Delta \gamma m c^2$[keV]')
#plt.ylabel(r'$V(\Delta \gamma m c^2)$')
#plt.legend()
#plt.tight_layout()
#plt.savefig('LHEnergySpread.png')
#plt.show()
#plt.clf()

#plt.scatter(ys, gammasf, s=2)
#plt.xlabel(r'$y$ [m]')
#plt.ylabel(r'$\Delta \gamma m c^2$ [keV]')
#plt.tight_layout()
#plt.savefig('yVersusE.png')
#plt.show()

#plt.scatter(xs, gammasf, s=2)
#plt.xlabel(r'$x$ [m]')
#plt.ylabel(r'$\Delta \gamma m c^2$ [keV]')
#plt.tight_layout()
#plt.savefig('xVersusE.png')
#plt.show()

tf = time.time()

print 'computed rms energy spread is', np.std(gammasf), 'keV'

print 'Laser heater simulation took', tf-t0, 'sec.'