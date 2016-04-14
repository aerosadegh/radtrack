#
# Encapsulation of statistics for a 6D particle distribution.
#  
# 
# Python imports
import math

# SciPy imports
import numpy as np
import scipy as sp


def calcAverages6D(array6D):
    return sp.average(array6D, axis=1)

def subtractAverages6D(array6D):
    averages6D = calcAverages6D(array6D)
    for nLoop in range(6):
        array6D[nLoop,:] -= averages6D[nLoop]

def calcVariance6D(array6D):
    npoints = array6D.shape[1]
    avgIter = array6D[:,0]
    varIter = sp.zeros(6)
    for nLoop in range(1,npoints):
        tmpData  = array6D[:,nLoop]
        tmpIter  = (tmpData - avgIter)
        avgIter += (tmpData - avgIter) / (nLoop+1) 
        varIter += (tmpData - avgIter) * tmpIter
    return varIter / npoints

def calcRmsValues6D(array6D):
    return sp.sqrt(calcVariance6D(array6D))

def normalizeRmsValues6D(array6D):
    invRmsValues6D = 1. / calcRmsValues6D(array6D)
    for nLoop in range(6):
        array6D[nLoop,:] *= invRmsValues6D[nLoop]

def calcMinValues6D(array6D):
    return np.min(array6D, axis=1)

def calcMaxValues6D(array6D):
    return np.max(array6D, axis=1)

def calcCorrelations6D(array6D):
    # for testing purposes only
    if False:
        print ' '
        print '...in RbStatistics6D:calcCorrelations6D()'
        print ' 1st particle: ', array6D[:,0]

    npoints = array6D.shape[1]
    averages6D = calcAverages6D(array6D)
    variance6D = calcVariance6D(array6D)
    correlations6D = sp.zeros(6*6).reshape(6,6)
    for iLoop in range(6):
        for jLoop in range(6):
            if iLoop == jLoop:
                correlations6D[iLoop, jLoop] = variance6D[iLoop]
            else:
                for nLoop in range(npoints):
                    correlations6D[iLoop, jLoop] += \
                        (array6D[iLoop,nLoop] - averages6D[iLoop]) * \
                        (array6D[jLoop,nLoop] - averages6D[jLoop])
                correlations6D[iLoop, jLoop] /= npoints
                #correlations6D[jLoop, iLoop]  = correlations6D[iLoop, jLoop]
    return correlations6D

def eraseCorrelations6D(array6D):
    npoints = array6D.shape[1]
    sigmaM = calcCorrelations6D(array6D)        
    eigVals, eigVecs = jacobiEigenSolver6D(sigmaM)
    
    verboseCheck = 0
    if verboseCheck == 1:
        print 'eigVals = ', eigVals

    temp6D = array6D.copy()
    for iLoop in range(6):
        for nLoop in range(npoints): array6D[iLoop,nLoop] = 0.0
                
    for iLoop in range(6):
        for jLoop in range(6):
            for nLoop in range(npoints):
                array6D[iLoop,nLoop] += eigVecs[jLoop,iLoop] * temp6D[jLoop,nLoop]

def jacobiEigenSolver6D(sigma6D):
    # Setup
    eVecs=sp.zeros(36).reshape(6,6)
    for ip in range(6): eVecs[ip,ip]=1.0

    bTemp=sp.zeros(6)
    zTemp=sp.zeros(6)
    eVals=sp.zeros(6)
    for ip in range(6):
        bTemp[ip]=sigma6D[ip,ip]
        eVals[ip]=sigma6D[ip,ip]

    # Top of the master loop
    numRotations = 0
    for nMaster in range(50):
        sm = 0.0
        for ip in range(5):
            for iq in range(ip+1,6):
                sm += math.fabs(sigma6D[ip,iq])
                
        # Check for convergence
        if sm == 0.0:
            return eVals, eVecs   # Success!
        
        # Convergence failed, so reset threshold
        if nMaster<3:
            threshold=0.2*sm/36.
        else:
            threshold=0.0
            
        # Next iteration
        for ip in range(5):
            for iq in range(ip+1,6):
                gScal=100.*math.fabs(sigma6D[ip,iq])
                if nMaster>3 and math.fabs(float(eVals[ip])+gScal)==math.fabs(eVals[ip]) \
                             and math.fabs(float(eVals[iq])+gScal)==math.fabs(eVals[iq]):
                    sigma6D[ip,iq]=0.0
                elif math.fabs(sigma6D[ip,iq])>threshold:
                    hScal=float(eVals[iq])-float(eVals[ip])
                    if math.fabs(hScal)+gScal==math.fabs(hScal):
                        tScal=float(sigma6D[ip,iq])/hScal
                    else:
                        theta=0.5*hScal/float(sigma6D[ip,iq])
                        tScal=1.0/(math.fabs(theta)+math.sqrt(1.0+theta**2))
                        if theta<0.: tScal*=-1.0
                    cTemp=1.0/math.sqrt(1.0+tScal**2)
                    sTemp=tScal*cTemp
                    tau=sTemp/(1.0+cTemp)
                    hScal=tScal*float(sigma6D[ip,iq])
                    zTemp[ip]-=hScal
                    zTemp[iq]+=hScal
                    eVals[ip]-=hScal
                    eVals[iq]+=hScal
                    sigma6D[ip,iq]=0.0
                    for jLoop in range(ip):
                        gScal=sigma6D[jLoop,ip]
                        hScal=sigma6D[jLoop,iq]
                        sigma6D[jLoop,ip]=gScal-sTemp*(hScal+gScal*tau)
                        sigma6D[jLoop,iq]=hScal+sTemp*(gScal-hScal*tau)
                    for jLoop in range(ip+1,iq):
                        gScal=sigma6D[ip,jLoop]
                        hScal=sigma6D[jLoop,iq]
                        sigma6D[ip,jLoop]=gScal-sTemp*(hScal+gScal*tau)
                        sigma6D[jLoop,iq]=hScal+sTemp*(gScal-hScal*tau)
                    for jLoop in range(iq+1,6):
                        gScal=sigma6D[ip,jLoop]
                        hScal=sigma6D[iq,jLoop]
                        sigma6D[ip,jLoop]=gScal-sTemp*(hScal+gScal*tau)
                        sigma6D[iq,jLoop]=hScal+sTemp*(gScal-hScal*tau)
                    for jLoop in range(6):
                        gScal=eVecs[jLoop,ip]
                        hScal=eVecs[jLoop,iq]
                        eVecs[jLoop,ip]=gScal-sTemp*(hScal+gScal*tau)
                        eVecs[jLoop,iq]=hScal+sTemp*(gScal-hScal*tau)
                    numRotations+=1
        
        # Collect results before checking again for convergence
        for ip in range(6):
            bTemp[ip]+=zTemp[ip]
            eVals[ip] =bTemp[ip]
            zTemp[ip] =0.0
    
    # No convergence after 50 iterations, so give up!
    raise Exception("Too many iterations in routine jacobiEigenSolver6D")
