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


class View(QtGui.QWidget):
    """Pane with buttons, parameters, and results windows.

    laid out horizontally.
    """
    def __init__(self, controller, parent=None):
        super(View, self).__init__(parent)
        self._controller = controller
        self.global_params = {}
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
            v,
        )

    def get_wavefront_params(self):
        skn = self.get_global_param('simulation_kind').name.lower()
        # return self._controller.params['simulation_kind'][skn]['wavefront']
        m = self._wavefront_models[skn]
        defaults = self._controller.defaults['simulation_kind'][skn]['wavefront']
        res = pkcollections.OrderedMapping()
        for (row, n) in enumerate(defaults):
            df = defaults[n]
            res[df.decl.name] = rt_popup.get_widget_value(df.decl, m.item(row, 1))
        return res

    def set_result_text(self, which, text):
        w = self._result_text[which]
        w.setText(text)
        w.repaint()

    def _add_action_buttons(self, main):
        """Buttons on the left size"""
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
            res = rt_popup.value_widget(df, df.value, param_widget)
            hb.addWidget(res[0])
            param_vbox.addLayout(hb)
            self.global_params[name] = res[0]
            return res

        def _models():
            self._wavefront_models = {}
            params = self._controller.params['simulation_kind']
            first_sk = None
            sk_defaults = self._controller.defaults['simulation_kind']
            for sk_name in sk_defaults:
                sk = srw_enums.SimulationKind.from_anything(sk_name)
                wf_defaults = sk_defaults[sk_name]['wavefront']
                if not first_sk:
                    first_sk = sk
                m = QtGui.QStandardItemModel(len(wf_defaults), 2);
                p = params[sk_name]['wavefront']
                for (row, n) in enumerate(wf_defaults):
                    d = wf_defaults[n]
                    item = QtGui.QStandardItem()
                    rt_qt.i18n_text(d.decl.label, item)
                    m.setItem(row, 0, item)
                    item = QtGui.QStandardItem()
                    rt_popup.set_widget_value(d.decl, p[d.decl.name], item)
                    m.setItem(row, 1, item)
                self._wavefront_models[sk_name] = m
            return self._wavefront_models[first_sk.name.lower()]

        def _view():
            v = WavefrontParams(param_widget)
            v.horizontalHeader().setVisible(0)
            v.horizontalHeader().setResizeMode(
                QtGui.QHeaderView.ResizeToContents)
            v.verticalHeader().setVisible(0)
            param_widget.setSizePolicy(
                QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
            v.horizontalHeader().setSizePolicy(
                QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
                
            stacker = QtGui.QStackedWidget()
            '''
            u = rt_popup.WidgetView(
                self._controller.defaults['radiation_source']['wiggler']['undulator'],
                self._controller.params['radiation_source']['wiggler']['undulator'],
                file_prefix='srw',
                parent=self,
            )
            dd = rt_popup.WidgetView(
                self._controller.defaults['radiation_source']['dual_dipole']['two_dipole'],
                self._controller.params['radiation_source']['dual_dipole']['two_dipole'],
                file_prefix='srw',
                parent=self,
            )
            d = rt_popup.WidgetView(
                self._controller.defaults['radiation_source']['multipole']['magnet'],
                self._controller.params['radiation_source']['multipole']['magnet'],
                file_prefix='srw',
                parent=self,
            )
            '''
            rs_defaults = self._controller.defaults['radiation_source']
            paramss = self._controller.params['radiation_source']
            for i in rs_defaults:
                for j in rs_defaults[i]:
                    d = rs_defaults[i][j]
                    p = paramss[i][j]
                    x = rt_popup.WidgetView(d,p,file_prefix='srw',parent=self)
                    stacker.addWidget(x)
            '''
            stacker.addWidget(u)
            stacker.addWidget(dd)
            stacker.addWidget(d)
            '''
            param_vbox.addWidget(stacker) 
            param_vbox.addWidget(v)
            first = _models()
            v.setModel(first)
            self._wavefront_view = v
            self.global_params['simulation_kind'].currentIndexChanged.connect(
                self._simulation_kind_changed)
            
            self.global_params['radiation_source'].currentIndexChanged.connect(stacker.setCurrentIndex)    

        _global_param('radiation_source')
        _global_param('polarization')
        _global_param('intensity')
        _global_param('simulation_kind')
        _view()
        self._add_vertical_stretch_spacer(param_vbox)
        main.addLayout(param_vbox)

    def _add_result_texts(self, main):
        """Adds two boxes on the right side"""

        def _add(name, label, desc):
            """Creates a stretchable TextEdit area with label above"""
            vbox = QtGui.QVBoxLayout()
            main.addLayout(vbox, stretch=1)
            qlabel = rt_qt.set_id(QtGui.QLabel(self), 'heading')
            for v in self.global_params.values():
                qlabel.setMinimumHeight(v.sizeHint().height())
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

    def _simulation_kind_changed(self):
        """Called when checkbox changes. Sets model on view appropriately"""
        self._wavefront_view.setModel(
            self._wavefront_models[self.get_global_param('simulation_kind').name.lower()])


class WavefrontParams(QtGui.QTableView):
    """Force size of QTableView to be maximum size based on the columns and rows"""

    def minimumSizeHint(self, *args, **kwargs):
        """Returns sizeHint so that the widget will be fixed size"""
        return self.sizeHint()

    def sizeHint(self, *args, **kwargs):
        """Return size dependent on height and width of model rows"""
        h = self.horizontalScrollBar().sizeHint().height() + 4
        for i in xrange(self.model().rowCount()):
            h += self.rowHeight(i)
        w = self.verticalScrollBar().sizeHint().width() + 10
        for i in xrange(self.model().columnCount()):
            w += self.columnWidth(i)
        return QtCore.QSize(w, h)

    def sizePolicy(self, *args, **kwargs):
        """Returns preferred so layout honors sizeHint"""
        return QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
