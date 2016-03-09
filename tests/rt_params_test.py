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
    d = rt_params.declarations('srw')['root']
    assert d['radiation_source']['undulator']['undulator']['period_len'].units == 'm', \
        'Undulator period length units should be centimeters'
    assert d['precision']['spectral_flux']['flux_calculation'].py_type \
        == srw_enums.FluxCalculation, \
        'Flux Calculation type should be srw_enums.Flux'
    l = list(iter(d['precision']['spectral_flux'].values()))
    assert 'Azimuthal Integration Precision' == l[3].label, \
        'Result should be ordered'


def test_defaults():
    """Verify a couple of values exist"""
    decl = rt_params.declarations('srw')
    d = rt_params.defaults('srw', decl['root'])
    assert isinstance(
        d['radiation_source']['undulator']['undulator']['orientation'].value,
        srw_enums.UndulatorOrientation), \
        'Value must be parsed correctly'
    assert 100 == \
        d['simulation_kind']['x_and_y']['wavefront']['num_points_x'].value, \
        'Value must be parsed correctly'


def test_init_params():
    """Verify a couple of values exist"""
    decl = rt_params.declarations('srw')['root']
    p = rt_params.init_params(
        rt_params.defaults('srw', decl),
    )
    assert 0.1 == p['beam']['avg_current'], \
        'Value must be converted to type correctly'
    assert 1000 == p['simulation_kind']['e']['wavefront']['num_points_energy'], \
        'Selectors must be parsed correctly'
    assert p


def test_iter_defaults():
    """Verify a couple of values exist"""
    decl = rt_params.declarations('srw')['root']
    defaults = rt_params.defaults('srw', decl)
    it = defaults['precision'].iter_leaves()
    assert 'Initial Harmonic' == it.next().decl.label, \
        'Ensure values are in order of leaves'
    assert 'Final Harmonic' == it.next().decl.label, \
        'Ensure see we can traverse to second leaf'
    it = defaults['precision'].iter_nodes()
    assert 'Precision' == it.next().decl.label, \
        'Ensure parent is first value'
    assert 'Spectral Flux Calculation' == it.next().decl.label, \
        'Ensure see first parent node'
    assert 'Initial Harmonic' == it.next().decl.label, \
        'Ensure see first leaf'
    assert 'Final Harmonic' == it.next().decl.label, \
        'Ensure see we can traverse to second leaf'
