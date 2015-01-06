"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

"""
#base imports
import sys
from PySide.QtCore import *
from PySide.QtGui import *
import numpy as np

#custom imports

#import your gui made from 'pyside-uic -o yourgui.py yourgui.ui'
from RadTrack.dcp.layout import *
from RadTrack.dcp.Servicelib import IFileTypeCheck
from RadTrack.dcp.Servicelib import column, columnS
from RadTrack.dcp.SDDSlib import SDDSconvert, SDDSParRead, SDDSColRead
from RadTrack.dcp.SRWlib import SRWFileRead
from RadTrack.dcp.Plotlib import *

# global constants and parameters
global MaxNumParam, IFileName, CFileName, PFileName, MaxNumLines
global MaxNumParam, MaxNumColum
 
class RbGui(QtGui.QMainWindow):
    #Constructor
    def __init__(self, parent=None):
        super(RbGui, self).__init__()
        self.ui = Ui_layout()
        self.ui.setupUi(self)
        
        #connections
        self.ui.actionOpen.triggered.connect(self.showDlg)
        self.ui.comboBox.currentIndexChanged.connect(self.graph) #show graph when parameter changes

    #input file
    def showDlg(self):
        #get file path
        IFileName, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                    '/home')
        OFileName="1.txt"
        PFileName='parameters.txt'
        CFileName='columns.txt'

        MaxNumParam=999
        MaxNumColum=999

        IFileType=IFileTypeCheck(IFileName)

        #sdds section incomplete
        if  IFileType.name=="sdds":
            (Npar, Ncol)=SDDSconvert(IFileName,MaxNumParam, CFileName, PFileName)           
            parn=SDDSParRead(PFileName) 
            (coln,Ncoln)=SDDSColRead(CFileName, Ncol, MaxNumColum)
            print (Npar, Ncol)
            Xvec=[float(s) for s in column(coln[1:Ncoln],0)]

            Yvec1=columnS(coln[1:Ncoln],1,4)
            #PlotColnS(Xvec,Yvec1,'-','o',"Plot","Distance, m","Function, a.u.")
            self.ui.widget.canvas.ax.clear()
            self.ui.widget_2.canvas.ax.clear()
            self.ui.widget.canvas.ax.plot(Xvec,Yvec1,'r.')
            self.ui.widget.canvas.draw()
            self.ui.tableWidget.clear()
            for i in range(20):
                for j in range(4):
                    self.ui.tableWidget.setItem(i, j, QTableWidgetItem(coln[i][j]))
                    
        elif IFileType.name=="srw":
            #read file
            (Npar,Ncol,parn,coln,Legend)=SRWFileRead(IFileName,MaxNumParam)
            print (Npar, Ncol)
            self.data = coln            

            #preview tables
            self.ui.tableWidget.clear()
            self.ui.tableWidget_2.clear()
            #set header for table 2
            self.ui.tableWidget_2.setHorizontalHeaderItem(0, QTableWidgetItem('Parameters'))
            self.ui.tableWidget_2.setHorizontalHeaderItem(1, QTableWidgetItem(None))
            #input data from file
            f=open(IFileName,'r',0)
            #read lines 1-9
            for i in range(1,11):
                line = f.readline()
                if i>1:
                    L = line.split('#') #parse line by #
                    L[2].rstrip() #removes \n
                    #set table items
                    self.ui.tableWidget_2.setItem( i-2 , 0, QTableWidgetItem(L[2]))
                    self.ui.tableWidget_2.setItem( i-2 , 1, QTableWidgetItem(L[1]))
                elif i<2:
                    L = line.split(']')
                    for j in range(0,3):
                        L[j] = L[j].translate(None, '#[T,') #removes  characters: #[T,
                        #set table header
                        self.ui.tableWidget.setHorizontalHeaderItem(j , QTableWidgetItem(L[j]))
                        
            f.close()
            #set table items from body for firt 20 data lines
            for i in range(20):
                for j in range(3):
                    self.ui.tableWidget.setItem(i, j, QTableWidgetItem(coln[i][j]))

    #graphs q v. B(q) and B(q) v. B(j) and B(k)
    def graph(self):
        num = self.ui.comboBox.currentIndex()
        Xvec = [i for i in range(np.shape(self.data)[0])]
        Yvec = [float(s) for s in column(self.data,num)]
        Yvec1 = None
        
        if num == 0:
            Yvec1= columnS(self.data,1,2)
        elif num == 1:
            Yvec1= columnS(self.data,0,2)
        elif num == 2:
            Yvec1= columnS(self.data,0,1)
        self.ui.widget.canvas.ax.clear()
        self.ui.widget_2.canvas.ax.clear()
        self.ui.widget.canvas.ax.plot(Xvec, Yvec, 'r.')
        self.ui.widget_2.canvas.ax.plot(Yvec, Yvec1, 'b--')
        self.ui.widget.canvas.draw()
        self.ui.widget_2.canvas.draw()
        
 
def main():

    app = QtGui.QApplication(sys.argv)
    myapp = RbGui()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
