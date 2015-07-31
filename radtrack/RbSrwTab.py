
from radtrack.rt_qt import QtGui

from radtrack import srw_multi_particle
from radtrack import srw_single_particle

from pykern.pkdebug import pkdc, pkdp

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
            srw_multi_particle.Controller.init_widget(self.stackwidget))
        self.stackwidget.addWidget(
            srw_single_particle.Controller.init_widget(self.stackwidget))
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
