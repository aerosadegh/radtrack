__author__ = 'swebb'

from matplotlib import pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

mpl.rc('text', usetex=True)
from RadTrack.ptclmovers.RbBorisVay import RbBorisVay
import scipy.constants as consts
import numpy as np

try:

    E0 = 1.e9
    B0 = 0.
    B = np.array([B0 * np.array([0., 0., 0.])])
    E = np.array([E0 * np.array([1., 0., 0.])])
    omega = 1.e14
    dt = 0.1/omega
    charge = consts.e
    mass = consts.electron_mass

    pusher = RbBorisVay(charge, mass, dt)

    gammavx = []
    gammavxIdeal=[]
    tArray = []
    v0 = [np.array([0., 0., 0.])]
    x0 = [np.zeros(3)]

    t = 0.

    x0 = pusher.halfmove(v0, x0, +1)
    t += 0.5*dt

    for idx in range(1000):
        Eomt = E*np.cos(omega*t)
        v0 = pusher.accelerate(v0, Eomt, B)
        x0 = pusher.move(v0, x0)
        gammavx.append(v0[0][0])
        gammavxIdeal.append((E0*charge/(mass*omega))*(np.sin(omega*t)))
        tArray.append(t)
        t += dt

    x0 = pusher.halfmove(v0, x0, -1)

    t -= dt

    plt.plot(tArray, gammavx, c='r', label='computed')
    plt.plot(tArray, gammavxIdeal, c='b', label='theoretical')
    plt.legend()
    plt.xlabel(r'$t$ [sec]')
    plt.ylabel(r'$\gamma v_x$ [m/s]')
    plt.tight_layout()
    plt.savefig('oscillatingDipole.png')

except Exception as e:
    print e
    raise

print 'Passed.'