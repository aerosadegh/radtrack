"""
Module defining interactive window for laser pulses.

Imports the auto-generated RbLaserModeInterface.py module, which is
created via pyside-uic.exe from Qt's RbLaserModeInterface.ui file.

Here, the window is instantiated and hooks to the production
Python code are established.

moduleauthor:: David Bruhwiler <bruhwiler@radiasoft.net>
Copyright (c) 2014 RadiaBeam Technologies. All rights reserved
"""

# system imports
#from __future__ import absolute_import, division, print_function, unicode_literals
import os.path
#import subprocess

# Python imports
import math

# SciPy imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

# PyQt4 imports
import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui

# RadTrack imports
import radtrack.fields.RbGaussHermiteMN as hermite
from radtrack.ui.LaserInterface import Ui_LaserInterface
from radtrack.RbUtility import convertUnitsStringToNumber, convertUnitsNumber
import radtrack.plot.RbPlotUtils
import sys

import sdds

class LaserTab(QtGui.QWidget):

    def __init__(self,parent=None):
        # initialization
        super(LaserTab, self).__init__()
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

        # create a menu for saving files
        exportMenu = QtGui.QMenu(self)
        saveToCSV = QtGui.QAction("RadTrack CSV format",self)
        exportMenu.addAction(saveToCSV)
        saveToSDDS = QtGui.QAction("SRW SDDS format",self)
        exportMenu.addAction(saveToSDDS)

        # associate these actions with class methods
        saveToCSV.triggered.connect(self.saveToCSV)
        saveToSDDS.triggered.connect(self.saveToSDDS)

        # grab an existing button & insert the menu
        saveToFileButton = self.ui.saveToFile
        saveToFileButton.setMenu(exportMenu)
        saveToFileButton.setPopupMode(QtGui.QToolButton.InstantPopup)

        # create a menu for importing particle data
        importMenu = QtGui.QMenu(self)
        readFromCSV = QtGui.QAction("RadTrack CSV format",self)
        importMenu.addAction(readFromCSV)
        readFromSDDS = QtGui.QAction("SRW SDDS format",self)
        importMenu.addAction(readFromSDDS)

        self.acceptsFileTypes = ['sdds', 'csv']

        # associate these actions with class methods
        readFromCSV.triggered.connect(self.readFromCSV)
        readFromSDDS.triggered.connect(self.readFromSDDS)

        # grab an existing button & insert the menu
        importFileButton = self.ui.importFile
        importFileButton.setMenu(importMenu)
        importFileButton.setPopupMode(QtGui.QToolButton.InstantPopup)

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
        self.ui.ghTable.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)
        self.ui.ghTable.setItem(0,0,QtGui.QTableWidgetItem('1'))
        self.ui.ghTable.setItem(0,1,QtGui.QTableWidgetItem('1'))
        maxLoop = max(self.mMax, 100)
        for iLoop in range(1,maxLoop):
            self.ui.ghTable.setItem(iLoop,0,QtGui.QTableWidgetItem('0'))
            self.ui.ghTable.setItem(iLoop,1,QtGui.QTableWidgetItem('0'))

        # file directories
        self.parent = parent
        if self.parent is None:
            self.parent = self
            self.parent.lastUsedDirectory = os.path.expanduser('~')
        self.fileExtension = '.sdds'
        self.exportToFile = self.saveToSDDS
        self.importFile = self.readFromSDDS

        # try to make the blank plotting regions look nice
        self.erasePlots()

        self.container = QtGui.QScrollArea(parent)
        self.container.setWidget(self)
        self.defaultTitle = self.parent.tr('Laser')

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
        if self.plotTitles == True:
            self.plotTitles = False
        else:
            self.plotTitles = True
        self.refreshPlots()

    def refreshPlots(self):
        # nothing to plot, if beam hasn't been initialized
        if self.pulseInitialized == False:
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
        # instance of the plot utility class
        myPlotUtils = radtrack.plot.RbPlotUtils.RbPlotUtils()

        zArr  = np.zeros(self.numZ)
        xArr  = np.zeros(self.numX)

        for iLoop in range(self.numZ):
            zArr[iLoop] = self.minZ + iLoop * (self.maxZ-self.minZ) / (self.numZ-1)
#            print 'zArr[', iLoop, '] = ', zArr[iLoop]

        for jLoop in range(self.numX):
            xArr[jLoop] = self.minX + jLoop * (self.maxX-self.minX) / (self.numX-1)
