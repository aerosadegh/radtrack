# -*- coding: utf-8 -*-
"""pytest for `radtrack.srw_params`

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open
import os.path

import pytest

from radtrack import srw_params
from radtrack import srw_enums


def test_declarations():
    """Verify a couple of values exist"""
    d = srw_params.declarations()
    assert d['Undulator']['Period Length']['units'] == 'cm', \
        'Undulator period length units should be centimeters'
    assert d['Spectral Flux Calculation']['Flux Calculation']['py_type'] \
        == srw_enums.Flux, \
        'Flux Calculation type should be srw_enums.Flux'
    _assert_unicode(d)


def test_defaults():
    """Verify a couple of values exist"""
    d = srw_params.defaults()
    assert d['Simulation Complexity']['MULTI_PARTICLE']['_value'] \
        == srw_enums.SimComplexity.MULTI_PARTICLE, \
        'Value must be parsed correctly'
    assert isinstance(
        d['Simulation Complexity']['MULTI_PARTICLE']['Undulator']['Undulator Orientation'],
        srw_enums.UndulatorOrientation), \
        'Value must be parsed correctly'


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
