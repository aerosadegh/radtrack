# -*- coding: utf-8 -*-
u"""Wrapper for srwlib import

:copyright: Copyright (c) 2015 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

try:
    import srwlib
    import uti_plot
except ImportError:
    from radtrack.srw import srwlib
    from radtrack.srw import uti_plot

# Initialize so doesn't files
uti_plot.uti_plot_init(backend=uti_plot.DEFAULT_BACKEND, fname_format=None)
