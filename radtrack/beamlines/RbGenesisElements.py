"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

classes for genesis propagation
"""

from __future__ import print_function, division, unicode_literals, absolute_import
from PyQt4.QtCore import Qt
from radtrack.beamlines.RbElementCommon import *
from radtrack.beamlines.RbBeamlines import BeamlineCommon
from radtrack.RbUtility import convertUnitsString, convertUnitsStringToNumber, roundSigFig
import math
from os.path import basename

class genesisElement(elementCommon):
    def componentLine(self):
        writeData = []
        for i in range(1, len(self.data)): # self.data[0] == length which is handled elsewhere
            try:
                writeData.append(str(convertUnitsStringToNumber(self.data[i], self.units[i])))
            except ValueError:
                writeData.append('0.0')

        return self.symbol + '     ' + '   '.join(writeData)


class GenesisBeamline(BeamlineCommon):
    pass


beamlineType = GenesisBeamline
fileExtension = 'lat'

class Drift(particleDrift, genesisElement):
    symbol = 'DL'
    elementDescription = 'A drift space'
    parameterNames = ['Length']
    units = ['m']
    dataType = ['double']
    parameterDescription = ['Length']

class Solenoid(genesisElement, solenoidPic):
    symbol = 'SL'
    elementDescription = 'A solenoid manget'
    parameterNames = ['Length', 'KS']
    units = ['m', 'rad/m', 'T', 'm', 'm', 'm']
    dataType = ['double', 'double']
    parameterDescription = ['Length', 'Geometric Strength, -Bs/(B*Rho)']

class Quadrupole(genesisElement, magnetPic):
    symbol = 'QF'
    elementDescription = 'A quadrupole magnet'
    parameterNames = ['Length', 'Focusing Strength (k)']
    units = ['m', 'T/m']
    dataType = ['double', 'double']
    parameterDescription = ['Length', 'Field Gradient']
    color = Qt.red

class Undulator(genesisElement, undulatorPic):
    symbol = 'AW'
    elementDescription = 'A wiggler or undulator for damping or excitation of the beam'
    parameterNames = ['Length', 'AW0']
    units = ['m', '']
    dataType = ['double', 'double']
    parameterDescription = ['Length', 'Dimensionless strength parameter']

classDictionary = dict()

for key in list(globals()):
    if hasattr(globals()[key], 'elementDescription'):
        classDictionary[key] = globals()[key]

advancedNames = []

def fileImporter(fileName):
    pass

def isInteger(x):
    return math.floor(x) == x

def fileExporter(outputFileName, elementDictionary, defaultBeamline):
    beamline = None
    if defaultBeamline:
        beamline = elementDictionary[defaultBeamline]
    else:
        for element in elementDictionary.values():
            if element.isBeamline():
                beamline = element
    if not beamline:
        if parent and basename(outputFileName).startswith(parent.tabPrefix):
            beamline = GenesisBeamline()
            beamline.data = elementDictionary.values() # save all elements in order created
        else:
            raise NameError('Cannot write file: no beam line was created.')

    unitLength = 1.0
    allLengths = []
    for element in elementDictionary.values():
        if not element.isBeamline():
            allLengths.append(element.getLength())
    while not all([isInteger(roundSigFig(x, 6)) for x in allLengths]):
        unitLength = unitLength/10.0
        allLengths = [10.0 * x for x in allLengths]


    with open(outputFileName, 'w') as outputFile:
        outputFile.write('# This Genesis file was created by RadTrack\n')
        outputFile.write('# RadTrack (c) 2013, RadiaSoft, LLC\n\n')
        outputFile.write('? VERSION = 1.0 \n')
        outputFile.write('? UNITLENGTH = ' + str(unitLength) + '\n\n')

        elementTypesWritten = [Drift] # Drifts are never written to files
        for elementType in [type(elementDictionary[elementName]) for elementName in beamline.fullElementNameList()]:
            if elementType in elementTypesWritten:
                continue
            elementTypesWritten.append(elementType)
            outputFile.write('\n ### ' + elementType.__name__ + 's\n')
            currentPosition = 0.0 # position at end of current element
            lastPositionOfElement = 0.0 # position at end of previous element of same type
            for partName in beamline.fullElementNameList():
                part = elementDictionary[partName]
                lastPosition = currentPosition # position at start of current element
                currentPosition += part.getLength()
                if type(part) != elementType:
                    continue
                outputFile.write(part.componentLine() + '   ' \
                                 + str(int(round(part.getLength()/unitLength))) + '   ' \
                                 + str(int(round((lastPosition - lastPositionOfElement)/unitLength))) + '\n')
                lastPositionOfElement = currentPosition
