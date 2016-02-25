# -*- coding: utf-8 -*-
u"""Main panel for simulation

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

from radtrack.rt_qt import QtCore, QtGui

from pykern.pkdebug import pkdc, pkdp
from pykern import pkio
from pykern import pkcollections
from pykern import pkresource

from radtrack import rt_popup
from radtrack import rt_qt
from radtrack import srw_enums


class WidgetHolder(object):
    def __init__(self, hbox, default, label, param_widget, controller):
        self.hbox = hbox
        self.default = default
        self.label = label
        self.controller = controller
        self.param_widget = param_widget
        self.widget = None
        self.stacker = None
        self.update_visibility()
        self.controller.register_static_widget(self)

    def set_stacker(self, stacker):
        self.stacker = stacker
        self.widget.currentIndexChanged.connect(self.stacker.setCurrentIndex)

    def update_visibility(self):
        d = self.default
        visible = self.controller.decl_is_visible(d.decl)
        self.label.setVisible(visible)
        value = d.value
        if self.widget:
            value = rt_popup.get_widget_value(d.decl, self.widget)
            self.hbox.removeWidget(self.widget)
            if self.stacker:
                self.widget.currentIndexChanged.disconnect()
            self.widget.deleteLater()
            self.widget = None
        res = rt_popup.value_widget(
            self.default,
            value,
            self.param_widget,
            self.controller,
        )
        self.widget = res[0]
        self.widget.setVisible(visible)
        self.hbox.addWidget(self.widget)
        if self.stacker:
            self.widget.currentIndexChanged.connect(self.stacker.setCurrentIndex)


class View(QtGui.QWidget):
    """Pane with buttons, parameters, and results windows.

    laid out horizontally.
    """
    def __init__(self, controller, parent=None):
        super(View, self).__init__(parent)
        self._controller = controller
        self.global_params = {}
        self._enum_info = {}
        self.setStyleSheet(pkio.read_text(pkresource.filename('srw_pane.css')))
        main = QtGui.QHBoxLayout()
        self._add_action_buttons(main)
        self._add_param_vbox(main)
        self._add_result_texts(main)
        self.setLayout(main)

    def get_global_param(self, name):
        #TODO (robnagler) hide the abstraction for now
        if name == 'wavefront':
            return self.get_wavefront_params()
        try:
            v = self.global_params[name]
        except KeyError:
            # We allow non-existent params
            return None
        return rt_popup.get_widget_value(
            self._controller.defaults[name].decl,
            v.widget,
        )

    def get_wavefront_params(self):
        n = self.get_global_param('simulation_kind').name.lower()
        m = self._enum_info[n]
        return m.get_params()

    def get_source_params(self):
        n = self.get_global_param('radiation_source').name.lower()
        m = self._enum_info[n]
        return m.get_params()

    def set_result_text(self, which, text):
        w = self._result_text[which]
        w.setText(text)
        w.repaint()

    def _add_action_buttons(self, main):
        """Buttons on the left side"""
        frame = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout()
        frame.setLayout(vbox)
        for n in self._controller.ACTION_NAMES:
            a = QtGui.QPushButton(n, frame)
            a.setDefault(False)
            a.setAutoDefault(False)
            vbox.addWidget(a)
            a.clicked.connect(self._controller.name_to_action(n))
        vbox.addStretch()
        main.addWidget(frame)

    def _add_param_vbox(self, main):
        param_vbox = QtGui.QVBoxLayout()
        param_widget = QtGui.QWidget(self)

        def _global_param(name):
            try:
                df = self._controller.defaults[name]
            except KeyError:
                return
            hb = QtGui.QHBoxLayout()
            label = rt_qt.set_id(QtGui.QLabel(param_widget), 'form_field')
            rt_qt.i18n_text(df.decl.label, label)
            hb.addWidget(label, alignment=QtCore.Qt.AlignRight)
            self.global_params[name] = WidgetHolder(
                hbox=hb,
                default=df,
                label=label,
                param_widget=param_widget,
                controller=self._controller,
            )
            param_vbox.addLayout(hb)

        def _view(name):
            stacker = QtGui.QStackedWidget()
            defaults = self._controller.defaults[name]
            params = self._controller.params[name]
            for i in defaults:
                for j in defaults[i]:
                    d = defaults[i][j]
                    p = params[i][j]
                    x = rt_popup.WidgetView(d, p, controller=self._controller, parent=self)
                    stacker.addWidget(x)
                self._enum_info[i] = x
            self.global_params[name].set_stacker(stacker)
            param_vbox.addWidget(stacker)

        _global_param('radiation_source')
        _view('radiation_source')
        _global_param('polarization')
        _global_param('intensity')
        _global_param('simulation_kind')
        _view('simulation_kind')

        self._add_vertical_stretch_spacer(param_vbox)
        main.addLayout(param_vbox)

    def _add_result_texts(self, main):
        """Adds two boxes on the right side"""

        def _add(name, label, desc):
            """Creates a stretchable TextEdit area with label above"""
            vbox = QtGui.QVBoxLayout()
            main.addLayout(vbox, stretch=1)
            qlabel = rt_qt.set_id(QtGui.QLabel(self), 'heading')
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
            'Simulation Results',
            'Click Simulate to run SRW',
        )
        _add(
            'analysis',
            'Analysis Results',
            'Click Analysis to approximate a simulation',
        )

    def _add_vertical_stretch_spacer(self, param_vbox):
        """Only way to ensure that the wavefront_view won't stretch"""
        fill_vbox = QtGui.QVBoxLayout()
        fill_widget = QtGui.QWidget(self)
        fill_widget.setSizePolicy(
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding,
        )
        fill_vbox.addWidget(fill_widget)
        param_vbox.addLayout(fill_vbox)
        param_vbox.addStretch()
