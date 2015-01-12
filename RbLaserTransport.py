import rbcbt, sys
from PyQt4 import QtGui, QtCore

class RbLaserTransport(rbcbt.RbCbt):
    def __init__(self, parent = None):
        rbcbt.RbCbt.__init__(self, 'laser', parent)


def main():
    app = QtGui.QApplication(sys.argv)
    myapp = RbLaserTransport()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
