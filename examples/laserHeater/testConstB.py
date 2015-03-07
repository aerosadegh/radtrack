__author__ = 'swebb'

from matplotlib import pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

mpl.rc('text', usetex=True)
from RadTrack.ptclmovers.RbBorisVay import RbBorisVay
import scipy.constants as consts
import numpy as np

try:

    print 'testing BorisVay in a constant magnetic field'
    E0 = 0.
    B0 = 0.3
    B = np.array([[B0, 0., 0.]])
    E = np.array([[0., 0., 0.]])
    charge = consts.e
    mass = consts.electron_mass
    vNaught = 1.3e3
    gamma0 = np.sqrt(vNaught**2/consts.c**2 + 1)
    Omega = consts.e * B0/(gamma0*consts.m_e)
    dt = 0.1/Omega

    pusher = RbBorisVay(charge, mass, dt)
    v0 = np.array([[0., vNaught, 0.]])
    x0 = np.array([[0., 0., 0.]])

    nsteps = 1000
    t = 0.

    v = []
    vTheoretical = []
    x0 = pusher.halfmove(v0, x0, +1)
    t += 0.5*dt

    vyIdeal = [0.]*nsteps
    vyComp  = [0.]*nsteps
    vzIdeal = [0.]*nsteps
    vzComp  = [0.]*nsteps
    vError  = [0.]*nsteps
    tArray = []

    for idx in range(nsteps):
        v0 = pusher.accelerate(v0, E, B)
        x0 = pusher.move(v0, x0)
        vyComp[idx] = v0[0][1]
        vzComp[idx] = v0[0][2]
        t += dt
        vyIdeal[idx] = vNaught*np.cos(Omega*t)
        vzIdeal[idx] = -vNaught*np.sin(Omega*t)
        vError[idx] = np.sqrt((vyComp[idx]-vyIdeal[idx])**2+
                              (vzComp[idx]-vzIdeal[idx])**2)/\
                      np.sqrt(vyIdeal[idx]**2 + vzIdeal[idx]**2)
        tArray.append(t)

    x0 = pusher.halfmove(v0, x0, -1)

    t -= dt

    plt.plot(tArray, vyIdeal, c='b', label=r'$u_y$ ideal')
    plt.plot(tArray, vyComp, c='r', label=r'$u_y$ comp.')
    plt.xlabel(r'$t$ [sec]')
    plt.ylabel(r'$u$ [m/s]')
    plt.legend()
    plt.tight_layout()
    plt.savefig('constBVyComparison.png')
    plt.clf()

    plt.scatter(vyComp, vzComp, label='computed', marker='o', c='b')
    plt.scatter(vyIdeal, vzIdeal, label='theoretical', marker='s',
                alpha=0.5, c='r', s=20)
    plt.legend()
    plt.xlabel(r'$\gamma v_y$ [m/s]')
    plt.ylabel(r'$\gamma v_z$ [m/s]')
    plt.tight_layout()
    plt.savefig('constBVelocities.png')
    plt.clf()

except Exception as e:
    print e
    raise

print 'Passed.'