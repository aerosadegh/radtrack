from PyQt4 import QtGui
from radtrack.RbSrwsingleA import rbsrw as rbsrwsingle
from radtrack import srw_multi_particle;


class RbSrwTab(QtGui.QWidget):
    defaultTitle = 'SRW'
    acceptsFileTypes = []
    task = 'Run an SRW simulation'
    category = 'simulations'

    def __init__(self, parent):
        if parent:
            self.parent = parent
        else:
            self.parent = self
        QtGui.QWidget.__init__(self)

        self.stackwidget = QtGui.QStackedWidget(self)
        self.stackwidget.addWidget(
            srw_multi_particle.Pane(self))
        self.stackwidget.addWidget(rbsrwsingle(self))
        self.srw_particle = QtGui.QCheckBox(self)
        self.srw_particle.setText('Single-Particle')

        layout = QtGui.QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(self.srw_particle)
        layout.addWidget(self.stackwidget)
        self.srw_particle.stateChanged.connect(self.togglesrw)

        self.container = self

    def exportToFile(self, fileName = None):
        with open(fileName, 'w'):
            pass

    def importFile(self, fileName = None):
        pass

    def togglesrw(self):
        self.stackwidget.setCurrentIndex(int(self.srw_particle.isChecked()))
        print self.stackwidget.currentIndex()
        print int(self.srw_particle.isChecked())
