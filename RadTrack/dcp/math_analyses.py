from PyQt4 import QtGui
from average import *
from four import *

class moverage(QtGui.QDialog):
    def __init__(self, parent = None):
        super(moverage, self).__init__()
        self.ui = Ui_average()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

class fourier(QtGui.QDialog):
    def __init__(self, parent = None):
        super(fourier, self).__init__()
        self.ui = Ui_four()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
