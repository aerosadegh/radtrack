import os, glob
from itertools import izip_longest
import radtrack.beamlines.RbElegantElements as ele
import radtrack.beamlines.RbOpticalElements as opt
from radtrack.RbUtility import insideQuote

import radtrack.util.resource as resource
if not os.getenv('RPN_DEFNS', None):
    os.environ['RPN_DEFNS'] = resource.filename('defns.rpn')

exportEnd = '_export.lte'

elegantFilesLocation = os.path.join(os.getcwd(), 'deprecated', 'elegant')
particleFileList = glob.glob(os.path.join(elegantFilesLocation, 'beamlines', '*.lte'))
opticalFileList = glob.glob(os.path.join(os.getcwd(), 'deprecated', 'laser_transport', '*.rad'))

fileLists = [particleFileList, opticalFileList]
fileHandlers = [ele, opt]

sddsFileName = os.path.join(elegantFilesLocation, 'bunches', 'elegantSimTest.sdds')
# Test that importing an .lte file and an exported version of that file
# result in the same elements being created
def test_import_export():
    for fileList, fileHandler in zip(fileLists, fileHandlers):
        for fileName in fileList:
            elementDictionary1, default1 = fileHandler.fileImporter(fileName)
            exportFileName = os.path.splitext(fileName)[0] + exportEnd
            fileHandler.exportToFile(exportFileName, elementDictionary1, default1)
            with open(exportFileName) as f:
                # Check that lines are not split inside quotes
                for line in f:
                    assert not insideQuote(line, len(line) - 1)

            elementDictionary2, default2 = fileHandler.fileImporter(exportFileName)

            #assert elementDictionary1 == elementDictionary2
            if not elementDictionary1 == elementDictionary2:
                for name in elementDictionary1:
                    e1 = elementDictionary1[name]
                    e2 = elementDictionary2[name]
                    if not e1 == e2:
                        print fileName
                        print name
                        for index in range(len(e1.data)):
                            assert e1.data[index].strip(' "') == e2.data[index].strip(' "')
            assert default1 == default2
            os.remove(exportFileName)

if __name__ == '__main__':
    test_import_export()
