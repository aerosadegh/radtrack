import sys
import radtrack.rbcbt as rbcbt
from PyQt4 import QtGui
import radtrack.beamlines.RbOpticalElements as module

class RbLaserTransport(rbcbt.RbCbt):
    def __init__(self, parent = None):
        rbcbt.RbCbt.__init__(self, module, parent)
        self.container = self
        self.defaultTitle = parent.tr('Laser Transport')


def main():
    app = QtGui.QApplication(sys.argv)
    myapp = RbLaserTransport()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
