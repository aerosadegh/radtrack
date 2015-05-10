"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from os.path import expanduser
import sdds
from functools import partial

import matplotlib

from radtrack.dcp.Servicelib import *
from radtrack.dcp.SRWlib import SRWFileRead1, SRW
from radtrack.dcp.Flatfilelib import FF, FFColRead
from radtrack.dcp.Plotlib2axis import *
from radtrack.dcp.moverage import *
from radtrack.dcp.FourieT import *
from radtrack.dcp.math_analyses import *
from radtrack.dcp.dcpwidget import Ui_dcpwidget


ColumnPicked = [0]
NumPage = 0
ColumnXAxis =-1
MaxNumParam=999
MaxNumColum=999


class RbDcp(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_dcpwidget()
        self.ui.setupUi(self)
        self.parent = parent
        if self.parent is None:
            self.parent = self
            self.parent.lastUsedDirectory = expanduser('~')
        self.acceptsFileTypes = ['save', 'sdds', 'srw', 'ff', 'out', 'mag',
                                 'twi', 'fin', 'sig', 'cen']
        self.ui.widget.canvas.ax2.set_visible(False)
        self.ui.page.activated.connect(self.sddspreview)
        self.ui.pushButton.clicked.connect(self.graph)
        self.ui.comboBox.addItem('<select>')
        self.ui.comboBox.addItem('FFT')
        self.ui.comboBox.addItem('average')
        self.ui.comboBox.activated.connect(self.math)
        self.currentFiletype = ''

        self.ui.data.setItem(1,0,QtGui.QTableWidgetItem('Description'))
        self.ui.data.setItem(2,0,QtGui.QTableWidgetItem('Name'))
        self.ui.data.setItem(3,0,QtGui.QTableWidgetItem('Units'))
        self.ui.param.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem('Description'))
        self.ui.param.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem('Value'))
        self.ui.param.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem('Unit'))
        self.ui.param.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem('Name'))

        self.container = self
        self.defaultTitle = self.parent.tr('Data Visualization')

    # This tab is only for reading files. It has no
    # data of its own to save. This creates a dummy
    # file to that the tab is reopened when the project
    # that contained this tab is reopened.
    def exportToFile(self, fileName):
        with open(fileName, 'w'):
            pass

    def setcurrentFile(self, type):
        self.currentFiletype = type

    def importFile(self, fnfromglobal):
        filetype = IFileTypeCheck(fnfromglobal)
        if filetype == 'sdds':
            self.showDCP_ele(fnfromglobal)
        elif filetype == 'out':
            self.showDCP_ele(fnfromglobal)
        elif filetype == 'mag':
            self.showDCP_ele(fnfromglobal)
        elif filetype == 'twi':
            self.showDCP_ele(fnfromglobal)
        elif filetype == 'fin':
            self.showDCP_ele(fnfromglobal)
        elif filetype == 'srw':
            self.showDCP_srw(fnfromglobal)
        elif filetype == 'ff':
            self.showDCP_ff(fnfromglobal)
        elif filetype == 'save':
            pass
        else:
            raise Exception("Could not open " + fnfromglobal)

        self.setcurrentFile(filetype)


    #for opening up elegant files
    def showDCP_ele(self, fnfromglobal):

        #reset data selection
        ColumnPicked = [0]
        ColumnXAxis = -1
        #resets & clears page selector
        self.ui.page.clear()
        self.ui.page.show()
        #get file info
        phile = QtCore.QFileInfo(fnfromglobal)
        self.ui.file.setText(str(phile.fileName()))
        #SDDS specific code
        self.x=sdds.SDDS(0)
        self.x.load(fnfromglobal)
        #get # of pages and columns
        (_,_,_,_,self.Ncol,_,_,Npage)=SDDSreshape(self.x,ColumnXAxis,ColumnPicked,NumPage)