#            print 'xArr[', jLoop, '] = ', xArr[jLoop]

        # specify y position for plot
        yValue = 0.

        # Calculate Ex at the 2D array of x,y values
        zxEData = np.zeros((self.numX, self.numZ))
        for iLoop in range(self.numZ):
            for jLoop in range(self.numX):
                zxEData[jLoop, iLoop] = np.real(self.myPulse.evalEnvelopeEx(xArr[jLoop], yValue, zArr[iLoop]))
#                print 'zxEData[', iLoop, jLoop, '] = ', zxEData[iLoop, jLoop]

        # generate the xy plot
        canvas = self.ui.zxPlot.canvas
        canvas.ax.clear()

        levels = myPlotUtils.generateContourLevels(zxEData)
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
        if self.plotTitles == True:
            canvas.ax.set_title('ZX slice, at  y={0:4.2f} [{1}]'.format(yValue*convertUnitsNumber(1, 'm', self.unitsXY),
                                                                        self.unitsXY))
        canvas.fig.tight_layout()
        canvas.fig.set_facecolor('w')
        canvas.draw()

    def plotZY(self):
        # instance of the plot utility class
        myPlotUtils = radtrack.plot.RbPlotUtils.RbPlotUtils()

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
#            print 'zArr[', iLoop, '] = ', zArr[iLoop]

        for jLoop in range(self.zyNumV):
            yArr[jLoop] = self.zyMinV + jLoop * (self.zyMaxV-self.zyMinV) / (self.zyNumV-1)
#            print 'xArr[', jLoop, '] = ', xArr[jLoop]

        # Choose values of x,t for plot
        xValue = 0.
        tValue = 0.

        # Calculate Ex at the 2D array of x,y values
        zyEData = np.zeros((self.zyNumV, self.zyNumH))
        for iLoop in range(self.zyNumH):
            for jLoop in range(self.zyNumV):
                zyEData[jLoop, iLoop] = self.myPulse.evaluateEx(xValue, yArr[jLoop], zArr[iLoop], tValue)
#                print 'zyEData[', iLoop, jLoop, '] = ', zyEData[iLoop, jLoop]

        # generate the xy plot
        canvas = self.ui.zyPlot.canvas
        canvas.ax.clear()

        levels = myPlotUtils.generateContourLevels(zyEData)
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
        if self.plotTitles == True:
            canvas.ax.set_title('ZY slice, at  x={0:4.2f} [{1}]'.format(xValue*convertUnitsNumber(1, 'm', self.unitsXY),
                                                                        self.unitsXY))
        canvas.fig.tight_layout()
        canvas.fig.set_facecolor('w')
        canvas.draw()

    def plotXY(self):
        # instance of the plot utility class
        myPlotUtils = radtrack.plot.RbPlotUtils.RbPlotUtils()

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

        levels = myPlotUtils.generateContourLevels(xyEData)
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
        if self.plotTitles == True:
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

        myPlotUtils = radtrack.plot.RbPlotUtils.RbPlotUtils()
        levels = myPlotUtils.generateContourLevels(self.ExGridExternal)
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
        if self.plotTitles == True:
            canvas.ax.set_title('slice: quadratic square; at z={0:4.2f} [{1}]'.format(0.,self.unitsZ))

        canvas.fig.tight_layout()
        canvas.fig.set_facecolor('w')
        canvas.draw()

    def generateCoeffs(self):
        # check whether the external fields exist
        if self.externalFields == False:
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

        print ' '
        print ' iError  = ', iError
        print ' message = ', message
        print ' nEvals  = ', nEvals
        print ' resVals = ', resVals

        # load the results into named variables (for clarity)
        wxFit = parFit[0]
        mCFit = np.zeros(self.mMax+1)
        for ii in range(self.mMax):
            mCFit[ii+1] = parFit[1+ii]
        nCFit = np.zeros(self.mMax+1)
        for ii in range(self.mMax+1):
            nCFit[ii] = parFit[self.mMax+1+ii]

        # check the results
        print ' '
        print 'The least squares minimization has completed:'
        print '  wx  = ', self.wx3, '; ', wxFit
        self.ui.ghTable.setItem(0,0,QTableWidgetItem(str(mCFit[0])))
        self.ui.ghTable.setItem(0,1,QTableWidgetItem(nCFit[0]))

        # load the coefficient table in the GUI
        minLoop = min(self.mMax, 101)
        for iLoop in range(0,minLoop):
            self.ui.ghTable.setItem(iLoop,0,QTableWidgetItem(str(mCFit[iLoop])))
            self.ui.ghTable.setItem(iLoop,1,QTableWidgetItem(str(nCFit[iLoop])))

        maxLoop = max(self.mMax, 101)
        for iLoop in range(minLoop+1,maxLoop):
            self.ui.ghTable.setItem(iLoop,0,QTableWidgetItem('0'))
            self.ui.ghTable.setItem(iLoop,1,QTableWidgetItem('0'))

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
            print ' '
            print 'Number of calls to method residual():'
        self.numFuncCalls += 1
        if 100*int(self.numFuncCalls/100.) == self.numFuncCalls:
            print '  ', self.numFuncCalls

