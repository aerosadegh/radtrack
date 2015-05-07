"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

classes for genesis propagation
"""

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QProgressDialog
from RbElementCommon import *
from RbBeamlines import BeamlineCommon
from radtrack.RbUtility import convertUnitsStringToNumber, convertUnitsString

class genesisElement(elementCommon):
    def componentLine(self):
        sentence = [(param, convertUnitsString(datum, unit)) \
                for param, datum, unit in \
                zip(self.parameterNames, self.data, self.units) if datum]

        sentence = '   '.join(self.data)
        #sentence = ', '.join(['='.join(phrase) for phrase in sentence])

        return type(self).__name__ + '     ' + sentence


class GenesisBeamline(BeamlineCommon):
    def componentLine(self):
        return self.name + ':    ' + self.displayLine()

beamlineType = GenesisBeamline
fileExtension = 'lat'

class QF(genesisElement, magnetPic):
    elementDescription = 'A quadrupole'
    parameterNames = ['K', 'L', 'D']
    units = ['T/m', 'm', 'm']
    dataType = ['double', 'double', 'double']
    parameterDescription = ['Field Gradient', 'Length','Spacing']
    color = Qt.red

class AW(genesisElement, undulatorPic):
    elementDescription = 'A wiggler or undulator for damping or excitation of the beam.'
    parameterNames = ['AW0', 'L','D']
    units = ['', 'm','m','m']
    dataType = ['double', 'double', 'double']
    parameterDescription = ['Dimensionless strength parameter', 'Length','Spacing']

class Unit_Length(genesisElement, driftPic):
    elementDescription = 'The length to which all Genesis elements are relative to'
    parameterNames = ['UNITLENGTH']
    units = ['m']
    dataType =['double']
    parameterDescription = ['length']

    def componentLine(self):
        sentence = [(param, convertUnitsString(datum, unit)) \
                for param, datum, unit in \
                zip(self.parameterNames, self.data, self.units) if datum]
        sentence = ''.join(['='.join(phrase) for phrase in sentence])
        return '?'+sentence

def nameMangler(name):
    return name

classDictionary = dict()

for key in list(globals()):
    if hasattr(globals()[key], 'elementDescription'):
        classDictionary[key] = globals()[key]

advancedNames = []

def fileImporter(fileName):
    pass


def fileExporter(outputFileName, elementDictionary, defaultBeamline):
    with open(outputFileName, 'w') as outputFile:
        outputFile.write('# This Genesis file was created by RadTrack\n')
        outputFile.write('# RadTrack (c) 2013, RadiaSoft, LLC\n\n')
        outputFile.write('? VERSION = 1.0 \n')
        fileWriteProgress = QProgressDialog('Writing to ' + outputFileName + ' ...',
                'Cancel',
                0,
                len(elementDictionary)-1)
        fileWriteProgress.setMinimumDuration(0)
        fileWriteProgress.setValue(0)
        for element in elementDictionary.values():
             if element.isBeamline():
                 for part in element.data:
                     outputFile.write(part.componentLine()+'\n')



'''
class DRIF(particleDrift, genesisElement):
    elementDescription = 'A drift space'
    parameterNames = ['L']
    units = ['m']
    dataType = ['double']
    parameterDescription = ['length']

class SOLE(elegantElement, solenoidPic):
    elementDescription = 'A solenoid.'
    parameterNames = ['L', 'KS', 'B', 'DX', 'DY', 'DZ']
    units = ['m', 'rad/m', 'T', 'm', 'm', 'm']
    dataType = ['double', 'double', 'double', 'double', 'double', 'double']
    parameterDescription = ['length', 'geometric strength, -Bs/(B*Rho)', 'field strength (used if KS is zero)', 'misalignment', 'misalignment', 'misalignment']
    '''
