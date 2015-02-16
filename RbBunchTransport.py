import rbcbt, sys
from PyQt4 import QtGui, QtCore

class RbBunchTransport(rbcbt.RbCbt):
    def __init__(self, parent = None):
        module = __import__('RadTrack.beamlines.RbElegantElements', fromlist='.')
        rbcbt.RbCbt.__init__(self, module, parent)


def main():
    app = QtGui.QApplication(sys.argv)
    myapp = RbBunchTransport()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
