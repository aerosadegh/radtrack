"""A collection of analytical results which return the exact solution to a
trial problem to benchmark particle movers

Includes:

* Motion in a constant electric field
* Motion in a constant magnetic field
* Crossed motion in perpendicular electric and magnetic fields

"""

__author__ = 'swebb'

import numpy as np
import scipy.linalg as linalg
import scipy.constants as consts

class PtclTests:

    def __init__(self):
        """does nothing"""

    def constnonrelmagfield(self, x0, v0, q, m, B, t):
        """
        Compute the motion of a charged particle with initial x0 and v0
        through a constant magnetic field
        :param x0: initial position
        :param v0: initial velocity
        :param q: charge
        :param m: mass
        :param B: magnetic field
        :param t: time to propagate
        :return: x, v after propagating for time t
        """
        # Normalize the magnetic field
        tau = q*B/(m)

        # Solve for the velocity using matrix exponentiation
        bMatrix = np.matrix([[0.,         tau[2], -1.*tau[1]],
                             [-1.*tau[2],   0.,     tau[0]],
                             [tau[1],   -1.*tau[0],   0.]])

        print 'BB = ', bMatrix

        greenFunc = linalg.expm(bMatrix*t)
        print 'greenFunc = ', greenFunc
        vfinal = greenFunc*np.matrix(v0).T

        # Compute x using some matrix identities
        xfinal = x0 + bMatrix.I*(greenFunc - np.identity(3))*np.matrix(v0).T

        # get shapes right
        vout = np.zeros(3)
        xout = np.zeros(3)

        vout[0] = vfinal[0,0]
        vout[1] = vfinal[1,0]
        vout[2] = vfinal[2,0]

        xout[0] = xfinal[0,0]
        xout[1] = xfinal[1,0]
        xout[2] = xfinal[2,0]

        return xout, vout


    def constrelmagfield(self, x0, u0, q, m, B, t):
        """
        Compute the relativistic motion of a charged particle with initial x0
        and u0 through a constant magnetic field
        :param x0: initial position
        :param v0: initial velocity beta*gamma
        :param q: charge
        :param m: mass
        :param B: magnetic field
        :param t: time to propagate
        :return: x, v after propagating for time t
        """
        # Properly normalize the vectors
        gamma = np.sqrt(np.dot(u0, u0)/consts.c**2 + 1)
        v0 = u0/gamma
        tau = q * B/(m * gamma)

        # Solve for the velocity using matrix exponentiation
        bMatrix = np.matrix([[0.,         tau[2], -1.*tau[1]],
                             [-1.*tau[2],   0.,     tau[0]],
                             [tau[1],   -1.*tau[0],   0.]])

        greenFunc = linalg.expm(bMatrix*t)
        vfinal = greenFunc*np.matrix(v0).T

        # Compute x using some matrix identities
        xfinal = x0 + bMatrix.I*(greenFunc - np.identity(3))*np.matrix(v0).T

        # get shapes right
        vout = np.zeros(3)
        xout = np.zeros(3)

        vout[0] = vfinal[0,0]
        vout[1] = vfinal[1,0]
        vout[2] = vfinal[2,0]

        xout[0] = xfinal[0,0]
        xout[1] = xfinal[1,0]
        xout[2] = xfinal[2,0]

        return xout, vout