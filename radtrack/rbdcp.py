"""
Copyright (c) 2015 RadiaBeam Technologies. All rights reserved
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from os.path import expanduser, dirname
import sdds
import sys

import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui, QtCore

from radtrack.dcp.Servicelib import *
from radtrack.dcp.SRWlib import SRWFileRead1, SRW
from radtrack.dcp.Plotlib2axis import *
from radtrack.gui.matplotlibwidget import matplotlibWidget

ColumnPicked = [0]
NumPage = 0
ColumnXAxis =-1
MaxNumParam=999
MaxNumColum=999

class RbDcp(QtGui.QWidget):
    acceptsFileTypes = ['save', 'twi','out','sig','cen','dat','txt','sdds','bun','fin']
    defaultTitle = 'Data Visualization'
    task = 'Analyze simulation results'
    category = 'tools'
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self)
        main = QtGui.QHBoxLayout()
        self.setLayout(main)
        self.parent = parent
        self.left_panel(main)
        self.right_panel(main)
        
        if self.parent is None:
            self.parent = self
            self.parent.lastUsedDirectory = expanduser('~').replace('\\', '\\\\')
        self.container = self
        self.currentFiletype = ''
        
    def exportToFile(self, fileName):
        with open(fileName, 'w'):
            pass
        
    def importFromFileList(self, listItem):
        self.importFile(listItem.text())
        
    def left_panel(self,main):
        frame = QtGui.QWidget(self)
        layout = QtGui.QVBoxLayout()
        a = QtGui.QLabel()
        b = QtGui.QLabel()
        c = QtGui.QLabel()
        a.setText('Available Data')
        layout.addWidget(a, alignment = QtCore.Qt.AlignCenter)
        self.files = QtGui.QListWidget(frame)
        self.files.setSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Preferred)
        layout.addWidget(self.files)
        b.setText('Quick Plot')
        layout.addWidget(b, alignment = QtCore.Qt.AlignCenter)
        self.quickplot = QtGui.QComboBox(frame)
        #self.quickplot.setSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Preferred)
        layout.addWidget(self.quickplot)
        c.setText('Custom Plot')
        layout.addWidget(c, alignment = QtCore.Qt.AlignCenter)
        form = QtGui.QFormLayout()
        self.xaxis = QtGui.QComboBox()
        self.yaxis = QtGui.QComboBox()
        form.addRow('x-axis',self.xaxis)
        form.addRow('y-axis',self.yaxis)
        layout.addLayout(form)
        button = QtGui.QPushButton(frame)
        button.setText('open')
        button.clicked.connect(lambda : self.importFile())
        layout.addWidget(button)
        layout.addStretch()   
        self.legend = QtGui.QTextEdit()
        self.legend.setSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Preferred)
        layout.addWidget(self.legend)
        main.addLayout(layout)
        self.files.itemClicked.connect(self.importFromFileList)
        self.quickplot.activated.connect(self.graphset)
        self.xaxis.activated.connect(self.customgraph)
        self.yaxis.activated.connect(self.customgraph)
        
    def right_panel(self,main):
        frame = QtGui.QWidget(self)
        vb = QtGui.QVBoxLayout()
        a = QtGui.QLabel()
        a.setText('DATA')
        vb.addWidget(a,alignment = QtCore.Qt.AlignCenter)
        self.data = QtGui.QTableWidget()
        self.data.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.MinimumExpanding)
        vb.addWidget(self.data)
        b = QtGui.QLabel()
        b.setText('PLOT')
        vb.addWidget(b,alignment = QtCore.Qt.AlignCenter)
        self.widget = matplotlibWidget()
        vb.addWidget(self.widget)
        main.addLayout(vb)
        
    def exportToFile(self, fileName):
        with open(fileName, 'w'):
            pass
        
    def importFromFileList(self, listItem):
        self.importFile(listItem.text())
        
    def importFile(self, openFile = None):
        if not openFile:
            openFile = QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.parent.lastUsedDirectory)
            if not openFile:
                return
            else:
                self.parent.lastUsedDirectory = dirname(openFile)

        ext = os.path.splitext(openFile)[-1].lower().lstrip(".")
        if ext in ['sdds', 'out', 'twi', 'sig', 'cen', 'bun', 'fin']:
            self.showDCP_ele(openFile)
        elif ext == 'save':
            return
        else:
            raise ValueError(openFile + " unrecognized file type.")

        for index in range(self.files.count()):
            if self.files.item(index).text() == openFile:
                self.files.setCurrentRow(index)
                break
        else:
            self.files.addItem(openFile)
            self.files.setCurrentRow(self.files.count() - 1)

        try:
            self.parent.addToRecentMenu(openFile, True)
        except AttributeError:
            pass

        self.currentFiletype = ext
        if ext == 'twi':
            self.twiselect()
        elif ext == 'out':
            self.outselect()
        elif ext == 'sig':
            self.sigselect()
            
        self.dataopt()
        
    def showDCP_ele(self, openFile):
        #reset data selection
        ColumnPicked = [0]
        ColumnXAxis = -1

        #SDDS specific code
        self.x=sdds.SDDS(0)
        self.x.load(openFile)

        #get # of pages and columns
        (_,_,_,_,self.Ncol,_,_,Npage)=SDDSreshape(self.x,ColumnXAxis,ColumnPicked,NumPage)
        stringOut="Columns: "+str(self.Ncol)+" Pages: "+str(Npage)+" ColumnElements: "+\
        str(np.shape(self.x.columnData)[2])
        paramsOut ='\nPARAMTER INFO \n'
        for i,a in enumerate(self.x.parameterName):
            paramsOut+=str(a)+'='+str(self.x.parameterData[i])+'\n'
        self.legend.setText(QtGui.QApplication.translate("dcpwidget",\
            'FILE INFO \n'+self.x.description[0]+stringOut+paramsOut, None, QtGui.QApplication.UnicodeUTF8))

        #preview of parameters
        self.preview()

        #preview of sdds data
        self.sddsprev()
        
    def sddsprev(self):
        ColumnPicked = []
        for i in range(self.Ncol):
            ColumnPicked.append(i)
        (Xrvec,Yrvec,YLab,Npar,Ncol,NcolPicked,NElemCol,Npage)=SDDSreshape(self.x,ColumnXAxis,ColumnPicked,NumPage) #reshapes file into vectors and a matrix

        for i, a in enumerate(Yrvec):
            #if i>0:# skip first column i+1=>i to adjust, because of extra 0 column!!!?
            if size(a)<1000:
                self.data.setRowCount(shape(Yrvec)[1]+4)
                for j, b in enumerate(a):
                    self.data.setItem(j+3,i,QtGui.QTableWidgetItem(str(b)))
            else:
                for j in range(1000):
                    self.data.setItem(j+3,i,QtGui.QTableWidgetItem(str(a[j])))
                    
    def preview(self):
        self.reset()

        #set table sizes
        self.data.setRowCount(1000)
        self.data.setColumnCount(self.Ncol+1)

        for i,a in enumerate(self.x.columnDefinition):
            self.data.setItem(0,i, QtGui.QTableWidgetItem(a[2]))
            self.data.setItem(2,i, QtGui.QTableWidgetItem(a[1]))

        for i,a in enumerate(self.x.columnName):
            self.data.setItem(1,i,QtGui.QTableWidgetItem(a))

    def reset(self):
        self.widget.canvas.ax.clear()
        self.widget.canvas.ax2.clear()
        self.widget.canvas.ax2.set_visible(False)
        self.data.clearContents()
        self.widget.canvas.draw()
        
    #displaying and setting data options method
    def dataopt(self):
        self.xaxis.clear()
        self.yaxis.clear()
        for i in self.x.columnName:
            self.xaxis.addItem(i)
            self.yaxis.addItem(i)

    def twiselect(self):
        self.quickplot.clear()
        self.quickplot.addItem('s v. beta x')
        self.quickplot.addItem('s v. beta y')
        
    def outselect(self):
        self.quickplot.clear()
        self.quickplot.addItem('t v. p')
        self.quickplot.addItem('x v. y')
        
    def sigselect(self):
        self.quickplot.clear()
        self.quickplot.addItem('s v. sigma x')
        self.quickplot.addItem('s v. sigma y')
        
    def graphset(self):
        if self.currentFiletype == 'twi':
            self.xaxis.setCurrentIndex(0)
            if self.quickplot.currentIndex() == 0:
                self.yaxis.setCurrentIndex(1)
            elif self.quickplot.currentIndex() == 1:
                self.yaxis.setCurrentIndex(7)
                
        elif self.currentFiletype == 'out':
            if self.quickplot.currentIndex() == 0:
                self.xaxis.setCurrentIndex(4)
                self.yaxis.setCurrentIndex(5)
            elif self.quickplot.currentIndex() == 1:
                self.xaxis.setCurrentIndex(0)
                self.yaxis.setCurrentIndex(2)
                
        elif self.currentFiletype == 'sig':
            self.xaxis.setCurrentIndex(0)
            if self.quickplot.currentIndex() == 0:
                self.yaxis.setCurrentIndex(53)
            elif self.quickplot.currentIndex() == 1:
                self.yaxis.setCurrentIndex(55)

        self.customgraph()
    
    def customgraph(self):
        ColumnXAxis=0
        xname = self.xaxis.currentText()
        yname = self.yaxis.currentText()
        linetype = ''
        marktype = 'o'
        if (self.currentFiletype == 'twi') or (self.currentFiletype =='sig'):
            linetype = '-'
            marktype = ''
            
        ColumnPicked = []

        #resets display
        self.widget.canvas.ax.clear()
        self.widget.canvas.ax2.clear()
        self.widget.canvas.draw()
        for i,a in enumerate(self.x.columnName):
            if xname == a:
                ColumnXAxis=i
            
            if yname == a:
                ColumnPicked.append(i)
                
        (Xrvec,Yrvec,Ylab,Npar,Ncol,NcolPicked,NElemCol,Npage)=SDDSreshape(self.x,ColumnXAxis,ColumnPicked,NumPage)
        Xlab=[self.x.columnDefinition[ColumnXAxis][2]+", "+self.x.columnDefinition[ColumnXAxis][1]]
        PlotColnS1(Xrvec,Yrvec,linetype,marktype,self.x.description[0],Xlab,Ylab, self.widget.canvas)
        self.widget.canvas.ax.set_xlabel(xname)
        self.widget.canvas.ax.set_ylabel(yname)
                
def main():
    app = QtGui.QApplication(sys.argv)
    myapp = RbDcp()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
