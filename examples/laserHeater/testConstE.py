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
    E0 = 1.e6
    B0 = 0.
    B = [B0 * np.array([0., 0., 0.])]
    E = [E0 * np.array([1., 0., 0.])]
    charge = consts.e
    mass = consts.electron_mass

    pusher = RbBorisVay(charge, mass, dt)

    energy = []
    distance = []
    v0 = [np.array([0., 0., 0.])]
    x0 = [np.zeros(3)]

    t = 0.


    x0 = pusher.halfmove(v0, x0, +1)
    t += 0.5*dt



    for idx in range(10000):
        v0 = pusher.accelerate(v0, E, B)
        x0 = pusher.move(v0, x0)
        energy.append(np.sqrt(np.dot(v0[0], v0[0])/consts.c**2 +
                              1.)*consts.m_e*consts.c**2 * 6.24e12) #energy
                              # in MeV
        distance.append(np.sqrt(np.dot(x0[0], x0[0])))
        t += dt



    x0 = pusher.halfmove(v0, x0, -1)

    t -= dt

    idealEnergy = [0.] * len(energy)
    errorEnergy = [0.] * len(energy)
    for idx in range(len(energy)):
        idealEnergy[idx] = \
            consts.elementary_charge * E0 * distance[idx]*6.24e12
        errorEnergy[idx] = abs(idealEnergy[idx] - energy[idx])


    plt.plot(distance, energy, c='r', label='Computed')
    plt.plot(distance, idealEnergy, c='b', label='Ideal')
    plt.legend()
    plt.xlabel(r'$l$ [m]')
    plt.ylabel(r'$\gamma m_e c^2$ [MeV]')
    plt.tight_layout()
    plt.savefig('constEEnergy.png')
    plt.clf()

    plt.plot(distance, errorEnergy, c='b')
    plt.xlabel(r'$l$ [m]')
    plt.ylabel(r'$|\gamma_{ideal} - \gamma_{computed}| m_e c^2$ [MeV]')
    plt.tight_layout()
    plt.savefig('constEError.png')
    plt.clf()



except Exception as e:
    print e
    raise

print 'Passed.'