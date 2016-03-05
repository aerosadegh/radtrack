# Classes here describe all optical elements that propgate
# wavefronts

from __future__ import print_function, division, unicode_literals, absolute_import
from PyQt4.QtCore import Qt
from radtrack.beamlines.RbElementCommon import *
from radtrack.beamlines.RbElegantElements import importFile, exportToFile
from radtrack.beamlines.RbBeamlines import BeamlineCommon
from radtrack.util.unitConversion import convertUnitsStringToNumber

class opticalElement(elementCommon):
    def componentLine(self):
        sentence = [(param, str(convertUnitsStringToNumber(datum, unit))) \
                for param, datum, unit in \
                zip(self.parameterNames, self.data, self.units) if datum]
        sentence = ', '.join(['='.join(phrase) for phrase in sentence])

        return self.name + ':    ' + type(self).__name__ + ', ' + sentence


class OpticalBeamline(BeamlineCommon):
    def componentLine(self):
        return self.name + ':    ' + self.displayLine()

beamlineType = OpticalBeamline
fileExtension = 'rad'

class DRIFT(driftPic, opticalElement):
    elementDescription = 'A straight section through a homogenous material.'
    parameterNames = ['L', 'N']
    units = ['m', '']
    dataType = ['double', 'double']
    parameterDescription = ['length of travel', 'index of refraction']
    beamColor = Qt.red
    beamWidth = .03 # meters

class CIRCULAR_APERTURE(opticalElement, aperturePic):
    elementDescription = 'A circular aperture for narrowing width of a beam.'
    parameterNames = ['R', 'L']
    units = ['m', 'm']
    dataType = ['double', 'double']
    parameterDescription = ['radius of aperture opening', 'thickness of aperture along beam path']
    beamWidth = DRIFT.beamWidth
    beamColor = DRIFT.beamColor

class RECTANGULAR_APERTURE(opticalElement, aperturePic):
    elementDescription = 'A rectangular aperture for narrowing width of a beam.'
    parameterNames = ['SIZE_X', 'SIZE_Y', 'L']
    units = ['m', 'm', 'm']
    dataType = ['double', 'double', 'double']
    parameterDescription = ['half-horizontal size of aperture opening', 'half-vertical size of aperture opening', 'thickness of aperture along beam path']
    beamWidth = DRIFT.beamWidth
    beamColor = DRIFT.beamColor

class LENS(opticalElement, lensPic):
    elementDescription = 'A thin lens.'
    parameterNames = ['F', 'R']
    units = ['m', 'm']
    dataType = ['double', 'double']
    parameterDescription = ['Focal length', 'Radius of lens']

    def radii(self):
        focalLength = self.findParameter(['F'])
        if focalLength > 0:
            return [1,-1]
        elif focalLength < 0:
            return [-1,1]
        else:
            return [0,0]

class THICK_LENS(opticalElement, lensPic):
    elementDescription = 'A thick lens with descriptions for curvature and index of refractions.'
    parameterNames = ['R1', 'R2', 'N', 'L', 'R']
    units = ['m', 'm', '', 'm', 'm']
    dataType = ['double', 'double', 'double', 'double', 'double']
    parameterDescription = ['Front radius of curvature (0 -> flat)', 'Back radius of curvature (0 -> flat)', 'Index of refraction', 'Thickness of Lens (length of travel)', 'Radius of Lens']

    def radii(self):
        return [self.findParameter(['R1']), -self.findParameter(['R2'])]

class MIRROR(opticalElement, mirrorPic):
    elementDescription = 'A flat mirror.'
    parameterNames = ['THETA', 'F', 'XSIZE', 'YSIZE']
    units = ['rad', 'm', 'm', 'm']
    dataType = ['double', 'double', 'double', 'double']
    parameterDescription = ['Angle off normal incidence', 'Focal length (0 -> flat)', 'Horizontal Size', 'Vertical Size']

class GRATING(opticalElement, gratingPic):
    elementDescription = 'A transmissive grating with vertically-oriented slits.'
    parameterNames = ['P', 'THETA', 'XSIZE', 'YSIZE']
    units = ['1/m', 'rad', 'm', 'm']
    dataType = ['double', 'double', 'double', 'double']
    parameterDescription = ['Lines per mm', 'Angle of mirror from perpendicular to beam.', 'Horizontal Size', 'Vertical Size']

class REFLECTIVE_GRATING(opticalElement, reflectiveGratingPic):
    elementDescription = 'A reflective grating with vertically-oriented slits.'
    parameterNames = ['P', 'THETA', 'BLAZE', 'XSIZE', 'YSIZE']
    units = ['1/m', 'rad', 'rad', 'm', 'm']
    dataType = ['double', 'double', 'double', 'double', 'double']
    parameterDescription = ['Lines per meter', 'Angle of mirror from perpendicular to beam.', 'Blaze angle of gratings', 'Horizontal length', 'Vertical length']

class WATCH_POINT(opticalElement, watchPic):
    elementDescription = 'Outputs the laser wavefront at the current position.'
    parameterNames = []
    units = []
    dataType = []
    parameterDescription = []
    flagSize = .1

classDictionary = dict()
for key in list(globals()):
    if hasattr(globals()[key], 'elementDescription'):
        classDictionary[key] = globals()[key]
advancedNames = []

fileImporter = lambda fileName, importDictionary = None : \
        importFile(fileName, importDictionary, classDictionary, lambda x : x.upper())

fileExporter = exportToFile
