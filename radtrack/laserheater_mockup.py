"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
version 2
"""
import os, re, cgi, shutil, sdds, multiprocessing
from radtrack.rt_qt import QtCore, QtGui
from pykern.pkdebug import pkdc
#from radtrack.BunchTab import BunchTab
#from radtrack.RbBunchTransport import RbBunchTransport
#from radtrack.RbGenesisTransport import RbGenesisTransport
from radtrack import rt_qt
from radtrack.util.unitConversion import convertUnitsStringToNumber, convertUnitsNumber
from radtrack.util.fileTools import isSDDS

class View(QtGui.QWidget):
    def __init__(self, controller, parent=None):
        super(View, self).__init__(parent)
        main = QtGui.QHBoxLayout()
        self._add_input(main)
        self._add_text(main)
        self.setLayout(main)
        
    def _add_input(self,main):
        vbox=QtGui.QVBoxLayout()
        beam_button=QtGui.QPushButton('beam')
        laser_button=QtGui.QPushButton('laser')
        beam_label=QtGui.QLineEdit('select beam')
        laser_label=QtGui.QLineEdit('select laser')
        hbox1=QtGui.QHBoxLayout()
        hbox2=QtGui.QHBoxLayout()
        hbox1.addWidget(beam_button)
        hbox1.addWidget(beam_label)
        hbox2.addWidget(laser_button)
        hbox2.addWidget(laser_label)
        vbox.addLayout(hbox1,stretch=1)
        vbox.addLayout(hbox2,stretch=1)
        main.addLayout(vbox,stretch=1)
        beam_button.clicked.connect(self.beam_click)
        laser_button.clicked.connect(self.laser_click)
        
    def laser_click(self):
        print('laser button clicked')
        
    def beam_click(self):
        print('beam button clicked')        
        
    def _add_text(self,main):
        def _add(name, label, desc):
            """Creates a stretchable TextEdit area with label above"""
            vbox = QtGui.QVBoxLayout()
            main.addLayout(vbox, stretch=1)
            qlabel = rt_qt.set_id(QtGui.QLabel(self), 'heading')
            #for v in self.global_params.values():
            #    qlabel.setMinimumHeight(v.sizeHint().height())
            rt_qt.i18n_text(label, qlabel)
            vbox.addWidget(qlabel, alignment=QtCore.Qt.AlignCenter)
            text = QtGui.QTextEdit(self)
            rt_qt.i18n_text(desc, text)
            text.setReadOnly(True)
            vbox.addWidget(text)
            self._result_text[name] = text
        
        self._result_text={}    
        _add('simulation','simulation status','click 1')
        _add('output','results','click 2')
        
if '__main__' == __name__:
    from radtrack import rt_qt
    rt_qt.run_app(lambda: View(None))