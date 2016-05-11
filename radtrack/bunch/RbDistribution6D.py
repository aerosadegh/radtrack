#
# Generate a 6D distribution that conforms very closely to a 'unit sphere'.
#
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
#
# Python imports
import math

# SciPy imports
import numpy as np

# RadiaBeam imports
import radtrack.bunch.RbTwiss2D as twiss
import radtrack.bunch.RbPhaseSpace6D as ps
import radtrack.statistics.RbStatistics6D as stats

class RbDistribution6D:
    def __init__(self, numParticles):
        # for testing purposes only
        if False:
            print ' '
            print ' ...in RbDistribution6D:__init__'
            print ' phaseSpace6D object will be instantiated!'

        self.phaseSpace6D = ps.RbPhaseSpace6D(numParticles)
        self.phaseSpace6D.checkArray()

        # set some defaults
        self.maxRmsFactor = 5.0
        self.distributionType = 'gaussian'
        return

    def getPhaseSpace6D(self):
        return self.phaseSpace6D

    def getDistributionType(self):
        return self.distributionType

    def setDistributionType(self, distributionType):
        if ( (distributionType == 'uniform')  or
             (distributionType == 'gaussian') or
             (distributionType == 'waterbag') or
             (distributionType == 'kv') ):
            self.distributionType = distributionType
        else:
            message = 'distributionType = ' + self.distributionType + ' -- not supported.'
            raise Exception(message)
        return

    def getMaxRmsFactor(self):
        return self.maxRmsFactor

    def setMaxRmsFactor(self, maxRmsFactor):
        # error handling of input data
        if (maxRmsFactor > 0.0):
            self.maxRmsFactor = maxRmsFactor
        else:
            message = 'maxRmsFactor = ' + str(maxRmsFactor) + '; must be > 0.'
            raise Exception(message)
        return

    def makeUniformDistribution(self):
        array6D = self.phaseSpace6D.getArray6D()
        numParticles = self.phaseSpace6D.getNumParticles()
        numInsideCircle = 0
        while (numInsideCircle < numParticles):
            testX = 2. * np.random.uniform(0.0,1.0,1) - 1.
            testY = 2. * np.random.uniform(0.0,1.0,1) - 1.
            testZ = 2. * np.random.uniform(0.0,1.0,1) - 1.
            testSum = testX**2 + testY**2 + testZ**2

            if (testSum < 1.):
                array6D[0, numInsideCircle] = testX
                array6D[2, numInsideCircle] = testY
                array6D[4, numInsideCircle] = testZ
                numInsideCircle += 1

        numInsideCircle = 0
        while (numInsideCircle < numParticles):
            testPx = 2. * np.random.uniform(0.0,1.0,1) - 1.
            testPy = 2. * np.random.uniform(0.0,1.0,1) - 1.
            testPz = 2. * np.random.uniform(0.0,1.0,1) - 1.
            testSum = testPx**2 + testPy**2 + testPz**2

            if (testSum < 1.):
                array6D[1, numInsideCircle] = testPx
                array6D[3, numInsideCircle] = testPy
                array6D[5, numInsideCircle] = testPz
                numInsideCircle += 1

        return

    def makeGaussianDistribution(self):
        array6D = self.phaseSpace6D.getArray6D()
        numParticles = self.phaseSpace6D.getNumParticles()
        for nLoop in range(6):
            numInsideCircle = 0
            while (numInsideCircle < numParticles):
                testPoint = np.random.normal(0.0, 1.0, 1)

                if (testPoint*testPoint < self.maxRmsFactor):
                    array6D[nLoop, numInsideCircle] = testPoint
                    numInsideCircle += 1
        return

    def initialPhaseSpace6D(self):
        if (self.distributionType == 'uniform'):
            self.makeUniformDistribution()
        elif (self.distributionType == 'gaussian'):
            self.makeGaussianDistribution()
        elif (self.distributionType == 'waterbag'):
            message = 'distributionType = ''waterbag'' is not yet implemented.'
            raise Exception(message)
        elif (self.distributionType == 'kv'):
            message = 'distributionType = ''kv'' is not yet implemented.'
            raise Exception(message)
        else:
            message = 'distributionType = ' + self.distributionType + ' -- not supported.'
            raise Exception(message)
        return

    def cleanPhaseSpace6D(self):
        stats.subtractAverages6D(self.phaseSpace6D.getArray6D())
        stats.eraseCorrelations6D(self.phaseSpace6D.getArray6D())
        stats.subtractAverages6D(self.phaseSpace6D.getArray6D())
        stats.normalizeRmsValues6D(self.phaseSpace6D.getArray6D())
        return

    def roundPhaseSpace6D(self):
        self.initialPhaseSpace6D()
        self.cleanPhaseSpace6D()
        return

    def calcAverages6D(self):
        averages = stats.calcAverages6D(self.phaseSpace6D.getArray6D())
        return averages

    def calcRmsValues6D(self):
        rmsValues = stats.calcRmsValues6D(self.phaseSpace6D.getArray6D())
        return rmsValues

    def calcTwissParams6D(self,twissParams6D):
        alphaRMS = np.zeros(3)
        betaRMS  = np.zeros(3)
        emitRMS  = np.zeros(3)

        sigma = stats.calcCorrelations6D(self.phaseSpace6D.getArray6D())
        for iLoop in range(3):
            ii = 2 * iLoop
            emitSQ = sigma[ii,ii]*sigma[ii+1,ii+1] - sigma[ii,ii+1]*sigma[ii+1,ii]

            if False:
                print ' '
                print ' numParticles = ', self.phaseSpace6D.getNumParticles()
                q6 = self.phaseSpace6D.getArray6D()
                print ' 1st particle: ', q6[:,0]

            if False:
                print ' '
                print ' iLoop, ii = ', iLoop, ii
                print ' sigma[', ii,   ii,  '] = ', sigma[ii,  ii  ]
                print ' sigma[', ii+1, ii,  '] = ', sigma[ii+1,ii  ]
                print ' sigma[', ii,   ii+1,'] = ', sigma[ii,  ii+1]
                print ' sigma[', ii+1, ii+1,'] = ', sigma[ii+1,ii+1]

            if emitSQ <= 0.0:
                message  = 'Error -- \n\n'
                message += '  emitSQ = ' + str(emitSQ) + ' must be > zero!\n'
                message += '  ...in RbDistribution6D:calcTwissParams6D()\n'
                message += '  iLoop, ii = ' + str(iLoop) + ', ' + str(ii) + '\n'
                raise Exception(message)

            emitRMS[iLoop]  =  math.sqrt(emitSQ)
            betaRMS[iLoop]  =  sigma[ii,ii]   / emitRMS[iLoop]
            alphaRMS[iLoop] = -sigma[ii,ii+1] / emitRMS[iLoop]

            if False:
                print ' '
                print ' alphaRMS, betaRMS, emitRMS = ', alphaRMS[iLoop], betaRMS[iLoop], emitRMS[iLoop]

        twissParams6D['twissX'] = twiss.RbTwiss2D(alphaRMS[0], betaRMS[0], emitRMS[0])
        twissParams6D['twissY'] = twiss.RbTwiss2D(alphaRMS[1], betaRMS[1], emitRMS[1])
        twissParams6D['twissZ'] = twiss.RbTwiss2D(alphaRMS[2], betaRMS[2], emitRMS[2])
        return

    def makeTwissDist6D(self,twissParams6D, meanMomentum):
        self.roundPhaseSpace6D()

        array6D = self.phaseSpace6D.getArray6D()
        temp6D = array6D.copy()