#        xDum = np.real(self.myPulse.evalEnvelopeEx(xTmp, yArr, self.w0_z))
        return _e - np.real(self.hS1.evalEnvelopeEx(_x, _y, self.w0_z)) \
                  - np.real(self.hS2.evalEnvelopeEx(_x, _y, self.w0_z))

    def erasePlots(self):
        self.ui.xyPlot.canvas.ax.clear()
        self.ui.xyPlot.canvas.ax.axis([-1., 1., -1., 1.])

        self.ui.xyPlot.canvas.ax.set_xlabel('x ['+self.unitsXY+']')
        self.ui.xyPlot.canvas.ax.set_ylabel('y ['+self.unitsXY+']')
#        if self.plotTitles == True:
#            self.ui.xyPlot.canvas.ax.set_title('cross-section')
        self.ui.xyPlot.canvas.fig.tight_layout()
        self.ui.xyPlot.canvas.fig.set_facecolor('w')

        self.ui.zxPlot.canvas.ax.clear()
        self.ui.zxPlot.canvas.ax.axis([-1., 1., -1., 1.])
        self.ui.zxPlot.canvas.ax.set_xlabel('z ['+self.unitsZ+']')
        self.ui.zxPlot.canvas.ax.set_ylabel('x ['+self.unitsXY+']')
#        if self.plotTitles == True:
#            self.ui.zxPlot.canvas.ax.set_title('cross-section')
        self.ui.zxPlot.canvas.fig.tight_layout()
        self.ui.zxPlot.canvas.fig.set_facecolor('w')
#        self.ui.zxPlot.canvas.draw()

        self.ui.zyPlot.canvas.ax.clear()
        self.ui.zyPlot.canvas.ax.axis([-1., 1., -1., 1.])
        self.ui.zyPlot.canvas.ax.set_xlabel('z ['+self.unitsZ+']')
        self.ui.zyPlot.canvas.ax.set_ylabel('y ['+self.unitsXY+']')
#        if self.plotTitles == True:
#            self.ui.zyPlot.canvas.ax.set_title('cross-section')
        self.ui.zyPlot.canvas.fig.tight_layout()
        self.ui.zyPlot.canvas.fig.set_facecolor('w')
