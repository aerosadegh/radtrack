#
# Data holding class for the rms Twiss parameters.
#  
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved 
# 


class RbTwiss2D:
    def __init__(self, alphaRMS, betaRMS, emitRMS):
        self.emitRMS  = emitRMS
        self.betaRMS  = betaRMS
        self.alphaRMS = alphaRMS
        self.gammaRMS = (1.0 + alphaRMS**2) / betaRMS

    def getEmitRMS(self):
        return self.emitRMS

    def getBetaRMS(self):
        return self.betaRMS

    def getAlphaRMS(self):
        return self.alphaRMS

    def getGammaRMS(self):
        return self.gammaRMS