#        for iLoop in range(6):
#            for nLoop in range(self.phaseSpace6D.getNumParticles()): array6D[iLoop,nLoop] = 0.0

        ii = -1
        for iLoop in range(0,5,2):

            ii +=1
            if   ii==0: twissObject = twissParams6D['twissX']
            elif ii==1: twissObject = twissParams6D['twissY']
            elif ii==2: twissObject = twissParams6D['twissZ']
            else:
                message = 'Error:  ii = ' + ii + ' -- not valid.'
                raise Exception(message)

            alphaII = twissObject.getAlphaRMS()
            betaII  = twissObject.getBetaRMS()
            gammaII = (1.0 + alphaII**2) / betaII

            if 0:
                print ' '
                print ' alpha, beta, gamma[', ii, '] = ', alphaII, betaII, gammaII

            gMinusB = gammaII - betaII
            rootFac = math.sqrt(gMinusB**2 + 4.0*alphaII**2)

            if 0:
                print ' gMinusB, rootFac[', ii, '] = ', gMinusB, rootFac

            if gMinusB >= 0.0:
                fac  = math.sqrt(0.5*(gammaII+betaII-rootFac))
                fInv = math.sqrt(0.5*(gammaII+betaII+rootFac))
            else:
                fac  = math.sqrt(0.5*(gammaII+betaII+rootFac))
                fInv = math.sqrt(0.5*(gammaII+betaII-rootFac))

            if 0:
                print ' fac, fInv[', ii, '] = ', fac, fInv

            if alphaII == 0.0:
                sinPhi = 0.0
                cosPhi = 1.0
            else:
                sinPhi = math.sqrt(0.5*(1.-math.fabs(gMinusB)/rootFac))
                cosPhi = math.sqrt(0.5*(1.+math.fabs(gMinusB)/rootFac))

            if alphaII*gMinusB < 0.0: sinPhi = -sinPhi

            rootFac = math.sqrt(twissObject.getEmitRMS())

            if 0:
                print ' sinPhi, cosPhi, rootFac[', ii, '] = ', sinPhi, cosPhi, rootFac

            for nLoop in range(self.phaseSpace6D.getNumParticles()):
                array6D[iLoop  ,nLoop] = rootFac*(fac *cosPhi*temp6D[iLoop,  nLoop] - \
                                                  fInv*sinPhi*temp6D[iLoop+1,nLoop])
                array6D[iLoop+1,nLoop] = rootFac*(fac *sinPhi*temp6D[iLoop,  nLoop] + \
                                                  fInv*cosPhi*temp6D[iLoop+1,nLoop])
        self.multiplyDistribComp(meanMomentum, 5)
        self.offsetDistribComp(meanMomentum, 5)

    def offsetDistribComp(self,offset,index):
        if index < 0 or index > 5:
            message = 'ERROR!  index is out of range: ' + str(index)
            raise Exception(message)

        array6D = self.phaseSpace6D.getArray6D()
        array6D[index,:] += offset

        return

    def multiplyDistribComp(self,factor,index):
        if index < 0 or index > 5:
            message = 'ERROR!  index is out of range: ' + str(index)
            raise Exception(message)

        array6D = self.phaseSpace6D.getArray6D()
        array6D[index,:] *= factor
        
        return
