import sys
import radtrack.rbcbt as rbcbt
from PyQt4 import QtGui
import radtrack.beamlines.RbElegantElements as module

class RbBunchTransport(rbcbt.RbCbt):
    defaultTitle = 'Elegant Bunch Transport'
    acceptsFileTypes = [module.fileExtension]
    task = 'Design an Elegant beam line'

    def __init__(self, parent = None):
        rbcbt.RbCbt.__init__(self, module, parent)

    def writeElegantFile(self, fileName, momentum):
        self.exportToFile(fileName)

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = RbBunchTransport()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
