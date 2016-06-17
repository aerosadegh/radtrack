# -*- coding: utf-8 -*-
"""Genesis Tab

:copyright: Copyright (c) 2015 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
#from pykern.pkdebug import pkdc, pkdp
from radtrack.rt_qt import QtGui

from radtrack import genesis_controller


class GenesisTab(QtGui.QWidget):
    defaultTitle = 'Genesis'
    acceptsFileTypes = ['in','out','dist']
    task = 'Run a Genesis simulation'
    category = 'simulations'
    
    def __init__(self, parent):
        super(GenesisTab, self).__init__(parent)
        layout = QtGui.QVBoxLayout(self)
        self.control = genesis_controller.Base()
        layout.addWidget(self.control.init_widget(self))
        self.setLayout(layout)
        self.parent=parent
        
    def exportToFile(self, fileName = None):
        self.control.write_simulation_file(fileName)

    def importFile(self, fileName = None):
        with open(fileName, 'r') as f:
            self.control.get_in(f)


if '__main__' == __name__:
    from radtrack import rt_qt
    rt_qt.run_app(lambda: GenesisTab(None))
