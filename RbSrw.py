"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

"""

import sys
from PyQt4 import QtGui, QtCore
from RadTrack.gui.RbBunchInterface import *

class RbSrw(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_bunchInterface()
        self.ui.setupUi(self)


def main():
    app = QtGui.QApplication(sys.argv)
    myapp = RbSrw()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
