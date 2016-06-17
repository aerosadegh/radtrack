import os, glob, subprocess, string
import radtrack.beamlines.RbElegantElements as ele
import radtrack.beamlines.RbOpticalElements as opt
from radtrack.util.stringTools import insideQuote

import radtrack.util.resource as resource
if not os.getenv('RPN_DEFNS', None):
    os.environ['RPN_DEFNS'] = resource.filename('defns.rpn')

exportEnd = '_export.lte'

elegantFilesLocation = os.path.join(os.getcwd(), 'use_cases', 'elegant')
opticalFilesLocation = os.path.join(os.getcwd(), 'use_cases', 'laser_transport')
particleSuffix = '.lte'
opticalSuffix = '.rad'

suffixes = [particleSuffix, opticalSuffix]
fileLocations = [elegantFilesLocation, opticalFilesLocation]
fileHandlers = [ele, opt]

# Can't handle these files with RPN calcs outside element descriptions or other errors
skipFiles = [os.path.join(os.getcwd(), n) for n in ['use_cases/elegant/elegantExamples/rfDeflectingCavity/lattice.lte',
                                                    'use_cases/elegant/elegantExamples/ellipseComparison/par10h.lte',
                                                    'use_cases/elegant/elegantExamples/chromaticResponse/full457MeV.lte',
                                                    'use_cases/elegant/elegantExamples/beamBreakup/lattice.lte',
                                                    'use_cases/elegant/elegantExamples/multibunchCollectiveEffects/APS-24Bunch-CBI/lattice.lte',
                                                    'use_cases/elegant/elegantExamples/rampTunesWithBeam/par10h.lte',
                                                    'use_cases/elegant/elegantExamples/pepperPot/lattice.lte']]

# Test that importing an .lte file and an exported version of that file
# result in the same elements being created
def test_import_export():
    for suffix, fileLocation, fileHandler in zip(suffixes, fileLocations, fileHandlers):
        for walkTuple in os.walk(fileLocation):
            dirName = walkTuple[0]
            for fileName in [os.path.join(dirName, name) for name in walkTuple[2] if name.endswith(suffix)]:
                if fileName in skipFiles:
                    continue
                elementDictionary1, default1 = fileHandler.fileImporter(fileName)
                exportFileName = os.path.splitext(fileName)[0] + exportEnd
                fileHandler.exportToFile(exportFileName, elementDictionary1, default1)
                with open(exportFileName) as f:
                    # Check that lines are not split inside quotes
                    for line in f:
                        assert not insideQuote(line, len(line) - 1)

                elementDictionary2, default2 = fileHandler.fileImporter(exportFileName)

                if not elementDictionary1 == elementDictionary2:
                    for name in elementDictionary1:
                        e1 = elementDictionary1[name]
                        e2 = elementDictionary2[name]
                        if not e1 == e2:
                            print fileName
                            print name
                            if not e1.isBeamline():
                                assert compareNormalizedElementData(e1, e2)
                            else:
                                for index in range(max(len(e1.data), len(e2.data))):
                                    assert compareNormalizedElementData(e1.data[index], e2.data[index])
                assert default1 == default2
                os.remove(exportFileName)


def compareNormalizedElementData(e1, e2):
    print e1.data
    print e2.data
    for thing1, thing2 in zip(e1.data, e2.data):
        for thing in [thing1, thing2]:
            thing = string.replace(thing, '-0', '-')
            if thing.startswith('.'):
                thing = '0' + thing
        if thing1 != thing2 and float(thing1) != float(thing2):
            return False
    return True


if __name__ == '__main__':
    test_import_export()
