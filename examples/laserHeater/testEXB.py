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
    E0 = 1.e-5
    B0 = 1.e-5
    B = [B0 * np.array([0., 1., 0.])]
    E = [E0 * np.array([1., 0., 0.])]
    charge = consts.e
    mass = consts.electron_mass

    pusher = RbBorisVay(charge, mass, dt)

    x = []
    y = []
    z = []
    tArray = []
    xIdeal = []
    yIdeal = []
    zIdeal = []
    ebConst = mass*E0/(charge * B0**2)
    Omega = charge * B0/mass
    v0 = [np.array([0., 0., 0.])]
    x0 = [np.zeros(3)]

    t = 0.

    x0 = pusher.halfmove(v0, x0, +1)

    x.append(x0[0][0])
    y.append(x0[0][1])
    z.append(x0[0][2])
    xIdeal.append(-ebConst*np.cos(Omega * t) + ebConst)
    yIdeal.append(-0.0001)
    zIdeal.append(-ebConst*np.sin(Omega * t) + E0*t/B0)
    tArray.append(t)
    t += 0.5*dt



    for idx in range(10000):
        v0 = pusher.accelerate(v0, E, B)
        x0 = pusher.move(v0, x0)
        x.append(x0[0][0])
        y.append(x0[0][1])
        z.append(x0[0][2])
        xIdeal.append(-ebConst*np.cos(Omega * t) + ebConst)
        yIdeal.append(-0.0001)
        zIdeal.append(-ebConst*np.sin(Omega * t) + E0*t/B0)
        tArray.append(t)
        t += dt



    x0 = pusher.halfmove(v0, x0, -1)

    x.append(x0[0][0])
    y.append(x0[0][1])
    z.append(x0[0][2])
    xIdeal.append(-ebConst*np.cos(Omega * t) + ebConst)
    yIdeal.append(-0.0001)
    zIdeal.append(-ebConst*np.sin(Omega * t) + E0*t/B0)
    tArray.append(t)
    t -= dt



    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x, y, z, linewidth=2)
    ax.plot(xIdeal, yIdeal, zIdeal, c='r')
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
    plt.savefig('EXB_trajectory.png')
    plt.clf()

    xError = [0.]*len(xIdeal)
    zError = [0.]*len(zIdeal)
    for idx in range(len(xIdeal)-1):
        xError[idx] = abs(xIdeal[idx] - x[idx])
        zError[idx] = abs(zIdeal[idx] - z[idx])

    plt.plot(tArray, xIdeal, c='b', label='Ideal')
    plt.plot(tArray, x, c='r', alpha=0.5, label='Computed')
    plt.xlabel(r'$t$ [sec]')
    plt.ylabel(r'$x$ [m]')
    plt.legend()
    plt.tight_layout()
    plt.savefig('xTrajectoriesCompared.png')
    plt.clf()
    plt.plot(tArray, xError)
    plt.xlabel(r'$t$ [sec]')
    plt.ylabel(r'$|x_{comp.} - x_{ideal}$ [m]')
    plt.tight_layout()
    plt.savefig('xTrajectoryError.png')
    plt.clf()

    plt.plot(tArray, zIdeal, c='b', label='Ideal')
    plt.plot(tArray, z, c='r', alpha=0.5, label='Computed')
    plt.xlabel(r'$t$ [sec]')
    plt.ylabel(r'$z$ [m]')
    plt.legend()
    plt.tight_layout()
    plt.savefig('zTrajectoriesCompared.png')
    plt.clf()
    plt.plot(tArray, zError)
    plt.xlabel(r'$t$ [sec]')
    plt.ylabel(r'$|z_{comp.} - z_{ideal}$ [m]')
    plt.tight_layout()
    plt.savefig('zTrajectoryError.png')
    plt.clf()




except Exception as e:
    print e
    raise

print 'Passed.'