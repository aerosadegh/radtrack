# -*- coding: utf-8 -*-
u"""Pop up window to enter params for a section of SRW.

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import enum

from radtrack.rt_qt import QtCore, QtGui, i18n_text, set_id, set_param, ENUM_TRUE_INDEX, ENUM_FALSE_INDEX

from pykern import pkcompat
from pykern import pkresource
from pykern import pkio
from pykern.pkdebug import pkdc, pkdp

from radtrack import RbUtility
from radtrack import rt_params

class Window(QtGui.QDialog):
    def __init__(self, declarations, params, file_prefix, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle(i18n_text(declarations['label']))
        self.setStyleSheet(pkio.read_text(pkresource.filename(file_prefix + '_popup.css')))
        self._form = Form(declarations, params, self)

    def get_params(self,):
        """Convert values in the window to "param" values"""
        return self._form._get_params()




class Form(object):
    BUTTON_HEIGHT = 30
    BUTTON_WIDTH = 120
    CHAR_HEIGHT = BUTTON_HEIGHT
    CHAR_WIDTH = 6
    MARGIN_HEIGHT = 20
    MARGIN_WIDTH = 30

    def __init__(self, declarations, params, window):
        super(Form, self).__init__()
        self._declarations = declarations
        self._frame = QtGui.QWidget(window)
        self._layout = QtGui.QFormLayout(self._frame)
        self._layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self._layout.setMargin(0)
        sizes = self._init_fields(params)
        self._init_buttons(window)
        self._set_geometry(sizes)

    def _get_params(self):
        def num(d, w):
            # need type checking
            if w is None:
                return None
            v = w.text()
            if d['units']:
                v = RbUtility.convertUnitsStringToNumber(v, d['units'])
            return d['py_type'](v)

        res = {}
        for d in rt_params.iter_primary_param_declarations(self._declarations):
            f = self._fields[d['label']]
            w = f['widget']
            if isinstance(d['py_type'], enum.EnumMeta):
                if d['display_as_checkbox']:
                    v = d['py_type'](ENUM_TRUE_INDEX if w.isChecked() else ENUM_FALSE_INDEX)
                else:
                    v = d['py_type'](w.itemData(w.currentIndex()).toInt()[0])
            elif d['py_type'] in (float, int):
                v = num(d, w)
            else:
                raise AssertionError('bad type: ' + str(d['py_type']))
            res[d['label']] = v
        return res

    def _init_buttons(self, window):
        self._buttons = QtGui.QDialogButtonBox(window)
        self._buttons.setOrientation(QtCore.Qt.Horizontal)
        self._buttons.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self._buttons.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self._buttons.setCenterButtons(1)
        s = QtGui.QSpacerItem(
            self.CHAR_WIDTH,
            self.CHAR_HEIGHT,
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding,
        )
        self._layout.addItem(s)
        self._layout.addRow(self._buttons)
        QtCore.QObject.connect(
            self._buttons, QtCore.SIGNAL('accepted()'), window.accept)
        QtCore.QObject.connect(
            self._buttons, QtCore.SIGNAL('rejected()'), window.reject)
        ###QtCore.QMetaObject.connectSlotsByName(window)

    def _init_fields(self, params):
        """Create widgets"""
        self._fields = {}
        res = {
            'num': 0,
            'max_value': 0,
            'max_label': 0,
        }

        def _label(d):
            qlabel = QtGui.QLabel(self._frame)
            l = i18n_text(d['label'], qlabel)
            if len(l) > res['max_label']:
                res['max_label'] = len(l)
            return qlabel

        def _heading(qlabel):
            set_id(qlabel, 'heading')
            qlabel.setAlignment(QtCore.Qt.AlignCenter)
            self._layout.addRow(qlabel)

        def _value_widget(d):
            t = d['py_type']
            if not isinstance(t, enum.EnumMeta):
                widget = QtGui.QLineEdit(self._frame)
                v = set_param(d, params, widget)
            else:
                if d['display_as_checkbox']:
                    widget = QtGui.QCheckBox(self._frame)
                    v = i18n_text(t(ENUM_TRUE_INDEX).display_name, widget)
                else:
                    widget = QtGui.QComboBox(self._frame)
                    v = ''
                    for e in t:
                        n = i18n_text(e.display_name)
                        widget.addItem(n, userData=e.value)
                        if len(n) > len(v):
                            v = n
                set_param(d, params, widget)
            return (widget, v)

        for d in rt_params.iter_display_declarations(self._declarations):
            qlabel = _label(d)
            if d['display_as_heading']:
                _heading(qlabel)
                widget = None
            else:
                set_id(qlabel, 'form_field')
                (widget, value) = _value_widget(d)
                self._layout.addRow(qlabel, widget)
                if len(value) > res['max_value']:
                    res['max_value'] = len(value)
            self._fields[d['label']] = {
                'qlabel': qlabel,
                'declaration': d,
                'widget': widget,
            }
            res['num'] += 1
        return res

    def _set_geometry(self, sizes):
        g = QtCore.QRect(
            self.MARGIN_WIDTH,
            self.MARGIN_HEIGHT,
            2 * self.MARGIN_WIDTH + (sizes['max_label'] + sizes['max_value']) * self.CHAR_WIDTH,
            2 * self.MARGIN_HEIGHT + self.CHAR_HEIGHT * sizes['num'] + self.BUTTON_HEIGHT,
        )
        self._frame.setGeometry(g)
