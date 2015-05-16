import sys
from PyQt4 import QtGui, QtCore
from genesis import *
from genesispages import *

class RbGenesis2(QtGui.QWidget):
    acceptsFileTypes = []
    defaultTitle = 'Genesis'
    task = 'Run a Genesis simulation'
    category = 'simulations'

    def __init__(self, parent=None):
        self.parent = parent
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_genesis()
        self.ui.setupUi(self)
        self.ui.undulator.clicked.connect(self.undpopup)
        self.ui.focus.clicked.connect(self.fodopopup)
        self.ui.beam.clicked.connect(self.beampopup)
        self.ui.radiation.clicked.connect(self.radpopup)
        self.ui.particle.clicked.connect(self.ploadpopup)
        self.ui.mesh.clicked.connect(self.meshpopup)
        self.ui.time.clicked.connect(self.timepopup)
        self.ui.simulation.clicked.connect(self.simpopup)
        self.ui.scan.clicked.connect(self.scanpopup)
        self.ui.io.clicked.connect(self.iopopup)
        self.all_parameters = []

        self.container = QtGui.QScrollArea(self.parent)
        self.container.setWidget(self)

    def exportToFile(self, fileName = None):
        with open(fileName, 'w'):
            pass

    def importFile(self, fileName = None):
        pass

    def makeinfile(self):
        outputFileName, _ = QFileDialog.getSaveFileName(self,'Save As',os.path.expanduser('~'), '*'+'in')
        with open(outputFileName, 'w') as outputFile:
            outputFile.write('$NEWRUN \n')
            #stuuuufffffff
            outputFile.write('$end')
                             

    def undpopup(self):
        dialog = undulator_dialog()
        if dialog.exec_():
            self.all_parameters.append(['AW0',dialog.ui.aw0.text()])
            self.all_parameters.append(['IWITYP',str(int(dialog.ui.iwityp.isChecked()))])
            self.all_parameters.append(['XKX','0'])
            self.all_parameters.append(['XKY','1'])
            self.all_parameters.append(['XLAMD',dialog.ui.xlamd.text()])
            self.all_parameters.append(['NWIG',dialog.ui.nwig.text()])
            self.all_parameters.append(['NSEC',dialog.ui.nsec.text()])
            self.all_parameters.append(['DELAW',dialog.ui.delaw.text()])
            self.all_parameters.append(['AWX',dialog.ui.awx.text()])
            self.all_parameters.append(['AWY',dialog.ui.awy.text()])
            self.all_parameters.append(['SEED',dialog.ui.seed.text()])
            self.all_parameters.append(['IERTYP',str(dialog.ui.iertyp.value())])
            
                                      
    def fodopopup(self):
        dialog = fodo_dialog()
        if dialog.exec_():
            pass
                                      
    def beampopup(self):
        dialog = beam_dialog()
        if dialog.exec_():
            pass

    def radpopup(self):
        dialog = radiation_dialog()
        if dialog.exec_():
            pass

    def ploadpopup(self):
        dialog = ploading_dialog()
        if dialog.exec_():
            pass

    def meshpopup(self):
        dialog = mesh_dialog()
        if dialog.exec_():
            pass

    def timepopup(self):
        dialog = time_dialog()
        if dialog.exec_():
            pass

    def simpopup(self):
        dialog = sim_dialog()
        if dialog.exec_():
            pass

    def scanpopup(self):
        dialog = scan_dialog()
        if dialog.exec_():
            pass

    def iopopup(self):
        dialog = io_dialog()
        if dialog.exec_():
            pass

'''class undulator_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(makeund(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        

class fodo_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(makefodo(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
class beam_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(makebeam(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

class radiation_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(makerad(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

class ploading_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(makepload(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
class mesh_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(makemesh(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

class time_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(maketime(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

class sim_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(makesim(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

class scan_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(makescan(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

class io_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        mainlayout = QtGui.QGridLayout(self)
        self.setMinimumSize(QtCore.QSize(400,400))
        mainlayout.addWidget(makeio(),0,0)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        mainlayout.addWidget(buttonBox,1,0)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)'''
        
def main():

    app = QtGui.QApplication(sys.argv)
    myapp = RbGenesis2()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        

        

        
                         
