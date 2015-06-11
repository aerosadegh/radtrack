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

class View(QtGui.QWidget):
    """Pane with buttons, parameters, and results windows.

    laid out horizontally.
    """
    def __init__(self, controller, parent=None, is_multi_particle=False):
        super(View, self).__init__(parent)
        self._controller = controller
        self.setStyleSheet(pkio.read_text(pkresource.filename('srw_pane.css')))
        main = QtGui.QHBoxLayout()
        self._add_action_buttons(main)
        self._add_param_vbox(main)
        self._add_result_texts(main)
        self.setLayout(main)

    def current_simulation_kind(self):
        v = self.simulation_kind.itemData(
                self.simulation_kind.currentIndex())
        (i, ok) = v.toInt()
        assert ok, \
            '{}: simulation_kind_value invalid'.format(v)
        return srw_enums.SimulationKind(i)

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

        def _selector():
            """Create simulation kind selector"""
            hb = QtGui.QHBoxLayout()
            label = set_id(QtGui.QLabel(param_widget), 'form_field')
            #TODO: Labels should be looked up
            i18n_text('Simulation Kind: ', label)
            hb.addWidget(label, alignment=QtCore.Qt.AlignRight)
            self.simulation_kind = QtGui.QComboBox(param_widget)
            hb.addWidget(self.simulation_kind)
            param_vbox.addLayout(hb)

        _selector()

        params = self._controller.params['Simulation Kind']
        self.wavefront_models = {}
        self.wavefront_view = WavefrontParams(param_widget)
        self.wavefront_view.horizontalHeader().setVisible(0)
        self.wavefront_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.wavefront_view.verticalHeader().setVisible(0)
        decl = list(
            rt_params.iter_primary_param_declarations(self._controller.declarations['Wavefront']))
        first_sk = None
        for sk in srw_enums.SimulationKind:
            #
            if sk.name not in params:
                continue
            if not first_sk:
                first_sk = sk
            self.simulation_kind.addItem(
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
            self.wavefront_models[sk.name] = m
        self.wavefront_view.setModel(
            self.wavefront_models[first_sk.name],
        )
        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        param_widget.setSizePolicy(policy)

        self.wavefront_view.horizontalHeader().setSizePolicy(
            QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)

        self.simulation_kind.currentIndexChanged.connect(
            self._simulation_kind_changed)

        param_vbox.addWidget(self.wavefront_view)
        self._add_vertical_stretch_spacer(param_vbox)
        main.addLayout(param_vbox)

    def _add_result_texts(self, main):
        """Adds two boxes on the right side"""

        self._result_text = {}

        def _result_text(name, label, desc):
            """Creates a stretchable TextEdit area with label above"""
            vbox = QtGui.QVBoxLayout()
            main.addLayout(vbox, stretch=1)
            qlabel = set_id(QtGui.QLabel(self), 'heading')
            qlabel.setMinimumHeight(self.simulation_kind.sizeHint().height())
            i18n_text(label, qlabel)
            vbox.addWidget(qlabel, alignment=QtCore.Qt.AlignCenter)
            text = QtGui.QTextEdit(self)
            i18n_text(desc, text)
            text.setReadOnly(True)
            vbox.addWidget(text)
            self._result_text[name] = text

        _result_text(
            'simulation',
            'Simulation Results',
            'Click Simulate to run SRW',
        )
        _result_text(
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
        self.wavefront_view.setModel(
            self.wavefront_models[self.current_simulation_kind().name])


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
