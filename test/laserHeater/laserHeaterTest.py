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

failed = False

try:
    print 'testing laser heater system... '

    from RadTrack.ptclmovers.RbLaserHeaterIntegrator\
        import RbLaserHeaterIntegrator as integrator
    from RadTrack.fields.RbIdealPlanarUndulator\
        import RbIdealPlanarUndulator as undulator
    from RadTrack.fields.RbGaussHermiteMN2\
        import RbGaussHermiteMN as laser

    import numpy as np
    from scipy import constants as consts
    from scipy import stats
    from scipy.special import jn
    from matplotlib import pyplot as plt
    import matplotlib as mpl
    mpl.rc('font',**{'family':'serif','serif':['Palatino']})
    mpl.rc('text', usetex=True)

    tol = 1.e-8

    # Beam parameters
    gamma0 = 264.188

    # Undulator parameters
    lambdaw = 0.05 # [m]
    B0      = 0.33 # [T]
    length  = .5  # [m]

    # Laser parameters
    laserP  = 1.2e6   # [Watts]
    lambda0 = 783.3e-9 # [m]
    lambdaR = 5.5     # [m]
    pol     = [1., 0., 0.]

    Kw = consts.e*B0*lambdaw/(consts.m_e*consts.c*2*consts.pi)
    resonantLambda = lambdaw*(1 + Kw**2/2)/(2.*gamma0**2)

    print '!------'
    print ' Simulating laser heater with laser wavelength', lambda0*10**9, 'nm'
    print 'and undulator resonant wavelength', resonantLambda*10**9, 'nm'

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
    hCoeffs = np.array([[1.]])
    mylaserfield = laser(pol, lambda0, waistX, waistY, wRotAngle, hCoeffs)

    # Undulator field
    myundulatorfield = undulator(B0, lambdaw)

    # Integrator
    myintegrator = integrator(mylaserfield, myundulatorfield)
    zInit  = -0.5*length
    zFinal = 0.5*length

    # Test particle
    x0 = 1.*waistX
    y0 = -2.1*waistY
    initPtcl = np.array([x0, 0., y0, 0.,
                         -consts.pi/2., gamma0])
    soln, zrange = myintegrator.integrate(zInit, zFinal, initPtcl)

    gamma = np.zeros(zrange.shape[0])
    gamma[:] = (soln[:,5])
    theta = np.zeros(zrange.shape[0])
    theta[:] = soln[:,4] #%(2*np.pi)

    # plt.scatter(theta, gamma) #*510.998
    # plt.xlabel(r'$\theta$')
    # plt.ylabel(r'$\Delta\gamma$')
    # plt.tight_layout()
    # plt.savefig('thetaVgamma.png')
    # plt.clf()
    # plt.plot(zrange, theta)
    # plt.xlabel(r'$z$')
    # plt.ylabel(r'$\theta$')
    # plt.tight_layout()
    # plt.savefig('thetaVz.png')
    # plt.clf()
    plt.plot(zrange, gamma) #*510.998
    plt.xlabel(r'$z$')
    plt.ylabel(r'$\Delta\gamma$')
    plt.tight_layout()
    plt.savefig('gammaVz.png')
    plt.clf()

    slope, intercept, rvalue, pvalue, stderr = stats.linregress(zrange, gamma)

    print '!~~~~~~~~'
    print 'Linear regression on gamma versus z yields a slope of', slope

    # Theoretical result from Huang, et al. LCLS laser heater paper (2004)
    P0 = 8.7e9 # I_A m c^2/e = 8.7 GW
    expectedSlope = np.sqrt(laserP/P0)
    expectedSlope *= Kw
    expectedSlope /= gamma0
    # Because 2*sigma_r^2 = w_0^2
    expectedSlope /= np.sqrt(waistX/np.sqrt(2))*np.sqrt(waistY/np.sqrt(2))
    A_JJ = jn(0, Kw**2/(4.+2.*Kw**2)) - jn(1, Kw**2/(4.+2.*Kw**2))
    expectedSlope *= A_JJ
    expectedSlope *= np.exp(-(x0**2/(waistX**2) + y0**2/(waistY**2)))

    print 'Theoretically predicted slope for gamma is', expectedSlope

    # Accepted slope, taken from simulation
    acceptedSlope = 0.000314232057721
    if (abs(slope-acceptedSlope)/acceptedSlope) > tol:
        failed = True
    if failed:
        raise Exception('laserHeaterTest has failed')

except Exception as e:
    print e
    raise

print 'Passed.'