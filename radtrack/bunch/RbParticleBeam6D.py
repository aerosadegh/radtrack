"""
Module representing a 6D phase space distribution of macroparticles.

We follow the conventions of the Elegant code from Argonne National Lab:
  The fundamental data structure is N rows by 6 columns
  N is the number of macroparticles
  We assume 6 phase space coordinates/momenta 
     x [m], xp=px/p0 [rad], y [m], yp=py/p0 [rad], s [m], (p-p0)/p0 [rad]
  Here, s is the total distance traveled along the accelerator axis,
        and p0 is the design momentum [eV/c]

moduleauthor:: David Bruhwiler <bruhwiler@radiasoft.net>
Copyright (c) 2013-2014 RadiaBeam Technologies. All rights reserved
"""

# Python imports
import math
from scipy import constants
from collections import OrderedDict

# RadiaBeam imports
#import radtrack.bunch.RbPhaseSpace6D as ps
import radtrack.bunch.RbDistribution6D as dist
import radtrack.bunch.RbTwiss2D as twiss

class RbParticleBeam6D:
    def __init__(self, numParticles):
        # instantiate a 6D phase space data object
#        self.phaseSpace6D = ps.RbPhaseSpace6D(numParticles)

        # instantiate local class variables
        self.distribution6D = dist.RbDistribution6D(numParticles)
        self.twissParams6D = OrderedDict( [('twissX', twiss.RbTwiss2D(0.,1.,1.e-6)),   \
                                           ('twissY', twiss.RbTwiss2D(0.,1.,1.e-6)),   \
                                           ('twissZ', twiss.RbTwiss2D(0.,1.,1.e-6))] )
        
        # define useful temporary variables
        self.rt2opi = math.sqrt(2./math.pi)
        
        # specify physical constants
        self.c     = constants.c          # speed of light [m/s]
        self.cSq   = self.c**2            # speed of light squared
        self.cInv  = 1./self.c            # one over the speed of light
        self.mu0   = constants.mu_0    # permeability of free space
        self.eps0  = constants.epsilon_0 # permittivity of free space
        self.eMass   = constants.m_e     # electron mass [kG]
        self.eCharge = constants.e   # elementary charge [C]
        self.eMassEV = self.eMass*self.cSq/self.eCharge  # eMass [eV]
        
        # specify some reasonable defaults
        self.designMomentumEV = 1.e+7     # 10 MeV/c
        self.totalCharge = 1.e-9          #  1 nC
        self.massEV = self.eMassEV        # electron mass
        return

#    def getPhaseSpace6D(self):
#        return self.phaseSpace6D

#    def setPhaseSpace6D(self, phaseSpace6D):
#        self.phaseSpace6D = phaseSpace6D
#        self.phaseSpace6D.checkArray()
#        return

    def getDesignMomentumEV(self):
        return self.designMomentumEV

    def setDesignMomentumEV(self, designMomentumEV):
        if (designMomentumEV > 0.):
            self.designMomentumEV = designMomentumEV
        else:
            message = 'ERROR!  designMomentumEV <= 0.: ' + str(designMomentumEV)
            raise Exception(message)
        return

    def getTotalCharge(self):
        return self.totalCharge

    def setTotalCharge(self, totalCharge):
        if (totalCharge > 0.):
            self.totalCharge = totalCharge
        else:
            message = 'ERROR!  totalCharge <= 0.: ' + str(totalCharge)
            raise Exception(message)
        return

    def getMassEV(self):
        return self.massEV

    def setMassEV(self, massEV):
        if (massEV > 0.):
            self.massEV = massEV
        else:
            message = 'ERROR!  massEV <= 0.: ' + str(massEV)
            raise Exception(message)
        return

    def getBeta0Gamma0(self):
        return self.designMomentumEV / self.massEV

    def getGamma0(self):
        return math.sqrt(self.getBeta0Gamma0()**2 +1.)

    def getBeta0(self):
        return self.getBeta0Gamma0() / self.getGamma0()

    # allowed values: 'twissX', 'twissY', 'twissZ'
    def getTwissParamsByName2D(self, twissName):
        return self.twissParams6D[twissName]

    def setTwissParamsByName2D(self, alpha, beta, emittance, twissName):
        self.twissParams6D[twissName] = twiss.RbTwiss2D(alpha, beta, emittance)
        return

    def calcTwissParams6D(self):
        self.distribution6D.calcTwissParams6D(self.twissParams6D)
        return

    def getDistribution6D(self):
        return self.distribution6D

    def makeParticlePhaseSpace6D(self, meanMomentum):
        self.distribution6D.makeTwissDist6D(self.twissParams6D, meanMomentum)
#        self.distribution6D.offsetDistribComp(self.getBetaGamma0(), 5)
#        self.distribution6D.multiplyDistribComp(self.cInv, 4)
        return
        
    def getCurrent(self):
        s=self.distribution6D.calcRmsValues6D()[4]
        t=s/(self.getBeta0()*self.c)
        I = self.totalCharge/t
        return I



