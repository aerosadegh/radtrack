# -*- coding: utf-8 -*-
u"""Mapping of rt_params to srw_params.

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

from pykern import pkarray
from pykern.pkdebug import pkdc, pkdi, pkdp

import srwlib
import uti_plot
# Initialize so that SRW doesn't generate files
uti_plot.uti_plot_init(backend=uti_plot.DEFAULT_BACKEND, fname_format=None)

def to_beam(params):
    """Convert params to `SRWLPartBeam`

    Args:
        params (dict): RT values in canonical form

    Returns:
        SRWLPartBeam: converted values
    """
    res = srwlib.SRWLPartBeam()
    res.Iavg = params['avg_current']
    m = res.partStatMom1
    m.x = params['horizontal_coord']
    m.y = params['vertical_coord']
    m.z = params['longitudinal_coord']
    m.xp = params['horizontal_angle']
    m.yp = params['vertical_angle']
    m.gamma = params['gamma']
    res.arStatMom2[0] = params['rms_horizontal_width'] ** 2
    res.arStatMom2[1] = 0
    res.arStatMom2[2] = params['rms_horizontal_divergence'] ** 2
    res.arStatMom2[3] = params['rms_vertical_width'] ** 2
    res.arStatMom2[4] = 0
    res.arStatMom2[5] = params['rms_vertical_divergence'] ** 2
    res.arStatMom2[10] = params['rms_energy_spread'] ** 2
    return res


def to_flux_precision(params):
    """Convert params to flux precision list

    Args:
        params (dict): RT values in canonical form

    Returns:
        list: five elements for flux
    """
    return _precision(
        params['spectral_flux'],
        (
            'initial_harmonic',
            'final_harmonic',
            'longitudinal',
            'azimuthal',
            'flux_calculation',
        ),
    )


def to_power_precision(params):
    """Convert params to power density precision list

    Args:
        params (dict): RT values in canonical form

    Returns:
        list: five elements for power density
    """
    return _precision(
        params['power_density'],
        (
            'factor',
            'density_computation',
            'longitudinal_pos',
            'azimuthal_pos',
            'num_points_trajectory',
        ),
    )


def to_undulator(params):
    """Convert params to `SRWLMagFldU` and `SRWLMagFldC`

    Args:
        params (dict): RT values in canonical form

    Returns:
        (SRWLMagFldU, SRWLMagFldC): converted values
    """
    harmB = srwlib.SRWLMagFldH()
    harmB.n = params['harmonic_num']
    harmB.B = params['magnetic_field']
    if params['orientation'].has_name('VERTICAL'):
        harmB.h_or_v = 'v'
    else:
        harmB.h_or_v = 'h'
    und = srwlib.SRWLMagFldU([harmB])
    und.per = params['period_len']
    und.nPer = params['num_periods']
    magFldCnt = srwlib.SRWLMagFldC(
        [und],
        pkarray.new_double([0]),
        pkarray.new_double([0]),
        pkarray.new_double([0]),
    )
    return (und, magFldCnt)


def to_wavefront(params):
    """Convert params to SRWLStokes Wavefront valuesa

    Args:
        params (dict): RT values in canonical formn

    Returns:
        SRWLStokes: converted values
    """
    res = srwlib.SRWLStokes()
    res.allocate(
        params['num_points_energy'],
        params['num_points_x'],
        params['num_points_y'],
    )
    m = res.mesh
    m.zStart = params['distance_to_window']
    m.eStart = params['initial_photon_energy']
    m.eFin = params['final_photon_energy']
    m.xStart = params['window_left_edge']
    m.xFin = params['window_right_edge']
    m.yStart = params['window_top_edge']
    m.yFin = params['window_bottom_edge']
    return res


def _fix_enum_value(v):
    return v.value if hasattr(v, 'value') else v


def _precision(params, labels):
    return [_fix_enum_value(params[k]) for k in labels]
