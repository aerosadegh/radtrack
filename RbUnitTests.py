from PySide import QtGui
import sys

app = QtGui.QApplication(sys.argv)

try:
    from test.UnitTests import \
            stripCommentsTest, \
            unitConversionTest, \
            expandCollapseBeamlineTest, \
            felCalcTest, \
            rpnTest, \
            importExportTest
except:
    print "Unit test failed.\n\n+ + + + + + +\n\n"
    raise
else:
    print "All unit tests passed."
