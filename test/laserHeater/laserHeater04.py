"""
Test for the laser heater infrastructure using the Gauss-Hermite laser mode
and a planar undulator. The parameters are fixed based on the LCLS laser
heater described by Huang et al., PRST-AB 7, 074401 (2004)

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
    print 'testing particle motion in the laser heater... '
    from RadTrack.ptclmovers.RbBorisVay import RbBorisVay
    from RadTrack.fields.RbGaussHermiteMN2 \
        import RbGaussHermiteMN as laserField
    from RadTrack.fields.RbIdealPlanarUndulator \
        import RbIdealPlanarUndulator as planarUndulator
    import numpy as np
    import scipy.constants as consts
    from matplotlib import pyplot as plt
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import scipy.stats as stats
    import scipy.special

    mpl.rc('font',**{'family':'serif','serif':['Palatino']})
    mpl.rc('text', usetex=True)

    tol = 1.e-8

    # Set up the undulator
    lambda_w = 0.05 # [m]
    B0 = 0.33 # [T]
    laserP = 1.2 # MW
    myplanarundulator = planarUndulator(B0, lambda_w)

    # Set up the laser
    lambda0 = 800.e-7 # [m]
    lambdaR = .5 # [m] the Rayleigh range
    waistX = np.sqrt(lambdaR * lambda0/np.pi)
    waistY = waistX
    E0 = np.sqrt(2.*laserP/(np.pi*waistX*waistY*consts.epsilon_0*consts.c)) #
    pol = E0*np.array([1., 0., 0.]) #E0 in Volts/meter

    wRotAngle = 0.
    # Pure Gaussian beam
    hCoeffs = np.array([[1.]])
    mylaserfield = laserField(pol, lambda0, waistX, waistY, wRotAngle, hCoeffs)

    # Determine dt to resolve the undulator motion, assuming a relativistic
    # particle
    dt = 0.05*min((lambda_w/consts.c), (lambda0/(2 *np.pi*consts.c)))
    charge = consts.e
    mass = consts.electron_mass
    pusher = RbBorisVay(charge, mass, dt)

    # Set up the length of the simulation
    # undulatorPeriods = 25
    undulatorLength = 0.5 #undulatorPeriods*lambda_w
    nsteps = int(undulatorLength/(consts.c * dt))
    #nsteps = 1000

    # Create a relativistic particle with 1 mm-mrad "emittance" in the
    # transverse gradient direction
    gamma0 = 26.4188
    v0 = consts.c * np.sqrt((1. - 1/gamma0**2))
    pos = np.array([[0., 0., -0.5*undulatorLength]])
    vel = np.array([[0., 0., gamma0*v0]])

    t = 0.
    # Initial half-move
    pos = pusher.halfmove(vel, pos, +1)
    t += 0.5*dt

    gamma = np.sqrt(np.dot(vel[0], vel[0])/consts.c**2 + 1)
    x = []
    x.append(pos[0][0])
    y = []
    y.append(pos[0][1])
    z = []
    z.append(pos[0][2])
    vx = []
    vx.append(vel[0][0]/(gamma*consts.c))
    vy = []
    vy.append(vel[0][1]/(gamma*consts.c))
    vz = []
    vz.append(vel[0][2]/(gamma*consts.c))

    gammaArray = []
    tList = []
    gammaArray.append(gamma)
    # Diagnostic purposes
    Efield = []
    E = myplanarundulator.evaluateEField(pos, t)
    E += mylaserfield.evaluateEField(pos, t)
    Efield.append(E[0][0])
    tList.append(t)

    print 'taking', nsteps, 'steps to solve the problem'

    for idx in range(nsteps):
        #E = myplanarundulator.evaluateEField(pos, t)
        B = myplanarundulator.evaluateBField(pos, t)
        E = mylaserfield.evaluateEField(pos, t)
        #B += mylaserfield.evaluateBField(pos, t)
        vel = pusher.accelerate(vel, E, B)
        pos = pusher.move(vel, pos)


            # Diagnostic purposes
        if idx%100 == 0:
            gamma = np.sqrt(np.dot(vel[0], vel[0])/consts.c**2 + 1)
            x.append(pos[0][0])
            vx.append(vel[0][0]/(gamma*consts.c))
            y.append(pos[0][1])
            vy.append(vel[0][1]/(gamma*consts.c))
            Efield.append(E[0][0])
            z.append(pos[0][2])
            vz.append(vel[0][2]/(gamma*consts.c))
            gammaArray.append(gamma)
            tList.append(t)

        t += dt

    plt.show()

    # Backwards half-move
    pos = pusher.halfmove(vel, pos, -1)
    t -= 0.5*dt

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x, y, z, linewidth=2)
    ax.plot(x, y, zs=min(z), zdir='z', alpha=0.25, c='k')
    ax.plot(x, z, zs=min(y), zdir='y', alpha=0.25, c='k')
    ax.plot(y, z, zs=min(x), zdir='x', alpha=0.25, c='k')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    ax.set_zlabel(r'$z$')
    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y), max(y))
    ax.set_zlim(min(z), max(z))

    #ax.legend()
    plt.savefig('laserHeater04Trajectory.png')
    plt.show()
    plt.clf()

    # Compare the computed undulator trajectory with the ideal
    #Zed = np.array(z)
    K = B0*lambda_w*consts.elementary_charge/(
        consts.electron_mass*consts.c*2*np.pi)
    #vxIdeal = -(K/gamma0) * np.sin(2*np.pi*Zed/lambda_w)
    #plt.plot(z, vxIdeal, '-.', linewidth=2, alpha=0.75, c='r', label='ideal')
    #plt.plot(z, vx, linewidth=1, alpha=0.75, c='b', label='computed')
    #plt.xlabel(r'$z$ [m]')
    #plt.ylabel(r'$\beta_x$')
    #plt.legend()
    #plt.savefig('laserHeater04Velocity.png')
    #plt.show()
    #plt.clf()

    gammaNP = np.array(gammaArray)
    plt.plot(z, (gammaNP-gamma0))
    plt.xlabel(r'$z [m]$')
    plt.ylabel(r'$(\gamma-\gamma_0)$')
    plt.savefig('laserHeater04Gamma.png')
    #plt.show()
    plt.clf()
    slope, intercept, r, p, err = stats.linregress(z, (gammaNP-gamma0))
    print 'slope =', slope
    print 'intercept =', intercept
    # Compare the slope to theory
    P0 = 8.7e12 # I_A m c^2/e
    slopeTheory = np.sqrt(laserP/P0)*(K/(gamma0*np.sqrt(waistX*waistY)))\
                  *( scipy.special.jn(0, K**2/(4+2*K**2))
                    -scipy.special.jn(1, K**2/(4+2*K**2)) )

    print slopeTheory


    plt.plot(z, Efield)
    plt.xlabel(r'$z [m]$')
    plt.ylabel(r'$E_x [V/m]$')
    plt.savefig('laserHeater04Efield.png')
    #plt.show()
    plt.clf()

    expectedVel = np.array([9.27087540e+08, 5.83274041e+07, 2.99618515e+10])
    velError = vel[0] - expectedVel
    metricVel = abs(np.dot(velError, velError)/np.dot(expectedVel,expectedVel))

    if metricVel > tol:
        print 'V failed tolerances with v =', vel[0], ', Expected:', expectedVel
        failed = True

    if failed:
        raise Exception('laserHeater04 has failed')

except Exception as e:
    print e
    raise

print 'Passed.'
