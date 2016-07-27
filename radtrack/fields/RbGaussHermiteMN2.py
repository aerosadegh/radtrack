"""
Module defining the GaussHermite (m,n) mode for a laser profile.
Copyright (c) 2014 RadiaBeam Technologies. All rights reserved
"""

__author__ = 'Stephen Webb, David Bruhwiler, T. Shaftan'
__copyright__ = "Copyright &copy RadiaBeam Technologies 2013, all rights " \
                "reserved"
__version__ = "0.1"
__email__ = "swebb@radiasoft.net"

# SciPy/NumPy imports
import numpy as np
from numpy.polynomial.hermite import hermval2d, hermval
import scipy.constants as consts
import copy

class RbGaussHermiteMN:
    """Module defining a Hermite-Gaussian laser field of order (m,n).
    For now, we assume linear polarization of E along, x.
    Also, the evaluation is done for z=0 (for simplicity)
    The time variable t is ignored.
    These limitations will be removed in the future.
    """

    def __init__(self, pol, lambda0, waistX, waistY, KL, zR, wRotAngle, hCoeffsIn):
        """The constructor requires some basic data.

        Args:
            pol:        polarization and amplitude of E-field at z=0
            lambda0:    central wavelength [m]
            waistX:     horiz. waist size  [m]
            waistY:     vert. waist size  [m]
            wRotAngle:  spot rotation angle [Rad]
            pol:        the polarization vector, specified with zero
                        rotation angle
            hCoeffs:    Coefficients for the n,m Hermite modes
        Returns:
            instance of the class
        Raises:
            NA
        """

        # Copy over the hermite coefficients
        self.setHermCoeffs(hCoeffsIn)

        # Useful quantities
        self.rt2opi = np.sqrt(2./np.pi)
        self.csqrd = consts.c**2

        # set input data (cannot change lambda0,k0, omega)
        self.lambda0 = lambda0         # central wavelength [m]
        self.k0 = 2.*np.pi/lambda0   # central wavenumber [Rad/m]
        self.omega = self.k0 * consts.c  # central frequency [Rad/m]
        self.KL=KL                      # equivalent K parameter for laser
        self.zR=zR                     # Raleigh range [m]
        self.setWaistX(waistX)         # horiz. waist size [m]
        self.setWaistY(waistY)         #  vert. waist size [m]
        self.setWRotAngle(wRotAngle)   # spot rotation angle [Rad]
        self.polVector = pol           # polarization vector

        # Create the rotation matrix and apply it to the polarization vector
        # The rotation matrix will be used to convert the coordinates of the
        #  particle date for computing the hermval2d
        self.rotationMatrix = np.zeros(9).reshape((3,3))
        self.rotationMatrix[0,0] = np.cos(self.wRotAngle)
        self.rotationMatrix[0,1] = -1.*np.sin(self.wRotAngle)
        self.rotationMatrix[1,0] = np.sin(self.wRotAngle)
        self.rotationMatrix[1,1] = np.cos(self.wRotAngle)
        self.rotationMatrix[2,2] = 1.

        # Apply to the polarization vector
        self.polVector = np.dot(self.rotationMatrix,self.polVector)


        # set defaults
        self.setXShift(0.)   # horiz. shift of the spot center
        self.setYShift(0.)   #  vert. shift of the spot center
        self.setZWaistX(0.)  # location (in z) of horiz. waist
        self.setZWaistY(0.)  # location (in z) of  vert. waist

        #self.setCoeffSingleModeX(0, 1.)       # horiz. coeff of Hermite
        # expansion
        #self.setCoeffSingleModeY(0, 1.)       # vert.  coeff of Hermite
        # expansion
        self.setFileName('rbGaussHermiteMN')  # name used for file I/O


# A design decision was made to *NOT* implement this method.
# Everything else depends on lambda0, so it's too disruptive to allow changes.
# Users may only set the value of lambda0 in the constructor. --dlb
#
#    def setLambda0(self,lambda0):
#        return

    #
    #
    #

    # set the horiz. waist size [m]
    def setWaistX(self,waistX):
        # error handling of input data
#        wFac = 3.
        wFac = 1.
        minSize = wFac*self.lambda0
        if waistX >= minSize:
            self.waistX  = waistX
        else:
            message = 'waistX = ' + str(waistX) + '; must be > ' + str(minSize)
            raise Exception(message)

        self.piWxFac = 1. #np.sqrt(self.rt2opi) #/waistX
        self.zRx = 0.5*self.k0*waistX**2  # horiz. Rayleigh range [m]
        self.qx0 = 0.0 + self.zRx*1j
        return

    # set the vert.  waist size [m]
    def setWaistY(self,waistY):
        # error handling of input data