#        self.ui.zyPlot.canvas.draw()

    def calculateLimits(self, _arr):
        # nothing to do, if beam hasn't been initialized
        if self.pulseInitialized == False:
            return

    def readFromSDDS(self, fileName = None):
        # use Qt file dialog
        if not fileName:
            fileName = QFileDialog.getOpenFileName(self, "Import Elegant/SDDS particle file -- ",
                                                  self.parent.lastUsedDirectory, "*.sdds")
        # if user cancels out, do nothing
        if fileName == '':
            return

        self.parent.lastUsedDirectory = os.path.dirname(fileName)
        base, ext = os.path.splitext(fileName)

        # throw exception for bad extensions
        if ext != '.sdds':
            msgBox = QtGui.QMessageBox()
            message  = 'ERROR --\n\n'
            message += '  The selected file extension "' + ext + '" is invalid.\n'
            message += '  Please select a file with extension ".sdds" - thanks!'
            msgBox.setText(message)
            msgBox.exec_()

        if False:
            print ' '
            print ' File to be parsed: ', fileName

        # index is always zero...?
        sddsIndex = 0

        # initialize sdds.sddsdata.pyd library (Windows only) with data file
        if sdds.sddsdata.InitializeInput(sddsIndex, fileName) != 1:
            sdds.sddsdata.PrintErrors(2)

        # get data storage mode...?
        sddsStorageMode = sdds.sddsdata.GetMode(sddsIndex)
        if False:
            print ' Storage mode for index ', sddsIndex, ': ', sddsStorageMode

        # get description text...?
        sddsDescription = sdds.sddsdata.GetDescription(sddsIndex)
        if False:
            print ' Description for index ', sddsIndex, ': ', sddsDescription

        # get parameter names
        paramNames = sdds.sddsdata.GetParameterNames(sddsIndex)
        numParams = len(paramNames)
        if False:
            print ' numParams = ', numParams
            print ' Parameter names for index ', sddsIndex, ': \n', paramNames

        # get parameter definitions
        paramDefs = range(numParams)
        for iLoop in range(numParams):
            paramDefs[iLoop] = sdds.sddsdata.GetParameterDefinition(sddsIndex,paramNames[iLoop])
            if False:
                print ' paramDefs[',iLoop,'] = ', paramDefs[iLoop]

        # give the user a look at the parameters (if any)
        msgBox = QtGui.QMessageBox()
        if numParams == 0:
            message  = 'WARNING --\n\n'
            message += 'No parameters were found in your selected SDDS file!!\n\n'
            message += 'It will be impossible to set the design momentum, or\n'
            message += '    the total beam charge, etc.'
        else:
            message  = 'The parameter names in your selected SDDS file are: \n'
            for iLoop in range(numParams):
                message += '    ' + paramNames[iLoop] + '\n'
            message += 'The parameter definitions in the file are: \n'
            for iLoop in range(numParams):
                message += '    ' + str(paramDefs[iLoop]) + '\n\n'
            message += 'WARNING --\n'
            message += '  Logic for extracting the design momentum, total beam\n'
            message += '  charge, etc. has not yet been implemented!'
        msgBox.setText(message)
        msgBox.exec_()

        # get column names
        columnNames = sdds.sddsdata.GetColumnNames(sddsIndex)
        numColumns = len(columnNames)
        if False:
            print ' numColumns = ', numColumns
            print ' Column names for index ', sddsIndex, ': \n', columnNames

        # initialize the parameter arrays
        paramData = range(numParams)
        for iLoop in range(numParams):
            paramData[iLoop] = []

        # column data has to be handled differently;
        #   it will be a 6D python array of N-D NumPy arrays
        columnData = range(numColumns)

        # read parameter data from the SDDS file
        # mus read particle data at the same time
        errorCode = sdds.sddsdata.ReadPage(sddsIndex)
