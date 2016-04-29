# -*- coding: utf-8 -*-
u"""Mapping of rt_params to srw_params.

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function

import argparse

from pykern import pkarray
from pykern.pkdebug import pkdc, pkdp
from pykern import pkcollections

import srwlib
from array import array

def to_beam(params):
    """Convert params to `SRWLPartBeam`

    Args:
        params (dict): RT values in canonical form

    Returns:
        SRWLPartBeam: converted values
    """

    res = srwlib.SRWLPartBeam()
    res.Iavg = params['current']
    m = res.partStatMom1
    m.x = params['horizontal_coord']
    m.y = params['vertical_coord']
    m.z = params['longitudinal_coord']
    m.xp = params['horizontal_angle']
    m.yp = params['vertical_angle']
    m.gamma = params['gamma']
    if 'rms_horizontal_width' in params:
        res.arStatMom2[0] = params['rms_horizontal_width'] ** 2
        res.arStatMom2[1] = 0
        res.arStatMom2[2] = params['rms_horizontal_divergence'] ** 2
        res.arStatMom2[3] = params['rms_vertical_width'] ** 2
        res.arStatMom2[4] = 0
        res.arStatMom2[5] = params['rms_vertical_divergence'] ** 2
        res.arStatMom2[10] = params['rms_energy_spread'] ** 2
    '''    
    print(res.arStatMom2[0])
    print(res.arStatMom2[2])
    print(res.arStatMom2[3])
    print(res.arStatMom2[5])
    print(res.arStatMom2[10])
    sigEperE = 0.1
    sigX = (1.5e-06/(64/0.511)*0.1)**(1/2) #horizontal RMS size of e-beam [m]
    sigXp = (1.5e-06/(64/0.511)/0.1) **(1/2) #horizontal RMS angular divergence
    sigY = sigX #vertical RMS size of e-beam [m]
    sigYp = sigXp #vertical RMS angular divergence [rad]
    res.arStatMom2 = {}
    res.arStatMom2[0]=sigX**2
    res.arStatMom2[1]=0
    res.arStatMom2[2]=sigXp**2
    res.arStatMom2[3]=sigY**2
    res.arStatMom2[4]=0
    res.arStatMom2[5]=sigYp**2
    res.arStatMom2[10]=sigEperE**2
    '''

    
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


def to_precision_single_particle(params):
    """Convert params to single particle precision list

    Args:
        params (dict): RT values in canonical form

    Returns:
        list: elements for power density
    """
    '''
    print(_precision(
        params,
        (
            'sr_calculation_method',
            'relative',
            'start_integration',
            'end_integration',
            'num_points_trajectory_calculation',
            'use_terminating_terms',
            'sampling_factor',
        ),
    ))'''
    return _precision(
        params,
        (
            'sr_calculation_method',
            'relative',
            'start_integration',
            'end_integration',
            'num_points_trajectory_calculation',
            'use_terminating_terms',
            'sampling_factor',
        ),
    )


def to_undulator_multi_particle(params):
    """Convert multi-particle params to `SRWLMagFldU` and `SRWLMagFldC`

    Adds to params.

    Args:
        params (dict): RT values in canonical form

    Returns:
        pkcollections.OrderedMapping: returns its argument (params)
    """
    res = pkcollections.OrderedMapping()
    harmB = srwlib.SRWLMagFldH()
    harmB.n = params['harmonic_num']
    harmB.B = params['magnetic_field']
    if params['orientation'] == 'VERTICAL':
        harmB.h_or_v = 'v'
    else:
        harmB.h_or_v = 'h'
    res.und = srwlib.SRWLMagFldU([harmB])
    res.und.per = params['period_len']
    res.und.nPer = params['num_periods']
    res.magFldCnt = srwlib.SRWLMagFldC(
        [res.und],
        pkarray.new_double([0]),
        pkarray.new_double([0]),
        pkarray.new_double([0]),
    )
    return res


def to_undulator_single_particle(params):
    """Convert single particle params to `SRWLMagFldU` and `SRWLMagFldC`

    Adds to params.

    Args:
        params (dict): RT values in canonical form

    Returns:
        pkcollections.OrderedMapping: returns its argument (params)
    """
    res = pkcollections.OrderedMapping()
    res.und = srwlib.SRWLMagFldU(
        [
            srwlib.SRWLMagFldH(
                1,
                'v',
                params['vertical_magnetic_field'],
                params['vertical_phase'],
                params['vertical_symmetry'],
                1,
            ),
            srwlib.SRWLMagFldH(
                1,
                'h',
                params['horizontal_magnetic_field'],
                params['horizontal_phase'],
                params['horizontal_symmetry'],
                1,
            ),
        ],
        params['period_len'],
        params['num_periods'],
    )
    res.magFldCnt = srwlib.SRWLMagFldC(
        [res.und],
        pkarray.new_double([params['horizontal_coord']]),
        pkarray.new_double([params['vertical_coord']]),
        pkarray.new_double([params['longitudinal_coord']]),
    )
    return res

def to_dipoles(params):
    """Convert  params to `SRWLMagFldM` and `SRWLMagFldC`

    Adds to params.

    Args:
        params (dict): RT values in canonical form

    Returns:
        pkcollections.OrderedMapping: returns its argument (params)
    """
    res = pkcollections.OrderedMapping()

    b0 = params['magnet_one']
    b1 = params['magnet_two']
    bend0 = srwlib.SRWLMagFldM(_G=b0['field'], _m=1, _n_or_s=sn(b0['nors']), _Leff=b0['l'], _Ledge=b0['l_edge'])
    bend1 = srwlib.SRWLMagFldM(_G=b1['field'],_m=1,_n_or_s=sn(b1['nors']),_Leff=b1['l'],_Ledge=b1['l_edge'])
    drift0 = srwlib.SRWLMagFldM(_G=0,_m=1,_n_or_s='n',_Leff=params['drift']['l'])
    arZero = array('d', [0]*3)
    arZc = array('d', [-b0['l']/2-params['drift']['l']/2, 0, b1['l']/2+params['drift']['l']/2])
    res.magFldCnt = srwlib.SRWLMagFldC([bend0, drift0, bend1], arZero, arZero, arZc)
    return res
    
def to_multipole(params):
    """Convert  params to `SRWLMagFldM` and `SRWLMagFldC`

    Adds to params.

    Args:
        params (dict): RT values in canonical form

    Returns:
        pkcollections.OrderedMapping: returns its argument (params)
    """
    res = pkcollections.OrderedMapping()
    
    arZero = array('d', [0]*1)
    arZc = array('d', [params['l']])
    m = srwlib.SRWLMagFldM(_G=params['field'],_m=params['morder'],_n_or_s=sn(params['nors']),_Leff=params['l'],_Ledge=params['l_edge'])
    res.magFldCnt = srwlib.SRWLMagFldC([m], arZero, arZero, arZc)
    
    return res
    

def to_wavefront_multi_particle(params):
    """Convert params to SRWLStokes Wavefront valuesa

    Args:
        params (dict): RT values in canonical form

    Returns:
        SRWLStokes: converted values
    """
    return _to_wavefront(params, srwlib.SRWLStokes())


def to_wavefront_single_particle(params):
    """Convert params to SRWLStokes Wavefront valuesa

    Args:
        params (dict): RT values in canonical form

    Returns:
        SRWLStokes: converted values
    """
    return _to_wavefront(params, srwlib.SRWLWfr())

def sn(x):
    if x: return 'n'
    else: return 's'
        
def _fix_type_value(v):
    if isinstance(v, bool):
        return int(v)
    if hasattr(v, 'value'):
        return v.value
    return v


def _precision(params, labels):
    return [_fix_type_value(params[k]) for k in labels]


def _to_wavefront(params, obj):
    obj.mesh.ne= params['num_points_energy']             
    obj.mesh.nx=params['num_points_x']
    obj.mesh.ny=params['num_points_y']
    obj.allocate(
        params['num_points_energy'],
        params['num_points_x'],
        params['num_points_y'],
    )
    obj.mesh.zStart = params['distance_to_window']
    obj.mesh.eStart = params['initial_photon_energy']
    obj.mesh.eFin = params['final_photon_energy']
    obj.mesh.xStart = params['window_left_edge']
    obj.mesh.xFin = params['window_right_edge']
    obj.mesh.yStart = params['window_top_edge']
    obj.mesh.yFin = params['window_bottom_edge']

    return obj
