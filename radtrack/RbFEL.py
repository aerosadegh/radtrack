from __future__ import absolute_import, division, print_function, unicode_literals
from PyQt4 import QtGui
from radtrack.ui.fel import Ui_Form
from radtrack.util.unitConversion import convertUnitsStringToNumber, \
                                         convertUnitsNumberToString, \
                                         displayWithUnitsNumber, \
                                         convertUnitsNumber, \
                                         separateNumberUnit
from radtrack.util.RbMath import roundSigFig
from radtrack.util.fileTools import getSaveFileName
from math import pi, sqrt, log10, floor, isinf, isnan
import numpy
import sys
import os

# Constants
c = 299792458 # m/s
e0 = 8.851e-12 # F/m
e_charge = 1.602177e-19 # C
e_mass = 0.511e6 # eV
e_mass_kg = e_mass*e_charge/(c**2) # kg
e_radius = (e_charge**2)/(4*pi*e0*e_mass_kg*(c**2)) # m

class RbFEL(QtGui.QWidget):
    acceptsFileTypes = ['fel']
    defaultTitle = 'FEL Calculator'
    task = 'Analyze FEL parameters'
    category = 'tools'

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        if parent == None:
            self.parent = self
            self.parent.lastUsedDirectory = os.path.expanduser('~')
        else:
            self.parent = parent

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("RadTrack FEL Calculator")

        # Renames
        self.ui.charge.setObjectName("Charge")
        self.ui.charge.unit = 'C'
        self.ui.charge.dictName = 'charge'
        self.ui.slicemit.setObjectName("Normalized slice emittance")
        self.ui.slicemit.unit = 'm*rad'
        self.ui.slicemit.dictName = 'slicemit'
        self.ui.ebeamenergy.setObjectName("Beam energy")
        self.ui.ebeamenergy.unit = 'eV'
        self.ui.ebeamenergy.dictName = 'ebeamenergy'
        self.ui.energyspread.setObjectName("Sliced energy spread")
        self.ui.energyspread.unit = ''
        self.ui.energyspread.dictName = 'energyspread'
        self.ui.bunchlen.setObjectName("Bunch length (time)")
        self.ui.bunchlen.unit = 's'
        self.ui.bunchlen.dictName = 'bunchLengthFWHM_sec'
        self.ui.reprate.setObjectName("Repetition rate")
        self.ui.reprate.unit = 'Hz'
        self.ui.reprate.dictName = 'reprate'
        self.ui.uperiod.setObjectName("Undulator period")
        self.ui.uperiod.unit = 'm'
        self.ui.uperiod.dictName = 'undulatorPeriod'
        self.ui.ufield.setObjectName("Undulator field")
        self.ui.ufield.unit = 'T'
        self.ui.ufield.dictName = 'ufield'
        self.ui.beta.setObjectName("Average beta function")
        self.ui.beta.unit = 'm'
        self.ui.beta.dictName = 'beta'
        self.ui.bunlen.setObjectName("Bunch length (distance)")
        self.ui.bunlen.unit = 'm'
        self.ui.bunlen.dictName = 'bunchLengthFWHM_m'
        self.ui.gamma.setObjectName("Relativistic gamma")
        self.ui.gamma.unit = ''
        self.ui.gamma.dictName = 'gamma'
        self.ui.edensity.setObjectName("Peak electron density")
        self.ui.edensity.unit = 'm^-3'
        self.ui.edensity.dictName = 'peakElectronDensity'
        self.ui.geoemit.setObjectName("Geometric emittance")
        self.ui.geoemit.unit = 'm*rad'
        self.ui.geoemit.dictName = 'geometricEmittance'
        self.ui.peakamp.setObjectName("Peak current")
        self.ui.peakamp.unit = 'A'
        self.ui.peakamp.dictName = 'peakamp'
        self.ui.rmssize.setObjectName("RMS beam size (average)")
        self.ui.rmssize.unit = 'm'
        self.ui.rmssize.dictName = 'rmsBeamSize'
        self.ui.uparam.setObjectName("Undulator parameter")
        self.ui.uparam.unit = ''
        self.ui.uparam.dictName = 'undulatorParameter'
        self.ui.uwave.setObjectName("Undulator wavenumber")
        self.ui.uwave.unit = 'm^-1'
        self.ui.uwave.dictName = 'undulatorWaveNumber'
        self.ui.averagepower.setObjectName("Average power")
        self.ui.averagepower.unit = 'W'
        self.ui.averagepower.dictName = 'averagePower'
        self.ui.radiatedwavelength.setObjectName("Radiated wavelength")
        self.ui.radiatedwavelength.unit = 'm'
        self.ui.radiatedwavelength.dictName = 'radiatedwavelength'
        self.ui.saturation.setObjectName("Saturation length")
        self.ui.saturation.unit = 'm'
        self.ui.saturation.dictName = 'saturationLength'
        self.ui.raleigh.setObjectName("Rayleigh range")
        self.ui.raleigh.unit = 'm'
        self.ui.raleigh.dictName = 'RayleighRange'
        self.ui.photonemit.setObjectName("Photon emittance")
        self.ui.photonemit.unit = 'm*rad'
        self.ui.photonemit.dictName = 'photonEmittance'
        self.ui.fel_1d.setObjectName("1D FEL parameter")
        self.ui.fel_1d.unit = ''
        self.ui.fel_1d.dictName = 'oneDFELParameter'
        self.ui.gain_1d.setObjectName("1D gain length")
        self.ui.gain_1d.unit = ''
        self.ui.gain_1d.dictName = 'oneDGainLength'
        self.ui.dfactor.setObjectName("Diffraction factor")
        self.ui.dfactor.unit = ''
        self.ui.dfactor.dictName = 'diffractionFactor'
        self.ui.efactor.setObjectName("Emittance factor")
        self.ui.efactor.unit = ''
        self.ui.efactor.dictName = 'emitanceFactor'
        self.ui.espreadfactor.setObjectName("Energy spread factor")
        self.ui.espreadfactor.unit = ''
        self.ui.espreadfactor.dictName = 'energySpreadFactor'
        self.ui.threedfel.setObjectName("3D FEL parameter")
        self.ui.threedfel.unit = ''
        self.ui.threedfel.dictName = 'threeDFELParameter'
        self.ui.gain_3d.setObjectName("3D gain length")
        self.ui.gain_3d.unit = 'm'
        self.ui.gain_3d.dictName = 'threeDGainLength'
        self.ui.total.setObjectName("3D effect total")
        self.ui.total.unit = ''
        self.ui.total.dictName = 'threeDEffectTotal'
        self.ui.sasepower.setObjectName("SASE power at saturation")
        self.ui.sasepower.unit = 'W'
        self.ui.sasepower.dictName = 'SASEpowerAtSaturation'
        self.ui.saseenergy.setObjectName("SASE pulsed energy")
        self.ui.saseenergy.unit = 'J'
        self.ui.saseenergy.dictName = 'pulsedSASEenergy'
        self.ui.x.setObjectName("X Axis")
        self.ui.y.setObjectName("Y Axis")
        self.ui.z.setObjectName("Z Axis")
        self.ui.xmin.setObjectName("Min X Value")
        self.ui.xmax.setObjectName("Max X Value")
        self.ui.ymin.setObjectName("Min Y Value")
        self.ui.ymax.setObjectName("Max Y Value")

        self.textBox = dict()
        self.valueFromTextBox = dict()
        self.textBoxFromDictName = dict()
        self.userInputBoxes = []

        maxLength = 0
        for thing in [getattr(self.ui, name) for name in sorted(dir(self.ui))]:
            if not hasattr(thing, 'unit'):
                continue
            length = QtGui.QFontMetrics(self.ui.x.font()).boundingRect(thing.objectName()).width()
            if length > maxLength:
                maxLength = length
            self.textBox[thing.objectName()] = thing
            self.textBoxFromDictName[thing.dictName] = thing
            if hasattr(thing, 'isReadOnly'):
                if thing.isReadOnly():
                    if thing.objectName().startswith("Bunch length"):
                        thing.setToolTip("FWHM")
                    else:
                        thing.setToolTip('')
                    self.ui.z.addItem(thing.objectName())
                    self.ui.target.addItem(thing.objectName())
                else:
                    self.ui.x.addItem(thing.objectName())
                    self.ui.y.addItem(thing.objectName())
                    self.ui.vary.addItem(thing.objectName())
                    thing.textEdited.connect(self.calculateAll)
                    thing.setToolTip(thing.unit)
                    self.userInputBoxes.append(thing)

        scrollBarWidth = self.style().pixelMetric(QtGui.QStyle.PM_ScrollBarExtent)
        extraSpace = 10
        comboWidth = maxLength + scrollBarWidth + extraSpace
        comboHeight = 22

        for thing in [self.ui.x, self.ui.y, self.ui.z]:
            self.textBox[thing.objectName()] = thing
            thing.setGeometry(thing.x(), thing.y(), comboWidth, comboHeight)
            thing.setCurrentIndex(-1)
        for thing in [self.ui.xmin, self.ui.xmax, self.ui.ymin, self.ui.ymax]:
            self.textBox[thing.objectName()] = thing

        # Connections
        self.ui.plotButton.clicked.connect(self.plot)
        self.ui.solve.clicked.connect(self.goalSeek)

        # Default/example values
        self.ui.charge.setText('300 pC')
        self.ui.slicemit.setText('1 mm*mrad')
        self.ui.ebeamenergy.setText('600 MeV')
        self.ui.energyspread.setText('.01%')
        self.ui.peakamp.setText('200 A')
        self.ui.reprate.setText('150 kHz')
        self.ui.radiatedwavelength.setText('13.5 nm')
        self.ui.ufield.setText('0.9 T')
        self.ui.beta.setText('1 m')

        self.calculateAll()

        for box in self.textBox.values():
            try:
                box.setCursorPosition(0)
            except AttributeError:
                pass

    def calculateAll(self):
        self.updateBoxes(calculate(self.userInputDict()))

    def updateBoxes(self, boxDict):
        for name in boxDict:
            self.setResultBox(self.textBoxFromDictName[name], boxDict[name])

    def userInputDict(self):
        userDict = dict()
        for box in self.userInputBoxes:
            userDict[box.dictName] = self.getValue(box)
        return userDict

    def unsetValue(self, textBox):
        textBox.clear()
        if textBox in self.valueFromTextBox:
            del self.valueFromTextBox[textBox]

    def getValue(self, textBox):
        try:
            self.valueFromTextBox[textBox] = convertUnitsStringToNumber(textBox.text(), textBox.unit)
            return self.valueFromTextBox[textBox]
        except ValueError:
            if textBox in self.valueFromTextBox:
                del self.valueFromTextBox[textBox]

    def setResultBox(self, textBox, value):
        if value is not None:
            self.valueFromTextBox[textBox] = value
            textBox.setText(displayWithUnitsNumber(roundSigFig(value, 5), textBox.unit))
            textBox.setCursorPosition(0)
        else:
            self.unsetValue(textBox)


    def plot(self):
        try:
            xTextBox = self.textBox[self.ui.x.currentText()]
            xOrginalValue = xTextBox.text()
            yTextBox = self.textBox[self.ui.y.currentText()]
            yOrginalValue = yTextBox.text()
            zTextBox = self.textBox[self.ui.z.currentText()]
        except KeyError:
            return # Combo box choice was left blank

        try:
            xmin = convertUnitsStringToNumber(self.ui.xmin.text(), xTextBox.unit)
            xmax = convertUnitsStringToNumber(self.ui.xmax.text(), xTextBox.unit)
            if xmin > xmax:
                xmin, xmax = xmax, xmin

            ymin = convertUnitsStringToNumber(self.ui.ymin.text(), yTextBox.unit)
            ymax = convertUnitsStringToNumber(self.ui.ymax.text(), yTextBox.unit)
            if ymin > ymax:
                ymin, ymax = ymax, ymin

        except ValueError: # text box left blank
            return

        numPoints = 32 # per variable, 32*32 = 1,024 points total

        xRange = numpy.linspace(xmin, xmax, numPoints)
        _, xAxisLabel, xRangeUnits = rangeUnits(xTextBox, xRange)

        yRange = numpy.linspace(ymin, ymax, numPoints)
        _, yAxisLabel, yRangeUnits = rangeUnits(yTextBox, yRange)

        Z = numpy.zeros((numPoints, numPoints))
        plotProgress = QtGui.QProgressDialog("Plotting ...", None, 0, (numPoints**2)-1)
        plotProgress.setMinimumDuration(0)

        try:
            for j, x in enumerate(xRange):
                for i, y in enumerate(yRange):
                    plotProgress.setValue(plotProgress.value()+1)
                    xTextBox.setText(str(x))
                    yTextBox.setText(str(y))
                    results = calculate(self.userInputDict())
                    try:
                        Z[i,j] = results[zTextBox.dictName]
                    except KeyError:
                        Z[i,j] = float('nan')

            zUnit, zAxisLabel, _ = rangeUnits(zTextBox, Z.flat)
            for z in numpy.nditer(Z, op_flags=['readwrite']):
                z[...] = util.convertUnitsNumber(z, zTextBox.unit, zUnit)

            # Plotting
            self.ui.plotWidget.canvas.fig.clear()
            self.ui.plotWidget.canvas.ax = self.ui.plotWidget.canvas.fig.add_subplot(111)
            ca = self.ui.plotWidget.canvas.ax.imshow(numpy.flipud(Z), cmap = 'hot',
                    extent = [min(xRangeUnits), max(xRangeUnits),
                    min(yRangeUnits), max(yRangeUnits)],
                    aspect = 'auto')
            self.ui.plotWidget.canvas.ax.set_xlabel(xAxisLabel)
            self.ui.plotWidget.canvas.ax.set_ylabel(yAxisLabel)
            cb = self.ui.plotWidget.canvas.fig.colorbar(ca)
            cb.set_label(zAxisLabel)
            self.ui.plotWidget.canvas.ax.set_xlim(min(xRangeUnits), max(xRangeUnits))
            self.ui.plotWidget.canvas.ax.set_ylim(min(yRangeUnits), max(yRangeUnits))
            self.ui.plotWidget.canvas.fig.tight_layout()
            self.ui.plotWidget.canvas.draw()

        finally:
            # Restore text boxes to original state
            xTextBox.setText(xOrginalValue)
            xTextBox.setCursorPosition(0)
            yTextBox.setText(yOrginalValue)
            yTextBox.setCursorPosition(0)
            self.calculateAll()


    def goalSeek(self):
        # Newton's method
        variableTextBox = self.textBox[self.ui.vary.currentText()]
        resultTextBox = self.textBox[self.ui.target.currentText()]
        self.ui.solverResult.setText('Searching...')

        maximumIterations = 1000
        success = False
        dxFactor = 1e-9
        try:
            x0 = self.valueFromTextBox[variableTextBox]
        except KeyError:
            x0 = dxFactor
        bestX = x0

        try:
            goal = convertUnitsStringToNumber(self.ui.lineEdit.text(), resultTextBox.unit)
            y0 = self.calculateValue(variableTextBox, x0, resultTextBox)
            bestError = abs((y0-goal)/goal)
            for i in range(maximumIterations):
                try:
                    y0 = self.calculateValue(variableTextBox, x0, resultTextBox)
                    error = abs((y0-goal)/goal)
                    if error < 1e-6:
                        success = True
                        break
                    else:
                        if error < bestError:
                            bestX = x0
                            bestError = error

                    dx = abs(dxFactor*x0)
                    slope = self.calculateSlope(variableTextBox, x0, dx, resultTextBox)

                    x0 = x0 - (y0-goal)/slope
                    if x0 < 0:
                        x0 = dx
                except (ZeroDivisionError, KeyError, OverflowError):
                    dxFactor = 2*dxFactor
                    x0 = x0+dx

        except ValueError: # "goal" is blank -> find extrema by Newton's method on slope
            dx = abs(dxFactor*x0)
            bestSlope = abs(self.calculateSlope(variableTextBox, x0, dx, resultTextBox))
            for i in range(maximumIterations):
                try:
                    dx = abs(dxFactor*x0)
                    slope = self.calculateSlope(variableTextBox, x0, dx, resultTextBox)
                    if abs(slope) < 1e-6:
                        success = True
                        break
                    else:
                        if slope < bestSlope:
                            bestX = x0
                            bestSlope = slope

                    secondDerivitive = self.calculateSecondDerivitive(variableTextBox, x0, dx, resultTextBox)

                    x0 = x0 - (slope)/secondDerivitive
                    if x0 < 0:
                        x0 = dx
                except (ZeroDivisionError, KeyError, OverflowError):
                    dxFactor = 2*dxFactor
                    x0 = x0+dx

        if success:
            value = x0
            self.ui.solverResult.setText('Success.')
        else:
            value = bestX
            self.ui.solverResult.setText('Failed. Could not find a solution.')

        variableTextBox.setText(displayWithUnitsNumber(roundSigFig(value, 5), variableTextBox.unit))
        variableTextBox.setCursorPosition(0)
        self.calculateAll()

    def calculateValue(self, inputBox, inputValue, resultBox):
        inputBox.setText(str(inputValue))
        result = calculate(self.userInputDict())
        return result[resultBox.dictName]

    def calculateSlope(self, inputBox, inputValue, inputStep, resultBox):
        return (self.calculateValue(inputBox, inputValue + inputStep, resultBox)
                - self.calculateValue(inputBox, inputValue, resultBox))/inputStep

    def calculateSecondDerivitive(self, inputBox, inputValue, inputStep, resultBox):
        return (self.calculateSlope(inputBox, inputValue + inputStep, inputStep, resultBox) -
                self.calculateSlope(inputBox, inputValue, inputStep, resultBox))/inputStep

    def exportToFile(self, fileName = None):
        if not fileName:
            fileName = getSaveFileName(self)
            if not fileName:
                return

        fileLines = []
        for box in self.textBox.values():
            try:
                try:
                    _, unit = separateNumberUnit(box.text())
                    value = convertUnitsNumberToString(self.valueFromTextBox[box], box.unit, unit)
                except (ValueError, KeyError):
                    value = box.text()
                fileLines.append(box.objectName() + ':' + value) # text box
            except AttributeError:
                fileLines.append(box.objectName() + ':' + box.currentText()) # combo box

        with open(fileName, 'w') as f:
            f.write('\n'.join(sorted(fileLines)))

    def importFile(self, fileName = None):
        if not fileName:
            fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.parent.lastUsedDirectory,
                fileTypeLists(self.acceptsFileTypes))
            if not fileName:
                return
            self.parent.lastUsedDirectory = os.path.dirname(fileName)

        with open(fileName, 'r') as f:
            for line in f:
                name, value = line.strip().split(':')
                box = self.textBox[name]
                try:
                    box.setText(value) # text box
                except AttributeError:
                    box.setCurrentIndex(box.findText(value)) # combo box

        self.calculateAll()
        self.plot()


