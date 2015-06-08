# -*- coding: utf-8 -*-
u"""Manipulate params in relation to the UI

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import enum

from radtrack.rtpyqt4 import QtGui, fromUtf8, translate

from radtrack import RbUtility

def from_dialog(params, dialog):
    """Convert values in the dialog to "param" values"""

    def num(d, v):
        # need type checking
        if v is None:
            return None
        v = v.text()
        if d['units']:
            v = RbUtility.convertUnitsStringToNumber(v, d['units'])
        return d['py_type'](v)

    for f in dialog.ui.fields.values():
        d = f['declaration']
        v = f['value']
        if isinstance(d['py_type'], enum.EnumMeta):
            if d['display_as_checkbox']:
                v = d['py_type'](1 if v.isChecked() else 0)
            else:
                v = d['py_type'](v.currentIndex())
        elif d['py_type'] in (float, int):
            v = num(d, v)
        else:
            raise AssertionError('bad type: ' + str(d['py_type']))
        params[d['rt_old']] = v


def init_params(widget, which):
    """Initialize ``widget.params`` from declarations and defaults.

    widget must have fields `params`, `defaults`, and `declarations`.
    Must implement `compute_secondary_params`

    Args:
        widget (QWidget): params, defaults, ec.
        declarations (dict): parameter spec
        defaults (dict): values

    Returns:
        dict: name to value
    """
    res = {}
    dflt = widget.defaults[which]
    for i, d in enumerate(widget.declarations[which].values()):
        #TODO(robnagler) this should be a list, perhaps (e.g. fields)
        if not isinstance(d, dict):
            continue
        res[d['rt_old']] = dflt[d['label']]
    widget.params[which] = res
    widget.compute_secondary_params(which)


def retranslate_dialog(ui_dialog, dialog, declarations):
    """Set the values from the dialog"""
    dialog.setWindowTitle(translate('Dialog', declarations['label'], None))
    for f in ui_dialog.fields.values():
        d = f['declaration']
        f['qlabel'].setText(translate('Dialog', d['label'], None))
        # Encapsulate in a widget based on type
        if isinstance(d['py_type'], enum.EnumMeta):
            if d['display_as_checkbox']:
                f['value'].setText(translate('Dialog', d['py_type'](1).display_name, None))
            else:
                for v in d['py_type']:
                    f['value'].setItemText(v.value, translate('Dialog', v.display_name, None))


def setup_ui(ui_dialog, dialog, declarations):
    """Create widgets"""
    ui_dialog.fields = {}
    for i, d in enumerate(declarations.values()):
        #TODO(robnagler) this should be a list, perhaps (e.g. fields)
        if not isinstance(d, dict):
            continue
        qlabel = QtGui.QLabel(ui_dialog.formLayoutWidget)
        qlabel.setObjectName(fromUtf8(d['label'] + ' label'))
        ui_dialog.formLayout.setWidget(i, QtGui.QFormLayout.LabelRole, qlabel)
        if isinstance(d['py_type'], enum.EnumMeta):
            if d['display_as_checkbox']:
                value = QtGui.QCheckBox(ui_dialog.formLayoutWidget)
            else:
                value = QtGui.QComboBox(ui_dialog.formLayoutWidget)
                for f in d['py_type']:
                    value.addItem(fromUtf8(''))
        else:
            value = QtGui.QLineEdit(ui_dialog.formLayoutWidget)
        value.setObjectName(fromUtf8(d['label']))
        ui_dialog.formLayout.setWidget(i, QtGui.QFormLayout.FieldRole, value)
        ui_dialog.fields[d['label']] = {
            # Not good to denormalize
            'qlabel': qlabel,
            'declaration': d,
            'value': value,
        }


def to_dialog(params, dialog):
    for f in dialog.ui.fields.values():
        d = f['declaration']
        v = f['value']
        p = params[d['rt_old']]
        if isinstance(d['py_type'], enum.EnumMeta):
            if d['display_as_checkbox']:
                v.setChecked(p.value == 1)
            else:
                v.setCurrentIndex(p.value)
        elif d['units']:
            v.setText(RbUtility.displayWithUnitsNumber(p, d['units']))
        else:
            v.setText(str(p))
