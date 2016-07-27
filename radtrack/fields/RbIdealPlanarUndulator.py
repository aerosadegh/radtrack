from __future__ import absolute_import, division, print_function, unicode_literals

"""
Module defining an ideal planar undulator

moduleauthor:: Stephen Webb <swebb@radiasoft.net
Copyright (c) 2014 RadiaBeam Technologies. All rights reserved
"""

__author__ = 'swebb&tshaftan'
__copyright__ = "Copyright &copy RadiaBeam Technologies 2013, all rights " \
                "reserved"
__version__ = "1.0"
__email__ = "swebb@radiasoft.net"

import numpy as np
import scipy.constants as consts

class RbIdealPlanarUndulator:

    def __init__(self, _B0, _lambda_w, _polarization='y'):
        """Create a planar undulator with default polarization in the 'y
        direction
        :param _B0: on-axis magnetic field (Tesla)
        :param _lambda_w: wiggler period (cm)
        :param _polarization: Polarization direction, defaults to 'y',
        can be set to 'x' or an arbitrary angle representing a skewed
        wiggler rotated counterclockwise about the z-axis
        :param _mass: mass of the particle, defaults to electron
        :param _charge: charge of the particle, defaults to electron
        :return:
        """
        self.B = _B0
        self.polarization=_polarization
        self.kwiggler = 2*np.pi/(_lambda_w)

    def evaluateEField(self,x,t):
        """Get the electric field at a space-time point for an ideal planar
        undulator
        :param x: numpy array of particle positions
        :param t: numpy array/scalar of time
        :return: numpy array of electric fields
        """

        E = np.zeros(x.shape[0]*3).reshape(x.shape[0], 3)

        return E

    def evaluateBField(self,x,t):
        """
        Get the magnetic field at a space-time point for an ideal planar
        undulator
        :param x: numpy array of particle positions
        :param t: numpy array/scalar of time
        :return: numpy array of magnetic fields
        """
        B = np.zeros(x.shape[0]*3).reshape(x.shape[0], 3)

        if self.polarization == 'y':
            B[:,1] = self.B*np.cos(self.kwiggler*x[:,2])
        elif self.polarization == 'x':
            B[:,0] = self.B*np.cos(self.kwiggler*x[:,2])
        else:
            B[:,1] = self.B*np.cos(self.kwiggler*x[:,2])*np.cos(
                self.polarization)
            B[:,0] = -self.B*np.cos(self.kwiggler*x[:,2])*np.sin(
                self.polarization)

        return B

    def getku(self):
        return self.kwiggler

    def getA(self, coords, z):

        Aw = (self.B/self.kwiggler)
        Aw *= np.cos(self.kwiggler*z)

        return Aw

    def getASqrd(self, coords):
        Aw = self.getAAmplitude(coords)
        return Aw**2

    def getAAmplitude(self, coords):
        return self.B

    def getAdAdX(self, coords, z):
        return 0.

    def getAdAdY(self, coords, z):
        return 0.
    
 #   def ky(self)
 #       return self.eOmc**2*self.B*self.kwiggler/np.sqrt(2.0)/self.gamma0
