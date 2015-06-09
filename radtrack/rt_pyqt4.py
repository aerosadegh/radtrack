# -*- coding: utf-8 -*-
u"""Wrapper for PyQt4 import. Sets QString version to 2.

:copyright: Copyright (c) 2015 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import inspect
import sys

import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui, QtCore

try:
    fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


def call_if_main(widget):
    """Invokes `widget` as a Qt program if caller is __main__.

    If `widget` is called, then will call :func:`sys.exit`

    Example:
        For a module which has an `rbsrw` class, put this at the end::

            call_if_main(rbsrw)

    Args:
        widget (QtGui.QWidget): what to call
    """
    f = None
    try:
        f = inspect.currentframe().f_back
        if f.f_globals['__name__'] != '__main__':
            return
    finally:
        # Avoid cycles in the stack
        del f
    app = QtGui.QApplication(sys.argv)
    myapp = widget()
    myapp.show()
    sys.exit(app.exec_())
