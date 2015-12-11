# -*- coding: utf-8 -*-
u"""Wrapper for PyQt4 import. Sets QString version to 2.

:copyright: Copyright (c) 2015 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import inspect
import sys

import enum
from pykern.pkdebug import pkdc, pkdp
from pykern import pkinspect

import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui, QtCore

from radtrack import RbUtility

#: Valid id names
ID_NAMES = [
    'heading',
    'form_field',
    'standard',
]

#: Index of True of an enumerated type. Not it's value, which may be anything
ENUM_TRUE_INDEX = 1

#: Index of False of an enumerated type. Not it's value, which may be anything
ENUM_FALSE_INDEX = 0


def run_app(init_widget):
    """Invokes `init_widget` as a Qt program if caller is __main__.

    If `init_widget` is called, then will call :func:`sys.exit`

    Example:
        For a module which has an `rbsrw` class, put this at the end::

            call_if_main(rbsrw)

    Args:
        widget (QtGui.QWidget): what to call
    """
    app = QtGui.QApplication(sys.argv)
    myapp = init_widget()
    myapp.show()
    sys.exit(app.exec_())


def i18n_text(text, widget=None, index=None):
    """Translates text with module as context and optionally sets it

    Will call `setItemText` or `setText` accordingly on `widget`.

    Args:
        text (str): what to translate
        widget (QWidget): what to set it on
        index (int): for setItemText

    Returns:
        str: Translated text
    """
    res = QtGui.QApplication.translate(
        pkinspect.caller_module().__name__,
        text,
        widget.__class__.__name__ if widget else None,
        QtGui.QApplication.UnicodeUTF8,
    )
    if widget:
        if index is not None:
            widget.setItemText(res)
        else:
            widget.setText(res)
    return res


def set_id(widget, id_name):
    """Call setObjectName making sure `class_name` exists

    Args:
        widget (QWidget): what to set it on
        id_name (str): valid name

    Returns:
        QWidget: widget
    """
    assert id_name in ID_NAMES, \
        '{}: unknown id_name'.format(id_name)
    widget.setObjectName(id_name)
    return widget
