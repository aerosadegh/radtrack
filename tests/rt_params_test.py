# -*- coding: utf-8 -*-
"""pytest for `radtrack.rt_params`

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open
import os.path

import pytest

from radtrack import rt_params
from radtrack import srw_enums


def test_declarations():
    """Verify a couple of values exist"""
    d = rt_params.declarations('srw')
    assert d['Undulator']['Period Length']['units'] == 'cm', \
        'Undulator period length units should be centimeters'
    assert d['Precision']['Flux Calculation']['py_type'] \
        == srw_enums.Flux, \
        'Flux Calculation type should be srw_enums.Flux'
    l = list(iter(d['Precision'].values()))
    assert 'Azimuthal Integration Precision' == l[4]['label'], \
        'Result should be ordered'
    _assert_unicode(d)


def test_defaults():
    """Verify a couple of values exist"""
    d = rt_params.defaults('srw')
    assert d['Simulation Complexity']['MULTI_PARTICLE']['_value'] \
        == srw_enums.SimComplexity.MULTI_PARTICLE, \
        'Value must be parsed correctly'
    assert isinstance(
        d['Simulation Complexity']['MULTI_PARTICLE']['Undulator']['Undulator Orientation'],
        srw_enums.UndulatorOrientation), \
        'Value must be parsed correctly'
    _assert_unicode(d)

def _assert_unicode(d, prefix=None):
    if isinstance(d, dict):
        for k, v in d.items():
            p = '{}.{}'.format(prefix, k) if prefix else k
            # TODO(robnagler) breaks with PY3
            assert isinstance(k, unicode), \
                '{}: key is not unicode'.format(p)
            _assert_unicode(v, p)
    elif type(d) == str:
        assert isinstance(d, unicode), \
            '{}: key is not unicode'.format(prefix)
