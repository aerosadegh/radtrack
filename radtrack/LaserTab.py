"""
Module defining interactive window for laser pulses.

Imports the auto-generated RbLaserModeInterface.py module, which is
created via pyside-uic.exe from Qt's RbLaserModeInterface.ui file.

Here, the window is instantiated and hooks to the production
Python code are established.

moduleauthor:: David Bruhwiler <bruhwiler@radiasoft.net>
Copyright (c) 2014 RadiaBeam Technologies. All rights reserved
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import math, sip
sip.setapi('QString', 2)

# SciPy imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

# PyQt4 imports
from PyQt4 import QtGui

# RadTrack imports
import radtrack.fields.RbGaussHermiteMN as hermite
from radtrack.ui.LaserInterface import Ui_LaserInterface
from radtrack.util.unitConversion import convertUnitsStringToNumber, convertUnitsNumber
from radtrack.util.plotTools import generateContourLevels


class LaserTab(QtGui.QWidget):
    acceptsFileTypes = ['sdds', 'csv']
    defaultTitle = 'Laser'
    task = 'Create a laser beam'
    category = 'beams'

    def __init__(self,parent=None):
        # initialization
        super(LaserTab, self).__init__(parent)
        self.ui = Ui_LaserInterface()
        self.ui.setupUi(self)

        # set default values
        self.numTicks = 5
        self.plotTitles = True

        self.lambda0 = 1.0e-06
        self.w0 = 20.e-06
        self.w0_z = 0.
        self.zR = math.pi*self.w0**2/self.lambda0    # Rayleigh range [m]

        # Define the maximum order(s) of the Hermite expansion
        self.mMax = 24

        # Create two instances of the Hermite expansion class
        self.hS1 = hermite.RbGaussHermiteMN(self.lambda0,self.w0,self.w0,0.)
        self.hS2 = hermite.RbGaussHermiteMN(self.lambda0,self.w0,self.w0,0.)

        # the laser pulse (to be instantiated later)
        self.myPulse = 0
        self.pulseInitialized = False

        # the external fields (used to find GH coefficients of laser pulse)
        self.externalFields = False

        # plotting flags
        self.plotTitles = True

        # link the simple push buttons to appropriate methods
        self.ui.generateCoeffs.clicked.connect(self.generateCoeffs)
        self.ui.noTitles.clicked.connect(self.togglePlotTitles)

        # create a menu for laser pulse generation
        pulseMenu = QtGui.QMenu(self)
        paraxialGaussian = QtGui.QAction("Paraxial approx - Gaussian",self)
        pulseMenu.addAction(paraxialGaussian)

        # associate these actions with class methods
        paraxialGaussian.triggered.connect(self.paraxialGaussian)

        # grab an existing button & insert the menu
        pulseButton = self.ui.generatePulse
        pulseButton.setMenu(pulseMenu)
        pulseButton.setPopupMode(QtGui.QToolButton.InstantPopup)

        # create a menu for external fields
        extFieldsMenu = QtGui.QMenu(self)
        mirrorWithHole = QtGui.QAction("Mirror with hole",self)
        extFieldsMenu.addAction(mirrorWithHole)

        # associate these actions with class methods
        mirrorWithHole.triggered.connect(self.mirrorWithHole)

        # grab an existing button & insert the menu
        extFieldsButton = self.ui.externalFields
        extFieldsButton.setMenu(extFieldsMenu)
        extFieldsButton.setPopupMode(QtGui.QToolButton.InstantPopup)

        # specify physical constants
        self.c     = 299792458.           # speed of light [m/s]
        self.cSq   = self.c**2            # speed of light squared
        self.cInv  = 1./self.c            # one over the speed of light
        self.mu0   = 4.0e-07 * math.pi    # permeability of free space
        self.eps0  = 1./self.mu0/self.cSq # permittivity of free space
        self.eMass   = 9.10938215e-31     # electron mass [kG]
        self.eCharge = 1.602176487e-19    # elementary charge [C]
        self.eMassEV = self.eMass*self.cSq/self.eCharge  # eMass [eV]

        # specify default values for all input fields
        self.ui.wavelength.setText("{:.0f}".format(self.lambda0*1.e+06) + ' um')
        self.ui.waistSize.setText("{:.0f}".format(self.w0*1.e+06) + ' um')
        self.ui.waistPosition.setText("{:.0f}".format(self.w0_z*1.e+3) + ' mm')

        self.unitsXY = 'um'
        self.unitsZ = 'mm'
        self.ui.unitsXY.setText(self.unitsXY)
        self.ui.unitsZ.setText(self.unitsZ)
        self.ui.numTicks.setText(str(self.numTicks))

        # load up the table of coefficients
        self.ui.ghTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.ui.ghTable.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)
        self.ui.ghTable.setItem(0,0,QtGui.QTableWidgetItem('1'))
        self.ui.ghTable.setItem(0,1,QtGui.QTableWidgetItem('1'))
        maxLoop = max(self.mMax, 100)
        for iLoop in range(1,maxLoop):
            self.ui.ghTable.setItem(iLoop,0,QtGui.QTableWidgetItem('0'))
            self.ui.ghTable.setItem(iLoop,1,QtGui.QTableWidgetItem('0'))

        # try to make the blank plotting regions look nice
        self.erasePlots()

    def paraxialGaussian(self):

        # get input from text boxes
        self.lambda0 = convertUnitsStringToNumber(self.ui.wavelength.text(), 'm')
        self.w0 = convertUnitsStringToNumber(self.ui.waistSize.text(), 'm')
        self.w0_z = convertUnitsStringToNumber(self.ui.waistPosition.text(), 'm')
        self.zR = math.pi*self.w0**2/self.lambda0    # horiz. Rayleigh range [m]

        # instantiate the laser pulse
        self.myPulse = hermite.RbGaussHermiteMN(self.lambda0,
                                                self.w0,
                                                self.w0,
                                                0.)

        # load up the coefficients
        mCoefs = np.zeros(8)
        nCoefs = np.zeros(8)
        for iLoop in range(8):
            mCoefs[iLoop] = float(self.ui.ghTable.item(iLoop,0).text())
            nCoefs[iLoop] = float(self.ui.ghTable.item(iLoop,1).text())

        self.myPulse.setMCoef(mCoefs)
        self.myPulse.setNCoef(nCoefs)

        # update flag accordingly
        self.pulseInitialized = True

        # generate the plots
        self.refreshPlots()

    def togglePlotTitles(self):
        self.plotTitles = not self.plotTitles
        self.refreshPlots()

    def refreshPlots(self):
        # nothing to plot, if beam hasn't been initialized
        if not self.pulseInitialized:
            return

        # get the specified units for plotting
        self.unitsXY = self.ui.unitsXY.text()
        self.unitsZ = self.ui.unitsZ.text()

        # get the number of tick marks
        self.numTicks = int(self.ui.numTicks.text())

        # Specify the desired grid size
        self.numZ = 64
        self.numX = 64
        self.numCellsZX = self.numZ * self.numX

        # specify the min's and max's
        self.minZ = self.w0_z - 4.*self.zR
        self.maxZ = self.w0_z + 4.*self.zR

        self.minX = -8.*self.w0
        self.maxX =  8.*self.w0

        self.plotXY()
        self.plotZY()
        self.plotZX()

    def plotZX(self):
        zArr  = np.zeros(self.numZ)
        xArr  = np.zeros(self.numX)

        for iLoop in range(self.numZ):
            zArr[iLoop] = self.minZ + iLoop * (self.maxZ-self.minZ) / (self.numZ-1)

        for jLoop in range(self.numX):
            xArr[jLoop] = self.minX + jLoop * (self.maxX-self.minX) / (self.numX-1)

        # specify y position for plot
        yValue = 0.

        # Calculate Ex at the 2D array of x,y values
        zxEData = np.zeros((self.numX, self.numZ))
        for iLoop in range(self.numZ):
            for jLoop in range(self.numX):
                zxEData[jLoop, iLoop] = np.real(self.myPulse.evalEnvelopeEx(xArr[jLoop], yValue, zArr[iLoop]))

        # generate the xy plot
        canvas = self.ui.zxPlot.canvas
        canvas.ax.clear()

        levels = generateContourLevels(zxEData)
        canvas.ax.contourf(zArr*convertUnitsNumber(1, 'm', self.unitsZ),
                           xArr*convertUnitsNumber(1, 'm', self.unitsXY),
                           zxEData, levels, extent='none', aspect='equal')

        canvas.ax.axis([self.minZ*convertUnitsNumber(1, 'm', self.unitsZ),
                        self.maxZ*convertUnitsNumber(1, 'm', self.unitsZ),
                        self.minX*convertUnitsNumber(1, 'm', self.unitsXY),
                        self.maxX*convertUnitsNumber(1, 'm', self.unitsXY)])
        canvas.ax.xaxis.set_major_locator(plt.MaxNLocator(self.numTicks))
        canvas.ax.yaxis.set_major_locator(plt.MaxNLocator(self.numTicks))
        canvas.ax.set_xlabel('z ['+self.unitsZ+']')
        canvas.ax.set_ylabel('x ['+self.unitsXY+']')
        if self.plotTitles:
            canvas.ax.set_title('ZX slice, at  y={0:4.2f} [{1}]'.format(yValue*convertUnitsNumber(1, 'm', self.unitsXY),
                                                                        self.unitsXY))
        canvas.fig.tight_layout()
        canvas.fig.set_facecolor('w')
        canvas.draw()

    def plotZY(self):
        freq0 = self.c / self.lambda0
        yLoc = 0.

        # Specify the desired grid size
        self.zyNumH = 64
        self.zyNumV = 64
        self.zyNumCells = self.zyNumH * self.zyNumV

        # specify the min's and max's
        self.zyMinH = -4.*self.lambda0
        self.zyMaxH =  4*self.lambda0

        self.zyMinV = -4.*self.w0
        self.zyMaxV =  4.*self.w0

        zArr = np.zeros(self.zyNumH)
        yArr = np.zeros(self.zyNumV)

        for iLoop in range(self.zyNumH):
            zArr[iLoop] = self.zyMinH + iLoop * (self.zyMaxH-self.zyMinH) / (self.zyNumH-1)

        for jLoop in range(self.zyNumV):
            yArr[jLoop] = self.zyMinV + jLoop * (self.zyMaxV-self.zyMinV) / (self.zyNumV-1)

        # Choose values of x,t for plot
        xValue = 0.
        tValue = 0.

        # Calculate Ex at the 2D array of x,y values
        zyEData = np.zeros((self.zyNumV, self.zyNumH))
        for iLoop in range(self.zyNumH):
            for jLoop in range(self.zyNumV):
                zyEData[jLoop, iLoop] = self.myPulse.evaluateEx(xValue, yArr[jLoop], zArr[iLoop], tValue)

        # generate the xy plot
        canvas = self.ui.zyPlot.canvas
        canvas.ax.clear()

        levels = generateContourLevels(zyEData)
        canvas.ax.contourf(zArr*convertUnitsNumber(1, 'm', self.unitsZ),
                           yArr*convertUnitsNumber(1, 'm', self.unitsXY),
                           zyEData, levels, extent='none', aspect='equal')
        # plt.colorbar(cs1, format='%3.2e')
        # plt.gcf().colorbar(contours, format='%3.2e')

        canvas.ax.axis([self.zyMinH*convertUnitsNumber(1, 'm', self.unitsZ),
                        self.zyMaxH*convertUnitsNumber(1, 'm', self.unitsZ),
                        self.zyMinV*convertUnitsNumber(1, 'm', self.unitsXY),
                        self.zyMaxV*convertUnitsNumber(1, 'm', self.unitsXY)])
        canvas.ax.xaxis.set_major_locator(plt.MaxNLocator(self.numTicks))
        canvas.ax.yaxis.set_major_locator(plt.MaxNLocator(self.numTicks))
        canvas.ax.set_xlabel('z ['+self.unitsZ+']')
        canvas.ax.set_ylabel('y ['+self.unitsXY+']')
        if self.plotTitles:
            canvas.ax.set_title('ZY slice, at  x={0:4.2f} [{1}]'.format(xValue*convertUnitsNumber(1, 'm', self.unitsXY),
                                                                        self.unitsXY))
        canvas.fig.tight_layout()
        canvas.fig.set_facecolor('w')
        canvas.draw()

    def plotXY(self):
        # Specify the desired grid size
        self.xyNumH = 64
        self.xyNumV = 64
        self.xyNumCells = self.xyNumH * self.xyNumV

        # specify the min's and max's
        self.xyMinH = -4.*self.w0
        self.xyMaxH =  4.*self.w0

        self.xyMinV = -4.*self.w0
        self.xyMaxV =  4.*self.w0

        xArr  = np.zeros(self.xyNumH)
        yArr  = np.zeros(self.xyNumV)
        xTmp  = np.zeros(self.xyNumV)

        for iLoop in range(self.xyNumH):
            xArr[iLoop] = self.xyMinH + iLoop * (self.xyMaxH-self.xyMinH) / (self.xyNumH-1)

        for jLoop in range(self.xyNumV):
            yArr[jLoop] = self.xyMinV + jLoop * (self.xyMaxV-self.xyMinV) / (self.xyNumV-1)

        # Calculate Ex at the 2D array of x,y values
        xyEData = np.zeros((self.xyNumV, self.xyNumH)) # interchange of V/H is weirdly necessary!?
        for iLoop in range(self.xyNumH):
            for jLoop in range(self.xyNumV):
                xTmp[jLoop] = xArr[iLoop]
            xyEData[0:self.xyNumV, iLoop] = \
                np.real(self.myPulse.evalEnvelopeEx(xTmp, yArr, self.w0_z))

        # generate the xy plot
        canvas = self.ui.xyPlot.canvas
        canvas.ax.clear()

        levels = generateContourLevels(xyEData)
        canvas.ax.contourf(xArr*convertUnitsNumber(1, 'm', self.unitsXY),
                           yArr*convertUnitsNumber(1, 'm', self.unitsXY),
                           xyEData, levels, extent='none', aspect='equal')

        # For some reason, I can't get the color bar to appear...
        #        contours = canvas.ax.contourf(xArr, yArr, xyEData, levels, extent='none', aspect='equal')
        #        plt.gcf().colorbar(contours, format='%3.2e')

        canvas.ax.axis([self.xyMinH*convertUnitsNumber(1, 'm', self.unitsXY),
                        self.xyMaxH*convertUnitsNumber(1, 'm', self.unitsXY),
                        self.xyMinV*convertUnitsNumber(1, 'm', self.unitsXY),
                        self.xyMaxV*convertUnitsNumber(1, 'm', self.unitsXY)])
        canvas.ax.xaxis.set_major_locator(plt.MaxNLocator(self.numTicks))
        canvas.ax.yaxis.set_major_locator(plt.MaxNLocator(self.numTicks))
        canvas.ax.set_xlabel('x ['+self.unitsXY+']')
        canvas.ax.set_ylabel('y ['+self.unitsXY+']')
        if self.plotTitles:
            canvas.ax.set_title('XY slice, at  z={0:4.2f} [{1}]'.format(self.w0_z*convertUnitsNumber(1, 'm', self.unitsZ),
                                                                        self.unitsZ))
        canvas.fig.tight_layout()
        canvas.fig.set_facecolor('w')
        canvas.draw()

    def mirrorWithHole(self):
        # toggle the corresponding flag
        self.externalFields = True

        # get input from text boxes
        self.lambda0 = convertUnitsStringToNumber(self.ui.wavelength.text(), 'm')
        self.w0 = convertUnitsStringToNumber(self.ui.waistSize.text(), 'm')
        self.w0_z = convertUnitsStringToNumber(self.ui.waistPosition.text(), 'm')
        self.zR = math.pi*self.w0**2/self.lambda0    # horiz. Rayleigh range [m]

        # load up the x,y locations of the mesh
        self.xMin = -4.*self.w0
        self.xMax =  4.*self.w0

        self.yMin = self.xMin
        self.yMax = self.xMax

        self.numPts = 64
        self.nCells = self.numPts**2

        self.xArr  = np.zeros(self.numPts)
        for iLoop in range(self.numPts):
            self.xArr[iLoop] = self.xMin + iLoop * (self.xMax-self.xMin) / (self.numPts-1)

        self.yArr  = np.zeros(self.numPts)
        for jLoop in range(self.numPts):
            self.yArr[jLoop] = self.yMin + jLoop * (self.yMax-self.yMin) / (self.numPts-1)

        self.xGrid = np.zeros((self.numPts, self.numPts))
        self.yGrid = np.zeros((self.numPts, self.numPts))

        for iLoop in range(self.numPts):
            for jLoop in range(self.numPts):
                self.xGrid[iLoop,jLoop] = self.xMin + iLoop * (self.xMax-self.xMin) / (self.numPts-1)
                self.yGrid[iLoop,jLoop] = self.yMin + jLoop * (self.yMax-self.yMin) / (self.numPts-1)

        # Create transverse field profile (#3 elliptical Gaussian donut)
        self.ExGridExternal = np.zeros((self.numPts, self.numPts))
        self.wx3  =  2.0 * self.w0
        self.rad1 =  1.0 * self.w0
        self.rad2 =  2.0 * self.w0
        for iLoop in range(self.numPts):
            for jLoop in range(self.numPts):
                xArg = self.xArr[iLoop]
                yArg = self.yArr[jLoop]
                rArg = math.sqrt(xArg**2 + yArg**2)
                rFactor = 1.0
                if rArg <= self.rad2:
                    rFactor = 0.5 + 0.5*math.cos(math.pi*((rArg-self.rad1)/(self.rad2-self.rad1) - 1.))
                if rArg <= self.rad1:
                    rFactor = 0.0
                self.ExGridExternal[iLoop, jLoop] = rFactor*math.exp(-(xArg/self.wx3)**2)*math.exp(-(yArg/self.wx3)**2)

        # generate the xy plot
        canvas = self.ui.xyPlotExtFields.canvas
        canvas.ax.clear()

        levels = generateContourLevels(self.ExGridExternal)
        canvas.ax.contourf(self.xGrid*convertUnitsNumber(1, 'm', self.unitsXY),
                           self.yGrid*convertUnitsNumber(1, 'm', self.unitsXY),
                           self.ExGridExternal, levels,
                           extent='none', aspect='equal')
        canvas.ax.xaxis.set_major_locator(plt.MaxNLocator(self.numTicks))
        canvas.ax.yaxis.set_major_locator(plt.MaxNLocator(self.numTicks))
        canvas.ax.set_xlabel('x ['+self.unitsXY+']')
        canvas.ax.set_ylabel('y ['+self.unitsXY+']')
        canvas.ax.axis([self.xMin*convertUnitsNumber(1, 'm', self.unitsXY),
                        self.xMax*convertUnitsNumber(1, 'm', self.unitsXY),
                        self.yMin*convertUnitsNumber(1, 'm', self.unitsXY),
                        self.yMax*convertUnitsNumber(1, 'm', self.unitsXY)])
        if self.plotTitles:
            canvas.ax.set_title('slice: quadratic square; at z={0:4.2f} [{1}]'.format(0.,self.unitsZ))

        canvas.fig.tight_layout()
        canvas.fig.set_facecolor('w')
        canvas.draw()

    def generateCoeffs(self):
        # check whether the external fields exist
        if not self.externalFields:
            return   # do nothing (should throw an exception)

        # set default values
        self.numFuncCalls = 0

        # choose initial guesses for all fitting parameters
        # also, specify the scale of variations for each
        paramGuess = np.zeros(2*self.mMax+2)
        paramGuess[0] = self.w0                  # horizontal waist
        paramGuess[1] = 1.0
        for ii in range(self.mMax-1):
            paramGuess[ii+2] = 1.e-5             # horiz. coeff's
        paramGuess[self.mMax+1] = 1.0
        for ii in range(self.mMax):
            paramGuess[self.mMax+1+ii] = 1.e-5   # vertical coeff's

        # invoke the least squares algorithm
        result = leastsq(self.residuals, paramGuess,
                         args=(np.reshape(self.ExGridExternal,self.nCells),
                         np.reshape(self.xGrid,self.nCells),
                         np.reshape(self.yGrid,self.nCells)),
                         full_output=True, ftol=1e-5,
                         maxfev=1200)

        parFit  = result[0]
        nEvals  = result[2]['nfev']
        resVals = result[2]['fvec']
        message = result[3]
        iError  = result[4]

        print(' ')
        print(' iError  = ', iError)
        print(' message = ', message)
        print(' nEvals  = ', nEvals)
        print(' resVals = ', resVals)

        # load the results into named variables (for clarity)
        wxFit = parFit[0]
        mCFit = np.zeros(self.mMax+1)
        for ii in range(self.mMax):
            mCFit[ii+1] = parFit[1+ii]
        nCFit = np.zeros(self.mMax+1)
        for ii in range(self.mMax+1):
            nCFit[ii] = parFit[self.mMax+1+ii]

        # check the results
        print(' ')
        print('The least squares minimization has completed:')
        print('  wx  = ', self.wx3, '; ', wxFit)
        self.ui.ghTable.setItem(0,0,QtGui.QTableWidgetItem(str(mCFit[0])))
        self.ui.ghTable.setItem(0,1,QtGui.QTableWidgetItem(nCFit[0]))

        # load the coefficient table in the GUI
        minLoop = min(self.mMax, 101)
        for iLoop in range(0,minLoop):
            self.ui.ghTable.setItem(iLoop,0,QtGui.QTableWidgetItem(str(mCFit[iLoop])))
            self.ui.ghTable.setItem(iLoop,1,QtGui.QTableWidgetItem(str(nCFit[iLoop])))

        maxLoop = max(self.mMax, 101)
        for iLoop in range(minLoop+1,maxLoop):
            self.ui.ghTable.setItem(iLoop,0,QtGui.QTableWidgetItem('0'))
            self.ui.ghTable.setItem(iLoop,1,QtGui.QTableWidgetItem('0'))

        # modify the laser pulse object, using these GH coefficients
        self.myPulse.setMCoef(mCFit)
        self.myPulse.setNCoef(nCFit)

        # regenerate the standard plots, using this new info
        self.refreshPlots()

    # Calculate residuals for the least squares analysis
    # params - array of fitting parameters
    def residuals(self, _params, _e, _x, _y):

        self.hS1.setWaistX(_params[0])
        self.hS1.setWaistY(_params[0])
        self.hS2.setWaistX(_params[0])
        self.hS2.setWaistY(_params[0])

        hCoefs = np.zeros(self.mMax+1)
        for ii in range(self.mMax):
            hCoefs[ii+1] = _params[1+ii]
        self.hS1.setMCoef(hCoefs)
        self.hS2.setNCoef(hCoefs)

        vCoefs = np.zeros(self.mMax+1)
        for ii in range(self.mMax+1):
            vCoefs[ii] = _params[self.mMax+1+ii]
        self.hS1.setNCoef(vCoefs)
        self.hS2.setMCoef(vCoefs)

        # let the user know what's going on if many function calls are required
        if self.numFuncCalls == 0:
            print(' ')
            print('Number of calls to method residual():')
        self.numFuncCalls += 1
        if 100*int(self.numFuncCalls/100.) == self.numFuncCalls:
            print('  ', self.numFuncCalls)

        return _e - np.real(self.hS1.evalEnvelopeEx(_x, _y, self.w0_z)) \
                  - np.real(self.hS2.evalEnvelopeEx(_x, _y, self.w0_z))

    def erasePlots(self):
        self.ui.xyPlot.canvas.ax.clear()
        self.ui.xyPlot.canvas.ax.axis([-1., 1., -1., 1.])

        self.ui.xyPlot.canvas.ax.set_xlabel('x ['+self.unitsXY+']')
        self.ui.xyPlot.canvas.ax.set_ylabel('y ['+self.unitsXY+']')
        self.ui.xyPlot.canvas.fig.tight_layout()
        self.ui.xyPlot.canvas.fig.set_facecolor('w')

        self.ui.zxPlot.canvas.ax.clear()
        self.ui.zxPlot.canvas.ax.axis([-1., 1., -1., 1.])
        self.ui.zxPlot.canvas.ax.set_xlabel('z ['+self.unitsZ+']')
        self.ui.zxPlot.canvas.ax.set_ylabel('x ['+self.unitsXY+']')
        self.ui.zxPlot.canvas.fig.tight_layout()
        self.ui.zxPlot.canvas.fig.set_facecolor('w')

        self.ui.zyPlot.canvas.ax.clear()
        self.ui.zyPlot.canvas.ax.axis([-1., 1., -1., 1.])
        self.ui.zyPlot.canvas.ax.set_xlabel('z ['+self.unitsZ+']')
        self.ui.zyPlot.canvas.ax.set_ylabel('y ['+self.unitsXY+']')
        self.ui.zyPlot.canvas.fig.tight_layout()
        self.ui.zyPlot.canvas.fig.set_facecolor('w')

    def importFile(self, fileName):
        pass

    def exportToFile(self, sddsFileName):
        with open(sddsFileName, 'w'):
            pass
