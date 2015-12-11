# -*- coding: utf-8 -*-
u"""?Base class for controllers

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

from pykern.pkdebug import pkdc, pkdp
from pykern import pkinspect

class Controller(object):
    """Base class for all RadTrack controllers"""

    @classmethod
    def init_widget(cls, parent=None):
        """Instantiates `cls` and calls `init`

        Args:
            cls (object): implements a controller
            parent (QWidget): widget

        Returns:
            QWidget: widget peer of this controller

        """
        return cls().init(parent)

    @classmethod
    def run_if_main(cls):
        """Passes `cls.init_widget` to rt_qt.run_app if running in main.

        If caller isn't main, does nothing. If called from main, will
        import rt_qt (which imports in PyQt4). Allows controller to be
        tested inline.
        """
        if not pkinspect.is_caller_main():
            return
        from radtrack import rt_qt
        rt_qt.run_app(cls.init_widget)
