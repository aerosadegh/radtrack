import os, glob, sys
import radtrack.beamlines.RbElegantElements as ele
import radtrack.beamlines.RbOpticalElements as opt
from radtrack.RbUtility import insideQuote

# QApplication needs to be instantiated to use QWidgets
# that can't be isolated from the rest of the application.
# If this isn't here, the test suite will simply halt with
# no messages.
#
# Note: make sure this is only called once during the entire test
# run. If more than one QApplications are created, python will
# crash at the end of the test suite.
from PyQt4 import QtGui
app = QtGui.QApplication(sys.argv)

exportEnd = '_export.lte'

particleFileList = glob.glob(
        os.path.join(os.getcwd(), 'deprecated', 'elegant', 'beamlines', '*.lte'))

opticalFileList = glob.glob(
        os.path.join(os.getcwd(), 'deprecated', 'laser_transport', '*.rad'))

fileLists = [particleFileList, opticalFileList]
fileHandlers = [ele, opt]

# Test that importing an .lte file and an exported version of that file
# result in the same elements being created
def test_import_export():
    for fileList, fileHandler in zip(fileLists, fileHandlers):
        for fileName in fileList:
            elementDictionary1, _ = fileHandler.fileImporter(fileName)
            exportFileName = os.path.splitext(fileName)[0] + exportEnd
            fileHandler.exportToFile(exportFileName, elementDictionary1)
            with open(exportFileName) as f:
                # Check that lines are not split inside quotes
                for lineNumber, line in enumerate(f.readlines()):
                    assert not insideQuote(line, len(line))

            elementDictionary2, _ = fileHandler.fileImporter(exportFileName)

            assert all([element1 == element2 for (element1, element2) in \
                    zip(elementDictionary1.values(), elementDictionary2.values())])

            os.remove(exportFileName)