#        print ' '
#        print ' errorCode = ', errorCode
        if errorCode != 1:
            sdds.sddsdata.PrintErrors(2)
        while errorCode > 0:
            for iLoop in range(numParams):
                paramData[iLoop].append(sdds.sddsdata.GetParameter(sddsIndex,iLoop))
            for jLoop in range(numColumns):
                tmpData = []
                tmpData.append(sdds.sddsdata.GetColumn(sddsIndex,jLoop))

                if False:
                    print ' '
                    print ' jLoop = ', jLoop
                    print ' tmpData = ', tmpData

                columnData[jLoop] = np.array(tmpData[0])

                if False:
                    print ' '
                    print ' columnData[', jLoop, '] = ', columnData[jLoop]

            errorCode = sdds.sddsdata.ReadPage(sddsIndex)

        # logic for deciphering and making use of parameter data goes here!

        # check whether the particle data is 6D
        if numColumns != 6:
            msgBox = QtGui.QMessageBox()
            message  = 'ERROR --\n\n'
            message += '  Particle data in the selected SDDS file is not 6D!\n\n'
            message += '  Column names are: \n'
            message += '    ' + str(columnNames) + '\n\n'
            message += 'Please select another file.\n'
            message += 'Thanks!'
            msgBox.setText(message)
            msgBox.exec_()
            return

        # get column definitions
        # units are in the 2nd column
        columnDefs = range(numColumns)
        unitStrings = range(numColumns)
        for iLoop in range(numColumns):
            columnDefs[iLoop] = sdds.sddsdata.GetColumnDefinition(sddsIndex,columnNames[iLoop])
            unitStrings[iLoop] = columnDefs[iLoop][1]
            if False:
                print ' columnDefs[',iLoop,'] = ', columnDefs[iLoop]
                print ' unitStrings[',iLoop,'] = ', unitStrings[iLoop]

        # begin deciphering the column data
        dataRead = [False, False, False, False, False, False]
        dataIndex = [-1, -1, -1, -1, -1, -1]
        for iLoop in range(6):
            if columnNames[iLoop]=='x' or columnNames[iLoop]=='X':
                if dataRead[0] == True:
                    message  = 'Error -- \n\n'
                    message += '  X column appears twice, for iLoop = '
                    message += str(dataIndex[0]) + ' and ' + str(iLoop)
                dataRead[0] = True
                dataIndex[0] = iLoop
            if columnNames[iLoop]=='xp' or columnNames[iLoop]=='px' or columnNames[iLoop]=="x'":
                if dataRead[1] == True:
                    message  = 'Error -- \n\n'
                    message += '  XP column appears twice, for iLoop = '
                    message += str(dataIndex[1]) + ' and ' + str(iLoop)
                dataRead[1] = True
                dataIndex[1] = iLoop
            if columnNames[iLoop]=='y' or columnNames[iLoop]=='Y':
                if dataRead[2] == True:
                    message  = 'Error -- \n\n'
                    message += '  Y column appears twice, for iLoop = '
                    message += str(dataIndex[2]) + ' and ' + str(iLoop)
                dataRead[2] = True
                dataIndex[2] = iLoop
            if columnNames[iLoop]=='yp' or columnNames[iLoop]=='py' or columnNames[iLoop]=="y'":
                if dataRead[3] == True:
                    message  = 'Error -- \n\n'
                    message += '  YP column appears twice, for iLoop = '
                    message += str(dataIndex[3]) + ' and ' + str(iLoop)
                dataRead[3] = True
                dataIndex[3] = iLoop
            if columnNames[iLoop]=='s' or columnNames[iLoop]=='ct' or columnNames[iLoop]=='t':
                if dataRead[4] == True:
                    message  = 'Error -- \n\n'
                    message += '  S column appears twice, for iLoop = '
                    message += str(dataIndex[4]) + ' and ' + str(iLoop)
                dataRead[4] = True
                dataIndex[4] = iLoop
            if columnNames[iLoop]=='p' or columnNames[iLoop]=='pt' or columnNames[iLoop]=='dp':
                if dataRead[5] == True:
                    message  = 'Error -- \n\n'
                    message += '  DP column appears twice, for iLoop = '
                    message += str(dataIndex[5]) + ' and ' + str(iLoop)
                dataRead[5] = True
                dataIndex[5] = iLoop

        # initial validation of the column data
        for iLoop in range(6):
            if dataRead[iLoop] == False:
                msgBox = QtGui.QMessageBox()
                message  = 'ERROR --\n\n'
                message += '  Not all of the data columns could be correctly interpreted!\n'
                message += '  These are the column headings that were parsed from the file:\n'
                message += '    ' + str(columnNames) + '\n\n'
                message += 'The parsing logic failed on: ' + columnNames[iLoop] + '\n'
                message += 'The code is looking for [x, xp, y, yp, s, dp] or something similar.'
                msgBox.setText(message)
                msgBox.exec_()
                return

        # check for unspecified units, and set them to default value
        # if the units are specified, but incorrect, the problem is detected below
        defaultUnits = ['m', 'rad', 'm', 'rad', 'm', 'rad']
        for iLoop in range(6):
#            print ' before: unitStrings[', iLoop, '] = ', unitStrings[iLoop]
            if unitStrings[iLoop] == '':
                unitStrings[iLoop] = defaultUnits[dataIndex[iLoop]]
#            print ' after: unitStrings[', iLoop, '] = ', unitStrings[iLoop]

        if False:
            print ' '
            print ' Here is columnData[:]:'
            print columnData

        # check that all data columns are the same length
        numElements = [0, 0, 0, 0, 0, 0]
        for iLoop in range(6):
            numElements[iLoop] = len(columnData[iLoop])
#            print ' size of column # ', iLoop, ' = ', numElements[iLoop]

        for iLoop in range(5):
            if numElements[iLoop+1] != numElements[0]:
                msgBox = QtGui.QMessageBox()
                message  = 'ERROR --\n\n'
                message += '  Not all of the data columns have the same length!\n'
                message += '  Here is the number of elements found in each column:\n'
                message += '    ' + str(numElements) + '\n\n'
                message += 'Please try again with a valid particle file...'
                message += 'Thanks!'
                msgBox.setText(message)
                msgBox.exec_()
                return

        # now we know the number of macro-particles
        numParticles = numElements[0]
#        print ' '
#        print ' numParticles = ', numParticles

        # all seems to be well, so load particle data into local array,
        #   accounting for any non-standard physical units
        tmp6 = np.zeros((6,numParticles))
        for iLoop in range(6):
            tmp6[dataIndex[iLoop],:] = columnData[iLoop]

        # another sanity check