#        wFac = 3.
        wFac = 1.
        minSize = wFac*self.lambda0
        if waistY >= minSize:
            self.waistY  = waistY
        else:
            message = 'waistY = ' + str(waistY) + '; must be > ' + str(minSize)
            raise Exception(message)

        self.piWyFac = 1. #np.sqrt(self.rt2opi) #/waistY
        self.zRy = 0.5*self.k0*waistY**2  #  vert. Rayleigh range [m]
        self.qy0 = 0.0 + self.zRy*1j
        return

    # spot rotation angle [Rad]
    def setWRotAngle(self,wRotAngle):
        self.wRotAngle = wRotAngle
        return

    def setHermCoeffs(self,coeffs):
        """ Set the Hermite-Gauss expansion coefficients

        :param coeffs:
        :return:
        """
        self.hermCoeffs = np.array(coeffs, dtype=complex)

    # horiz. shift of the spot center
    def setXShift(self,xShift):
        self.xShift = xShift
        return

    # vert.  shift of the spot center
    def setYShift(self,yShift):
        self.yShift = yShift
        return

    # set location (in z) of horiz. waist
    def setZWaistX(self,zWaistX):
        self.zWaistX = zWaistX
        return

    # set location (in z) of  vert. waist
    def setZWaistY(self,zWaistY):
        self.zWaistY = zWaistY
        return

    #
    # The "guts" of the class, evaluateEField and evaluateBField.
    # These take numpy arrays of position and a single time float as an
    # argument and return an array of electric and magnetic fields ordered
    # for each particle
    #

    def evaluateEField(self, coords, t):
        """ Calculate the electric field for an array of particles with
        positions x at time t in a Hermite-Gauss laser field

        :param x: numpy array of particle positions
        :param t: time as a float
        :return: numpy array of electric field 3-component vectors
        """

        # Create empty electric field holder
        theEFields = np.zeros(coords.shape[0] * 3, dtype=complex)\
            .reshape(coords.shape[0], 3)

        # Create a temporary variable to store rotated coordinates. This
        # prevents accidental re-assignment. Only access the rotatedCoords
        # from here on out
        #rotatedCoords = np.zeros(coords.shape[0]*3).reshape(coords.shape[
        # 0], 3)
        rotatedCoords = np.dot(self.rotationMatrix, coords.T).T

        # Compute the Hermite-Gauss coefficients, which have some
        # z-dependence that requires they be computed for every time step.
        # This multiplies the base laser mode coefficients, and therefore
        # has to be created as a temporary variable to avoid modifying the
        # original laser parameters. This assumes a 2D laser
        qxz    = np.zeros(rotatedCoords.shape[0], dtype=complex)
        qxz[:] = (rotatedCoords[:,2] - self.zWaistX) + self.qx0
        xrFac  = 0.5 * self.k0 / qxz
        xzFac  = (np.sqrt(2)/self.waistX)/\
                 np.sqrt(1+((coords[:,2]-self.zWaistX)/self.zRx)**2)

        qyz    = np.zeros(rotatedCoords.shape[0], dtype=complex)
        qyz[:] = (rotatedCoords[:,2] - self.zWaistY) + self.qy0
        yrFac  = 0.5 * self.k0 / qyz
        yzFac  = (np.sqrt(2)/self.waistY)/\
                 np.sqrt(1+((coords[:,2]-self.zWaistY)/self.zRy)**2)

        # Iterate over the coefficients, computing the particle-dependent
        # normalization coefficients for the Hermite-Gauss series
        # Have to compute the Hermite-Gauss series explicitly for optimal
        # control -- recommend against attempting to use hermval2d
        ptclCoefs = copy.deepcopy([self.hermCoeffs]*coords.shape[0])

        for idx in range(0,coords.shape[0]):
            for nidx in range(0,self.hermCoeffs.shape[0]):
                for midx in range(0,self.hermCoeffs.shape[1]):
                    ptclCoefs[idx][nidx,midx] /=\
                        np.sqrt(np.math.factorial(midx)*(2.**midx)*
                                np.math.factorial(nidx)*(2.**nidx))
                    ptclCoefs[idx][nidx,midx] *= (self.piWxFac)*np.sqrt(
                        self.qx0/qxz[idx])
                    ptclCoefs[idx][nidx,midx] *= (self.qx0*qxz[idx].conjugate()/
                        self.qx0.conjugate()/qxz[idx])**(0.5*(midx))

                    ptclCoefs[idx][nidx,midx] *= (self.piWyFac)*np.sqrt(
                        self.qy0/qyz[idx])
                    ptclCoefs[idx][nidx,midx] *= (self.qy0*qxz[idx].conjugate()/
                        self.qy0.conjugate()/qyz[idx])**(0.5*(nidx))

        # Explicitly iterate through the particles, since this seems to be
        # the only way to keep control over the Hermite functions
        myNewCoeffs = np.zeros(self.hermCoeffs.shape[0], dtype=complex)
        for idx in range(0,coords.shape[0]):
            for xidx in range(0, self.hermCoeffs.shape[0]):
                myNewCoeffs[xidx] = hermval(yzFac[idx]*coords[idx,1],
                                            ptclCoefs[idx][xidx])

            theEFields[idx,:] = self.polVector[:]* \
                                hermval(xzFac[idx]*coords[idx,0], myNewCoeffs)

            theEFields[idx]*=\
                np.exp(-(xrFac[idx]*(coords[idx,0]**2+coords[idx,1]**2)*1j))

            theEFields[idx,:] *= \
                np.exp(-(yrFac[idx]*(coords[idx,0]**2+coords[idx,1]**2)*1j))


            theEFields[idx]*=\
                np.exp((self.omega * t - self.k0 * coords[idx,2])*1j)

        return theEFields.real

    def evaluateBField(self, coords, t):
        """ Compute the magnetic field for an array of particles with
        positions x at time t in a Hermite-Gauss laser field

        :param x: numpy array of particle positions
        :param t: time as a float
        :return: numpy array of magnetic field 3-component vectors
        """
        #raise Warning('B field for GaussHermite not currently implemented, '
        #              'returns 0.')

        # Create empty B-field holder
        theBFields = np.zeros(coords.shape[0] * 3).reshape(coords.shape[0], 3)

        return theBFields

    def getk0(self):
        return self.k0

    def getA(self, coords, z):

        # Unpack the coordinates
        x, px, y, py, theta, gamma = coords

        # Compute the Hermite-Gauss coefficients, which have some
        # z-dependence that requires they be computed for every time step.
        # This multiplies the base laser mode coefficients, and therefore
        # has to be created as a temporary variable to avoid modifying the
        # original laser parameters. This assumes a 2D laser
        qxz = (z - self.zWaistX) + self.qx0
        xrFac  = 0.5 * self.k0 / qxz
        xzFac  = (np.sqrt(2)/self.waistX)/\
                 np.sqrt(1+((z-self.zWaistX)/self.zRx)**2)

        qyz = (z - self.zWaistY) + self.qy0
        yrFac  = 0.5 * self.k0 / qyz
        yzFac  = (np.sqrt(2)/self.waistY)/\
                 np.sqrt(1+((z-self.zWaistY)/self.zRy)**2)

        # Iterate over the coefficients, computing the particle-dependent
        # normalization coefficients for the Hermite-Gauss series
        # Have to compute the Hermite-Gauss series explicitly for optimal
        # control -- recommend against attempting to use hermval2d
        ptclCoefs = copy.deepcopy(self.hermCoeffs)

        for nidx in range(0,self.hermCoeffs.shape[0]):
            for midx in range(0,self.hermCoeffs.shape[1]):
                ptclCoefs[nidx,midx] *= (self.piWxFac)*np.sqrt(
                    self.qx0/qxz)
                ptclCoefs[nidx,midx] *= (self.qx0*qxz.conjugate()/
                    self.qx0.conjugate()/qxz)**(0.5*(midx))

                ptclCoefs[nidx,midx] *= (self.piWyFac)*np.sqrt(
                    self.qy0/qyz)
                ptclCoefs[nidx,midx] *= (self.qy0*qxz.conjugate()/
                    self.qy0.conjugate()/qyz)**(0.5*(nidx))

        # Explicitly iterate through the particles, since this seems to be
        # the only way to keep control over the Hermite functions
        myNewCoeffs = np.zeros(self.hermCoeffs.shape[0], dtype=complex)
        for xidx in range(0, self.hermCoeffs.shape[0]):
            myNewCoeffs[xidx] = hermval(yzFac*y,ptclCoefs[xidx])

        Alaser = hermval(xzFac*x, myNewCoeffs)

        Alaser *= np.exp(-(xrFac*(x**2)*1j))

        Alaser *= np.exp(-(yrFac*(y**2)*1j))
        Alaser /= self.omega*1j
        Alaser *= np.sqrt(np.dot(self.polVector, self.polVector))

        return abs(Alaser)

    def getATS(self, coords, z):
        x, px, y, py, theta, gamma = coords

        w=self.waistX*(1.0+(z/self.zR)**2)**0.5
        R=z*(1.0+(z/self.zR)**2)**0.5+1E-3
        eta=np.arctan(z/self.zR)
        rho2=(x**2+y**2)
        laserA=self.KL*self.waistX/w*np.exp(-rho2/w**2) #*np.cos(self.k0*z-eta+self.k0*rho2/2/R)

#        laserA=0.038 #plane laser wave
        
        return laserA

# Get the name of the file used for saving data (not used)
    def getFileName(self):
        message = 'method "getFileName" is not implemented'
        raise Exception(message)
        return self.fileName

# Set the name of the file used for saving data (not used)
    def setFileName(self, fileName):
        # error handling of input data
        if (len(fileName) > 0):
            self.fileName = fileName
        else:
            message = 'fileName must have length > 0'
            raise Exception(message)
        return
