import rbcbt, sys
from PyQt4 import QtGui
import RadTrack.beamlines.RbElegantElements as module

class RbBunchTransport(rbcbt.RbCbt):
    def __init__(self, parent = None):
        rbcbt.RbCbt.__init__(self, module, parent)


def main():
    app = QtGui.QApplication(sys.argv)
    myapp = RbBunchTransport()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
