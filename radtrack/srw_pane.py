# -*- coding: utf-8 -*-
u"""Main panel for simulation

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

from radtrack.rt_qt import QtCore, QtGui, i18n_text, set_id, set_param

from pykern.pkdebug import pkdc, pkdi, pkdp
from pykern import pkio
from pykern import pkresource

from radtrack import rt_params
from radtrack import srw_enums

RESULTS_STRETCH = 4

PARAMS_STRETCH = 5

class View(QtGui.QWidget):
    def __init__(self, controller, parent=None, is_multi_particle=False):
        super(View, self).__init__(parent)
        self._controller = controller
        self.is_multi_particle = is_multi_particle

        self.setStyleSheet(pkio.read_text(pkresource.filename('srw_pane.css')))
        main = QtGui.QHBoxLayout()

        button_widget = QtGui.QWidget(self)
        button_vbox = QtGui.QVBoxLayout()
        button_widget.setLayout(button_vbox)
        self.action_box = {}
        for n in ('Precision', 'Undulator', 'Beam', 'Analyze', 'Simulate'):
            a = QtGui.QPushButton(n, button_widget)
            a.setDefault(False)
            a.setAutoDefault(False)
            button_vbox.addWidget(a)
            policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
            #a.setSizePolicy(policy)
            self.action_box[n] = a
            self.action_box[n].clicked.connect(
                getattr(controller, 'action_' + n.lower()))
        button_widget.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        main.addWidget(button_widget)
        pkdp('main.sizeHint={}', main.sizeHint())

        param_vbox = QtGui.QVBoxLayout()
        param_widget = QtGui.QWidget(self)
        main.addLayout(param_vbox, stretch=PARAMS_STRETCH)

        hb = QtGui.QHBoxLayout()

        label = set_id(QtGui.QLabel(param_widget), 'form_field')
        i18n_text('Simulation Kind: ', label)
        hb.addWidget(label, alignment=QtCore.Qt.AlignRight)
        self.simulation_kind_value = QtGui.QComboBox(param_widget)
        hb.addWidget(self.simulation_kind_value)
        param_vbox.addLayout(hb)

        params = controller.params['Simulation Kind']
        self.wavefront_param_models = {}
        self.wavefront_param_view = QtGui.QTableView(param_widget)
        param_vbox.addWidget(self.wavefront_param_view)

        self.wavefront_param_view.horizontalHeader().setVisible(0)
        #self.wavefront_param_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.wavefront_param_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.wavefront_param_view.verticalHeader().setVisible(0)
        decl = list(
            rt_params.iter_primary_param_declarations(controller.declarations['Wavefront']))

        first_sk = None
        for sk in srw_enums.SimulationKind:
            if sk.name not in params:
                continue
            if not first_sk:
                first_sk = sk
            self.simulation_kind_value.addItem(
                i18n_text(sk.display_name),
                userData=sk.value,
            )
            m = QtGui.QStandardItemModel(len(decl), 2);
            p = params[sk.name]['Wavefront']
            for (row, d) in enumerate(decl):
                item = QtGui.QStandardItem()
                i18n_text(d['label'], item)
                m.setItem(row, 0, item)
                item = QtGui.QStandardItem()
                set_param(d, p, item)
                m.setItem(row, 1, item)
            self.wavefront_param_models[sk.name] = m
        self.wavefront_param_view.setModel(
            self.wavefront_param_models[first_sk.name])

        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        param_widget.setSizePolicy(policy)

        self.result_text = {}
        self._result_text(
            'simulation',
            'Simulation Results',
            'Click Simulate to run SRW',
            main,
        )
        self._result_text(
            'analysis',
            'Analysis Results',
            'Click Analysis to approximate a simulation',
            main,
        )
        policy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.wavefront_param_view.setSizePolicy(policy)
        self.wavefront_param_view.horizontalHeader().setSizePolicy(
            QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)

        self.simulation_kind_value.currentIndexChanged.connect(
            self.simulation_kind_changed)
        self.setLayout(main)

        fill_vbox = QtGui.QVBoxLayout()
        fill_widget = QtGui.QWidget(self)
        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        fill_widget.setSizePolicy(policy)

        button_vbox.addStretch()
        # Adding either forces scrollbars
        #param_vbox.addStretch()
        #main.addStretch()


    def simulation_kind_changed(self):
        self.wavefront_param_view.setModel(
            self.wavefront_param_models[self.current_simulation_kind().name])

    def current_simulation_kind(self):
        v = self.simulation_kind_value.itemData(
                self.simulation_kind_value.currentIndex())
        (i, ok) = v.toInt()
        assert ok, \
            '{}: simulation_kind_value invalid'.format(v)
        return srw_enums.SimulationKind(i)

    def set_result_text(self, which, text):
        w = self.result_text[which]
        w.setText(text)
        w.repaint()

    def _result_text(self, name, label, desc, main):
        vbox = QtGui.QVBoxLayout()
        main.addLayout(vbox, stretch=RESULTS_STRETCH)
        qlabel = set_id(QtGui.QLabel(self), 'heading')
        qlabel.setMinimumHeight(self.simulation_kind_value.sizeHint().height())
        i18n_text(label, qlabel)
        vbox.addWidget(qlabel, alignment=QtCore.Qt.AlignCenter)
        text = QtGui.QTextEdit(self)
        i18n_text(desc, text)
        vbox.addWidget(text)
        self.result_text[name] = text
