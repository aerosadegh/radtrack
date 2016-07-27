"""
Module defining a real planar undulator with transversely varying fields.
The fields are the approximate fields as described in Chap. 7 of J. A.
Clarke "The Science and Technology of Undulators and Wigglers"

moduleauthor:: Stephen Webb <swebb@radiasoft.net
Copyright (c) 2014 RadiaBeam Technologies. All rights reserved
"""

__author__ = 'swebb'
__copyright__ = "Copyright &copy RadiaBeam Technologies 2013, all rights " \
                "reserved"
__version__ = "0.1"
__email__ = "swebb@radiasoft.net"

# SciPy imports
import numpy as np
import scipy.constants as consts


class RbPlanarUndulator:
    def __init__(self, _B0, _lambda_w, _gap, _polarization='y', _gamma0):
        """Create a planar undulator with default polarization in the 'y
        direction
        :param _B0: magnetic field strength of permanent magnets (Tesla)
        :param _lambda_w: wiggler period (cm)
        :param gap:  size of the gap (cm)
        :param polarization: Polarization direction, defaults to 'y',
        can be set to 'x' or an arbitrary angle representing a skewed
        wiggler rotated counterclockwise about the z-axis
        :return:
        """
        self.B = _B0
        self.polarization = _polarization
        self.h = _gap
        self.kwiggler = 2 * np.pi / (_lambda_w)
        self.gapFactor = 1.-np.exp(-self.h * self.kwiggler)
        self.gamma0 = _gamma0

    def evaluateEField(self, x, t):
        """Get the electric field at a space-time point for an ideal planar
        undulator
        :param x: numpy array of particle positions
        :param t: numpy array/scalar of time
        :return: numpy array of electric fields
        """

        E = np.zeros(x.shape[0] * 3).reshape(x.shape[0], 3)

        return E

    def evaluateBField(self, x, t):
        """
        Get the magnetic field at a space-time point for an ideal planar
        undulator
        :param x: numpy array of particle positions
        :param t: numpy array/scalar of time
        :return: numpy array of magnetic fields
        """
        B = np.zeros(x.shape[0] * 3).reshape(x.shape[0], 3)

        if self.polarization == 'y':
            B[:, 1] = self.B * np.cos(self.kwiggler * x[:, 2]) \
                      * np.cosh(self.kwiggler * x[:, 1]) * self.gapFactor
        elif self.polarization == 'x':
            B[:, 0] = self.B * np.cos(self.kwiggler * x[:, 2]) \
                      * np.cosh(self.kwiggler * x[:, 0]) * self.gapFactor
        else:
            gapCoords = np.cos(self.polarization)*x[:,1] - np.sin(
                self.polarization)*x[:,0]
            B[:, 0] = -self.B * np.cos(self.kwiggler * x[:, 2]) \
                      * np.cosh(self.kwiggler * gapCoords[:]) * \
                      self.gapFactor \
                      * np.sin(self.polarization)
            B[:, 1] = self.B * np.cos(self.kwiggler * x[:, 2]) \
                      * np.cosh(self.kwiggler * gapCoords[:]) * \
                      self.gapFactor \
                      * np.cos(self.polarization)

        return B


