#!/usr/bin/python
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as Navigationtoolbar
from matplotlib.figure import Figure


#Embeddable matplotlib figure/canvas
class MplCanvas(FigureCanvas): 
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
 
        super(MplCanvas, self).__init__(self.fig)
        super(MplCanvas, self).setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        super(MplCanvas, self).updateGeometry()
 
#creates embeddable matplotlib figure/canvas with toolbar
class matplotlibWidget(QtGui.QWidget):
 
    def __init__(self, parent = None):
        super(matplotlibWidget, self).__init__(parent)
        self.create_framentoolbar()

    def create_framentoolbar(self):
        self.frame = QtGui.QWidget()
        self.canvas = MplCanvas()
        self.canvas.setParent(self.frame)
        self.mpltoolbar = Navigationtoolbar(self.canvas, self.frame)
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.mpltoolbar)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
