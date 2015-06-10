# -*- coding: utf-8 -*-
u"""Pop up window to enter params for a section of SRW.

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import enum

from radtrack.rt_pyqt4 import QtCore, QtGui, fromUtf8, translate

from pykern import pkcompat
from pykern import pkresource
from pykern import pkio
from pykern.pkdebug import pkdc, pkdp

from radtrack import RbUtility
from radtrack import rt_params

#: Index of True of an enumerated type. Not it's value, which may be anything
ENUM_TRUE_INDEX = 1

#: Index of False of an enumerated type. Not it's value, which may be anything
ENUM_FALSE_INDEX = 0

class Window(QtGui.QDialog):
    def __init__(self, declarations, params, file_prefix, parent=None):
        super(Window, self).__init__(parent)
        self._retranslate(declarations)
        self.setStyleSheet(pkio.read_text(pkresource.filename(file_prefix + '_popup.css')))
        self._form = Form(declarations, params, self)

    def get_params(self,):
        """Convert values in the window to "param" values"""
        return self._form._get_params()

    def _retranslate(self, declarations):
        self.setWindowTitle(translate('window', declarations['label'], None))


class Form(object):
    BUTTON_HEIGHT = 30
    BUTTON_WIDTH = 120
    CHAR_HEIGHT = BUTTON_HEIGHT
    CHAR_WIDTH = 6
    MARGIN_HEIGHT = 20
    MARGIN_WIDTH = 30

    def __init__(self, declarations, params, window):
        super(Form, self).__init__()
        window.setObjectName(fromUtf8('form'))
        self._frame = QtGui.QWidget(window)
        self._frame.setObjectName(fromUtf8('form'))
        self._layout = QtGui.QFormLayout(self._frame)
        self._layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self._layout.setMargin(0)
        self._layout.setObjectName(fromUtf8('layout'))
        num_fields = self._init_fields(declarations)
        (max_label, max_value) = self._retranslate(window)
        self._init_buttons(window)
        max_value = self._set_params(params, max_value)
        self._set_geometry(max_label, max_value, num_fields)

    def _get_params(self):
        def num(d, v):
            # need type checking
            if v is None:
                return None
            v = v.text()
            if d['units']:
                v = RbUtility.convertUnitsStringToNumber(v, d['units'])
            return d['py_type'](v)

        res = {}
        for d in rt_params.iter_primary_param_declarations(self._declarations):
            f = self._fields[d['label']]
            v = f['value']
            if isinstance(d['py_type'], enum.EnumMeta):
                if d['display_as_checkbox']:
                    v = d['py_type'](ENUM_TRUE_INDEX if v.isChecked() else ENUM_FALSE_INDEX)
                else:
                    v = d['py_type'](v.itemData(v.currentIndex()).toInt()[0])
            elif d['py_type'] in (float, int):
                v = num(d, v)
            else:
                raise AssertionError('bad type: ' + str(d['py_type']))
            res[d['label']] = v
        return res

    def _init_buttons(self, window):
        self._buttons = QtGui.QDialogButtonBox(window)
        self._buttons.setOrientation(QtCore.Qt.Horizontal)
        self._buttons.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self._buttons.setObjectName(fromUtf8('_buttons'))
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
            self._buttons, QtCore.SIGNAL(fromUtf8('accepted()')), window.accept)
        QtCore.QObject.connect(
            self._buttons, QtCore.SIGNAL(fromUtf8('rejected()')), window.reject)
        QtCore.QMetaObject.connectSlotsByName(window)

    def _init_fields(self, declarations):
        """Create widgets"""
        self._fields = {}
        self._declarations = declarations
        num = 0
        for d in rt_params.iter_display_declarations(self._declarations):
            qlabel = QtGui.QLabel(self._frame)
            if d['display_as_heading']:
                qlabel.setObjectName(fromUtf8('heading'))
                qlabel.setAlignment(QtCore.Qt.AlignCenter)
                self._layout.addRow(qlabel)
                value = None
            else:
                qlabel.setObjectName(fromUtf8(d['label'] + ' label'))
                if isinstance(d['py_type'], enum.EnumMeta):
                    if d['display_as_checkbox']:
                        value = QtGui.QCheckBox(self._frame)
                    else:
                        value = QtGui.QComboBox(self._frame)
                        for f in d['py_type']:
                            value.addItem(fromUtf8(''), userData=f.value)
                else:
                    value = QtGui.QLineEdit(self._frame)
                value.setObjectName(fromUtf8(d['label']))
                #value.setVerticalPolicy(QtCore.QSizePolicy.Expanding)
                self._layout.addRow(qlabel, value)
            self._fields[d['label']] = {
                # Not good to denormalize
                'qlabel': qlabel,
                'declaration': d,
                'value': value,
            }
            num += 1
        return num

    def _set_geometry(self, max_label, max_value, num_fields):
        g = QtCore.QRect(
            self.MARGIN_WIDTH,
            self.MARGIN_HEIGHT,
            2 * self.MARGIN_WIDTH + (max_label + max_value) * self.CHAR_WIDTH,
            2 * self.MARGIN_HEIGHT + self.CHAR_HEIGHT * num_fields + self.BUTTON_HEIGHT,
        )
        self._frame.setGeometry(g)

    def _retranslate(self, window):
        """Set the values from the window"""
        max_label = 0
        max_value = 0
        for d in rt_params.iter_display_declarations(self._declarations):
            f = self._fields[d['label']]
            l = translate('Dialog', d['label'], None)
            if len(l) > max_label:
                max_label = len(l)
            f['qlabel'].setText(l)
            if d['display_as_heading']:
                continue
            # Encapsulate in a widget based on type
            if isinstance(d['py_type'], enum.EnumMeta):
                if d['display_as_checkbox']:
                    l = translate(
                        'Dialog',
                        d['py_type'](ENUM_TRUE_INDEX).display_name,
                        None,
                    )
                    f['value'].setText(l)
                    if len(l) > max_value:
                        max_value = len(l)
                else:
                    for i, v in enumerate(d['py_type']):
                        l = translate('Dialog', v.display_name, None)
                        f['value'].setItemText(i, l)
                        if len(l) > max_value:
                            max_value = len(l)
        return (max_label, max_value)

    def _set_params(self, params, max_value):
        for d in rt_params.iter_primary_param_declarations(self._declarations):
            f = self._fields[d['label']]
            v = f['value']
            p = params[d['label']]
            if isinstance(d['py_type'], enum.EnumMeta):
                if d['display_as_checkbox']:
                    v.setChecked(d['py_type'](ENUM_TRUE_INDEX) == p)
                else:
                    v.setCurrentIndex(list(d['py_type']).index(p))
                continue
            if d['units']:
                l = RbUtility.displayWithUnitsNumber(p, d['units'])
                v.setText(l)
            else:
                # translate('Dialog', v.display_name, None)
                l = pkcompat.locale_str(str(p))
            v.setText(l)
            if len(l) > max_value:
                max_value = len(l)
        return max_value
