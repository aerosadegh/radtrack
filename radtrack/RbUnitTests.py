import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui
import sys

app = QtGui.QApplication(sys.argv)

try:
    from examples.UnitTests import \
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
