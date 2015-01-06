import sys
import numpy as np
from PySide.QtCore import *
from PySide.QtGui import *
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
import RadTrack.fields.RbGaussHermiteMN as hermite
from RadTrack.gui.dcp3 import *

class RbContour(QMainWindow):
    def __init__(self, parent=None):
        super(RbContour, self).__init__()
        self.ui = Ui_DCP3()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.display)
    

    def display(self):
        mystring = self.ui.lineEdit.text()
        hcoef = int(mystring)
        # Specify the desired grid size
        numX = 100 
        numY = 100
        numCells = numX * numY 

        # Specify the laser beam parameters
        wavelength = 10.e-06         # central wavelength [m]
        w0x = 10.*wavelength  # w0 at z=0.

        # load up the x,y locations of the mesh [m]
        xMin = -4.*w0x
        xMax =  4.*w0x
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
        gh00.setCoeffSingleMode(hcoef, exMax, 0, 1.)

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
    myapp = RbContour()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
