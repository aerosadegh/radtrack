__author__ = 'swebb'

from matplotlib import pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

mpl.rc('text', usetex=True)
from radtrack.ptclmovers.RbBorisVay import RbBorisVay
import scipy.constants as consts
import numpy as np

try:

    dt = 1.e-8
    B = [1.e-5 * np.array([1., 0.1, 0.])]
    E = [1.e-5 * np.array([0., 0., 1.])]
    charge = consts.e
    mass = consts.electron_mass

    pusher = RbBorisVay(charge, mass, dt)

    x = []
    y = []
    z = []
    gamma = 3.
    uMag = consts.c * np.sqrt(gamma**2 - 1.)
    uDir = 1.4*np.pi
    uDir2 = 0.1*np.pi
    v0 = [np.array([uMag * np.cos(uDir) * np.sin(uDir2), uMag * np.sin(uDir) *
                    np.sin(uDir2), uMag * np.cos(uDir2)])]
    x0 = [np.zeros(3)]

    x.append(x0[0][0])
    y.append(x0[0][1])
    z.append(x0[0][2])

    gammaArray = []

    gamma = np.sqrt(np.dot(v0[0], v0[0])/consts.c**2 + 1)
    gammaArray.append(gamma)

    x0 = pusher.halfmove(v0, x0, +1)

    for idx in range(10000):
        v0 = pusher.accelerate(v0, E, B)
        x0 = pusher.move(v0, x0)
        x.append(x0[0][0])
        y.append(x0[0][1])
        z.append(x0[0][2])
        gamma = np.sqrt(np.dot(v0[0], v0[0])/consts.c**2 + 1)
        gammaArray.append(gamma)

    x0 = pusher.halfmove(v0, x0, -1)

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

    ax.legend()
    plt.savefig('BorisVayTrajectory.png')

    plt.clf()

    expectedx0 = np.array([-3563.32861125,   336.10744549,   550.92910024])
    expectedv0 = np.array([ -1.77869689e+08, 7.19781526e+08, -4.11437817e+08])

    tol = 1.e-8

    failed = False
    xerror = x0[0] - expectedx0
    uerror = v0[0] - expectedv0
    metricX = np.dot(xerror, xerror)/np.dot(expectedx0, expectedx0)
    metricV = np.dot(uerror, uerror)/np.dot(expectedv0, expectedv0)

    print 'testBorisVay:'
    print 'Xerror =', metricX
    print 'Verror =', metricV

    if metricX > tol:
        print 'X failed tolerances with x =', x0, ', Expected:', expectedx0
        failed = True

    if metricV > tol:
        print 'V failed tolerances with v =', v0, ', Expected:', expectedv0
        failed = True

    if failed:
        raise Exception('emPusherTest has failed')

except Exception as e:
    print e
    raise

print 'Passed.'