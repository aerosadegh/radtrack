# -*- coding: utf-8 -*-
"""SRW Tab

:copyright: Copyright (c) 2015 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from pykern.pkdebug import pkdc, pkdp

from radtrack.rt_qt import QtGui

from radtrack import srw_controller


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
        self.srw_particle = QtGui.QCheckBox(self)
        self.srw_particle.setText('Single-Particle')
        layout = QtGui.QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(self.srw_particle)
        layout.addWidget(srw_controller.Base.init_widget(None, complexity_widget=self.srw_particle))

    def exportToFile(self, fileName = None):
        with open(fileName, 'w'):
            pass

    def importFile(self, fileName = None):
        pass


if '__main__' == __name__:
    from radtrack import rt_qt
    rt_qt.run_app(lambda: RbSrwTab(None))
