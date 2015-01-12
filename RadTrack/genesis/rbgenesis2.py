import sys
from PyQt4 import QtGui, QtCore
from genesis import *
from genesispages import *

class RbGenesis2(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_genesis()
        self.ui.setupUi(self)
        self.ui.undulator.clicked.connect(self.undpopup)
        self.ui.focus.clicked.connect(self.fodopopup)
        self.ui.beam.clicked.connect(self.beampopup)

    def undpopup(self):
        dialog = undulator_dialog()
        if dialog.exec_():
            pass
                                      
    def fodopopup(self):
        dialog = fodo_dialog()
        if dialog.exec_():
            pass
                                      
    def beampopup(self):
        dialog = beam_dialog()
        if dialog.exec_():
            pass
                                      


class undulator_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(makeund(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)

class fodo_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(makefodo(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)
        
class beam_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(makebeam(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)
        

def main():

    app = QtGui.QApplication(sys.argv)
    myapp = RbGenesis2()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        

        

        
                         
