import sys
#from genesis import *
from genesispages import *
from PySide import QtGui, QtCore

class RbGenesis(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setMinimumSize(QtCore.QSize(350,400))
        self.stackwidget = QtGui.QStackedWidget()               
        
        self.stackwidget.addWidget(makeund())
        self.stackwidget.addWidget(makefodo())
        self.stackwidget.addWidget(makebeam())

        mainlayout = QtGui.QGridLayout()
        mainlayout.addWidget(self.stackwidget,0,0,1,6)
        self.b = QtGui.QPushButton('back')
        mainlayout.addWidget(self.b,1,1)
        self.n = QtGui.QPushButton('next')
        mainlayout.addWidget(self.n,1,4)

        self.setLayout(mainlayout)

        self.n.clicked.connect(self.nex)
        self.b.clicked.connect(self.bac)

    def nex(self):
        i = self.stackwidget.currentIndex()
        i = i+1
        self.stackwidget.setCurrentIndex(i)
    def bac(self):
        i = self.stackwidget.currentIndex()
        i = i-1
        self.stackwidget.setCurrentIndex(i)    


        

def main():

    app = QtGui.QApplication(sys.argv)
    myapp = RbGenesis()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
