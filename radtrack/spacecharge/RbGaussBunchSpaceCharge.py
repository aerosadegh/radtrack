#!/usr/bin/env python

# Python imports 
import math

# RadiaBeam imports
import radtrack.quadrature.RbGaussianQuadrature as gquad

# Functions defining the analytic electric and magnetic fields
#   of a Gaussian 2D ellipse or 3D ellipsoid of charge.
# We assume the beam is moving along x with constant, positive
#   velocity and that it has been doing so for a 'long' time.
# We assume free space boundary conditions.
# We assume an electron beam, with gamma*xRms > yRms.
# 
class RbGaussBunchSpaceCharge:

    # set up basic physical parameters of the bunch
    #   charge [C]   -  total bunch charge
    #   energy [eV]  -  mean kinetic energy
    #   position [m] -  beam center (along x) at t=0 
    #   xRms [m]     -  longitudinal RMS size
    #   yRms [m]     -  transverse RMS size (axisymmetric)
    def __init__(self, charge, energy, position, xRms, yRms):
        self.Q    = charge
        self.KE   = energy
        self.x0   = position    
        self.xRms = xRms
        self.yRms = yRms
        self.zRms = yRms
        
        # specify physical constants
        self.c     = 299792458.           # speed of light [m/s]
        self.cSq   = self.c**2            # speed of light [m/s]
        self.mu0   = 4.0e-07 * math.pi    # permeability of free space
        self.eps0  = 1./self.mu0/self.cSq # permittivity of free space
        self.eMass   = 9.10938215e-31     # electron mass [kG]
        self.eCharge = 1.602176487e-19    # elementary charge [C]
        self.eMassEV = self.eMass*self.cSq/self.eCharge  # eMass [eV]
        
        # calculate the relativistic beta, gamma factors
        self.beamG  = 1 + self.KE/self.eMassEV   # beam gamma
        self.beamBG = math.sqrt(self.beamG**2-1) # beam beta*gamma
        self.beamB  = self.beamBG / self.beamG   # beam beta 
        self.beamV  = self.beamB  * self.c       # [m/s] beam velocity 
        self.beamU  = self.beamBG * self.c       # [m/s] gamma*v
        
        # calcuate the 2D line charge that best approximated 3D fields
#        self.Q2D = self.calcQ2D()
#        self.Q2D = self.calcQ2Db()

# This choice works for the Bragg/ATF parameters
        self.Q2D = self.Q / self.yRms / 3.
        
        # create an instance of the Gaussian quadrature class
        self.gQuad = gquad.RbGaussianQuadrature()
        
        # specify number of quadrature evaluation points
        self.numQuadEvals = 20

        return
    
    # messing around
    def calcQ2Db(self):
        ratio = self.yRms / (self.beamG * self.xRms)
        print ' ratio = ', ratio
        return self.Q * ratio**0.11 * 12000.
    
    # Compute Q2D, the line charge that yields max(Ey2D) ~ max(Ey3D)
    def calcQ2D(self):
        ratio = self.yRms / (self.beamG * self.xRms)
        ratSq = ratio**2
        lnFac = 0.5*ratSq*math.log((1.-math.sqrt(1.-ratSq))/(1.+math.sqrt(1.-ratSq)))/math.sqrt(1.-ratSq)
        fac0  = 0.45 / self.yRms / (1.-ratio)
