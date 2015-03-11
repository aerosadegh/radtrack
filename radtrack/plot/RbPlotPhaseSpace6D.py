# 
# Generate 2D scatter plots of particle phase space predictions
#  
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved 
# 
# python imports
import math

# SciPy imports
import numpy as np
import matplotlib.pyplot as plt

class RbPlotPhaseSpace6D:
    def __init__(self, phaseSpace6D):
        # error checking
        phaseSpace6D.checkArray()
        tmpPoints = phaseSpace6D.getNumParticles()
        if (tmpPoints > 1):
            self.npoints = tmpPoints
        else:
            message = 'ERROR - phaseSpace6D.getNumParticles() < 2: ' + str(tmpPoints)
            raise Exception(message)
        
        self.data6D = phaseSpace6D.getArray6D()
        
        self.label=np.array(['x [m]', 'px', 'y [m]', 'py', 'z [m]', 'pz'])
        self.title='no plot title specified'
        self.figNum = 0
        return

    def setTitle(self,title):
        self.title = title
        return

    def getTitle(self):
        return self.title

    def setLabel(self,index,label):
        self.label[index] = label
        return

    def getLabel(self,index):
        return self.label[index]

    def getData6D(self):
        return self.data6D

    def setData6D(self,data6D):
        self.data6D = data6D
        return

    def plotData6D(self,hIndex,vIndex):
        hArray = self.data6D[hIndex,:]
        vArray = self.data6D[vIndex,:]

        hMin = min(hArray)
        hMax = max(hArray)
        if -hMin > hMax:
            hMax = math.fabs(hMin)
        else:
            hMin = -hMax

        vMin = min(vArray)
        vMax = max(vArray)
        if -vMin > vMax:
            vMax = math.fabs(vMin)
        else:
            vMin = -vMax

        self.figNum += 1
        plt.figure(self.figNum)
        plt.scatter(hArray, vArray, marker=',',s=1, c='k')
        plt.axis([hMin, hMax, vMin, vMax])

        plt.xlabel(self.label[hIndex])
        plt.ylabel(self.label[vIndex])
        plt.title(self.title)

        return

    def showPlots(self):
        plt.show()
        return
