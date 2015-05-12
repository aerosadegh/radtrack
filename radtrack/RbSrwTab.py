from PyQt4 import QtGui
from radtrack.RbSrwsingleA import rbsrw as rbsrwsingle
from radtrack.RbSrwmultiA import rbsrw as rbsrwmulti


class RbSrwTab(QtGui.QWidget):
    def __init__(self, parent):
        if parent:
            self.parent = parent
        else:
            self.parent = self
        QtGui.QWidget.__init__(self)

        self.stackwidget = QtGui.QStackedWidget(self)
        self.stackwidget.addWidget(rbsrwmulti(self))
        self.stackwidget.addWidget(rbsrwsingle(self))
        self.srw_particle = QtGui.QCheckBox(self)
        self.srw_particle.setText('Single-Particle')

        layout = QtGui.QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(self.srw_particle)
        layout.addWidget(self.stackwidget)
        self.srw_particle.stateChanged.connect(self.togglesrw)

        self.container = self
        self.defaultTitle = self.parent.tr('SRW')
        self.acceptsFileTypes = []

    def togglesrw(self):
        self.stackwidget.setCurrentIndex(int(self.srw_particle.isChecked()))
        print self.stackwidget.currentIndex()
        print int(self.srw_particle.isChecked())
