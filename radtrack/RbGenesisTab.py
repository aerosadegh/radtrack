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
    acceptsFileTypes = ['in']
    task = 'Run a Genesis simulation'
    category = 'simulations'
    
    def __init__(self,parent):
        if parent:
            self.parent = parent
        else:
            self.parent = self
            
        QtGui.QWidget.__init__(self)
        layout = QtGui.QVBoxLayout(self)
        self.control = genesis_controller.Base()
        layout.addWidget(self.control.init_widget(self))
        self.setLayout(layout)
        
    def exportToFile(self, fileName = None):
        with open(fileName, 'w'):
            pass

    def importFile(self, fileName = None):
        with open(fileName, 'r') as f:
            self.control.get_in(f)


if '__main__' == __name__:
    from radtrack import rt_qt
    rt_qt.run_app(lambda: GenesisTab(None))
