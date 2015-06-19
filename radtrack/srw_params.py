# -*- coding: utf-8 -*-
u"""Mapping of rt_params to srw_params.

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

from pykern import pkarray
from pykern.pkdebug import pkdc, pkdi, pkdp

# from radtrack.rt_srwlib import srwlib, uti_plot
try:
    import srwlib
    import uti_plot
except ImportError:
    from radtrack.srw import srwlib
    from radtrack.srw import uti_plot


def to_beam(params):
    """Convert params to `SRWLPartBeam`

    Args:
        params (dict): RT values in canonical form

    Returns:
        SRWLPartBeam: converted values
    """
    res = srwlib.SRWLPartBeam()
    res.Iavg = params['Average Current']
    m = res.partStatMom1
    m.x = params['Initial Horizontal Coordinate']
    m.y = params['Initial Vertical Coordinate']
    m.z = params['Initial Longitudinal Coordinate']
    m.xp = params['Initial Horizontal Angle']
    m.yp = params['Initial Vertical Angle']
    m.gamma = params['Relativistic Energy (gamma)']
    res.arStatMom2[0] = params['RMS Horizontal Width'] ** 2
    res.arStatMom2[1] = 0
    res.arStatMom2[2] = params['RMS Horizontal Divergence'] ** 2
    res.arStatMom2[3] = params['RMS Vertical Width'] ** 2
    res.arStatMom2[4] = 0
    res.arStatMom2[5] = params['RMS Vertical Divergence'] ** 2
    res.arStatMom2[10] = params['RMS Energy Spread'] ** 2
    return res


def to_flux_precision(params):
    """Convert params to flux precision list

    Args:
        params (dict): RT values in canonical form

    Returns:
        list: five elements for flux
    """
    return _precision(
        params,
        (
            'Initial Harmonic',
            'Final Harmonic',
            'Longitudinal Integration Precision',
            'Azimuthal Integration Precision',
            'Flux Calculation',
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
        params,
        (
            'Precision Factor',
            'Density Computation Method',
            'Initial Longitudinal Position',
            'Initial Azimuthal Position',
            'Number of Points along Trajectory',
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
    harmB.n = params['Harmonic Number']
    harmB.B = params['Magnetic Field']
    if params['Undulator Orientation'].has_name('VERTICAL'):
        harmB.h_or_v = 'v'
    else:
        harmB.h_or_v = 'h'
    und = srwlib.SRWLMagFldU([harmB])
    und.per = params['Period Length']
    und.nPer = params['Number of Periods']
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
        params['Number of points along Energy'],
        params['Number of points along X'],
        params['Number of points along Y'],
    )
    m = res.mesh
    m.zStart = params['Distance to Window']
    m.eStart = params['Initial Photon Energy']
    m.eFin = params['Final Photon Energy']
    m.xStart = params['Window Left Edge']
    m.xFin = params['Window Right Edge']
    m.yStart = params['Window Top Edge']
    m.yFin = params['Window Bottom Edge']
    return res


def _fix_enum_value(v):
    return v.value if hasattr(v, 'value') else v


def _precision(params, labels):
    return [_fix_enum_value(params[k]) for k in labels]
