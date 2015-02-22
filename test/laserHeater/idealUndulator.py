"""
Test for the laser heater infrastructure using the Gauss-Hermite laser mode
and a planar undulator. This test just checks pure ideal undulator motion.

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
    print 'testing particle motion in an ideal undulator field... '
    from RadTrack.ptclmovers.RbBorisVay import RbBorisVay
    from RadTrack.fields.RbIdealPlanarUndulator \
        import RbIdealPlanarUndulator as planarUndulator
    import numpy as np
    import scipy.constants as consts
    from matplotlib import pyplot as plt
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D

    mpl.rc('text', usetex=True)

    tol = 1.e-8

    # Set up the undulator
    lambda_w = 0.025 # [cm]
    B0 = 1.75 # [T]
    # rotate the undulator a little to get off-axis effects
    angle = 2*np.pi*0.1
    myplanarundulator = planarUndulator(B0, lambda_w)

    # Determine dt to resolve the undulator motion, assuming a relativistic
    # particle
    dt = 0.1*(lambda_w/consts.c)
    charge = consts.e
    mass = consts.electron_mass
    pusher = RbBorisVay(charge, mass, dt)

    # Create a relativistic particle with zero transverse momentum
    gamma0 = 100.
    v0 = consts.c * (1. - 1/gamma0**2)
    pos = np.array([[0., 0., 0.]])
    vel = np.array([[0., 0., gamma0*v0]])


    # Set up the length of the simulation
    undulatorPeriods = 10
    undulatorLength = undulatorPeriods*lambda_w
    nsteps = int(undulatorLength/(consts.c * dt))

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
    gammaArray.append(gamma)

    for idx in range(nsteps):
        E = myplanarundulator.evaluateEField(pos, t)
        B = myplanarundulator.evaluateBField(pos, t)
        vel = pusher.accelerate(vel, E, B)
        pos = pusher.move(vel, pos)

        gamma = np.sqrt(np.dot(vel[0], vel[0])/consts.c**2 + 1)
        x.append(pos[0][0])
        vx.append(vel[0][0]/(gamma*consts.c))
        y.append(pos[0][1])
        vy.append(vel[0][1]/(gamma*consts.c))
        z.append(pos[0][2])
        vz.append(vel[0][2]/(gamma*consts.c))
        gammaArray.append(gamma)
        t += dt

    # Backwards half-move
    pos = pusher.halfmove(vel, pos, -1)
    t -= 0.5*dt

    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')

    #ax.plot(x, y, z, linewidth=2)
    #ax.plot(x, y, zs=min(z), zdir='z', alpha=0.25, c='k')
    #ax.plot(x, z, zs=min(y), zdir='y', alpha=0.25, c='k')
    #ax.plot(y, z, zs=min(x), zdir='x', alpha=0.25, c='k')
    #ax.set_xlabel(r'$x$')
    #ax.set_ylabel(r'$y$')
    #ax.set_zlabel(r'$z$')
    #ax.set_xlim(min(x), max(x))
    #ax.set_ylim(min(y), max(y))
    #ax.set_zlim(min(z), max(z))

    #ax.legend()
    #plt.savefig('laserHeater02Trajectory.png')
    #plt.show()
    #plt.clf()

    # Compare the computed undulator trajectory with the ideal
    #Zed = np.array(z)
    #K = B0*lambda_w*consts.elementary_charge/(
    #    consts.electron_mass*consts.c*2*np.pi)
    #vxIdeal = -(K/gamma0) * np.sin(2*np.pi*Zed/lambda_w)
    #plt.plot(z, vxIdeal, '-.', linewidth=2, alpha=0.75, c='r', label='ideal')
    #plt.plot(z, vx, linewidth=2, alpha=0.75, c='b', label='computed')
    #plt.xlabel(r'$z [m]$')
    #plt.ylabel(r'$\beta_x$')
    #plt.legend()
    #plt.savefig('laserHeater02Velocity.png')
    #plt.show()
    #plt.clf()

    gammaNP = np.array(gammaArray)
    #plt.plot(z, (gammaNP-gamma0)/gamma0)
    #plt.xlabel(r'$z [m]$')
    #plt.ylabel(r'$(\gamma-\gamma_0)/\gamma_0$')
    #plt.savefig('laserHeater02Gamma.png')
    #plt.show()
    #plt.clf()

    expectedVel = np.array([7.61814727e+08, 0.00000000e+00, 2.99665660e+10])

    for idx in range(0,gammaNP.size-1,1):
        if abs(gammaNP[idx+1] - gammaNP[idx]) > tol:
            print 'Gamma failed to remain conserved beyond tolerances.'
            failed = True

    velError = vel[0] - expectedVel
    metricVel = abs(np.dot(velError, velError)/np.dot(expectedVel,expectedVel))

    if metricVel > tol:
        print 'V failed tolerances with v =', vel[0], ', Expected:', expectedVel
        failed = True

    if failed:
        raise Exception('idealUndulator has failed')

except Exception as e:
    print e
    raise

print 'Passed.'
