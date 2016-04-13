# -*- coding: utf-8 -*-
"""Pop up window to enter params for a section of SRW.

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function

import collections
import enum

from radtrack.rt_qt import QtCore, QtGui

from pykern import pkcompat
from pykern import pkresource
from pykern import pkio
from pykern import pkcollections
from pykern.pkdebug import pkdc, pkdp
from pykern import pkcompat

from radtrack.util.unitConversion import convertUnitsStringToNumber, displayWithUnitsNumber
from radtrack import rt_params
from radtrack import rt_qt

def get_widget_value(decl, widget):
    def _num(d, w):
        # need type checking
        if w is None:
            return None
        v = w.text()
        if d.units:
            v = convertUnitsStringToNumber(v, d.units)
        return d.py_type(v)

    if issubclass(decl.py_type, bool):
        return widget.isChecked()
    elif isinstance(decl.py_type, enum.EnumMeta):
        return list(decl.py_type)[widget.currentIndex()]
    elif issubclass(decl.py_type, float) or issubclass(decl.py_type, int):
        return _num(decl, widget)
    elif issubclass(decl.py_type,str):
        return widget.text()
    else:
        raise AssertionError('bad type: ' + str(decl.py_type))


def set_widget_value(decl, param, widget):
    """Sets parameter value accordingly on widget

    Args:
        decl (dict): decl for parameter
        param (dict): value
        widget (widget): what to set on

    Returns:
        str: value that was set
    """
    t = decl.py_type
    if isinstance(t, enum.EnumMeta):
        widget.setCurrentIndex(list(t).index(param))
        return rt_qt.i18n_text(param.display_name)
    if issubclass(t, bool):
        widget.setChecked(param)
        # Approximate size of checkbox
        return ' '
    if decl.units:
        l = displayWithUnitsNumber(param, decl.units)
    else:
        l = str(param)
    widget.setText(l)
    return l


def value_widget(default, value, parent, controller):
    d = default.decl
    t = d.py_type
    v = None
    if isinstance(t, enum.EnumMeta):
        widget = QtGui.QComboBox(parent)
        v = ''
        choices = t
        if default.children:
            choices = []
            for c in pkcollections.map_values(default.children):
                if controller.decl_is_visible(c.decl):
                    choices.append(c.value)
        for e in choices:
            n = rt_qt.i18n_text(e.display_name)
            widget.addItem(n, userData=e.value)
            if len(n) > len(v):
                v = n
        # If value is not in choices, nothing will be selected
        set_widget_value(d, value, widget)
    elif issubclass(t, bool):
        widget = QtGui.QCheckBox(parent)
        v = rt_qt.i18n_text(d.label)
        set_widget_value(d, value, widget)
    else:
        widget = QtGui.QLineEdit(parent)
        v = set_widget_value(d, value, widget)
    return (widget, v)


class Window(QtGui.QDialog):
    def __init__(self, defaults, params, controller, parent=None, tabinput=False):
        super(Window, self).__init__(parent)
        self._controller = controller
        self.setWindowTitle(rt_qt.i18n_text(defaults.decl.label))
        self.setStyleSheet(pkio.read_text(pkresource.filename(controller.FILE_PREFIX + '_popup.css')))
        self._form = Form(defaults, params, self, dynamic_popup=True)
        self.parent=parent
        if tabinput:
            if tabinput:
                b=QtGui.QPushButton('Retrieve'+tabinput)
            self._form._buttons.addButton(b,QtGui.QDialogButtonBox.ActionRole)
            #b.clicked.connect(lambda:self.from_tab(tabinput))
            

    def get_params(self,):
        """Convert values in the window to "param" values"""
        return self._form._get_params()
                    

class WidgetView(QtGui.QWidget):
    def __init__(self, defaults, params, controller, parent=None):
        super(WidgetView, self).__init__(parent)
        self._controller = controller
        self.setStyleSheet(pkio.read_text(pkresource.filename(controller.FILE_PREFIX + '_popup.css')))
        self._form = Form(defaults, params, self, dynamic_popup=False)

    def get_params(self,):
        """Convert values in the window to "param" values"""
        return self._form._get_params()


class Form(object):
    BUTTON_HEIGHT = 30
    BUTTON_WIDTH = 120
    CHAR_HEIGHT = BUTTON_HEIGHT - 2
    CHAR_WIDTH = 6
    MARGIN_HEIGHT = 20
    MARGIN_WIDTH = 30

    def __init__(self, defaults, params, window, dynamic_popup=True):
        super(Form, self).__init__()
        self._defaults = defaults
        self._controller = window._controller
        self._frame = QtGui.QWidget()
        self._layout = QtGui.QFormLayout()
        self._layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self._layout.setMargin(0)
        self._dynamic_popup = dynamic_popup
        sizes = self._init_fields(params)
        if self._dynamic_popup:
            self._set_geometry(sizes)
        sa = QtGui.QScrollArea()
        self._frame.setLayout(self._layout)
        sa.setWidget(self._frame)
        self.mainlayout = QtGui.QFormLayout(window)
        self.mainlayout.addRow(sa)
        if self._dynamic_popup:
            self._init_buttons(window)
        else:
            self._controller.register_static_widget(self)
        self.update_visibility()

    def update_visibility(self):
        for f in self._fields.values():
            visibility = self._controller.decl_is_visible(f['decl'])
            if f['widget']:
                f['widget'].setVisible(visibility)
            f['qlabel'].setVisible(visibility)
        if not self._dynamic_popup:
            self._frame.adjustSize()

    def _get_params(self):

        def _iter_children(parent_defaults):
            res = collections.OrderedDict()
            for df in pkcollections.map_values(parent_defaults.children):
                d = df.decl
                if df.children:
                    res[d.name] = _iter_children(df)
                    continue
                f = self._fields[d.qualified_name]
                res[d.name] = get_widget_value(d, f['widget'])
            return res

        return _iter_children(self._defaults)

    def _init_buttons(self, window):
        self._buttons = rt_qt.set_id(QtGui.QDialogButtonBox(window), 'standard')
        self._buttons.setCenterButtons(1)
        self._buttons.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        for b in self._buttons.buttons():
            b.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.mainlayout.addRow(self._buttons)
        #self._buttons.addButton(b,QtGui.QDialogButtonBox.ActionRole)
        QtCore.QObject.connect(
            self._buttons, QtCore.SIGNAL('accepted()'), window.accept)
        QtCore.QObject.connect(
            self._buttons, QtCore.SIGNAL('rejected()'), window.reject)
        #QtCore.QObject.connect(
        #    self._buttons, QtCore.SIGNAL('clicked()'), report)
        #b.clicked.connect(report)
        
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
            l = rt_qt.i18n_text(d.label, qlabel)
            if len(l) > res['max_label']:
                res['max_label'] = len(l)
            return qlabel

        def _heading(qlabel):
            rt_qt.set_id(qlabel, 'heading')
            qlabel.setAlignment(QtCore.Qt.AlignCenter)
            self._layout.addRow(qlabel)

        def _iter_children(parent_default, p):
            for df in pkcollections.map_values(parent_default.children):
                d = df.decl
                qlabel = _label(d)
                if df.children:
                    _heading(qlabel)
                    res['num'] += 1
                    widget = None
                    _iter_children(df, p[d.name])
                else:
                    if not self._dynamic_popup:
                        qlabel.setWordWrap(True);
                    rt_qt.set_id(qlabel, 'form_field')
                    (widget, value) = value_widget(
                        df,
                        p[d.name],
                        self._frame,
                        self._controller,
                    )
                    self._layout.addRow(qlabel, widget)
                    if len(value) > res['max_value']:
                        res['max_value'] = len(value)
                self._fields[d.qualified_name] = {
                    'qlabel': qlabel,
                    'widget': widget,
                    'decl': d,
                }
                res['num'] += 1

        _iter_children(self._defaults, params)
        return res

    def _set_geometry(self, sizes):
        g = QtCore.QRect(
            self.MARGIN_WIDTH,
            self.MARGIN_HEIGHT,
            2 * self.MARGIN_WIDTH + (sizes['max_label'] + sizes['max_value']) * self.CHAR_WIDTH,
            2 * self.MARGIN_HEIGHT + self.CHAR_HEIGHT * sizes['num'] + self.BUTTON_HEIGHT,
        )
        self._frame.setGeometry(g)
