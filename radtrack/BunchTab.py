# -*- coding: utf-8 -*-
u"""Interactive window for charged particle bunches

Imports the auto-generated RbBunchInterface.py module, which is
created via pyside-uic.exe from Qt's RbBunchInterface.ui file.

Here, the window is instantiated and hooks to the production Python code are established.

:copyright: Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import sys, re, os, time, math, csv

# SciPy imports
import numpy as np
import matplotlib.pyplot as plt

# PyQt4 imports
from PyQt4 import QtGui

# RadTrack imports
import radtrack.bunch.RbParticleBeam6D as beam
import radtrack.statistics.RbStatistics6D as stat
from radtrack.ui.BunchInterface import Ui_bunchInterface
import radtrack.RbUtility as util

import sdds

class BunchTab(QtGui.QWidget):
    acceptsFileTypes = ['sdds', 'csv', 'out', 'bun']
    defaultTitle = 'Bunch'
    task = 'Create an electron beam'
    category = 'beams'

    def __init__(self,parent=None):       # initialization
        super(BunchTab, self).__init__()
        self.ui = Ui_bunchInterface()
        self.ui.setupUi(self)

        # set default values for flags
        self.numTicks = 5
        self.plotFlag = 'scatter'
        self.axisFlag = 'symmetric'
        self.plotTitles = True
        self.longTwissFlag = 'alpha-bct-dp'
        self.perpTwissFlag = 'rms-geometric'
        self.myBunch = None
        self.distributionFlag = 'gaussian'
        self.xyAspectRatioSquare = True

        # link the simple push buttons to appropriate methods
        self.ui.calculateTwiss.clicked.connect(self.calculateTwiss)
        self.ui.aspectRatio.clicked.connect(self.toggleAspectRatio)
        self.ui.noTitles.clicked.connect(self.togglePlotTitles)

        # define the generateBunch button
        self.ui.generateBunch.clicked.connect(lambda : self.generateBunch())

        # create a menu for defining the distribution type (need to rename)
        bunchMenu = QtGui.QMenu(self)
        radtrackGaussian = QtGui.QAction("RadTrack - gaussian",self)
        bunchMenu.addAction(radtrackGaussian)
#        radtrackUniform = QtGui.QAction("RadTrack - uniform",self)
#        bunchMenu.addAction(radtrackUniform)
#        elegantGaussian = QtGui.QAction("Elegant - gaussian",self)
#        bunchMenu.addAction(elegantGaussian)

        # associate these actions with class methods
        radtrackGaussian.triggered.connect(self.radtrackGaussian)
 #       radtrackUniform.triggered.connect(self.radtrackUniform)
 #       elegantGaussian.triggered.connect(self.elegantGaussian)

        # define the distribTypeButton
        distribTypeButton = self.ui.distribType
        distribTypeButton.setMenu(bunchMenu)
        distribTypeButton.setPopupMode(QtGui.QToolButton.InstantPopup)

        # create a menu for plot type
        plotsMenu = QtGui.QMenu(self)
        scatterPlots = QtGui.QAction("scatter",self)
        plotsMenu.addAction(scatterPlots)
        contourPlots = QtGui.QAction("contour",self)
        plotsMenu.addAction(contourPlots)
        comboPlots = QtGui.QAction("combo",self)
        plotsMenu.addAction(comboPlots)
        erasePlots = QtGui.QAction("erase",self)
        plotsMenu.addAction(erasePlots)

        # associate these actions with class methods
        scatterPlots.triggered.connect(self.scatterPlots)
        contourPlots.triggered.connect(self.contourPlots)
        comboPlots.triggered.connect(self.comboPlots)
        erasePlots.triggered.connect(self.erasePlots)

        # grab an existing button & insert the menu
        plotsButton = self.ui.plotType
        plotsButton.setMenu(plotsMenu)
        plotsButton.setPopupMode(QtGui.QToolButton.InstantPopup)

        # create a menu for axis type
        axisMenu = QtGui.QMenu(self)
        bunchCenteredAxis = QtGui.QAction("bunch-centered",self)
        axisMenu.addAction(bunchCenteredAxis)
        compactAxis = QtGui.QAction("compact",self)
        axisMenu.addAction(compactAxis)
        symmetricAxis = QtGui.QAction("symmetric",self)
        axisMenu.addAction(symmetricAxis)

        # associate these actions with class methods
        bunchCenteredAxis.triggered.connect(self.bunchCenteredAxis)
        compactAxis.triggered.connect(self.compactAxis)
        symmetricAxis.triggered.connect(self.symmetricAxis)

        # grab an existing button & insert the menu
        axisButton = self.ui.axisType
        axisButton.setMenu(axisMenu)
        axisButton.setPopupMode(QtGui.QToolButton.InstantPopup)

        # create a menu for transverse Twiss conventions
        perpTwissMenu = QtGui.QMenu(self)
        rmsNormalized = QtGui.QAction("rms, normalized",self)
        perpTwissMenu.addAction(rmsNormalized)
#        ninetyNormalized = QtGui.QAction("90%, normalized",self)
#        perpTwissMenu.addAction(ninetyNormalized)
#        rmsGeometric = QtGui.QAction("rms, geometric",self)
#        perpTwissMenu.addAction(rmsGeometric)

        # associate these actions with class methods
        rmsNormalized.triggered.connect(self.rmsNormalized)
#        ninetyNormalized.triggered.connect(self.ninetyNormalized)
#        rmsGeometric.triggered.connect(self.rmsGeometric)

        # grab an existing button & insert the menu
        perpTwissButton = self.ui.perpTwissSpec
        perpTwissButton.setMenu(perpTwissMenu)
        perpTwissButton.setPopupMode(QtGui.QToolButton.InstantPopup)

        # create a menu for longitudinal Twiss conventions
        longTwissMenu = QtGui.QMenu(self)
        alphaBctDp = QtGui.QAction("alpha-bct-dp",self)
        longTwissMenu.addAction(alphaBctDp)
#        couplingBctDp = QtGui.QAction("coupling-bct-dp",self)
#        longTwissMenu.addAction(couplingBctDp)
#        alphaBetaEmit = QtGui.QAction("alpha-beta-emit",self)
#        longTwissMenu.addAction(alphaBetaEmit)

        # associate these actions with class methods
        alphaBctDp.triggered.connect(self.alphaBctDp)
#        couplingBctDp.triggered.connect(self.couplingBctDp)
#        alphaBetaEmit.triggered.connect(self.alphaBetaEmit)

        # grab an existing button & insert the menu
        longTwissButton = self.ui.longTwissSpec
        longTwissButton.setMenu(longTwissMenu)
        longTwissButton.setPopupMode(QtGui.QToolButton.InstantPopup)

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
        numParticles = 800
        self.designMomentumEV = 2.e+8
        self.totalCharge = 1.e-9
        self.ui.numPtcls.setText("{:d}".format(numParticles))
        self.ui.designMomentum.setText("{:.0f}".format(self.designMomentumEV*1.e-6) + ' MeV')
        self.ui.totalCharge.setText("{:.0f}".format(self.totalCharge*1.e9) + ' nC')

        self.unitsPos = 'mm'
        self.unitsAngle = 'mrad'
        self.ui.unitsPos.setText(self.unitsPos)
        self.ui.unitsAngle.setText(self.unitsAngle)
        self.ui.numTicks.setText(str(self.numTicks))

        self.ui.twissTable.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)
        self.ui.twissTable.setItem(0,0,QtGui.QTableWidgetItem('0.'))
        self.ui.twissTable.setItem(1,0,QtGui.QTableWidgetItem('0.'))
        self.ui.twissTable.setItem(0,1,QtGui.QTableWidgetItem('1 m'))
        self.ui.twissTable.setItem(1,1,QtGui.QTableWidgetItem('1 m'))
        self.ui.twissTable.setItem(0,2,QtGui.QTableWidgetItem('1 micron'))
        self.ui.twissTable.setItem(1,2,QtGui.QTableWidgetItem('1 micron'))

        self.ui.twissTableZ.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)
        self.ui.twissTableZ.setItem(0,0,QtGui.QTableWidgetItem('0'))
        self.ui.twissTableZ.setItem(0,1,QtGui.QTableWidgetItem('1 mm'))
        self.ui.twissTableZ.setItem(0,2,QtGui.QTableWidgetItem('1.e-3'))

        self.ui.offsetTable.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)
        self.ui.offsetTable.setItem(0,0,QtGui.QTableWidgetItem('0 mm'))
        self.ui.offsetTable.setItem(1,0,QtGui.QTableWidgetItem('0 mm'))
        self.ui.offsetTable.setItem(2,0,QtGui.QTableWidgetItem('0 mm'))
        self.ui.offsetTable.setItem(0,1,QtGui.QTableWidgetItem('0 mrad'))
        self.ui.offsetTable.setItem(1,1,QtGui.QTableWidgetItem('0 mrad'))
        self.ui.offsetTable.setItem(2,1,QtGui.QTableWidgetItem('0 mrad'))

        # file directories
        self.parent = parent
        if self.parent is None:
            self.parent = self
            self.parent.lastUsedDirectory = os.path.expanduser('~')
        self.exportToFile = self.saveToSDDS

        # try to make the blank plotting regions look nice
        self.erasePlots()

        # instantiate an object for doing statistics
        self.myStat = stat.RbStatistics6D()

        self.container = QtGui.QScrollArea(self.parent)
        self.container.setWidget(self)

    def radtrackGaussian(self):
        self.distributionFlag = 'gaussian'

#    def radtrackUniform(self):
#        msgBox = QtGui.QMessageBox()
#        msgBox.setText("This feature has not yet been implemented. Coming soon!")
#        msgBox.exec_()

#    def elegantGaussian(self):
#        msgBox = QtGui.QMessageBox()
#        msgBox.setText("This feature has not yet been implemented. Coming soon!")
#        msgBox.exec_()

    def generateBunch(self, displayErrors = True):
        errorMessage = []
        self.parent.ui.statusbar.showMessage('Generating bunch ...')

        # Get input from text boxes. If errors are not being displayed
        # to the user (displayErrors == False), then silently
        # replace invalide values with defaults.
        try:
            numParticles = int(self.ui.numPtcls.text())
        except ValueError:
            numParticles = 0
        if numParticles <= 0:
            if displayErrors:
                errorMessage.append(self.ui.numPtclsLabel.text().strip() + ' must be a postive number.')
            else:
                numParticles = 800

        try:
            self.designMomentumEV = util.convertUnitsStringToNumber(self.ui.designMomentum.text(), 'eV')
        except ValueError:
            self.designMomentumEV = 0
        if self.designMomentumEV <= 0:
            if displayErrors:
                errorMessage.append(self.ui.designMomentumLabel.text().strip() + ' must be a positive value.')
            else:
                self.designMomentumEV = 2.e+8

        try:
            self.totalCharge = util.convertUnitsStringToNumber(self.ui.totalCharge.text().strip(), 'C')
        except ValueError:
            self.totalCharge = 0
        if self.totalCharge <= 0:
            if displayErrors:
                errorMessage.append(self.ui.charge.text() + ' must be a positive value.')
            else:
                self.totalCharge = 1.e-9

        if errorMessage:
            QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                    'Input Error' + ('s' if len(errorMessage) > 1 else ''),
                    '\n'.join(errorMessage),
                    QtGui.QMessageBox.Ok,
                    self).exec_()
            self.parent.ui.statusbar.clearMessage()
            self.myBunch = None
            return

        beta0gamma0 = self.designMomentumEV / self.eMassEV
        gamma0 = math.sqrt(beta0gamma0**2 + 1.)
        beta0 = beta0gamma0 / gamma0

        # get input from the table of Twiss parameters
        self.twissAlphaX = util.convertUnitsStringToNumber(self.ui.twissTable.item(0,0).text(), '')
        self.twissAlphaY = util.convertUnitsStringToNumber(self.ui.twissTable.item(1,0).text(), '')
        self.twissBetaX  = util.convertUnitsStringToNumber(self.ui.twissTable.item(0,1).text(), 'm/rad')
        self.twissBetaY  = util.convertUnitsStringToNumber(self.ui.twissTable.item(1,1).text(), 'm/rad')
        self.twissEmitNX = util.convertUnitsStringToNumber(self.ui.twissTable.item(0,2).text(), 'm*rad')
        self.twissEmitNY = util.convertUnitsStringToNumber(self.ui.twissTable.item(1,2).text(), 'm*rad')

        if self.longTwissFlag == "alpha-bct-dp":
            self.twissAlphaZ = util.convertUnitsStringToNumber(self.ui.twissTableZ.item(0,0).text(), '')
            self.bctRms = util.convertUnitsStringToNumber(self.ui.twissTableZ.item(0,1).text(), 'm')
            self.dPopRms  = float(self.ui.twissTableZ.item(0,2).text())

            self.twissEmitNZ = (self.bctRms/beta0) * self.dPopRms / math.sqrt(1.+self.twissAlphaZ**2)
            self.twissBetaZ  = (self.bctRms/beta0) / self.dPopRms * math.sqrt(1.+self.twissAlphaZ**2)

        # elif self.longTwissFlag == "coupling-bct-dp":
        #     msgBox = QtGui.QMessageBox()
        #     message  = 'Error --\n\n'
        #     message += '  longTwissFlag has been specified as "'+self.longTwissFlag+'".\n'
        #     message += '  This value is not yet supported, but is coming soon!\n\n'
        #     message += 'Please go to the "Specification Type" button and choose "alpha-bct-dp".\n\n'
        #     msgBox.setText(message)
        #     msgBox.exec_()
        # elif self.longTwissFlag == "alpha-beta-emit":
        #     msgBox = QtGui.QMessageBox()
        #     message  = 'Error --\n\n'
        #     message += '  longTwissFlag has been specified as "'+self.longTwissFlag+'".\n'
        #     message += '  This value is not yet supported, but is coming soon!\n\n'
        #     message += 'Please go to the "Specification Type" button and choose "alpha-bct-dp".\n\n'
        #     msgBox.setText(message)
        #     msgBox.exec_()
        # else:
        #     msgBox = QtGui.QMessageBox()
        #     message  = 'Error --\n\n'
        #     message += '  longTwissFlag has been specified as "'+self.longTwissFlag+'".\n'
        #     message += '  This choice is invalid!\n\n'
        #     message += 'Please use the "Specification Type" button to choose a valid option.\n\n'
        #     msgBox.setText(message)
        #     msgBox.exec_()

        # Get input from the table of phase space offsets
        self.offsetX  = util.convertUnitsStringToNumber(self.ui.offsetTable.item(0,0).text(), 'm')
        self.offsetY  = util.convertUnitsStringToNumber(self.ui.offsetTable.item(1,0).text(), 'm')
        self.offsetT  = util.convertUnitsStringToNumber(self.ui.offsetTable.item(2,0).text(), 'm')
        self.offsetXP = util.convertUnitsStringToNumber(self.ui.offsetTable.item(0,1).text(), 'rad')
        self.offsetYP = util.convertUnitsStringToNumber(self.ui.offsetTable.item(1,1).text(), 'rad')
        self.offsetPT = util.convertUnitsStringToNumber(self.ui.offsetTable.item(2,1).text(), 'rad')

        # instantiate the particle bunch
        self.myBunch = beam.RbParticleBeam6D(numParticles)
        self.myBunch.setDesignMomentumEV(self.designMomentumEV)
        self.myBunch.setTotalCharge(self.totalCharge)
        self.myBunch.setMassEV(self.eMassEV)     # assume electrons

        # specify the distribution flag and extent
        self.myDist = self.myBunch.getDistribution6D()
        self.myDist.setDistributionType(self.distributionFlag)
        self.myDist.setMaxRmsFactor(3.)

        # specify the Twiss parameters
        self.myBunch.setTwissParamsByName2D(self.twissAlphaX,self.twissBetaX,
                                            self.twissEmitNX/beta0gamma0,'twissX')
        self.myBunch.setTwissParamsByName2D(self.twissAlphaY,self.twissBetaY,
                                            self.twissEmitNY/beta0gamma0,'twissY')
        self.myBunch.setTwissParamsByName2D(self.twissAlphaZ,self.twissBetaZ,
                                            self.twissEmitNZ,'twissZ')

        # create the distribution
        self.myBunch.makeParticlePhaseSpace6D()

        # offset the distribution
        if (self.offsetX  != 0.):
            self.myDist.offsetDistribComp(self.offsetX,  0)
        if (self.offsetXP != 0.):
            self.myDist.offsetDistribComp(self.offsetXP, 1)
        if (self.offsetY  != 0.):
            self.myDist.offsetDistribComp(self.offsetY,  2)
        if (self.offsetYP != 0.):
            self.myDist.offsetDistribComp(self.offsetYP, 3)
        if (self.offsetT  != 0.):
            self.myDist.offsetDistribComp(self.offsetT,  4)
        if (self.offsetPT != 0.):
            self.myDist.offsetDistribComp(self.offsetPT, 5)

        # generate the plots
        self.refreshPlots()
        self.parent.ui.statusbar.clearMessage()

    def compactAxis(self):
        self.axisFlag = 'compact'
        self.refreshPlots()

    def symmetricAxis(self):
        self.axisFlag = 'symmetric'
        self.refreshPlots()

    def bunchCenteredAxis(self):
        self.axisFlag = 'bunch-centered'
        self.refreshPlots()

    def toggleAspectRatio(self):
        self.xyAspectRatioSquare = not self.xyAspectRatioSquare
        self.refreshPlots()

    def togglePlotTitles(self):
        self.plotTitles = not self.plotTitles
        self.refreshPlots()

    def scatterPlots(self):
        self.plotFlag = 'scatter'
        self.refreshPlots()

    def contourPlots(self):
        self.plotFlag = 'contour'
        self.refreshPlots()

    def comboPlots(self):
        self.plotFlag = 'combo'
        self.refreshPlots()

    def refreshPlots(self):
        self.parent.ui.statusbar.showMessage('Redrawing plots ...')
        # nothing to plot, if beam hasn't been initialized
        if not self.myBunch:
            self.erasePlots()
            return

        # get the specified units for plotting
        self.unitsPos = self.ui.unitsPos.text()
        self.unitsAngle = self.ui.unitsAngle.text()

        # get the number of tick marks
        self.numTicks = int(self.ui.numTicks.text())

        # create local pointer to particle array
        tmp6 = self.myBunch.getDistribution6D().getPhaseSpace6D().getArray6D()

        self.calculateLimits(tmp6)

        numParticles = tmp6.shape[1]
        nLevels = 5 + int(math.pow(numParticles, 0.33333333))
        nDivs = 10 + int(math.pow(numParticles, 0.2))

        # generate the four plots
        self.plotXY( util.convertUnitsNumber(tmp6[0,:], 'm', self.unitsPos),
                     util.convertUnitsNumber(tmp6[2,:], 'm', self.unitsPos),
                     nDivs, nLevels)

        self.plotXPX(util.convertUnitsNumber(tmp6[0,:], 'm', self.unitsPos),
                     util.convertUnitsNumber(tmp6[1,:], 'rad', self.unitsAngle),
                     nDivs, nLevels)

        self.plotYPY(util.convertUnitsNumber(tmp6[2,:], 'm', self.unitsPos),
                     util.convertUnitsNumber(tmp6[3,:], 'rad', self.unitsAngle),
                     nDivs, nLevels)

        self.plotSDP(util.convertUnitsNumber(tmp6[4,:], 'm', self.unitsPos),
                     util.convertUnitsNumber(tmp6[5,:], 'rad', self.unitsAngle),
                     nDivs, nLevels)

        self.parent.ui.statusbar.clearMessage()


    def calculateLimits(self, _arr):
        # nothing to do, if beam hasn't been initialized
        if not self.myBunch:
            return

        # get average, RMS, min, max values and diffs
        avgArray = self.myStat.calcAverages6D(_arr)
        rmsArray = self.myStat.calcRmsValues6D(_arr)
        minArray = self.myStat.calcMinValues6D(_arr)
        maxArray = self.myStat.calcMaxValues6D(_arr)

        # calculate the differences, imposing symmetry
        diffZero = np.zeros(6)
        for iLoop in range(6):
            diffZero[iLoop] = max( (avgArray[iLoop]-minArray[iLoop]),
                    (maxArray[iLoop]-avgArray[iLoop]) )

        # now switch based on the specified axis flag
        # specify plot limits, symmetric around the zero axis
        if self.axisFlag == 'symmetric':
            self.xMax  = (abs(avgArray[0])+diffZero[0])*util.convertUnitsNumber(1, 'm', self.unitsPos)
            self.xpMax = (abs(avgArray[1])+diffZero[1])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)
            self.yMax  = (abs(avgArray[2])+diffZero[2])*util.convertUnitsNumber(1, 'm', self.unitsPos)
            self.ypMax = (abs(avgArray[3])+diffZero[3])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)
            self.ptMax = (abs(avgArray[5])+diffZero[5])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)

            self.xMin  = -self.xMax
            self.xpMin = -self.xpMax
            self.yMin  = -self.yMax
            self.ypMin = -self.ypMax
            self.ptMin = -self.ptMax

        # specify plot limits, symmetric around the bunch (confined to 3 rms)
        elif self.axisFlag == 'compact':
            self.xMin  = (avgArray[0]-3.*rmsArray[0])*util.convertUnitsNumber(1, 'm', self.unitsPos)
            self.xpMin = (avgArray[1]-3.*rmsArray[1])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)
            self.yMin  = (avgArray[2]-3.*rmsArray[2])*util.convertUnitsNumber(1, 'm', self.unitsPos)
            self.ypMin = (avgArray[3]-3.*rmsArray[3])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)
            self.ptMin = (avgArray[5]-3.*rmsArray[5])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)

            self.xMax  = (avgArray[0]+3.*rmsArray[0])*util.convertUnitsNumber(1, 'm', self.unitsPos)
            self.xpMax = (avgArray[1]+3.*rmsArray[1])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)
            self.yMax  = (avgArray[2]+3.*rmsArray[2])*util.convertUnitsNumber(1, 'm', self.unitsPos)
            self.ypMax = (avgArray[3]+3.*rmsArray[3])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)
            self.ptMax = (avgArray[5]+3.*rmsArray[5])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)

        # symmetric around the bunch
        elif self.axisFlag == 'bunch-centered':
            self.xMin  = (avgArray[0]-diffZero[0])*util.convertUnitsNumber(1, 'm', self.unitsPos)
            self.xpMin = (avgArray[1]-diffZero[1])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)
            self.yMin  = (avgArray[2]-diffZero[2])*util.convertUnitsNumber(1, 'm', self.unitsPos)
            self.ypMin = (avgArray[3]-diffZero[3])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)
            self.ptMin = (avgArray[5]-diffZero[5])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)

            self.xMax  = (avgArray[0]+diffZero[0])*util.convertUnitsNumber(1, 'm', self.unitsPos)
            self.xpMax = (avgArray[1]+diffZero[1])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)
            self.yMax  = (avgArray[2]+diffZero[2])*util.convertUnitsNumber(1, 'm', self.unitsPos)
            self.ypMax = (avgArray[3]+diffZero[3])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)
            self.ptMax = (avgArray[5]+diffZero[5])*util.convertUnitsNumber(1, 'rad', self.unitsAngle)

        if self.axisFlag=='compact' or self.axisFlag=='symmetric-compact':
            # sMin / sMax always have to be 'bunch centered'
            self.sMin  = (avgArray[4]-3.*rmsArray[4])*util.convertUnitsNumber(1, 'm', self.unitsPos)
            self.sMax  = (avgArray[4]+3.*rmsArray[4])*util.convertUnitsNumber(1, 'm', self.unitsPos)

        if self.axisFlag=='symmetric' or self.axisFlag=='bunch-centered':
            # sMin / sMax always have to be 'bunch centered'
            self.sMin  = (avgArray[4]-diffZero[4])*util.convertUnitsNumber(1, 'm', self.unitsPos)
            self.sMax  = (avgArray[4]+diffZero[4])*util.convertUnitsNumber(1, 'm', self.unitsPos)


    def plotGenericBefore(self, hData, vData, _canvas, nDivs, nLevels):
        _canvas.ax.clear()
        self.scatConPlot(hData, vData, _canvas.ax, nDivs, nLevels)
        _canvas.ax.xaxis.set_major_locator(plt.MaxNLocator(self.numTicks))
        _canvas.ax.yaxis.set_major_locator(plt.MaxNLocator(self.numTicks))

    def plotGenericAfter(self, _canvas, title):
        if self.plotTitles:
            _canvas.ax.set_title(title)
        _canvas.fig.set_facecolor('w')
        _canvas.fig.tight_layout()
        _canvas.draw()


    def plotXY(self, hData, vData, nDivs, nLevels):
        self.plotGenericBefore(hData, vData, self.ui.xyPlot.canvas, nDivs, nLevels)
        self.ui.xyPlot.canvas.ax.axis([self.xMin, self.xMax, self.yMin, self.yMax])
        if self.xyAspectRatioSquare:
            self.ui.xyPlot.canvas.ax.set_aspect('equal', 'datalim')
        else:
            self.ui.xyPlot.canvas.ax.set_aspect('auto', 'datalim')
        self.ui.xyPlot.canvas.ax.set_xlabel('x ['+self.unitsPos+']')
        self.ui.xyPlot.canvas.ax.set_ylabel('y ['+self.unitsPos+']')

        self.plotGenericAfter(self.ui.xyPlot.canvas, 'cross-section')

    def plotXPX(self, hData, vData, nDivs, nLevels):
        self.plotGenericBefore(hData, vData, self.ui.xpxPlot.canvas, nDivs, nLevels)
        self.ui.xpxPlot.canvas.ax.axis([self.xMin, self.xMax, self.xpMin, self.xpMax])
        self.ui.xpxPlot.canvas.ax.set_xlabel('x ['+self.unitsPos+']')
        self.ui.xpxPlot.canvas.ax.set_ylabel("x' ["+self.unitsAngle+']')
        self.plotGenericAfter(self.ui.xpxPlot.canvas, 'horizontal')

    def plotYPY(self, hData, vData, nDivs, nLevels):
        self.plotGenericBefore(hData, vData, self.ui.ypyPlot.canvas, nDivs, nLevels)
        self.plotGenericBefore(hData, vData, self.ui.ypyPlot.canvas, nDivs, nLevels)
        self.ui.ypyPlot.canvas.ax.axis([self.yMin, self.yMax, self.ypMin, self.ypMax])
        self.ui.ypyPlot.canvas.ax.set_xlabel('y ['+self.unitsPos+']')
        self.ui.ypyPlot.canvas.ax.set_ylabel("y' ["+self.unitsAngle+']')
        self.plotGenericAfter(self.ui.ypyPlot.canvas, 'vertical')

    def plotSDP(self, hData, vData, nDivs, nLevels):
        self.plotGenericBefore(hData, vData, self.ui.tpzPlot.canvas, nDivs, nLevels)
        self.ui.tpzPlot.canvas.ax.axis([self.sMin, self.sMax, self.ptMin, self.ptMax])
        self.ui.tpzPlot.canvas.ax.set_xlabel('s ['+self.unitsPos+']')
        self.ui.tpzPlot.canvas.ax.set_ylabel(r'$(p-p_0)/p_0$ ['+self.unitsAngle+']')
        self.plotGenericAfter(self.ui.tpzPlot.canvas, 'longitudinal')

    """
    Generalized algorithm for plotting contour and/or scatter plots.
      self.plotFlag is queried to determine what's done.

    Adapted from open source method: scatter_contour.py
    https://github.com/astroML/astroML/blob/master/astroML/plotting/scatter_contour.py

    Parameters
    ----------
    x, y   : x and y data for the contour plot
    ax     : the axes on which to plot
    divs   : desired number of divisions along each axis
    levels : integer or array (optional, default=10)
             number of contour levels, or array of contour levels

    Returns
    -------
    points, contours :
       points   - return value of ax.scatter()
       contours - return value of ax.contourf()
       Note: value is 'None' if plot wasn't generated

    """
    def scatConPlot(self, x, y, ax, divs=10, levels=10):

        # logic for finding and plotting density contours
        if self.plotFlag=='contour' or self.plotFlag=='combo':

            if self.plotFlag == 'combo':
                threshold = 8

            if self.plotFlag == 'contour':
                threshold = 1

            # generate the 2D histogram, allowing the algorithm to use
            #   all data points, automatically calculating the 2D extent
            myHist, edges = np.histogramdd([x,y], divs)
            xbins, ybins = edges[0], edges[1]

            # specify contour levels, allowing user to input simple integer
            levels = np.asarray(levels)
            # if user specified an integer, then populate levels reasonably
            if levels.size == 1:
                levels = np.linspace(threshold, myHist.max(), levels)

            # define the 'extent' of the contoured area, using the
            #   the horizontal and vertical arrays generaed by histogram2d()
            extent = [xbins[0], xbins[-1], ybins[0], ybins[-1]]
            i_min = np.argmin(levels)

            # draw a zero-width line, which defines the outer polygon,
            #   in order to reduce the number of points drawn
            outline = ax.contour(myHist.T, levels[i_min:i_min+1],linewidths=0,extent=extent)

            # generate the contoured image, filled or not
            #   use myHist.T, rather than full myHist, to limit extent of the contoured region
            #   i.e. only the high-density regions are contoured
            #   the return value is potentially useful to the calling method
            contours = ax.contourf(myHist.T, levels, extent=extent)

        # no need for contours; particles only
        else:
            contours = None

        # logic for finding particles in low-density regions
        if self.plotFlag == 'combo':

            # create new 2D array that will hold a subset of the particles
            #   i.e. only those in the low-density regions
            lowDensityArray = np.hstack([x[:, None], y[:, None]])

            # extract only those particles outside the high-density region
            if len(outline.allsegs[0]) > 0:
                outer_poly = outline.allsegs[0][0]
                try:
                    # this works in newer matplotlib versions
                    from matplotlib.path import Path
                    points_inside = Path(outer_poly).contains_points(lowDensityArray)
                except ImportError:
                    # this works in older matplotlib versions
                    import matplotlib.nxutils as nx
                    points_inside = nx.points_inside_poly(x, outer_poly)
                Xplot = lowDensityArray[~points_inside]

            # there is no high-density region, so plot all the particles
            else:
                Xplot = lowDensityArray

        # load up all of the particles for plotting
        if self.plotFlag == 'scatter':
            Xplot = np.hstack([x[:, None], y[:, None]])

        # overlay scatter plot on top of contour plot generated above
        #   the return value is potentially useful to the calling method
        if self.plotFlag=='combo' or self.plotFlag=='scatter':
            points = ax.scatter(Xplot[:,0], Xplot[:,1], marker=',', s=1, c='k')
        else:
            # no particle plotting needed
            points = None

        # Return plot objects; useful for creating colorbars, etc.
        #   Value is 'None' if corresponding plot was not generated.
        return points, contours

    def erasePlots(self):
        plots = [self.ui.xyPlot, self.ui.xpxPlot, self.ui.ypyPlot, self.ui.tpzPlot]

        for plot in plots:
            plot.canvas.ax.clear()

        if self.plotTitles:
            self.ui.xyPlot.canvas.ax.set_title('cross-section')
            self.ui.xpxPlot.canvas.ax.set_title('horizontal')
            self.ui.ypyPlot.canvas.ax.set_title('vertical')
            self.ui.tpzPlot.canvas.ax.set_title('longitudinal')

        self.ui.xyPlot.canvas.ax.set_xlabel('x ['+self.unitsPos+']')
        self.ui.xyPlot.canvas.ax.set_ylabel('y ['+self.unitsPos+']')

        self.ui.xpxPlot.canvas.ax.set_xlabel('x ['+self.unitsPos+']')
        self.ui.xpxPlot.canvas.ax.set_ylabel("x' ["+self.unitsAngle+']')

        self.ui.ypyPlot.canvas.ax.set_xlabel('y ['+self.unitsPos+']')
        self.ui.ypyPlot.canvas.ax.set_ylabel("y' ["+self.unitsAngle+']')

        self.ui.tpzPlot.canvas.ax.set_xlabel('s ['+self.unitsPos+']')
        self.ui.tpzPlot.canvas.ax.set_ylabel(r'$(p-p_0)/p_0$ ['+self.unitsAngle+']')


        for plot in plots:
            plot.canvas.ax.axis([-1., 1., -1., 1.])
            plot.canvas.fig.set_facecolor('w')
            plot.canvas.fig.tight_layout()
            plot.canvas.draw()

    def rmsNormalized(self):
        # specify the perpendicular Twiss conventions
        self.perpTwissFlag = 'rms-normalized'

        # Do nothing for now, as this is the default choice
        #   and alternate choices haven't yet been implemented.
        # In the future, the 'Twiss Parameters' input box will
        #   be appropriately modified.

#     def rmsGeometric(self):
#         # specify the perpendicular Twiss conventions
# #        self.perpTwissFlag = 'rms-geometric'
#
#         # not yet implemented...
#         msgBox = QtGui.QMessageBox()
#         msgBox.setText("This feature has not yet been implemented. Coming soon!")
#         msgBox.exec_()
#
#     def ninetyNormalized(self):
#         # specify the perpendicular Twiss conventions
# #        self.perpTwissFlag = '90%-normalized'
#
#         # not yet implemented...
#         msgBox = QtGui.QMessageBox()
#         msgBox.setText("This feature has not yet been implemented. Coming soon!")
#         msgBox.exec_()

    def alphaBctDp(self):
        # specify the longitudinal Twiss conventions
        self.longTwissFlag = 'alpha-bct-dp'

        # Do nothing for now, as this is the default choice
        #   and alternate choices haven't yet been implemented.
        # In the future, the 'Longitudinal phase space' input box will
        #   be appropriately modified.

#     def couplingBctDp(self):
#         # specify the longitudinal Twiss conventions
# #        self.longTwissFlag = 'coupling-bct-dp'
#
#         msgBox = QtGui.QMessageBox()
#         msgBox.setText("This feature has not yet been implemented. Coming soon!")
#         msgBox.exec_()
#
#     def alphaBetaEmit(self):
#         # specify the longitudinal Twiss conventions
# #        self.longTwissFlag = 'alpha-beta-emit'
#
#         msgBox = QtGui.QMessageBox()
#         msgBox.setText("This feature has not yet been implemented. Coming soon!")
#         msgBox.exec_()

    # calculate the Twiss parameters
    def calculateTwiss(self):
        # nothing to do, if beam hasn't been initialized
        if not self.myBunch:
            return

        # let the bunch object to the heavy lifting
        self.myBunch.calcTwissParams6D()

        # now ask for the results
        self.twissX = self.myBunch.getTwissParamsByName2D('twissX')
        self.twissY = self.myBunch.getTwissParamsByName2D('twissY')
        self.twissZ = self.myBunch.getTwissParamsByName2D('twissZ')

        self.twissAlphaX = self.twissX.getAlphaRMS()
        self.twissAlphaY = self.twissY.getAlphaRMS()
        self.twissAlphaZ = self.twissZ.getAlphaRMS()

        self.twissBetaX = self.twissX.getBetaRMS()
        self.twissBetaY = self.twissY.getBetaRMS()
        self.twissBetaZ = self.twissZ.getBetaRMS()

        # load Twiss parameters into window for user to see
        self.ui.twissTable.setItem(0,0,QtGui.QTableWidgetItem("{:.5e}".format(self.twissAlphaX)))
        self.ui.twissTable.setItem(1,0,QtGui.QTableWidgetItem("{:.5e}".format(self.twissAlphaY)))
        self.ui.twissTable.setItem(0,1,QtGui.QTableWidgetItem("{:.5e}".format(self.twissBetaX)))
        self.ui.twissTable.setItem(1,1,QtGui.QTableWidgetItem("{:.5e}".format(self.twissBetaY)))

        # need the design momentum in order to handle the longitudinal phase space
        self.designMomentumEV = self.myBunch.getDesignMomentumEV()
        beta0gamma0 = self.designMomentumEV / self.eMassEV
        gamma0 = math.sqrt(beta0gamma0**2 + 1.)
        beta0 = beta0gamma0 / gamma0

        if self.longTwissFlag == "alpha-bct-dp":
            self.twissAlphaZ = self.twissZ.getAlphaRMS()
            self.twissBetaZ = self.twissZ.getBetaRMS()
            self.twissEmitNZ = self.twissZ.getEmitRMS()

            self.bctRms = beta0*math.sqrt(self.twissEmitNZ*self.twissBetaZ)
            twissGammaZ = (1.+self.twissAlphaZ**2) / self.twissBetaZ
            self.dPopRms = math.sqrt(self.twissEmitNZ*twissGammaZ)

            self.ui.twissTableZ.setItem(0,0,QtGui.QTableWidgetItem("{:.5e}".format(self.twissAlphaZ)))
            self.ui.twissTableZ.setItem(0,1,QtGui.QTableWidgetItem("{:.5e}".format(self.bctRms)))
            self.ui.twissTableZ.setItem(0,2,QtGui.QTableWidgetItem("{:.5e}".format(self.dPopRms)))

        # elif self.longTwissFlag == "coupling-bct-dp":
        #     msgBox = QtGui.QMessageBox()
        #     message  = 'Error --\n\n'
        #     message += '  longTwissFlag has been specified as "'+self.longTwissFlag+'".\n'
        #     message += '  This value is not yet supported, but is coming soon!\n\n'
        #     message += 'Please go to the "Specification Type" button and choose "alpha-bct-dp".\n\n'
        #     msgBox.setText(message)
        #     msgBox.exec_()
        # elif self.longTwissFlag == "alpha-beta-emit":
        #     msgBox = QtGui.QMessageBox()
        #     message  = 'Error --\n\n'
        #     message += '  longTwissFlag has been specified as "'+self.longTwissFlag+'".\n'
        #     message += '  This value is not yet supported, but is coming soon!\n\n'
        #     message += 'Please go to the "Specification Type" button and choose "alpha-bct-dp".\n\n'
        #     msgBox.setText(message)
        #     msgBox.exec_()
        # else:
        #     msgBox = QtGui.QMessageBox()
        #     message  = 'Error --\n\n'
        #     message += '  longTwissFlag has been specified as "'+self.longTwissFlag+'".\n'
        #     message += '  This choice is invalid!\n\n'
        #     message += 'Please use the "Specification Type" button to choose a valid option.\n\n'
        #     msgBox.setText(message)
        #     msgBox.exec_()

        # get average values
        avgArray = self.myStat.calcAverages6D(self.myBunch.getDistribution6D().getPhaseSpace6D().getArray6D())

        # load offsets into window for user to see
        self.ui.offsetTable.setItem(0,0,QtGui.QTableWidgetItem("{:.5e}".format(avgArray[0])))
        self.ui.offsetTable.setItem(1,0,QtGui.QTableWidgetItem("{:.5e}".format(avgArray[2])))
        self.ui.offsetTable.setItem(2,0,QtGui.QTableWidgetItem("{:.5e}".format(avgArray[4])))
        self.ui.offsetTable.setItem(0,1,QtGui.QTableWidgetItem("{:.5e}".format(avgArray[1])))
        self.ui.offsetTable.setItem(1,1,QtGui.QTableWidgetItem("{:.5e}".format(avgArray[3])))
        self.ui.offsetTable.setItem(2,1,QtGui.QTableWidgetItem("{:.5e}".format(avgArray[5])))

        # obtain top-level parameters
        self.designMomentumEV = self.myBunch.getDesignMomentumEV()
        numParticles = self.myBunch.getDistribution6D().getPhaseSpace6D().getNumParticles()

        # load values into window for user to see
        self.ui.numPtcls.setText("{:d}".format(numParticles))
        self.ui.designMomentum.setText("{:.0f}".format(self.designMomentumEV*1.e-6) + ' MeV')
        self.ui.totalCharge.setText("{:.0f}".format(self.totalCharge*1.e9) + ' nC')

        # normalize the emittance here
        self.twissEmitNX = self.twissX.getEmitRMS() * beta0gamma0
        self.twissEmitNY = self.twissY.getEmitRMS() * beta0gamma0
        self.twissEmitNZ = self.twissZ.getEmitRMS() * beta0gamma0
        self.ui.twissTable.setItem(0,2,QtGui.QTableWidgetItem("{:.5e}".format(self.twissEmitNX)))
        self.ui.twissTable.setItem(1,2,QtGui.QTableWidgetItem("{:.5e}".format(self.twissEmitNY)))

    def importFile(self, fileName = None):
        """Allow importing from CSV or SDDS"""
        # use Qt file dialog
        if not fileName:
            fileName = QtGui.QFileDialog.getOpenFileName(self, "Import particle file",
                    self.parent.lastUsedDirectory, util.fileTypeList(self.acceptsFileTypes))

        # if user cancels out, do nothing
        if not fileName:
            return

        self.parent.lastUsedDirectory = os.path.dirname(fileName)

        if re.search('\.csv$', fileName, re.IGNORECASE):
            self.readFromCSV(fileName)
        else:
            self.readFromSDDS(fileName)

    def readFromSDDS(self, fileName):
        # index is always zero...?
        sddsIndex = 0

        # initialize sdds.sddsdata.pyd library (Windows only) with data file
        if sdds.sddsdata.InitializeInput(sddsIndex, fileName) != 1:
            sdds.sddsdata.PrintErrors(1)

        # get parameter names
        paramNames = sdds.sddsdata.GetParameterNames(sddsIndex)

        # get parameter definitions
        paramDefs = [sdds.sddsdata.GetParameterDefinition(sddsIndex, param) for param in paramNames]

        # give the user a look at the parameters (if any)
        finalMsgBox = None
        if not paramNames:
            message  = 'WARNING --\n\n'
            message += 'No parameters were found in your selected SDDS file!!\n\n'
            message += 'The design momentum, total beam charge, etc., will have to be manually entered.'
            finalMsgBox = QtGui.QMessageBox(self)
            finalMsgBox.setText(message)

        # get column names
        columnNames = sdds.sddsdata.GetColumnNames(sddsIndex)

        # column data has to be handled differently;
        #   it will be a 6D python array of N-D NumPy arrays
        columnData = range(len(columnNames))

        # read parameter data from the SDDS file
        # mus read particle data at the same time
        errorCode = sdds.sddsdata.ReadPage(sddsIndex)
        if errorCode != 1:
            sdds.sddsdata.PrintErrors(1)
        while errorCode > 0:
            for jLoop in range(len(columnNames)):
                columnData[jLoop] = np.array(sdds.sddsdata.GetColumn(sddsIndex,jLoop))

            errorCode = sdds.sddsdata.ReadPage(sddsIndex)

        # get column definitions
        # units are in the 2nd column
        columnDefs = [sdds.sddsdata.GetColumnDefinition(sddsIndex,name) for name in columnNames]
        unitStrings = [cD[1] for cD in columnDefs]

        # begin deciphering the column data
        dataIndex = [-1 for i in range(6)]
        message = ''
        for iLoop in range(len(columnNames)):
            if columnNames[iLoop]=='x' or columnNames[iLoop]=='X':
                if dataIndex[0] >= 0:
                    message  = 'Error -- \n\n'
                    message += '  X column appears twice, for iLoop = '
                    message += str(dataIndex[0]) + ' and ' + str(iLoop)
                dataIndex[0] = iLoop
            if columnNames[iLoop]=='xp' or columnNames[iLoop]=='px' or columnNames[iLoop]=="x'":
                if dataIndex[1] >= 0:
                    message  = 'Error -- \n\n'
                    message += '  XP column appears twice, for iLoop = '
                    message += str(dataIndex[1]) + ' and ' + str(iLoop)
                dataIndex[1] = iLoop
            if columnNames[iLoop]=='y' or columnNames[iLoop]=='Y':
                if dataIndex[2] >= 0:
                    message  = 'Error -- \n\n'
                    message += '  Y column appears twice, for iLoop = '
                    message += str(dataIndex[2]) + ' and ' + str(iLoop)
                dataIndex[2] = iLoop
            if columnNames[iLoop]=='yp' or columnNames[iLoop]=='py' or columnNames[iLoop]=="y'":
                if dataIndex[3] >= 0:
                    message  = 'Error -- \n\n'
                    message += '  YP column appears twice, for iLoop = '
                    message += str(dataIndex[3]) + ' and ' + str(iLoop)
                dataIndex[3] = iLoop
            if columnNames[iLoop]=='s' or columnNames[iLoop]=='ct' or columnNames[iLoop]=='t':
                if dataIndex[4] >= 0:
                    message  = 'Error -- \n\n'
                    message += '  S column appears twice, for iLoop = '
                    message += str(dataIndex[4]) + ' and ' + str(iLoop)
                dataIndex[4] = iLoop
            if columnNames[iLoop]=='p' or columnNames[iLoop]=='pt' or columnNames[iLoop]=='dp':
                if dataIndex[5] >= 0:
                    message  = 'Error -- \n\n'
                    message += '  DP column appears twice, for iLoop = '
                    message += str(dataIndex[5]) + ' and ' + str(iLoop)
                dataIndex[5] = iLoop

            if message:
                msgBox = QtGui.QMessageBox()
                msgBox.setText(message)
                msgBox.exec_()
                return

        # initial validation of the column data
        if any([d < 0 for d in dataIndex]):
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
            if not unitStrings[iLoop]:
                unitStrings[iLoop] = defaultUnits[dataIndex[iLoop]]

        # check that all data columns are the same length
        numElements = [len(col) for col in columnData]

        if any([n != numElements[0] for n in numElements]):
            msgBox = QtGui.QMessageBox()
            message  = 'ERROR --\n\n'
            message += '  Not all of the data columns have the same length!\n'
            message += '  Here is the number of elements found in each column:\n'
            message += '    ' + str(numElements) + '\n\n'
            message += 'Please try again with a valid particle file.'
            msgBox.setText(message)
            msgBox.exec_()
            return

        # now we know the number of macro-particles
        numParticles = numElements[0]

        # all seems to be well, so load particle data into local array,
        #   accounting for any non-standard physical units
        tmp6 = np.array([columnData[dataIndex[i]] for i in range(6)])

        # close the SDDS particle file
        if sdds.sddsdata.Terminate(sddsIndex) != 1:
            sdds.sddsdata.PrintErrors(1)

        # instantiate the particle bunch
        self.myBunch = beam.RbParticleBeam6D(numParticles)
        self.myBunch.setDesignMomentumEV(self.designMomentumEV)
        self.myBunch.setMassEV(self.eMassEV)     # assume electrons

        # load particle array into the phase space object
        self.myBunch.getDistribution6D().getPhaseSpace6D().setArray6D(tmp6)

        # post top-level parameters to GUI
        self.ui.numPtcls.setText("{:d}".format(numParticles))
        self.ui.designMomentum.setText("{:.0f}".format(self.designMomentumEV*1.e-6) + ' MeV')
        self.ui.totalCharge.setText("{:.0f}".format(self.totalCharge*1.e9) + ' nC')

        # calculate bunch statistics and populate text boxes
        self.calculateTwiss()

        # plot the results
        if finalMsgBox is not None:
            finalMsgBox.show()

        self.refreshPlots()

    def readFromCSV(self, fileName):
        # check whether this is a RadTrack generated CSV file
        with open(fileName) as fileObject:
            csvReader = csv.reader(fileObject, delimiter=',')
            for lineNumber, rawData in enumerate(csvReader, 1):
                # make sure this file follows the RadTrack format
                if lineNumber == 1:
                    if rawData[0] != 'RadTrack':
                        msgBox = QtGui.QMessageBox()
                        message  = 'ERROR --\n\n'
                        message += '  The selected CSV file was not generated by RadTrack.\n'
                        message += '  Please select another file.\n\n'
                        msgBox.setText(message)
                        msgBox.exec_()
                        return
                # ignore the 2nd line
                elif lineNumber == 2:
                    continue
                # 3rd line contains the parametic data
                elif lineNumber == 3:
                    self.designMomentumEV = float(rawData[0])
                    self.totalCharge = float(rawData[1])
                # don't read beyond the first three lines
                elif lineNumber > 3:
                    break

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
            msgBox.setText(message)
            msgBox.exec_()
            return

        # store the number of particles read from the file
        numParticles = arrayShape[1]

        # instantiate the particle bunch
        self.myBunch = beam.RbParticleBeam6D(numParticles)
        self.myBunch.setDesignMomentumEV(self.designMomentumEV)
        self.myBunch.setMassEV(self.eMassEV)     # assume electrons

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

    def saveToCSV(self, fileName = None):
        if not fileName:
            fileName = util.getSaveFileName(self, 'csv')
            if not fileName:
                return

        # make sure the top-level parameters are up-to-date
        self.designMomentumEV = util.convertUnitsStringToNumber(self.ui.designMomentum.text(), 'eV')
        self.totalCharge = util.convertUnitsStringToNumber(self.ui.totalCharge.text(), 'C')

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
        if not sddsFileName:
            sddsFileName = util.getSaveFileName(self, 'sdds')
            if not sddsFileName:
                return

        # create local pointer to particle array
        self.generateBunch(False) # False --> don't display error boxes
        tmp6 = self.myBunch.getDistribution6D().getPhaseSpace6D().getArray6D()

        mySDDS = sdds.SDDS(0)
        mySDDS.description[0] = "RadTrack"
        mySDDS.description[1] = "Copyright 2013-2015 by RadiaBeam Technologies. All rights reserved."
        mySDDS.parameterName = ["designMomentumEV", "totalCharge", "eMassEV"]
        mySDDS.parameterData = [[self.designMomentumEV],
                                [self.totalCharge],
                                [self.eMassEV]]
        mySDDS.parameterDefinition = [["","","","",mySDDS.SDDS_DOUBLE,""],
                                      ["","","","",mySDDS.SDDS_DOUBLE,""],
                                      ["","","","",mySDDS.SDDS_DOUBLE,""]]
        mySDDS.columnName = ["x", "xp", "y", "yp", "t", "p"]

        mySDDS.columnData = [[list(tmp6[0,:])], [list(tmp6[1,:])],
                             [list(tmp6[2,:])], [list(tmp6[3,:])],
                             [list(tmp6[4,:])], [list(tmp6[5,:])]]

        mySDDS.columnDefinition = [["","m",  "","",mySDDS.SDDS_DOUBLE,0],
                                   ["","","","",mySDDS.SDDS_DOUBLE,0],
                                   ["","m",  "","",mySDDS.SDDS_DOUBLE,0],
                                   ["","","","",mySDDS.SDDS_DOUBLE,0],
                                   ["","s",  "","",mySDDS.SDDS_DOUBLE,0],
                                   ["","m_ec","","",mySDDS.SDDS_DOUBLE,0]]
        mySDDS.save(sddsFileName)

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = BunchTab()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
