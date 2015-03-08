"""
Module defining interactive window for Gauss-Hermite laser modes.

Imports the auto-generated RbLaserModeInterface.py module, which is
created via pyside-uic.exe from Qt's RbLaserModeInterface.ui file.

Here, the window is instantiated and hooks to the production
Python code are established.

moduleauthor:: David Bruhwiler <bruhwiler@radiasoft.net>
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
"""

# system imports
import sys

# SciPy imports
import numpy as np
import matplotlib

# PyQt4 imports
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# RadTrack imports
import radtrack.fields.RbGaussHermiteMN as hermite
from radtrack.gui.RbLaserModeInterface import *

class RbLaserModeWindow(QMainWindow):
    def __init__(self,parent=None):
	super(RbLaserModeWindow, self).__init__()
	self.ui = Ui_laserModeInterface()
	self.ui.setupUi(self)

	self.ui.generatePulse.clicked.connect(self.display)

    def display(self):
        # get output from text boxes
        hcoef = int(self.ui.hModeInput.text())
        vcoef = int(self.ui.vModeInput.text())

        # Specify the desired grid size
        numX = 128 
        numY = 128
        numCells = numX * numY 

        # Specify the laser beam parameters
        wavelength = 10.e-06         # central wavelength [m]
        w0x = 10.*wavelength  # w0 at z=0.

        # load up the x,y locations of the mesh [m]
        xMin = -8.*w0x
        xMax =  8.*w0x
        yMin = xMin
        yMax = xMax

        xArr  = np.zeros(numX)
        xGrid = np.zeros((numX, numY))
        yArr  = np.zeros(numY)
        yGrid = np.zeros((numX, numY))
        for iLoop in range(numX):
            xArr[iLoop] = xMin + iLoop * (xMax-xMin) / (numX-1)

        for jLoop in range(numY):
            yArr[jLoop] = yMin + jLoop * (yMax-yMin) / (numY-1)

        for iLoop in range(numX):
            for jLoop in range(numY):
                xGrid[iLoop,jLoop] = xMin + iLoop * (xMax-xMin) / (numX-1)
                yGrid[iLoop,jLoop] = yMin + jLoop * (yMax-yMin) / (numY-1)

        # Create a class instance for mode 0,0 (Gaussian)
        exMax = 1.3e+09
        gh00 = hermite.RbGaussHermiteMN(wavelength,w0x,2.0*w0x,0.)
        gh00.setCoeffSingleModeX(hcoef, exMax)
        gh00.setCoeffSingleModeY(vcoef, 1.)

        # Calculate Ex at the 2D array of x,y values
        Ex = np.reshape(gh00.evaluateEx(np.reshape(xGrid,numCells),   \
                                        np.reshape(yGrid,numCells), 0., 0.), (numX, numY))

        # Create scaled values, so the plot can show microns, rather than meters
        x_nm  = xGrid*1.e6
        xL_nm = xMin *1.e6
        xR_nm = xMax *1.e6

        y_nm  = yGrid*1.e6
        yL_nm = yMin *1.e6
        yR_nm = yMax *1.e6
        
        self.ui.widget.canvas.ax.clear()
        self.ui.widget.canvas.ax.contourf(x_nm, y_nm, Ex, 20)
        self.ui.widget.canvas.draw()


def main():
    app = QtGui.QApplication(sys.argv)
    myapp = RbLaserModeWindow()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
