# -*- coding: utf-8 -*-
u"""pytest for :mod:`radtrack.RbGlobal`

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open
import sip
sip.setapi('QString', 2)

import os
import pytest

def test_conformance():
    """Verify GUI is syntactically correct"""
    import radtrack.RbGlobal
    # Would like to call_main, but that doesn't work, because Qt
    # does something strange that causes the application to exit
    # without being able to catch the exception.