#        print(self.x.description[0])
        print("%d %d %d" %(self.Ncol, Npage, np.shape(self.x.columnData)[2]))
        stringOut=" Columns: "+str(self.Ncol)+" Pages: "+str(Npage)+" ColumnElements: "+\
        str(np.shape(self.x.columnData)[2])
        self.ui.textEdit.setText(QtGui.QApplication.translate("dcpwidget",\
            self.x.description[0]+stringOut, None, QtGui.QApplication.UnicodeUTF8))
        for i in range(Npage):
            self.ui.page.addItem(str(i))
        self.ui.page.setCurrentIndex(0)
        #preview of parameters
        self.preview()
        #preview of sdds data
        self.sddsprev()

    #for opening up srw files and then previews and then previews
    def showDCP_srw(self,fnfromglobal):
        #reset data selection
        ColumnPicked = [0]
        ColumnXAxis = -1
        #disable pages(have yet to see a srw files with multiple pages)
        self.ui.page.hide()
        #get file
        phile = QtCore.QFileInfo(fnfromglobal)
        self.ui.file.setText(str(phile.fileName()))
        self.ui.textEdit.setText(QtGui.QApplication.translate("dcpwidget",\
            'SRW legend', None, QtGui.QApplication.UnicodeUTF8))
        #SRW specific
        x = SRW()
        self.x=SRWFileRead1(x,fnfromglobal,MaxNumParam)
        #get columns
        (_,_,_,self.Ncol,_,_)=SRWreshape(self.x,ColumnXAxis,ColumnPicked)
        ColumnPicked = []
        for i in range(self.Ncol):
            ColumnPicked.append(i)
        stringOut=" Columns: "+str(np.shape(x.columnData)[0])+" Pages: 1"+" ColumnElements: "+\
        str(np.shape(x.columnData)[1])
        self.ui.textEdit.setText(QtGui.QApplication.translate("dcpwidget",\
            'SRW legend'+stringOut, None, QtGui.QApplication.UnicodeUTF8))
        #preview parameters
        self.preview()
        #preview srw data
        self.srwprev()

    #for opening plain text/flat files and then previews
    def showDCP_ff(self,fnfromglobal):
        #reset data selection
        ColumnPicked = [0]
        ColumnXAxis = -1
        #hide pages
        self.ui.page.hide()
        phile = QtCore.QFileInfo(fnfromglobal)
        self.ui.file.setText(str(phile.fileName()))
        self.ui.textEdit.setText(QtGui.QApplication.translate("dcpwidget",\
            'flat file', None, QtGui.QApplication.UnicodeUTF8))
        x = FF()
        xlabel=r'$\tau$'
        (self.x,_)=FFColRead(x,fnfromglobal,MaxNumColum)
        (_,_,self.Ncol,_,_)=FFreshape(self.x,ColumnXAxis,ColumnPicked)
        stringOut=" Columns: "+str(np.shape(x.columnData)[0])+" Pages: 1"+" ColumnElements: "+\
        str(np.shape(x.columnData)[1])
        self.ui.textEdit.setText(QtGui.QApplication.translate("dcpwidget",\
            xlabel+'Flat File legend'+stringOut, None, QtGui.QApplication.UnicodeUTF8))
        #preveiw parameters
        self.preview()
        #preview data
        self.ffprev()


    #this method is needed for updating after selcting a new sdds page
    def sddspreview(self):
        self.preview()
        self.sddsprev()

    #this method allows only one x and quickview selection at a time
    def action(self, i, n):
        self.ui.data.setFocus()
        if n == 1 or n == 4:
            for index, data in enumerate(self.select):
                if index != i and self.select[index].currentIndex()==1:
                    self.select[index].setCurrentIndex(0)
                if index != i and self.select[index].currentIndex()==4:
                    self.select[index].setCurrentIndex(0)
                #make math functions one at a time?
        if n == 4:
            self.quickview()
        if n == 5:
            dialog = fourier()
            self.ui.widget.canvas.ax.clear()
            self.ui.widget.canvas.ax2.clear()
            self.ui.widget.canvas.draw()
            NumPage = self.ui.page.currentIndex()
            if dialog.exec_():
                Np = int(dialog.ui.n.text())
                y = []
                y.append(self.ui.data.currentColumn())
                ColumnXAxis = -1
                if self.currentFiletype == 'sdds':
                    (Xrvec,Yrvec,YLab,Npar,Ncol,NcolPicked,NElemCol,Npage)=SDDSreshape(self.x,ColumnXAxis,y,NumPage)
                elif self.currentFiletype == 'srw':
                    (Xrvec,Yrvec,Npar,Ncol,NcolPicked,NElemCol)=SRWreshape(self.x,ColumnXAxis,y)
                elif self.currentFiletype =='ff':
                    (Xrvec,Yrvec,Ncol,NcolPicked,NElemCol)=FFreshape(self.x,ColumnXAxis,y)

                Y_k = fftshift(fft(ifftshift(Yrvec)))
                k = fftshift(fftfreq(len(Yrvec)))
                self.ui.widget.canvas.ax.plot(k, Y_k)
                self.ui.widget.canvas.draw()

        if n == 6:
            dialog = moverage()
            #self.ui.widget.canvas.ax.clear()
            #self.ui.widget.canvas.ax2.clear()
            #self.ui.widget.canvas.draw()
            NumPage = self.ui.page.currentIndex()
            if dialog.exec_():
                w = int(dialog.ui.lineEdit.text())
                y = []
                y.append(self.ui.data.currentColumn())
                ColumnXAxis = -1
                for i in range(1,self.Ncol+1):
                    a = self.ui.data.cellWidget(0,i)
                    if a.currentIndex()==1:
                         ColumnXAxis=i-1
                if self.currentFiletype == 'sdds':
                    (Xrvec,Yrvec,YLab,Npar,Ncol,NcolPicked,NElemCol,Npage)=SDDSreshape(self.x,ColumnXAxis,y,NumPage)
                elif self.currentFiletype == 'srw':
                    (Xrvec,Yrvec,Npar,Ncol,NcolPicked,NElemCol)=SRWreshape(self.x,ColumnXAxis,y)
                elif self.currentFiletype =='ff':
                    (Xrvec,Yrvec,Ncol,NcolPicked,NElemCol)=FFreshape(self.x,ColumnXAxis,y)
                y = movingaverage(Yrvec[0],w)
                self.ui.widget.canvas.ax.plot(y)
                self.ui.widget.canvas.draw()


    #sets up tables and preview paramter data
    def preview(self):
        self.reset()
        NumPage = self.ui.page.currentIndex()
        self.select = []
        self.ColumnPicked = []
        #set table sizes
        self.ui.data.setRowCount(1000)
        self.ui.data.setColumnCount(self.Ncol+1)
        self.ui.param.setRowCount(size(self.x.parameterName))

        for i,a in enumerate(self.x.columnDefinition):
            self.ui.data.setItem(1,i+1, QtGui.QTableWidgetItem(a[2]))
            self.ui.data.setItem(3,i+1, QtGui.QTableWidgetItem(a[1]))

        for i,a in enumerate(self.x.columnName):
            self.ui.data.setItem(2,i+1,QtGui.QTableWidgetItem(a))

        for i,a in enumerate(self.x.parameterDefinition):
            self.ui.param.setItem(i,0,QtGui.QTableWidgetItem(a[2]))
            self.ui.param.setItem(i,2,QtGui.QTableWidgetItem(a[1]))

        for i,a in enumerate(self.x.parameterName):
            self.ui.param.setItem(i,3,QtGui.QTableWidgetItem(a))

        for i,a in enumerate(self.x.parameterData):
            self.ui.param.setItem(i,1,QtGui.QTableWidgetItem(str(a)))

        for i in range(self.Ncol):
            xin = QtGui.QComboBox()
            xin.addItem('<select>')
            xin.addItem('X')
            xin.addItem('Y0')
            xin.addItem('Y1')
            xin.addItem('Quick View')
            xin.addItem('FFT')
            xin.addItem('Average')
            self.select.append(xin)
            combocallback = partial(self.action, i)
            self.ui.data.setCellWidget(0,i+1,self.select[i])
            xin.activated.connect(combocallback) #previously used index change signal
            self.ColumnPicked.append(i)

    #shows sdds data
    def sddsprev(self):
        (Xrvec,Yrvec,YLab,Npar,Ncol,NcolPicked,NElemCol,Npage)=SDDSreshape(self.x,ColumnXAxis,self.ColumnPicked,NumPage) #reshapes file into vectors and a matrix

        for i, a in enumerate(Yrvec):
            #if i>0:# skip first column i+1=>i to adjust, because of extra 0 column!!!?
            if size(a)<1000:
                self.ui.data.setRowCount(shape(Yrvec)[1]+4)
                for j, b in enumerate(a):
                    self.ui.data.setItem(j+4,i+1,QtGui.QTableWidgetItem(str(b)))
            else:
                for j in range(1000):
                    self.ui.data.setItem(j+4,i+1,QtGui.QTableWidgetItem(str(a[j])))
    #shows srw data
    def srwprev(self):
        (Xrvec,Yrvec,Npar,Ncol,NcolPicked,NElemCol)=SRWreshape(self.x,ColumnXAxis,self.ColumnPicked)
        for i, a in enumerate(Yrvec):
            if size(a)<1000:
                self.ui.data.setRowCount(shape(Yrvec)[1])
                for j, b in enumerate(a):
                    self.ui.data.setItem(j+4,i+1,QtGui.QTableWidgetItem(str(b)))
            else:
                for j in range(1000):
                    self.ui.data.setItem(j+4,i+1,QtGui.QTableWidgetItem(str(a[j])))
    #shows ff data
    def ffprev(self):
        (Xrvec,Yrvec,Ncol,NcolPicked,NElemCol)=FFreshape(self.x,ColumnXAxis,self.ColumnPicked)
        for i, a in enumerate(Yrvec):
            if size(a)<1000:
                self.ui.data.setRowCount(shape(Yrvec)[1])
                for j, b in enumerate(a):
                    self.ui.data.setItem(j+4,i+1,QtGui.QTableWidgetItem(str(b)))
            else:
                for j in range(1000):
                    self.ui.data.setItem(j+4,i+1,QtGui.QTableWidgetItem(str(a[j])))

    #data plotting method
    def graph(self):
        #resets display
        self.ui.widget.canvas.ax.clear()
        self.ui.widget.canvas.ax2.clear()
        self.ui.widget.canvas.draw()
        #resets data selections
        self.y=[]
        PlotAxisMarker = []
        Yrvec1=[]
        Yrvec2=[]
        NumPage = self.ui.page.currentIndex()
        ColumnXAxis=-1
        #searches through selections
        for i in range(1,self.Ncol+1):
            a = self.ui.data.cellWidget(0,i)
            if a.currentIndex()==1:
                ColumnXAxis=i-1
            elif a.currentIndex()==2:
                self.y.append(i-1)
                PlotAxisMarker.append(1)
            elif a.currentIndex()==3:
                self.y.append(i-1)
                PlotAxisMarker.append(2)
        #reshapes file into vectors and a matrix
        if self.currentFiletype == 'sdds':
            (Xrvec,Yrvec,YLab,Npar,Ncol,NcolPicked,NElemCol,Npage)=SDDSreshape(self.x,ColumnXAxis,self.y,NumPage)
            Xlab=[self.x.columnDefinition[ColumnXAxis][2]+", "+self.x.columnDefinition[ColumnXAxis][1]]
        elif self.currentFiletype == 'srw':
            (Xrvec,Yrvec,Npar,Ncol,NcolPicked,NElemCol)=SRWreshape(self.x,ColumnXAxis,self.y)
            #problems with srw axis data....empty
            Xlab = self.x.columnName
            YLab = self.x.columnDefinition
        elif self.currentFiletype == 'ff':
            (Xrvec,Yrvec,Ncol,NcolPicked,NElemCol)=FFreshape(self.x,ColumnXAxis,self.y)
            Xlab = self.x.columnName
            YLab = self.x.columnDefinition
        #delegates data between left and right vertical axis
        for n,i in enumerate(PlotAxisMarker):
            if i == 1:
                self.ui.widget.canvas.ax2.set_visible(False)
                Yrvec1.append(Yrvec[n])
            elif i == 2:
                self.ui.widget.canvas.ax2.set_visible(True)
                Yrvec2.append(Yrvec[n])

        #plots the data
        PlotColnS2(Xrvec,Yrvec1,Yrvec2,'','bo','rs',self.x.description[0],Xlab,YLab, self.ui.widget.canvas)

    #method for quickly displaying data to see its general form
    def quickview(self):
        self.ui.widget.canvas.ax.clear()
        self.ui.widget.canvas.ax2.clear()
        self.ui.widget.canvas.draw()
        y = []
        NumPage = self.ui.page.currentIndex()
        #ColumnXAxis = -1
        #searches through selections
        for i in range(1,self.Ncol+1):
            a = self.ui.data.cellWidget(0,i)
            if a.currentIndex()==4:
                y.append(i-1)

        if self.currentFiletype == 'sdds':
            (Xrvec,Yrvec,YLab,Npar,Ncol,NcolPicked,NElemCol,Npage)=SDDSreshape(self.x,-1,y,NumPage)
        elif self.currentFiletype == 'srw':
            (Xrvec,Yrvec,Npar,Ncol,NcolPicked,NElemCol)=SRWreshape(self.x,-1,y)
        elif self.currentFiletype =='ff':
            (Xrvec,Yrvec,Ncol,NcolPicked,NElemCol)=FFreshape(self.x,ColumnXAxis,self.y)
        #matplotlib.pyplot.figure
        matplotlib.pyplot.plot(Xrvec,Yrvec[0],'ko')
        matplotlib.pyplot.show()

    def math(self):
        #self.ui.widget.canvas.ax.clear()
        #self.ui.widget.canvas.ax2.clear()
        #self.ui.widget.canvas.draw()
        if self.ui.comboBox.currentIndex() == 1:
            a = self.ui.data.selectedItems()
            b = []
            Np = 5000
            for i in a:
                b.append(float(i.text()))
            t = scipy.linspace(0,Np,Np)
            #print(np.asarray(b) SHOULD USE FFTSHIFT!!!!!!!!!!!!!!!!!)
            (fft_c, freqs) = FourT(np.asarray(b),t,Np) #scipy.fftpack.rfft(b)
            self.ui.widget.canvas.ax.plot(freqs[0:Np/2],fft_c.real[0:Np/2], '-b.')
            self.ui.widget.canvas.ax2.plot(freqs[0:Np/2],fft_c.imag[0:Np/2], '-g.')
            self.ui.widget.canvas.draw()
        if self.ui.comboBox.currentIndex() == 2:
            a = self.ui.data.selectedItems()
            b = []
            #for i in a:
            #    b.append(float(i.text()))
            #yvec = roll_avg(b,5,b[0])
            #yvec = [1,2,3]
            #self.ui.widget.canvas.ax.plot([1,2,3])
            #self.ui.widget.canvas.draw()


    def reset(self):
        self.ui.widget.canvas.ax.clear()
        self.ui.widget.canvas.ax2.clear()
        self.ui.widget.canvas.ax2.set_visible(False)
        #self.ui.page.clear()
        self.ui.param.clear()
        self.ui.data.clear()
        self.ui.data.setItem(1,0,QtGui.QTableWidgetItem('Description'))
        self.ui.data.setItem(2,0,QtGui.QTableWidgetItem('Name'))
        self.ui.data.setItem(3,0,QtGui.QTableWidgetItem('Units'))
        self.ui.param.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem('Description'))
        self.ui.param.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem('Value'))
        self.ui.param.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem('Unit'))
        self.ui.param.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem('Name'))
        self.ui.widget.canvas.draw()