#        myShape = np.shape(tmp6)
#        print ' '
#        print ' myShape = ', myShape

        # close the SDDS particle file
        if sdds.sddsdata.Terminate(sddsIndex) != 1:
            sdds.sddsdata.PrintErrors(2)

        # instantiate the particle bunch
        self.myBunch = beam.RbParticleBeam6D(numParticles)
        self.myBunch.setDesignMomentumEV(self.designMomentumEV)
        self.myBunch.setMassEV(self.eMassEV)     # assume electrons
        self.pulseInitialized = True

        # load particle array into the phase space object
        self.myBunch.getDistribution6D().getPhaseSpace6D().setArray6D(tmp6)

        # post top-level parameters to GUI
        self.ui.numPtcls.setText("{:d}".format(numParticles))
        self.ui.designMomentum.setText("{:.0f}".format(self.designMomentumEV*1.e-6) + ' MeV')
        self.ui.totalCharge.setText("{:.0f}".format(self.totalCharge*1.e9) + ' nC')

        # calculate bunch statistics and populate text boxes
        self.calculateTwiss()

        # plot the results
        self.refreshPlots()

    def readFromCSV(self, fileName = None):
        if fileName is None or fileName == '':
            fileName = QtGui.QFileDialog.getOpenFileName(self, "Import RadTrack particle file -- ",
                                                      self.parent.lastUsedDirectory, "*.csv")
            if fileName == '':
                return
            self.parent.lastUsedDirectory = os.path.dirname(fileName)

        base, ext = os.path.splitext(fileName)

        # notify user about bad extensions
        if ext != '.csv':
            msgBox = QtGui.QMessageBox()
            message  = 'ERROR --\n\n'
            message += '  The selected file extension "' + ext + '" is invalid.\n'
            message += '  Please select a file with extension ".csv" - thanks!'
            msgBox.setText(message)
            msgBox.exec_()

        # check whether this is a RadTrack generated CSV file
        fileObject = open(fileName)
        csvReader = csv.reader(fileObject, delimiter=',')
        lineNumber = 0
        for rawData in csvReader:
            lineNumber += 1

            # for testing purposes
            if False:
                print ' '
                print ' lineNumber = ', lineNumber
                print ' rawData = ', rawData

            # make sure this file follows the RadTrack format
            if lineNumber == 1:
                if rawData[0] != 'RadTrack':
                    fileObject.close()
                    msgBox = QtGui.QMessageBox()
                    message  = 'ERROR --\n\n'
                    message += '  The selected CSV file was not generated by RadTrack.\n'
                    message += '  Please select another file.\n\n'
                    message += 'Thanks!'
                    msgBox.setText(message)
                    msgBox.exec_()
            # ignore the 2nd line
            elif lineNumber == 2:
                continue
            # 3rd line contains the parametic data
            elif lineNumber == 3:
                self.designMomentumEV = float(rawData[0])
                self.totalCharge = float(rawData[1])
                # for testing only
                if False:
                    print ' '
                    print ' p0 = ', self.designMomentumEV
                    print ' Q  = ', self.totalCharge
            # don't read beyond the first three lines
            elif lineNumber > 3:
                break

        # close the file
        fileObject.close()

        # load file into temporary data array
        tmp6 = np.loadtxt(fileName,dtype=float,skiprows=5,delimiter=',',unpack=True)

        # check whether the particle data is 6D
        arrayShape = np.shape(tmp6)
        numDimensions = arrayShape[0]
        if numDimensions != 6:
            msgBox = QtGui.QMessageBox()
            message  = 'ERROR --\n\n'
            message += '  Particle data in the selected CSV file is not 6D!\n'
            message += '  Please select another file.\n\n'
            message += 'Thanks!'
            msgBox.setText(message)
            msgBox.exec_()
            return

        # store the number of particles read from the file
        numParticles = arrayShape[1]

        # instantiate the particle bunch
        self.myBunch = beam.RbParticleBeam6D(numParticles)
        self.myBunch.setDesignMomentumEV(self.designMomentumEV)
        self.myBunch.setMassEV(self.eMassEV)     # assume electrons
        self.pulseInitialized = True

        # load particle array into the phase space object
        self.myBunch.getDistribution6D().getPhaseSpace6D().setArray6D(tmp6)

        # for testing purposes only
        if False:
            print ' '
            print ' numParticles = ', numParticles
            q6 = self.myBunch.getDistribution6D().getPhaseSpace6D().getArray6D()
            print ' 1st particle: ', q6[:,0]

        # post top-level parameters to GUI
        self.ui.numPtcls.setText("{:d}".format(numParticles))
        self.ui.designMomentum.setText("{:.0f}".format(self.designMomentumEV*1.e-6) + ' MeV')
        self.ui.totalCharge.setText("{:.0f}".format(self.totalCharge*1.e9) + ' nC')

        # calculate bunch statistics and populate text boxes
        self.calculateTwiss()

        # plot the results
        self.refreshPlots()

    def saveToCSV(self, fileName = None):
        if fileName is None or fileName == '':
            fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save distribution to RadTrack file ...',
                             self.parent.lastUsedDirectory, "*.csv")
            if fileName == '':
                return
            if not fileName.endswith('.csv'):
                fileName = fileName + '.csv'
            self.parent.lastUsedDirectory = os.path.dirname(fileName)

        base, ext = os.path.splitext(fileName)

        # throw exception for bad extensions
        if ext != '.csv':
            msgBox = QtGui.QMessageBox()
            message  = 'ERROR --\n\n'
            message += '  The specified file extension "' + ext + '" is not ".csv"!\n'
            message += '  Please try again, but be sure to specify a ".csv" extension.\n\n'
            message += 'Thanks!'
            msgBox.setText(message)
            msgBox.exec_()
            return

        # make sure the top-level parameters are up-to-date
        self.designMomentumEV = convertUnitsStringToNumber(self.ui.designMomentum.text(), 'eV')
        self.totalCharge = convertUnitsStringToNumber(self.ui.totalCharge.text(), 'C')

        # create local pointer to particle array
        tmp6 = self.myBunch.getDistribution6D().getPhaseSpace6D().getArray6D()
        numParticles = tmp6.shape[1]

        # create a header to identify this as a RadTrack file
        h1 = 'RadTrack,Copyright 2012-2014 by RadiaBeam Technologies LLC - All rights reserved (C)\n '
        # names of the top-level parameters
        h2 = 'p0 [eV],Q [C],mass [eV]\n '
        # values of the top-level parameters
        h3 = str(self.designMomentumEV)+','+str(self.totalCharge)+','+str(self.eMassEV)+'\n '
        # label the columns
        h4 = 'x,xp,y,yp,s,dp\n '
        # specify the units
        h5 = '[m],[rad],[m],[rad],[m],[rad]'
        # assemble the full header
        myHeader = h1 + h2 + h3 + h4 + h5
        # write particle data into the file
        #   The following ugliness is used to accommodate savetxt()
        #   There is probably a better way...
        f6 = np.zeros((numParticles,6))
        f6[:,0] = tmp6[0,:]
        f6[:,1] = tmp6[1,:]
        f6[:,2] = tmp6[2,:]
        f6[:,3] = tmp6[3,:]
        f6[:,4] = tmp6[4,:]
        f6[:,5] = tmp6[5,:]
        np.savetxt(fileName, f6, fmt='%.12e', delimiter=',', comments='', header=myHeader)

    def saveToSDDS(self, sddsFileName = None):
        if sddsFileName is None or sddsFileName == '':
            sddsFileName = QtGui.QFileDialog.getSaveFileName(self, 'Save distribution to Elegant/SDDS file ...',
                              self.parent.lastUsedDirectory, "*.sdds")
            if sddsFileName == '':
                return
            if not sddsFileName.endswith(".sdds"):
                sddsFileName = sddsFileName + ".sdds"
            self.parent.lastUsedDirectory = os.path.dirname(sddsFileName)

        base, ext = os.path.splitext(sddsFileName)

        # check for bad extensions
        if ext != '.sdds':
            msgBox = QtGui.QMessageBox()
            message  = 'ERROR --\n\n'
            message += '  The specified file extension "' + ext + '" is not ".sdds"!\n'
            message += '  Please try again, but be sure to specify a ".sdds" extension.\n\n'
            message += 'Thanks!'
            msgBox.setText(message)
            msgBox.exec_()
            return

        # make sure the top-level parameters are up-to-date
        self.designMomentumEV =convertUnitsStringToNumber(self.ui.designMomentum.text(), 'eV')
        self.totalCharge = convertUnitsStringToNumber(self.ui.totalCharge.text(), 'C')

        # create local pointer to particle array
        tmp6 = self.myBunch.getDistribution6D().getPhaseSpace6D().getArray6D()

        mySDDS = sdds.SDDS(0)
        mySDDS.description[0] = "RadTrack"
        mySDDS.description[1] = "Copyright 2013-2014 by RadiaBeam Technologies. All rights reserved."
        mySDDS.parameterName = ["designMomentumEV", "totalCharge", "eMassEV"]
        mySDDS.parameterData = [[self.designMomentumEV],
                                [self.totalCharge],
                                [self.eMassEV]]
        mySDDS.parameterDefinition = [["","","","",mySDDS.SDDS_DOUBLE,""],
                                      ["","","","",mySDDS.SDDS_DOUBLE,""],
                                      ["","","","",mySDDS.SDDS_DOUBLE,""]]
        mySDDS.columnName = ["x", "xp", "y", "yp", "s", "dp"]
        mySDDS.columnData = [[list(tmp6[0,:])], [list(tmp6[1,:])],
                             [list(tmp6[2,:])], [list(tmp6[3,:])],
                             [list(tmp6[4,:])], [list(tmp6[5,:])]]

        if False:
            print ' '
            print ' Here is mySDDS.columnData[:]:'
            print mySDDS.columnData

        mySDDS.columnDefinition = [["","m",  "","",mySDDS.SDDS_DOUBLE,0],
                                   ["","rad","","",mySDDS.SDDS_DOUBLE,0],
                                   ["","m",  "","",mySDDS.SDDS_DOUBLE,0],
                                   ["","rad","","",mySDDS.SDDS_DOUBLE,0],
                                   ["","m",  "","",mySDDS.SDDS_DOUBLE,0],
                                   ["","rad","","",mySDDS.SDDS_DOUBLE,0]]
        mySDDS.save(sddsFileName)

