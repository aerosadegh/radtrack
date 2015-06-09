# -*- coding: utf-8 -*-
"""pytest for `radtrack.rt_params`

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open
import os.path

import pytest
from pykern.pkdebug import pkdc, pkdi, pkdp

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
    assert isinstance(
        d['Simulation Complexity']['MULTI_PARTICLE']['Undulator']['Undulator Orientation'],
        srw_enums.UndulatorOrientation), \
        'Value must be parsed correctly'
    assert 101 == \
        d['Simulation Complexity']['MULTI_PARTICLE'] \
        ['Simulation Kind']['X_AND_Y']['Wavefront']['Number of points along X'], \
        'Value must be parsed correctly'
    _assert_unicode(d)


def test_init_params():
    """Verify a couple of values exist"""
    p = rt_params.init_params(
        rt_params.defaults('srw')['Simulation Complexity']['MULTI_PARTICLE'],
        rt_params.declarations('srw'),
    )
    assert 0.5 == p['Beam']['Average Current'], \
        'Value must be converted to type correctly'
    assert 1000 == p['Simulation Kind']['E']['Wavefront']['Number of points along Energy'], \
        'Selectors must be parsed correctly'
    assert p


def test_iter_declarations():
    """Verify a couple of values exist"""
    declarations = rt_params.declarations('srw');
    it = rt_params.iter_display_declarations(declarations['Precision'])
    assert 'Spectral Flux Calculation' == it.next()['label'], \
        'When iter_display_declarations, should see headings'
    assert 'Initial Harmonic' == it.next()['label'], \
        'Ensure values are in order '
    it = rt_params.iter_primary_param_declarations(declarations['Precision'])
    assert 'Initial Harmonic' == it.next()['label'], \
        'When iter_primary_param_declarations, should not see heading'
    it = rt_params.iter_primary_param_declarations(declarations['Undulator'])
    assert 5 == len(list(it)), \
        'When iter_primary_param_declarations, should not see computed params'


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
