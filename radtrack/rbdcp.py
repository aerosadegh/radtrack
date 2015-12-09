"""
Copyright (c) 2015 RadiaBeam Technologies. All rights reserved
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from os.path import expanduser, dirname
import sdds, sys, math

import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui, QtCore

from radtrack.dcp.Servicelib import *
from radtrack.dcp.SRWlib import SRWFileRead1, SRW
from radtrack.gui.matplotlibwidget import matplotlibWidget
from radtrack.RbUtility import scatConPlot

NumPage = 0
ColumnXAxis =-1
MaxNumParam=999

class RbDcp(QtGui.QWidget):
    acceptsFileTypes = ['save', 'twi','out','sig','cen','dat','txt','sdds','bun','fin','dat']
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
        layout.addWidget(self.quickplot)
        c.setText('Custom Plot')
        layout.addWidget(c, alignment = QtCore.Qt.AlignCenter)
        form = QtGui.QFormLayout()
        self.xaxis = QtGui.QComboBox()
        self.yaxis = QtGui.QComboBox()
        self.plotType = QtGui.QComboBox()
        self.plotType.addItem('Scatter')
        self.plotType.addItem('Scatter-Line')
        self.plotType.addItem('Line')
        self.plotType.addItem('Contour')
        self.plotType.addItem('Combo')
        form.addRow('x-axis',self.xaxis)
        form.addRow('y-axis',self.yaxis)
        form.addRow('Plot type', self.plotType)
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
        self.plotType.activated.connect(self.customgraph)
        
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
        elif ext == 'dat':
            self.showDCP_srw(openFile)
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
        #get file info
        phile = QtCore.QFileInfo(openFile)

        #SDDS specific code
        self.x=sdds.SDDS(0)
        self.x.load(openFile)

        #get # of pages and columns
        (_,_,_,_,Ncol,_,_,Npage)=SDDSreshape(self.x,ColumnXAxis,ColumnPicked,NumPage)
        stringOut="Columns: "+str(Ncol)+" Pages: "+str(Npage)+" ColumnElements: "+\
        str(np.shape(self.x.columnData)[2])
        paramsOut ='\nPARAMTER INFO \n'
        for i,a in enumerate(self.x.parameterName):
            paramsOut+=str(a)+'='+str(self.x.parameterData[i])+'\n'
        self.legend.setText(QtGui.QApplication.translate("dcpwidget",\
            'FILE INFO \n'+'File Name: '+phile.fileName()+'\nFile Size: '+str(phile.size())+' bytes \n'+\
            self.x.description[0]+stringOut+paramsOut, None, QtGui.QApplication.UnicodeUTF8))

        #preview of parameters
        self.preview(Ncol)

        #preview of sdds data
        self.sddsprev(Ncol)
        
    def showDCP_srw(self, openFile):
        #reset data selection
        ColumnPicked = [0]
        ColumnXAxis = -1
        #get file info
        phile = QtCore.QFileInfo(openFile)
        
        #SRW specific
        x = SRW()
        self.x=SRWFileRead1(x,openFile,MaxNumParam)
        #get columns
        (_,_,_,Ncol,_,_)=SRWreshape(self.x,ColumnXAxis,ColumnPicked)
        stringOut="Columns: "+str(np.shape(x.columnData)[0])+" Pages: 1"+" ColumnElements: "+\
        str(np.shape(x.columnData)[1])
        self.legend.setText(QtGui.QApplication.translate("dcpwidget", 'FILE INFO \n'+'File Name: '+\
            phile.fileName()+'\nFile Size: '+str(phile.size())+' bytes \n'+stringOut, None, QtGui.QApplication.UnicodeUTF8))
            
        self.preview(Ncol)
        self.srwprev(Ncol)
        
    def srwprev(self,Ncol):
        ColumnPicked = range(Ncol)
        (Xrvec,Yrvec,Npar,Ncol,NcolPicked,NElemCol)=SRWreshape(self.x,ColumnXAxis,ColumnPicked)
        for i, a in enumerate(Yrvec):
            if len(a)<1000:
                self.data.setRowCount(np.shape(Yrvec)[1])
                for j, b in enumerate(a):
                    self.data.setItem(j+3,i,QtGui.QTableWidgetItem(str(b)))
            else:
                for j in range(1000):
                    self.data.setItem(j+3,i,QtGui.QTableWidgetItem(str(a[j])))
        
    def sddsprev(self,Ncol):
        ColumnPicked = range(Ncol)
        (Xrvec,Yrvec,YLab,Npar,Ncol,NcolPicked,NElemCol,Npage)=SDDSreshape(self.x,ColumnXAxis,ColumnPicked,NumPage) #reshapes file into vectors and a matrix

        for i, a in enumerate(Yrvec):
            #if i>0:# skip first column i+1=>i to adjust, because of extra 0 column!!!?
            if len(a)<1000:
                self.data.setRowCount(np.shape(Yrvec)[1]+4)
                for j, b in enumerate(a):
                    self.data.setItem(j+3,i,QtGui.QTableWidgetItem(str(b)))
            else:
                for j in range(1000):
                    self.data.setItem(j+3,i,QtGui.QTableWidgetItem(str(a[j])))
                    
    def preview(self,Ncol):
        self.reset()

        #set table sizes
        self.data.setRowCount(1000)
        self.data.setColumnCount(Ncol+1)

        for i,a in enumerate(self.x.columnDefinition):
            self.data.setItem(0,i, QtGui.QTableWidgetItem(a[2]))
            self.data.setItem(2,i, QtGui.QTableWidgetItem(a[1]))

        for i,a in enumerate(self.x.columnName):
            self.data.setItem(1,i,QtGui.QTableWidgetItem(a))

    def reset(self):
        self.widget.canvas.ax.clear()
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
    
        def find_param(pname):
            output = None
            for i,a in enumerate(self.x.columnName):
                if pname == a:
                    output = i
                    break
            if output == None:
                raise TypeError('Parameter Not Found, NaN')
            return output
            
        if self.currentFiletype == 'twi':
            self.xaxis.setCurrentIndex(find_param('s')) #0
            if self.quickplot.currentIndex() == 0:
                self.yaxis.setCurrentIndex(find_param('betax')) #1
            elif self.quickplot.currentIndex() == 1:
                self.yaxis.setCurrentIndex(find_param('betay')) #7
                
        elif self.currentFiletype == 'out':
            if self.quickplot.currentIndex() == 0:
                self.xaxis.setCurrentIndex(find_param('t'))#4
                self.yaxis.setCurrentIndex(find_param('p'))#5
            elif self.quickplot.currentIndex() == 1:
                self.xaxis.setCurrentIndex(find_param('x'))#0
                self.yaxis.setCurrentIndex(find_param('y'))#2
                
        elif self.currentFiletype == 'sig':
            self.xaxis.setCurrentIndex(find_param('s'))#0
            if self.quickplot.currentIndex() == 0:
                self.yaxis.setCurrentIndex(find_param('Sx'))#53
            elif self.quickplot.currentIndex() == 1:
                self.yaxis.setCurrentIndex(find_param('Sy'))#55

        self.customgraph()
    
    def customgraph(self):
        self.parent.ui.statusbar.showMessage('Drawing plot ...')
        ColumnXAxis=0
        xname = self.xaxis.currentText()
        ColumnXAxis = self.xaxis.currentIndex()
        yname = self.yaxis.currentText()
        ColumnPicked = [self.yaxis.currentIndex()]

        if self.currentFiletype == 'dat':
            (Xrvec,Yrvec,Npar,Ncol,NcolPicked,NElemCol)=SRWreshape(self.x,ColumnXAxis,ColumnPicked)
        else:
            (Xrvec,Yrvec,Ylab,Npar,Ncol,NcolPicked,NElemCol,Npage)=SDDSreshape(self.x,ColumnXAxis,ColumnPicked,NumPage)

        try:
            yu = ' ['+self.x.columnDefinition[ColumnPicked[0]][1]+']'
            xu = ' ['+self.x.columnDefinition[ColumnXAxis][1]+']'
        except IndexError:
            yu = ''
            xu = ''

        # Plot
        try:
            numParticles = np.shape(Xrvec)[0]
            nLevels = 5 + int(math.pow(numParticles, 0.333333333))
            nDivs = 10 + int(math.pow(numParticles, 0.2))
            self.widget.canvas.ax.clear()
            scatConPlot(self.plotType.currentText().lower(), Xrvec, Yrvec[0,:], self.widget.canvas.ax, nDivs, nLevels)
            self.widget.canvas.ax.set_xlabel(xname + xu)
            self.widget.canvas.ax.set_ylabel(yname + yu)
            self.widget.canvas.fig.set_facecolor('w')
            self.widget.canvas.fig.tight_layout()

            margin = 0.05 # percentage of width and height
            xMin = min(Xrvec)
            xMax = max(Xrvec)
            xRange = xMax - xMin
            yMin = min(Yrvec[0])
            yMax = max(Yrvec[0])
            yRange = yMax - yMin

            self.widget.canvas.ax.set_xlim([xMin - margin*xRange, xMax + margin*xRange])
            self.widget.canvas.ax.set_ylim([yMin - margin*yRange, yMax + margin*yRange])
            self.widget.canvas.draw()

        except ValueError: # Attempted to plot non-numeric values
            pass

        self.parent.ui.statusbar.clearMessage()
                
def main():
    app = QtGui.QApplication(sys.argv)
    myapp = RbDcp()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
