"""
Copyright (c) 2015 RadiaBeam Technologies. All rights reserved
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from os.path import expanduser, dirname, splitext
import sdds, sys, math, h5py, numpy

import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui, QtCore

from radtrack.dcp.Servicelib import *
from radtrack.dcp.SRWlib import SRW
from radtrack.ui.matplotlibwidget import matplotlibWidget
from radtrack.util.plotTools import scatConPlot
from radtrack.util.stringTools import removeWhitespace, isNumber
from radtrack.util.fileTools import isSDDS

NumPage = 0
ColumnXAxis =-1
MaxNumParam=999

class RbDcp(QtGui.QWidget):
    acceptsFileTypes = ['save', 'twi','out','sig','cen','dat','txt','sdds','bun','fin','h5','dist','beam']
    defaultTitle = 'Data Visualization'
    task = 'Analyze simulation results'
    category = 'tools'
    
    def __init__(self, parent = None):
        super(RbDcp, self).__init__(parent)
        main = QtGui.QHBoxLayout()
        self.setLayout(main)
        self.parent = parent
        self.left_panel(main)
        self.right_panel(main)
        
        if self.parent is None:
            self.parent = self
            self.parent.lastUsedDirectory = expanduser('~').replace('\\', '\\\\')
        self.currentFiletype = ''
        self.fileData = None
        
    def exportToFile(self, fileName):
        with open(fileName, 'w'):
            pass
        
    def importFromFileList(self, listItem):
        self.importFile(listItem.text())
        
    def left_panel(self,main):
        layout = QtGui.QVBoxLayout()
        a = QtGui.QLabel()
        b = QtGui.QLabel()
        c = QtGui.QLabel()
        a.setText('Available Data')
        layout.addWidget(a, alignment = QtCore.Qt.AlignCenter)
        self.files = QtGui.QListWidget()
        self.files.setSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Preferred)
        layout.addWidget(self.files)
        b.setText('Quick Plot')
        layout.addWidget(b, alignment = QtCore.Qt.AlignCenter)
        self.quickplot = QtGui.QComboBox()
        layout.addWidget(self.quickplot)
        c.setText('Custom Plot')
        layout.addWidget(c, alignment = QtCore.Qt.AlignCenter)
        form = QtGui.QFormLayout()
        self.xaxis = QtGui.QComboBox()
        self.yaxis = QtGui.QComboBox()
        self.plotType = QtGui.QComboBox()
        self.plotType.addItem('Linear')
        self.plotType.addItem('Log-Log')
        self.plotType.addItem('Semi-Log X')
        self.plotType.addItem('Semi-Log Y')
        self.plotStyle = QtGui.QComboBox()
        self.plotStyle.addItem('Scatter')
        self.plotStyle.addItem('Scatter-Line')
        self.plotStyle.addItem('Line')
        self.plotStyle.addItem('Contour')
        self.plotStyle.addItem('Combo')
        form.addRow('x-axis',self.xaxis)
        form.addRow('y-axis',self.yaxis)
        form.addRow('Plot Type', self.plotType)
        form.addRow('Plot Style', self.plotStyle)
        layout.addLayout(form)

        layout.addStretch()   
        self.legend = QtGui.QTextEdit()
        self.legend.setSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Preferred)
        layout.addWidget(self.legend)
        main.addLayout(layout)
        self.files.itemClicked.connect(self.importFromFileList)
        self.quickplot.activated.connect(self.graphset)
        self.xaxis.activated.connect(self.customgraph)
        self.yaxis.activated.connect(self.customgraph)
        self.plotStyle.activated.connect(self.customgraph)
        self.plotType.activated.connect(self.customgraph)
        
    def right_panel(self,main):
        vb = QtGui.QVBoxLayout()
        a = QtGui.QLabel()
        a.setText('DATA')
        vb.addWidget(a,alignment = QtCore.Qt.AlignCenter)
        self.data = QtGui.QTableWidget()
        self.data.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.MinimumExpanding)
        self.data.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
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

        ext = splitext(openFile)[-1].lower().lstrip(".")
        self.currentFiletype = ext
        if isSDDS(openFile):
            try:
                self.showDCP_ele(openFile)
                self.currentFiletype = 'sdds'
            except Exception as e:
                QtGui.QMessageBox.warning(self, 'Error Opening File', 'The file ' + openFile + ' could not be opened.\n\n' + str(e))
        elif ext == 'dat':
            self.showDCP_srw(openFile)
        elif ext == 'h5':
            self.showDCP_gen(openFile)
        elif ext == 'dist' or ext == 'beam':
            self.showPlain(openFile)
        elif ext == 'save':
            return
        else:
            QtGui.QMessageBox.warning(self, "Error Importing File", "Could not open: " + openFile + "\nUnrecognized file type.")
            return

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

        if ext == 'twi':
            self.twiselect()
        elif ext == 'out':
            self.outselect()
        elif ext == 'sig':
            self.sigselect()         
        elif ext == 'h5':
            self.h5select()
            
    def showPlain(self,openFile):
        def flatprev(f):
            for i,a in enumerate(f):
                if self.data.rowCount()<(len(a)+3):
                    if len(a)<1000:
                        self.data.setRowCount(len(a)+3)
                    else: self.data.setRowCount(1003)              
                for j,b in enumerate(a):
                    if j>=1000:
                        break
                    self.data.setItem(j+3,i,QtGui.QTableWidgetItem(str(b))) 
                    
        self.fileData = [[],[],[],[],[],[],[]]
        p = None
        self.reset()
        self.data.setColumnCount(7)
        self.data.setRowCount(3)

        with open(openFile) as phile:
            for j,line in enumerate(phile):
                e=[]
                if '?' in line and 'COLUMN' in line:
                    p=line.split('COLUMNS')[1].strip('\n').strip().split(' ')                 
                elif '#' in line:
                    continue
                elif '?' not in line:
                    #removes empty unicode artifacts
                    for i in line.strip().lstrip('u').rstrip('\n').split(' '):
                        if i: e.append(float(i.strip().strip('\n')))
                    for x,i in enumerate(e):
                        try:
                            self.fileData[x].append(i)
                        except ValueError:
                            print('fail')

        try:        
            for i,a in enumerate(p):
                self.data.setItem(1,i,QtGui.QTableWidgetItem(a))
        except TypeError:
            print('no parameters')
        flatprev(self.fileData)
        self.dataopt(p)
        
            
    def showDCP_gen(self, openFile):
        def genprev(f):
            for i,a in enumerate(f.keys()):
                if self.data.rowCount()<len(f[a]):
                    self.data.setRowCount(len(f[a]))
                try:
                    for j,b in enumerate(f[a]):
                        if j >= 1000:
                            break
                        if type(b) == numpy.ndarray:
                            self.data.setItem(j+3,i,QtGui.QTableWidgetItem(str(b[0])))             
                        else:
                            self.data.setItem(j+3,i,QtGui.QTableWidgetItem(str(b)))             
                except AttributeError:
                    pass
        def preview(Ncol):
            self.reset()
            self.data.setColumnCount(Ncol)
            self.data.setRowCount(3)
            for i,a in enumerate(self.fileData.keys()):
                self.data.setItem(1,i,QtGui.QTableWidgetItem(a))
                        
        phile = QtCore.QFileInfo(openFile)
        self.fileData=h5py.File(openFile)
        try:
            self.fileData['s']
        except KeyError:
            self.fileData.create_dataset('s', shape = (self.fileData['lattice']['z'].shape[0],1),data = self.fileData['lattice']['z'])
        Ncol = len(self.fileData.keys())
        stringOut = "Columns: "+ str(Ncol) + " Pages: 1" + " ColumnElements: ?"
        self.legend.setText(QtGui.QApplication.translate("dcpwidget", 'FILE INFO \n'+'File Name: '+\
            phile.fileName()+'\nFile Size: '+str(phile.size())+' bytes \n'+stringOut, None, QtGui.QApplication.UnicodeUTF8))
        
        preview(Ncol)
        #preview hdf5 file data    
        genprev(self.fileData)
        #populate graph options
        self.dataopt(self.fileData.keys())       
            
    def showDCP_ele(self, openFile):
        def sddsprev(Ncol):
            ColumnPicked = range(Ncol)
            (Xrvec,Yrvec,YLab,Npar,Ncol,NcolPicked,NElemCol,Npage)=SDDSreshape(self.fileData,ColumnXAxis,ColumnPicked,NumPage) #reshapes file into vectors and a matrix

            for i, a in enumerate(Yrvec):
                #if i>0:# skip first column i+1=>i to adjust, because of extra 0 column!!!?
                for j, b in enumerate(a):
                    if j >= 1000:
                        break
                    self.data.setItem(j+3,i,QtGui.QTableWidgetItem(str(b)))
                else:
                    self.data.setRowCount(np.shape(Yrvec)[1]+3)
                    
        #reset data selection
        ColumnPicked = [0]
        ColumnXAxis = -1
        #get file info
        phile = QtCore.QFileInfo(openFile)

        #SDDS specific code
        try:
            self.fileData=sdds.SDDS(0)
            self.fileData.load(openFile)
        except Exception:
            QtGui.QMessageBox.warning(self, "Error Importing File", "The file " + openFile + " does not contain any data.")
            return

        #get # of pages and columns
        (_,_,_,_,Ncol,_,_,Npage)=SDDSreshape(self.fileData,ColumnXAxis,ColumnPicked,NumPage)
        stringOut="Columns: "+str(Ncol)+" Pages: "+str(Npage)+" ColumnElements: "+\
        str(np.shape(self.fileData.columnData)[2])
        paramsOut ='\nPARAMTER INFO \n'
        for i,a in enumerate(self.fileData.parameterName):
            paramsOut+=str(a)+'='+str(self.fileData.parameterData[i])+'\n'
        self.legend.setText(QtGui.QApplication.translate("dcpwidget",\
            'FILE INFO \n'+'File Name: '+phile.fileName()+'\nFile Size: '+str(phile.size())+' bytes \n'+\
            self.fileData.description[0]+stringOut+paramsOut, None, QtGui.QApplication.UnicodeUTF8))

        #preview of parameters
        self.preview(Ncol)

        #preview of sdds data
        sddsprev(Ncol)
        
        #populate graph data
        self.dataopt(self.fileData.columnName)
         
    def showDCP_srw(self, openFile):
        def srwprev(Ncol):
            ColumnPicked = range(Ncol)
            (Xrvec,Yrvec,Npar,Ncol,NcolPicked,NElemCol)=SRWreshape(self.fileData,ColumnXAxis,ColumnPicked)
            for i, a in enumerate(Yrvec):
                for j, b in enumerate(a):
                    if j >= 1000:
                        break
                    self.data.setItem(j+3,i,QtGui.QTableWidgetItem(str(b)))
                else:
                    self.data.setRowCount(np.shape(Yrvec)[1])
        #reset data selection
        ColumnPicked = [0]
        ColumnXAxis = -1
        #get file info
        phile = QtCore.QFileInfo(openFile)
        
        #SRW specific
        self.fileData = SRW(openFile,MaxNumParam)
        #get columns
        (_,_,_,Ncol,_,_)=SRWreshape(self.fileData,ColumnXAxis,ColumnPicked)
        stringOut="Columns: "+str(np.shape(self.fileData.columnData)[0])+" Pages: 1"+" ColumnElements: "+\
        str(np.shape(self.fileData.columnData)[1])
        self.legend.setText(QtGui.QApplication.translate("dcpwidget", 'FILE INFO \n'+'File Name: '+\
            phile.fileName()+'\nFile Size: '+str(phile.size())+' bytes \n'+stringOut, None, QtGui.QApplication.UnicodeUTF8))
            
        self.preview(Ncol)
        srwprev(Ncol)
        self.dataopt(self.fileData.columnName)

                    
    def preview(self,Ncol):
        if not self.fileData:
            return

        self.reset()

        #set table sizes
        self.data.setRowCount(1003)
        self.data.setColumnCount(Ncol)

        for i,a in enumerate(self.fileData.columnDefinition):
            self.data.setItem(0,i, QtGui.QTableWidgetItem(a[2]))
            self.data.setItem(2,i, QtGui.QTableWidgetItem(a[1]))

        for i,a in enumerate(self.fileData.columnName):
            self.data.setItem(1,i,QtGui.QTableWidgetItem(a))

    def reset(self):
        self.widget.canvas.ax.clear()
        self.data.clearContents()
        self.widget.canvas.draw()
        
    #displaying and setting data options method
    def dataopt(self,options):
        self.xaxis.clear()
        self.yaxis.clear()
        for i, name in enumerate(options): #self.fileData.columnName
            if isNumber(self.data.item(4, i).text()):
                self.xaxis.addItem(name)
                self.yaxis.addItem(name)

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

    def h5select(self):
        self.quickplot.clear()
        self.quickplot.addItem('s v. Power')
        self.quickplot.addItem('s v. Increment')
        self.quickplot.addItem('s v. Phase')
        self.quickplot.addItem('s v. Rad. Size')
        self.quickplot.addItem('s v. Energy')
        self.quickplot.addItem('s v. X Beam Size')
        self.quickplot.addItem('s v. Y Beam Size')
        self.quickplot.addItem('s v. Bunching Fundamental')
        self.quickplot.addItem('s v. Error')
        
    def graphset(self):
    
        def find_param(pname):
            output = None
            for i in range(self.xaxis.count()):
                if self.xaxis.itemText(i) == pname:
                    output = i
                    break
            if output == None:
                raise TypeError('Parameter Not Found: ' + pname)
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

        elif self.currentFiletype == 'h5':
            self.xaxis.setCurrentIndex(find_param('s'))
            param = self.quickplot.currentText().split('.')[1].strip().split()[0].lower()
            try:
                self.yaxis.setCurrentIndex(find_param(param))
            except TypeError:
                try:
                    self.yaxis.setCurrentIndex(find_param('signal' + param))
                except TypeError:
                    param = removeWhitespace(self.quickplot.currentText()).split('.', 1)[1].lower()
                    param = param.replace('.', '')
                    self.yaxis.setCurrentIndex(find_param(param))
     
        self.customgraph()
    
    def customgraph(self):
        if not self.fileData:
            return

        self.parent.ui.statusbar.showMessage('Drawing plot ...')
        #ColumnXAxis=0
        xname = self.xaxis.currentText()
        yname = self.yaxis.currentText()
        if self.currentFiletype in ['sdds', 'out', 'twi', 'sig', 'cen', 'bun', 'fin','dat']:
            ColumnXAxis = self.fileData.columnName.index(xname)
            ColumnPicked = [self.fileData.columnName.index(yname)]

        if self.currentFiletype == 'dat':
            (Xrvec,Yrvec,Npar,Ncol,NcolPicked,NElemCol)=SRWreshape(self.fileData,ColumnXAxis,ColumnPicked)
        elif self.currentFiletype in ['sdds', 'out', 'twi', 'sig', 'cen', 'bun', 'fin']:
            (Xrvec,Yrvec,Ylab,Npar,Ncol,NcolPicked,NElemCol,Npage)=SDDSreshape(self.fileData,ColumnXAxis,ColumnPicked,NumPage)
        elif self.currentFiletype == 'dist' or self.currentFiletype=='beam':
            Xrvec=numpy.array(self.fileData[self.xaxis.currentIndex()])
            shape=numpy.shape(self.fileData[self.xaxis.currentIndex()])[0]
            Yrvec=numpy.reshape(numpy.array(self.fileData[self.yaxis.currentIndex()]),[1,shape])
        else:
            shape = numpy.shape(self.fileData[xname])[0]
            #print('x shap: ',shape)
            #print('xrvec shap: ', numpy.array(self.fileData[xname]).shape,' xrvec siz: ',numpy.array(self.fileData[xname]).size)
            #print('yrvec shap: ', numpy.array(self.fileData[yname]).shape,' yrvec siz: ',numpy.array(self.fileData[yname]).size)
            Xrvec = numpy.reshape(numpy.array(self.fileData[xname]),-1)
            Yrvec = numpy.reshape(numpy.array(self.fileData[yname]),[1,shape])
            #print('after reshpae')
            #print('xrvec shap: ', Xrvec.shape,' xrvec siz: ',Xrvec.size)
            #print('yrvec shap: ', Yrvec.shape,' yrvec siz: ',Yrvec.size)
        try:
            yu = ' ['+self.fileData.columnDefinition[ColumnPicked[0]][1]+']'
            xu = ' ['+self.fileData.columnDefinition[ColumnXAxis][1]+']'
        except IndexError:
            yu = ''
            xu = ''
        except AttributeError:
            yu = ''
            xu = ''

        # Plot
        try:
            numParticles = np.shape(Xrvec)[0]
            nLevels = 5 + int(math.pow(numParticles, 0.333333333))
            nDivs = 10 + int(math.pow(numParticles, 0.2))
            self.widget.canvas.ax.clear()
            scatConPlot(self.plotStyle.currentText().lower(),
                        removeWhitespace(self.plotType.currentText().lower()),
                        Xrvec,
                        Yrvec[0,:],
                        self.widget.canvas.ax,
                        nDivs,
                        nLevels)
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
            print(numpy.shape(Xrvec))
            print(numpy.shape(Yrvec))
            

        self.parent.ui.statusbar.clearMessage()
                
def main():
    app = QtGui.QApplication(sys.argv)
    myapp = RbDcp()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
