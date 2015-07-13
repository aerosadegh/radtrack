# -*- coding: utf-8 -*-
"""pytest for `radtrack.rt_params`

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open
import os.path

import pytest
from pykern.pkdebug import pkdc, pkdp

from radtrack import rt_params
from radtrack import srw_enums


def test_declarations():
    """Verify a couple of values exist"""
    d = rt_params.declarations('srw')
    pkdp(d['precision']['spectral_flux'].children)
    assert d['undulator']['period_len'].units == 'cm', \
        'Undulator period length units should be centimeters'
    assert d['precision']['spectral_flux']['flux_calculation'].py_type \
        == srw_enums.FluxCalculation, \
        'Flux Calculation type should be srw_enums.Flux'
    pkdp(d['precision']['spectral_flux'].values()[3])
    l = list(iter(d['precision']['spectral_flux'].values()))
    assert 'Azimuthal Integration Precision' == l[3].label, \
        'Result should be ordered'
    _assert_unicode(d)


def test_defaults():
    """Verify a couple of values exist"""
    decl = rt_params.declarations('srw')['simulation_complexity']['multi_particle']
    d = rt_params.defaults('srw_multi', decl)
    assert isinstance(
        d['undulator']['orientation'].value,
        srw_enums.UndulatorOrientation), \
        'Value must be parsed correctly'
    assert 101 == \
        d['simulation_kind']['x_and_y']['wavefront']['num_points_x'].value, \
        'Value must be parsed correctly'
    _assert_unicode(d)


def test_init_params():
    """Verify a couple of values exist"""
    decl = rt_params.declarations('srw')['simulation_complexity']['multi_particle']
    p = rt_params.init_params(
        rt_params.defaults('srw_multi', decl),
    )
    assert 0.5 == p['beam']['avg_current'], \
        'Value must be converted to type correctly'
    assert 1000 == p['simulation_kind']['e']['wavefront']['num_points_energy'], \
        'Selectors must be parsed correctly'
    assert p


def test_iter_declarations():
    """Verify a couple of values exist"""
    decl = rt_params.declarations('srw');
    it = rt_params.iter_display_declarations(decl['precision'])
    assert 'Spectral Flux Calculation' == it.next()['label'], \
        'When iter_display_declarations, should see headings'
    assert 'Initial Harmonic' == it.next()['label'], \
        'Ensure values are in order '
    it = rt_params.iter_primary_param_declarations(declarations['precision'])
    assert 'Initial Harmonic' == it.next()['label'], \
        'When iter_primary_param_declarations, should not see heading'
    it = rt_params.iter_primary_param_declarations(declarations['Undulator'])
    assert 5 == len(list(it)), \
        'When iter_primary_param_declarations, should not see computed params'


def _assert_unicode(d, prefix=None):
    if d.children:
        for k, v in d.items():
            pkdp('{} {}', k, v)
            p = '{}.{}'.format(prefix, k) if prefix else k
            # TODO(robnagler) breaks with PY3
            assert isinstance(k, unicode), \
                '{}: key is not unicode'.format(p)
            _assert_unicode(v, p)
    elif type(d) == str:
        assert isinstance(d, unicode), \
            '{}: key is not unicode'.format(prefix)
