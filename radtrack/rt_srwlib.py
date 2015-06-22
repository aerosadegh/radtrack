# -*- coding: utf-8 -*-
u"""Wrapper for srwlib import

:copyright: Copyright (c) 2015 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

# We need to eliminate 'import *' usage; however,
#    until that happens, we put it here in a common file
import srwlib
from srwlib import *

import uti_plot
from uti_plot import *

# Initialize so that SRW doesn't generate files
uti_plot.uti_plot_init(backend=uti_plot.DEFAULT_BACKEND, fname_format=None)