#        fac0  = 2.5 / self.yRms / (1.-ratio)
        return self.Q * fac0 * (1.+lnFac)

    # Helper function
    def aFac(self, u):
        return math.sqrt(1.+(self.beamG*self.xRms/self.yRms-1.)*u)

    # Helper function
    def bFac(self, u):
        return math.sqrt(1.+(self.yRms/self.beamG/self.xRms-1.)*u)

    # Helper function
    def cFac(self, u):
        return math.sqrt(1.+(self.zRms**2/(self.yRms*self.beamG*self.xRms)-1.)*u)

    # Function used to get Ex2D from quadrature algorithm
    def func2Dx(self, u, xRel, y, zDummy):
        aFac = self.aFac(u)
        bFac = self.bFac(u)
        fac0 = self.beamG * self.xRms * self.yRms
        eFac = math.exp(-0.5*u*((xRel/aFac)**2+(y/bFac)**2)/fac0)
        return eFac / (aFac**3 * bFac)
    
     # Function used to get Ey2D and Bz2D from quadrature algorithm
    def func2Dy(self, u, xRel, y, zDummy):
        aFac = self.aFac(u)
        bFac = self.bFac(u)
        fac0 = self.beamG * self.xRms * self.yRms
        eFac = math.exp(-0.5*u*((xRel/aFac)**2+(y/bFac)**2)/fac0)
        return eFac / (aFac * bFac**3)

    # Function used to get Ex3D from quadrature algorithm
    def func3Dx(self, u, xRel, y, z):
        aFac = self.aFac(u)
        bFac = self.bFac(u)
        cFac = self.cFac(u)
        fac0 = self.beamG * self.xRms * self.yRms
        eFac = math.exp(-0.5*u*((xRel/aFac)**2+(y/bFac)**2+(z/cFac)**2)/fac0)
        return math.sqrt(u) * eFac / (aFac**3 * bFac * cFac)
    
    # Function used to get Ey3D and Bz3D from quadrature algorithm
    def func3Dy(self, u, xRel, y, z):
        aFac = self.aFac(u)
        bFac = self.bFac(u)
        cFac = self.cFac(u)
        fac0 = self.beamG * self.xRms * self.yRms
        eFac = math.exp(-0.5*u*((xRel/aFac)**2+(y/bFac)**2+(z/cFac)**2)/fac0)
        return math.sqrt(u) * eFac / (aFac * bFac**3 * cFac)
    
    # Function used to get Ez3D and By3D from quadrature algorithm
    def func3Dz(self, u, xRel, y, z):
        aFac = self.aFac(u)
        bFac = self.bFac(u)
        cFac = self.cFac(u)
        fac0 = self.beamG * self.xRms * self.yRms
        eFac = math.exp(-0.5*u*((xRel/aFac)**2+(y/bFac)**2+(z/cFac)**2)/fac0)
        return math.sqrt(u) * eFac / (aFac * bFac * cFac**3)
    
    # Compute center (along x) of the drifting relativistic bunch
    def getBeamCenter(self, t):
        return self.beamV*t - self.x0
    
    # Compute the scale factor in 2D
    def getScaleFactor2D(self):
       return self.Q2D/self.eps0/(2.*math.pi)**1.5/(self.yRms*self.beamG*self.xRms)
    
    # Compute the scale factor in 3D
    def getScaleFactor3D(self):
        return self.Q/self.eps0/(2.*math.pi)**1.5/(self.yRms*self.beamG*self.xRms)**1.5
    
    # Compute longitudinal field Ex for a 2D ellipse of charge
    def calcEx2D(self, x, y, t):
        xRel = self.beamG*(x-self.getBeamCenter(t))
        val = self.gQuad.gaussQuadPletzer(0., 1., self.func2Dx, xRel, y, 0., self.numQuadEvals)
        return self.getScaleFactor2D() * xRel * val
    
    # Compute transverse field Ey for a 2D ellipse of charge
    def calcEy2D(self, x, y, t):
        xRel = self.beamG*(x-self.getBeamCenter(t))
        val = self.gQuad.gaussQuadPletzer(0., 1., self.func2Dy, xRel, y, 0., self.numQuadEvals)
        return self.getScaleFactor2D() * self.beamG * y * val
        
    # The Ez component is zero in 2D x-y (slab) geometry
    def calcEz2D(self, x, y, t):
        return 0.
    
    # The longitudinal B-field for an idealized bunch is zero.
    def calcBx2D(self, x, y, t):
        return 0.
        
    # The By component is zero in 2D x-y (slab) geometry
    def calcBy2D(self, x, y, t):
        return 0.

    # Compute transverse field Bz for a 2D ellipse of charge
    def calcBz2D(self, x, y, t):
        return self.beamB * self.calcEy2D(x, y, t) / self.c
    
    # Compute longitudinal field Ex for a 3D ellipsoid of charge
    def calcEx3D(self, x, y, z, t):
        xRel = self.beamG*(x-self.getBeamCenter(t))
        val = self.gQuad.gaussQuadPletzer(0., 1., self.func3Dx, xRel, y, z, self.numQuadEvals)
        return self.getScaleFactor3D() * xRel * val
    
    # Compute transverse field Ey for a 3D ellipsoid of charge
    def calcEy3D(self, x, y, z, t):
        xRel = self.beamG*(x-self.getBeamCenter(t))
        val = self.gQuad.gaussQuadPletzer(0., 1., self.func3Dy, xRel, y, z, self.numQuadEvals)
        return self.getScaleFactor3D() * self.beamG * y * val
    
    # Compute transverse field Ez for a 3D ellipsoid of charge
    def calcEz3D(self, x, y, z, t):
        xRel = self.beamG*(x-self.getBeamCenter(t))
        val = self.gQuad.gaussQuadPletzer(0., 1., self.func3Dy, xRel, y, z, self.numQuadEvals)
        return self.getScaleFactor3D() * self.beamG * y * val
    
    # The longitudinal B-field for an idealized bunch is zero.
    def calcBx3D(self, x, y, z, t):
        return 0.
    
    # Compute transverse field By for a 3D ellipse of charge
    def calcBy3D(self, x, y, z, t):
        return self.beamB * self.calcEz3D(x, y, z, t) / self.c
    
    # Compute transverse field Bz for a 3D ellipse of charge
    def calcBz3D(self, x, y, z, t):
        return self.beamB * self.calcEy3D(x, y, z, t) / self.c
