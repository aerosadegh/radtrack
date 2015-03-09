"""Class to implement the relativistic Vay push for particle-field
interactions. Vay has many nice properties, such as exact cancellations of
forces to avoid spurious accelerations, and symplecticity.

moduleauthor:: Stephen Webb <swebb@radiasoft.net
Copyright (c) 2014 RadiaBeam Technologies. All rights reserved
"""

__author__ = 'swebb'
__copyright__ = "Copyright &copy RadiaBeam Technologies 2013, all rights " \
                "reserved"
__version__ = "1.0"
__email__ = "swebb@radiasoft.net"

import numpy as np
import scipy.constants as consts

class RbBorisVay:

    def __init__(self, _charge, _mass, _dt):

        # Set relevant parameter
        self.dto2 = _dt/2.
        self.charge2mass = (_charge/_mass)*self.dto2


    def move(self, u, x):
        """ Carries out the relativistic move

        :param u: list of particle velocities beta*gamma as numpy arrays
        :param x: list of particle positions as numpy arrays
        :return: x returns new positions
        """
        dt = 2.*self.dto2
        for idx in range(len(x)):
            gamma = np.sqrt(np.dot(u[idx], u[idx])/consts.c**2 + 1)
            x[idx] += dt * u[idx]/gamma

        return x


    def halfmove(self, u, x, pm):
        """ Carries out a relativistic half-move to synchronize u and x.
        This should be used as a forward half-move at the beginning of an
        update sequence, and a backward half-move at the end.

        :param u: list of particle velocities beta*gamma as numpy arrays
        :param x: list of particle positions as numpy arrays
        :param pm: positive indicates forward half-move, negative indicates
        backward half-move
        :return: x returns new positions
        """
        if pm > 0:
            sgn = 1.
        else:
            sgn = -1.

        for idx in range(len(x)):
            gamma = np.sqrt(np.dot(u[idx], u[idx])/consts.c**2 + 1)
            x[idx] += sgn*self.dto2 * u[idx]/gamma

        return x


    def accelerate(self, u, efield, bfield):
        """ Carries out the relativistic accelerate

        :param u: list of particle velocities beta*gamma as numpy arrays
        :param efield: list of electric fields as numpy arrays
        :param bfield: list of magnetic fields as numpy arrays
        :return:
        """
        for idx in range(len(u)):

            gamma = np.sqrt((np.dot(u[idx], u[idx])/consts.c**2 + 1.))

            tau = self.charge2mass*bfield[idx]
            tausqrd = np.dot(tau,tau)
            eps = self.charge2mass*efield[idx]

            # Compute the first-half intermediate velocity
            uprime = u[idx] + (2.*eps + np.cross(u[idx]/gamma,tau))

            # Many intermediate variables for Vay
            gammaprime=np.sqrt(np.dot(uprime,uprime)/consts.c**2+1)
            sigma=gammaprime**2 - tausqrd
            ustar=np.dot(uprime, tau)/consts.c
            gammap1 = np.sqrt(sigma**2 + 4.*(tausqrd + ustar**2))
            gammap1 += sigma
            gammap1 *= 0.5
            gammap1 = np.sqrt(gammap1)

            t = tau/gammap1
            tsqrd = np.dot(t,t)
            s = 1./(1 + tsqrd)

            u[idx] = s*(uprime + np.dot(uprime,t)*t + np.cross(uprime, t))

        return u