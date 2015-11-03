# -*- coding: utf-8 -*-
"""pytest for `radtrack.genesis_enums`

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function

import pytest

from radtrack import genesis_enums


def test_density_method():
    """Verify a couple of values exist"""
    d = genesis_enums.CellStart
    assert d(0.) == d.FULL, \
        'FULL should be 0.0'
    assert d(.5) == d.HALF, \
        'HALF should be 0.5'
    assert d(0.5) == 0.5, \
        'CellStart(.5) == .5'
    assert d.HALF > d.FULL, \
        'HALF > FULL'
