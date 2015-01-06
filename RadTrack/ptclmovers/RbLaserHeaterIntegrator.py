"""Class to implement the laser heater calculation using the scipy ODEInt
package to integrate the equations of motion

moduleauthor:: Stephen Webb <swebb@radiasoft.net
Copyright (c) 2014 RadiaBeam Technologies. All rights reserved
"""

__author__ = 'swebb'
__copyright__ = "Copyright &copy RadiaBeam Technologies 2013, all rights " \
                "reserved"
__version__ = "1.0"
__email__ = "swebb@radiasoft.net"

import numpy as np
from scipy.integrate import odeint
import scipy.constants as consts
from scipy.special import jn

class RbLaserHeaterIntegrator:

    def __init__(self, laser, undulator):


        self.laserField = laser
        self.undulatorField = undulator

        self.ku = self.undulatorField.getku()
        self.kl = self.laserField.getk0()
        self.eOmc = consts.e/(consts.m_e*consts.c)
        awSqrd = self.eOmc**2*\
                 self.undulatorField.getAAmplitude([0.,0.,0.,0.,0.,0.])**2
        self.fB = jn(0, awSqrd/(4.+2.*awSqrd)) - jn(1, awSqrd/(4.+2.*awSqrd))

        print 'a_w =', np.sqrt(awSqrd)
        print 'fB =', self.fB
        print 'k_l =', self.kl, 'm^-1'
        print 'k_u =', self.ku, 'm^-1'

    def canonicalEquations(self, coords, z):
        X, PX, Y, PY, Theta, Gamma = coords

        derivX = PX/Gamma
        derivY = PY/Gamma
        derivPX = -0.5*self.undulatorField.getAdAdX(coords, z)/Gamma
        derivPY = -0.5*self.undulatorField.getAdAdY(coords, z)/Gamma
        wigglerA = self.undulatorField.getAAmplitude(coords)
        laserA = self.laserField.getA(coords, z)
        derivTheta = self.ku -\
                     self.kl*(
                        1 + PX**2 + PY**2 +
                        (self.eOmc**2)*self.undulatorField.getASqrd(coords)/2.-
                        (self.eOmc**2) * self.fB * wigglerA*
                        laserA*np.cos(Theta))\
                     /(2*Gamma**2)
        derivGamma = -self.kl*(self.eOmc**2)*self.fB*wigglerA*laserA\
                     *np.sin(Theta)/Gamma #

        return np.array([derivX, derivPX, derivY, derivPY, derivTheta,
                         derivGamma])


    def integrate(self, zinitial, zfinal, coords):

        # Resolve the undulator period
        dz = 2.*np.pi*0.01/self.ku
        zrange = np.arange(zinitial, zfinal, dz)

        soln = odeint(self.canonicalEquations, coords, zrange)

        return soln, zrange