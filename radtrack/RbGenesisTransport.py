import sys
import radtrack.rbcbt as rbcbt
from PyQt4 import QtGui
import radtrack.beamlines.RbGenesisElements as module

class RbGenesisTransport(rbcbt.RbCbt):
    defaultTitle = 'Genesis Bunch Transport'
    acceptsFileTypes = [module.fileExtension]
    task = 'Design a Genesis beam line'

    def __init__(self, parent = None):
        rbcbt.RbCbt.__init__(self, module, parent)

    def writeElegantFile(self, fileName, momentum):
        with open(fileName, "w") as outputFile:
            outputFile.write('! This Elegant file was created by RadTrack\n')
            outputFile.write('! RadTrack (c) 2013, RadiaSoft, LLC\n\n')

            for element in self.elementDictionary.values():
                outputFile.write(element.elegantElement(momentum).componentLine() + '\n')

            outputFile.write('\nRETURN')


def main():
    app = QtGui.QApplication(sys.argv)
    myapp = RbGenesisTransport()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