def rangeUnits(textBox, array):
    # For some reason, max() doesn't work on numpy arrays containing non-finite numbers
    maxValue = float('-inf')
    for value in array:
        if isfinite(value) and value > maxValue:
            maxValue = value
    if textBox.unit != '':
        unit = displayWithUnitsNumber(maxValue, textBox.unit).split()[1]
        rangeInUnits = [convertUnitsNumber(value, textBox.unit, unit) for value in array]
    else:
        power = int(round(floor(log10(abs(maxValue)))/3)*3) # round power to nearest multiple of 3
        unit = '10^' + str(power) if power != 0 else ''
        rangeInUnits = [x/(10**power) for x in array]

    axisLabel = textBox.objectName() + (' (' + unit + ')' if unit else '')
    return unit, axisLabel, rangeInUnits

def isfinite(number):
    return not isnan(number) and not isinf(number)


def calculate(userInputDict):
    # Every time the user changes the text in an input text box,
    # an attempt is made to calculate every output box.
    # This way, the derived values are filled in as
    # the user enters data. If an output cannot be calculated,
    # it is simply skipped.

    mingXieMatrix = [[    0.55 , 0.0  , 1.6 , 0.0 ],
                     [    3.0  , 0.0  , 0.0 , 2.0 ],
                     [    0.35 , 0.0  , 2.9 , 2.4 ],
                     [   51.0  , 0.95 , 0.0 , 3.0 ],
                     [    5.4  , 0.7  , 1.9 , 0.0 ],
                     [ 1140.0  , 2.2  , 2.9 , 3,2 ]]

    charge = userInputDict['charge']
    peakCurrent = userInputDict['peakamp']
    normalizedSliceEmittance = userInputDict['slicemit']
    kineticEnergy = userInputDict['ebeamenergy']
    slicedEnergySpread = userInputDict['energyspread']
    repititionRate = userInputDict['reprate']
    undulatorField = userInputDict['ufield']
    averageBetaFunction = userInputDict['beta']
    radiatedWaveLength = userInputDict['radiatedwavelength']

    resultDict = dict()
    for name in [
                 'bunchLengthFWHM_sec',
                 'bunchLengthFWHM_m',
                 'gamma',
                 'rmsBeamSize',
                 'peakElectronDensity',
                 'geometricEmittance',
                 'undulatorPeriod',
                 'undulatorParameter',
                 'undulatorWaveNumber',
                 'oneDFELParameter',
                 'oneDGainLength',
                 'RayleighRange',
                 'diffractionFactor',
                 'photonEmittance',
                 'emitanceFactor',
                 'energySpreadFactor',
                 'threeDEffectTotal',
                 'threeDFELParameter',
                 'threeDGainLength',
                 'SASEpowerAtSaturation',
                 'pulsedSASEenergy',
                 'averagePower',
                 'saturationLength'
                ]:
        resultDict[name] = None

    errorsToCatch = (UnboundLocalError, TypeError, ZeroDivisionError, OverflowError)
    try:
        bunchLengthFWHM_sec = charge/peakCurrent
        resultDict['bunchLengthFWHM_sec'] = bunchLengthFWHM_sec
    except errorsToCatch:
        pass

    try:
        bunchLengthFWHM_m = bunchLengthFWHM_sec*c
        resultDict['bunchLengthFWHM_m'] = bunchLengthFWHM_m
    except errorsToCatch:
        pass

    try:
        gamma = (kineticEnergy/e_mass)+1
        resultDict['gamma'] = gamma
    except errorsToCatch:
        pass

    try:
        rmsBeamSize = sqrt(averageBetaFunction*normalizedSliceEmittance/gamma)
        resultDict['rmsBeamSize'] = rmsBeamSize
    except errorsToCatch:
        pass

    try:
        peakElectronDensity = peakCurrent/(e_charge*c*2*pi*(rmsBeamSize**2))
        resultDict['peakElectronDensity'] = peakElectronDensity
    except errorsToCatch:
        pass

    try:
        geometricEmittance = normalizedSliceEmittance/gamma
        resultDict['geometricEmittance'] = geometricEmittance
    except errorsToCatch:
        pass

    try:
        betaR = sqrt(1-1/(gamma**2)) # relativistic beta
        undulatorConstant = e_charge*undulatorField/(2*pi*betaR*e_mass_kg*c)
        A = (undulatorConstant**2)/2.0
        D = 18*(gamma**2)*radiatedWaveLength*(A**2)
        X = (D + sqrt((D**2) + 12*(A**3)))**(1.0/3.0)
        C1 = (18**(1.0/3.0))*A
        C2 = (2.0/3.0)**(1.0/3.0)
        undulatorPeriod = X/C1 - C2/X
        resultDict['undulatorPeriod'] = undulatorPeriod
    except errorsToCatch:
        pass

    try:
        undulatorParameter = undulatorConstant*undulatorPeriod
        resultDict['undulatorParameter'] = undulatorParameter
    except errorsToCatch:
        pass

    try:
        undulatorWaveNumber = 2*pi/undulatorPeriod
        resultDict['undulatorWaveNumber'] = undulatorWaveNumber
    except errorsToCatch:
        pass

    try:
        oneDFELParameter = ((pi*e_radius*peakElectronDensity*(undulatorParameter**2)/(undulatorWaveNumber**2))**(1.0/3.0))/(2*gamma)
        resultDict['oneDFELParameter'] = oneDFELParameter
    except errorsToCatch:
        pass

    try:
        oneDGainLength = undulatorPeriod/(4*pi*sqrt(3)*oneDFELParameter)
        resultDict['oneDGainLength'] = oneDGainLength
    except errorsToCatch:
        pass

    try:
        RayleighRange = 4*pi*(rmsBeamSize**2)/radiatedWaveLength
        resultDict['RayleighRange'] = RayleighRange
    except errorsToCatch:
        pass

    try:
        diffractionFactor = oneDGainLength/RayleighRange
        resultDict['diffractionFactor'] = diffractionFactor
    except errorsToCatch:
        pass

    try:
        photonEmittance = radiatedWaveLength/(4*pi)
        resultDict['photonEmittance'] = photonEmittance
    except errorsToCatch:
        pass

    try:
        emitanceFactor = (geometricEmittance/photonEmittance)*(oneDGainLength/averageBetaFunction)
        resultDict['emitanceFactor'] = emitanceFactor
    except errorsToCatch:
        pass

    try:
        energySpreadFactor = slicedEnergySpread/(oneDFELParameter*sqrt(3))
        resultDict['energySpreadFactor'] = energySpreadFactor
    except errorsToCatch:
        pass

    try:
        threeDEffectTotal = 0
        for row in mingXieMatrix:
            threeDEffectTotal += row[0]*(diffractionFactor**row[1])*(emitanceFactor**row[2])*(energySpreadFactor**row[3])
        resultDict['threeDEffectTotal'] = threeDEffectTotal
    except errorsToCatch:
        pass

    try:
        threeDFELParameter = oneDFELParameter/(1+threeDEffectTotal)
        resultDict['threeDFELParameter'] = threeDFELParameter
    except errorsToCatch:
        pass

    try:
        threeDGainLength = oneDGainLength*(1+threeDEffectTotal)
        resultDict['threeDGainLength'] = threeDGainLength
    except errorsToCatch:
        pass

    try:
        SASEpowerAtSaturation = e_mass_kg*(c**2)*gamma*threeDFELParameter*peakCurrent/e_charge
        resultDict['SASEpowerAtSaturation'] = SASEpowerAtSaturation
    except errorsToCatch:
        pass

    try:
        pulsedSASEenergy = SASEpowerAtSaturation*bunchLengthFWHM_sec
        resultDict['pulsedSASEenergy'] = pulsedSASEenergy
    except errorsToCatch:
        pass

    try:
        averagePower = pulsedSASEenergy*repititionRate
        resultDict['averagePower'] = averagePower
    except errorsToCatch:
        pass

    try:
        saturationLength = undulatorPeriod/threeDFELParameter
        resultDict['saturationLength'] = saturationLength
    except errorsToCatch:
        pass

    return resultDict


def main():
    app = QtGui.QApplication(sys.argv)
    window = RbFEL()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
