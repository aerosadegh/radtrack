#
# This class holds an arbitrary 3D electromagnetic field.
#  
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved 
# 
# SciPy imports
import numpy as np

class EMField3D:
    def __init__(self):
        return

    def evaluateE3D(self,x,y,z,t):
        Ex = 0.
        Ey = 0.
        Ez = 0.
        return Ex, Ey, Ez

    def evaluateEx(self,x,y,z,t):
        Ex = 0.
        return Ex

    def evaluateEy(self,x,y,z,t):
        Ey = 0.
        return Ey

    def evaluateEz(self,x,y,z,t):
        Ez = 0.
        return Ez

    def evaluateB3D(self,x,y,z,t):
        Bx = 0.
        By = 0.
        Bz = 0.
        return Bx, By, Bz

    def evaluateBx(self,x,y,z,t):
        Bx = 0.
        return Bx

    def evaluateBy(self,x,y,z,t):
        By = 0.
        return By

    def evaluateBz(self,x,y,z,t):
        Bz = 0.
        return Bz

    def getFileName(self):
        return self.fileName

    def setFileName(self, fileName):
        # error handling of input data
        if (len(fileName) > 0):
            self.fileName = fileName
        else:
            message = 'fileName must have length > 0'
            raise Exception(message)
        return
