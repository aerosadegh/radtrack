# -*- coding: utf-8 -*-
u"""Main panel for simulation

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open
import os

from radtrack.rt_qt import QtCore, QtGui

from pykern.pkdebug import pkdc, pkdp
from pykern import pkio
from pykern import pkcollections
from pykern import pkresource

from radtrack import rt_popup
from radtrack import rt_qt
from radtrack import genesis_enums


class View(QtGui.QWidget):
    def __init__(self, controller, parent=None):
        super(View, self).__init__(parent)
        self._controller = controller
        self.global_params = {}
        self.setStyleSheet(pkio.read_text(pkresource.filename('srw_pane.css')))
        main = QtGui.QHBoxLayout()
        self._add_action_buttons(main)
        #self._add_param_vbox(main)
        self._add_result_texts(main)
        self.setLayout(main)
        self.parent=parent
        
    def set_result_text(self, which, text):
        w = self._result_text[which]
        w.setText(text)
        w.repaint()
        
    def _add_action_buttons(self, main):
        """Buttons on the left size"""
        frame = QtGui.QWidget(self)
        gbox = QtGui.QGridLayout()
        frame.setLayout(gbox)
        for i , n in enumerate(self._controller.ACTION_NAMES):
            a = QtGui.QPushButton(n.replace('_',' '), frame)
            a.setDefault(False)
            a.setAutoDefault(False)
            columnspan = 1
            if n == 'Simulate':
                columnspan=2
            gbox.addWidget(a,i/2,i%2,1,columnspan)
            a.clicked.connect(self._controller.name_to_action(n))
        #gbox.addStretch()
        main.addWidget(frame)
        
    def _add_result_texts(self, main):
        """Adds 1 boxes on the right side"""

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

        self._result_text = {}
        _add(
            'simulation',
            'Simulation Status',
            'Click Simulate to run Genesis',
        )
        
             
        vbox = QtGui.QVBoxLayout()
        main.addLayout(vbox, stretch=1)
        qlabel = rt_qt.set_id(QtGui.QLabel(self), 'heading')
        rt_qt.i18n_text('output files', qlabel)
        vbox.addWidget(qlabel, alignment=QtCore.Qt.AlignCenter)
        text = QtGui.QListWidget(self)
        text.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #rt_qt.i18n_text(desc, text)
        #text.setReadOnly(True)
        vbox.addWidget(text)
        self._result_text['output'] = text
