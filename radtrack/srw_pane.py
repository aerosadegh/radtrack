# -*- coding: utf-8 -*-
u"""Main panel for simulation

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

from radtrack.rt_qt import QtCore, QtGui, call_if_main, i18n_text, set_id, set_param

from pykern.pkdebug import pkdc, pkdi, pkdp
from pykern import pkio
from pykern import pkresource

from radtrack import rt_params
from radtrack import srw_enums

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

        main.addWidget(button_widget)
        pkdp('main.sizeHint={}', main.sizeHint())

        param_vbox = QtGui.QVBoxLayout()
        param_widget = QtGui.QWidget(self)
        main.addLayout(param_vbox, stretch=4)

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


        i = 0
        for sk in srw_enums.SimulationKind:
            if sk.name not in params:
                continue
            self.simulation_kind_value.addItem(
                i18n_text(sk.display_name),
                userData=sk.value,
            )
            pkdi(self.simulation_kind_value.itemData(i).toString())
            i += 1
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
        self.wavefront_param_view.setModel(self.wavefront_param_models['E'])

        pkdp('param_vbox.sizeHint={}', param_vbox.sizeHint())
        pkdp('main.sizeHint={}', main.sizeHint())


        #### Simulation Results

        simulation_vbox = QtGui.QVBoxLayout()
        main.addLayout(simulation_vbox, stretch=3)
        label = QtGui.QLabel(self)
        label.setMinimumHeight(self.simulation_kind_value.sizeHint().height())
        i18n_text('Simulation Results', label)
        set_id(label, 'heading')
        simulation_vbox.addWidget(label, alignment=QtCore.Qt.AlignCenter)
        self.simulate_results = QtGui.QTextEdit(self)
        simulation_vbox.addWidget(self.simulate_results)
        i18n_text('Click the Simulate button to run SRW', self.simulate_results)

        #### Analysis Results

        analysis_vbox = QtGui.QVBoxLayout()
        main.addLayout(analysis_vbox, stretch=3)
        label = set_id(QtGui.QLabel(self), 'heading')
        label.setText('Analysis Results')
        label.setMinimumHeight(self.simulation_kind_value.sizeHint().height())
        analysis_vbox.addWidget(label, alignment=QtCore.Qt.AlignCenter)
        self.analysis_results = QtGui.QTextEdit(self)
        analysis_vbox.addWidget(self.analysis_results)
        i18n_text(
            'Click the Analyze button to approximate a simulation',
            self.analysis_results,
        )

        pkdp('param_vbox.sizeHint={}', param_vbox.sizeHint())
        pkdp('main.sizeHint={}', main.sizeHint())
        pkdp('simulation_kind.sizeHint={}', self.simulation_kind_value.sizeHint())

        pkdp('label.sizeHint={}', label.sizeHint())

        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        param_widget.setSizePolicy(policy)

        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        button_widget.setSizePolicy(policy)

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