"""
    def doStuff(self):
        # get output from text boxes
        hcoef = int(self.ui.hModeInput.text())
        vcoef = int(self.ui.vModeInput.text())

        # Specify the desired grid size
        xyNumH = 128
        xyNumV = 128
        xyNumCells = xyNumH * xyNumV

        # Specify the laser beam parameters
        wavelength = 10.e-06         # central wavelength [m]
        w0x = 10.*wavelength  # w0 at z=0.

        # load up the x,y locations of the mesh [m]
        xyMinH = -8.*w0x
        xyMaxH =  8.*w0x
        xyMinV = xyMinH
        xyMaxV = xyMaxH

        xArr  = np.zeros(xyNumH)
        xGrid = np.zeros((xyNumH, xyNumV))
        yArr  = np.zeros(xyNumV)
        yGrid = np.zeros((xyNumH, xyNumV))
        for iLoop in range(xyNumH):
            xArr[iLoop] = xyMinH + iLoop * (xyMaxH-xyMinH) / (xyNumH-1)

        for jLoop in range(xyNumV):
            yArr[jLoop] = xyMinV + jLoop * (xyMaxV-xyMinV) / (xyNumV-1)

        for iLoop in range(xyNumH):
            for jLoop in range(xyNumV):
                xGrid[iLoop,jLoop] = xyMinH + iLoop * (xyMaxH-xyMinH) / (xyNumH-1)
                yGrid[iLoop,jLoop] = xyMinV + jLoop * (xyMaxV-xyMinV) / (xyNumV-1)

        # Create a class instance for mode 0,0 (Gaussian)
        exMax = 1.3e+09
        gh00 = RbGaussHermiteMN.RbGaussMN(wavelength,w0x,2.0*w0x,0.)
        gh00.setCoeffSingleModeX(hcoef, exMax)
        gh00.setCoeffSingleModeY(vcoef, 1.)

        # Calculate Ex at the 2D array of x,y values
        Ex = np.reshape(gh00.evaluateEx(np.reshape(xGrid,xyNumCells),   \
                                        np.reshape(yGrid,xyNumCells), 0., 0.), (xyNumH, xyNumV))

        # Create scaled values, so the plot can show microns, rather than meters
        x_nm  = xGrid*1.e6
        xL_nm = xyMinH *1.e6
        xR_nm = xyMaxH *1.e6

        y_nm  = yGrid*1.e6
        yL_nm = xyMinV *1.e6
        yR_nm = xyMaxV *1.e6

        self.ui.widget.canvas.ax.clear()
        self.ui.widget.canvas.ax.contourf(x_nm, y_nm, Ex, 20)
        self.ui.widget.canvas.draw()
"""

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = LaserTab()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
