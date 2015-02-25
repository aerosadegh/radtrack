"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

"""

import sys
from PyQt4 import QtGui, QtCore
from newsrw import Ui_Form as Ui_newsrw
from undulatorforsrw import Ui_Dialog as und_dlg
from beamforsrw import Ui_Dialog as beam_dlg
from precisionofsrw import Ui_Dialog as prec_dlg

class rbsrw(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_newsrw()
        self.ui.setupUi(self)
        self.srwdictionary = dict()
        #dialog boxes
        self.dialogu = DialogU()
        self.dialogb = DialogB()
        self.dialogp = DialogP()
        #set srw initial values in a dictionary
        self.set_und_values()
        self.set_beam_values()
        self.set_prec_values()
        #connections
        self.ui.undulator.clicked.connect(self.makeund)
        self.ui.beam.clicked.connect(self.makebeam)
        self.ui.precision.clicked.connect(self.setprec)
        self.ui.deparg.currentIndexChanged.connect(self.thin)
        
    def set_und_values(self):
        for i in range(self.dialogu.ui.formLayout.rowCount()):
            self.srwdictionary[self.dialogu.ui.formLayout.itemAt(i,0).widget().text()]=float(self.dialogu.ui.formLayout.itemAt(i,1).widget().text())
            
    def set_beam_values(self):
        for i in range(self.dialogb.ui.formLayout.rowCount()):
            self.srwdictionary[self.dialogb.ui.formLayout.itemAt(i,0).widget().text()]=float(self.dialogb.ui.formLayout.itemAt(i,1).widget().text())
            
    def set_prec_values(self):
        for i in range(self.dialogp.ui.formLayout.rowCount()):
            try:
                self.srwdictionary[self.dialogp.ui.formLayout.itemAt(i,0).widget().text()]=float(self.dialogp.ui.formLayout.itemAt(i,1).widget().text())
            except AttributeError:
                self.srwdictionary[self.dialogp.ui.formLayout.itemAt(i,0).widget().text()]=float(self.dialogp.ui.formLayout.itemAt(i,1).widget().currentIndex())
    
    '''
    def get_und_values(self):
        for i in range(self.dialogu.ui.formLayout.rowCount()):
            self.dialogp.ui.formLayout.itemAt(i,1).widget().setText(str(self.srwdictionary[self.dialogu.ui.formLayout.itemAt(i,0).widget().text()]))
            
    def get_beam_values(self):
        for i in range(self.dialogb.ui.formLayout.rowCount()):
            self.dialogb.ui.formLayout.itemAt(i,1).widget().setText(str(self.srwdictionary[self.dialogb.ui.formLayout.itemAt(i,0).widget().text()]))
            
    def get_prec_values(self):
        for i in range(self.dialog.ui.formLayout.rowCount()):
            try:
                self.dialogp.ui.formLayout.itemAt(i,1).widget().setText(str(self.srwdictionary[self.dialogp.formLayout.itemAt(i,0).widget().text()]))
            except AttributeError:
                self.dialogp.ui.formLayout.itemAt(i,1).widget().setCurrentIndex(self.srwdictionary[self.dialogp.ui.formLayout(i,0).widget().text()])         
    '''
    def thin(self,i):
        thintable = [[10000,1,1,20,10,3000,0,0,0,0],
                     [1,100,3,20,685,685,0,0,0,0],
                     [1,3,100,20,685,685,0,0,0,0],
                     [1,100,100,20,685,685,0,0,0,0],
                     [1000,100,3,20,10,3000,0,0,0,0],
                     [1000,3,100,20,10,3000,0,0,0,0],
                     [1000,30,30,20,10,3000,0,0,0,0]]
                     
        for n,x in enumerate(thintable[i]):
            self.ui.tableWidget.setItem(n,0,QtGui.QTableWidgetItem(str(x)))
                     
    def thick(self,i):
        thicktable = [[10000,1,1,20,10,3000,-0.002,-0.002,0.002,0.002],
                     [1,100,3,20,685,685,-0.002,-0.002,0.002,0.002],
                     [1,3,100,20,685,685,-0.002,-0.002,0.002,0.002],
                     [1,100,100,20,685,685,-0.002,-0.002,0.002,0.002],
                     [1000,100,3,20,10,3000,-0.002,-0.002,0.002,0.002],
                     [1000,3,100,20,10,3000,-0.002,-0.002,0.002,0.002],
                     [1000,30,30,20,10,3000,-0.002,-0.002,0.002,0.002]]
                     
        for n,x in enumerate(thicktable[i]):
            self.ui.tableWidget.setItem(n,0,QtGui.QTableWidgetItem(str(x)))
        
    def makeund(self):
        if self.dialogu.exec_():
            self.set_und_values()
            
    def makebeam(self):
        if self.dialogb.exec_():
            self.set_beam_values()
            
    def setprec(self):
        if self.dialogp.exec_():
            self.set_prec_values()
        
        
class DialogU(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = und_dlg()
        self.ui.setupUi(self)
        self.ui.numper.setText('40.5')  #Number of ID Periods (without accounting for terminations)
        self.ui.undper.setText('0.049') #Period Length
        self.ui.bx.setText('0.0')       #Peak Vertical field
        self.ui.by.setText('0.57')      #Peak Horizontal field
        self.ui.phbx.setText('0')       #Initial Phase of the Horizontal field component
        self.ui.phby.setText('0')       #Initial Phase of the Vertical field component
        self.ui.sbx.setText('-1')       #Symmetry of the Horizontal field component vs Longitudinal position
        self.ui.sby.setText('1')        #Symmetry of the Vertical field component vs Longitudinal position
        self.ui.xcid.setText('0')       #Misaligment. Horizontal Coordinate of Undulator Center 
        self.ui.ycid.setText('0')       #Misaligment. Vertical Coordinate of Undulator Center 
        self.ui.zcid.setText('0')       #Misaligment. Longitudinal Coordinate of Undulator Center
                
class DialogB(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = beam_dlg()
        self.ui.setupUi(self)
        self.ui.iavg.setText('0.5')     #Above is the UP class, this is elecBeam.iavg
        self.ui.partstatmom1x.setText('0')  #elecBeam.partStatMom1.x, initial x-offset    
        self.ui.partstatmom1y.setText('0')  #elecBeam.partStatMom1.y, initial y-offset
        self.ui.partstatmom1z.setText('0.0') #elecBeam.partStatMom1.z, initial z-offset
        self.ui.partstatmom1xp.setText('0') #elecBeam.partStatMom1.xp, initial x angle offset
        self.ui.partstatmom1yp.setText('0') #elecBeam.partStatMom1.yp, initial y angle offset
        self.ui.partstatmom1gamma.setText('5870.925') # electron beam relative energy, gamma
        
class DialogP(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = prec_dlg()
        self.ui.setupUi(self)
        self.ui.meth.setCurrentIndex(1) #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
        self.ui.relprec.setText('0.01') #relative precision
        self.ui.zstartint.setText('0') #longitudinal position to start integration (effective if < zEndInteg)
        self.ui.zendint.setText('0') #longitudinal position to finish integration (effective if > zStartInteg)
        self.ui.nptraj.setText('20000') #Number of points for trajectory calculation
        self.ui.usetermin.setCurrentIndex(1) #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
        self.ui.sampfactnxny.setText('0') #sampling factor for adjusting nx, ny (effective if > 0)
        
                
def main():
    app = QtGui.QApplication(sys.argv)
    myapp = rbsrw()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

