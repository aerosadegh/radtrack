#
# Class to hold miscellaneous plotting utilities.
#  
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

# SciPy imports
import matplotlib.pyplot as plt
import numpy as np

class RbPlotUtils():

    # function to generate contour levels
    def generateContourLevels(self, field, nLevels=40, multiplier=1.1):
        # generate symmetric min/max values
        eMax = multiplier * np.max(field)
        eMin = multiplier * np.min(field)
        if abs(eMin) < eMax:
            eMax = np.around(eMax, decimals=3)
            eMin = -eMax
        else:
            eMin= np.around(eMin, decimals=3)
            eMax = abs(eMin)
            
        # create the level values
        eLevels = []
        deltaE = (eMax-eMin) / nLevels
        for iLoop in range(nLevels):
            eLevels.append(eMin + iLoop*deltaE)
    
        return eLevels
