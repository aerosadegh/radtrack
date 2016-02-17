# -*- coding: utf-8 -*-
#C:\d from old\RadiaBeam\RadSoft\radtrack\tests>py.test ProcessSRWOutput_test.py
u"""PyTest for :mod:`radiasoft.AnalyticCalc`
"""
from __future__ import absolute_import, division, print_function

import os
import numpy as np
import matplotlib.pyplot as plt
import pytest

from scipy.signal import argrelextrema
from pykern.pkdebug import pkdc, pkdp
from pykern import pkunit

from radtrack import rt_params
from radtrack import srw_multi_particle
from radtrack import srw_params
from radtrack import srw_enums
from radtrack.srw import AnalyticCalc


def test_1():
    pkdp(_params('sample').radiation_source.undulator)
    p = srw_multi_particle.simulate(_params('sample'))
    e_p, I_rad = _results(
        [p.stkF.mesh.eStart, p.stkF.mesh.eFin, p.stkF.mesh.ne],
        p.stkF.arS,
    )
    maxI = max(I_rad)
    pkdp('Spectral Amplitude: {:g} ph/s/mrad2', maxI)
    maxima_s = _maxima(I_rad, 3)
    pkdp('maxima: {}', maxima_s)
    z_distance, x_trajectory = _results(
        p.ctMesh,
        p.partTraj.arX,
    )
    minX = min(x_trajectory)
    maxX = max(x_trajectory)
    minZ = min(z_distance)
    maxZ = max(z_distance)
    pkdp('Length of ID: {:g} m', maxZ - minZ)
    pkdp('Oscillation Amplitude: {:g} mm', (maxX - minX)/2)
    L_trajectory = _path_length(z_distance, x_trajectory)
    pkdp('Length of Trajectory: {:g} m', L_trajectory)

    plt.figure()
    plt.plot(e_p, I_rad)
    for i in maxima_s:
	plt.scatter(e_p[i], I_rad[i], color='red')
    plt.grid()
    plt.show()
    plt.clf()
    plt.plot(z_distance,x_trajectory,'.b',linestyle='-')
    maxima_t = _maxima(x_trajectory, 10)
    for i in maxima_t:
	plt.scatter(z_distance[i], x_trajectory[i], color='red')
    plt.grid()
    plt.show()
    plt.clf()

def _maxima(seq, deltI):
    assert seq
    return argrelextrema(np.array(seq), np.greater, order=deltI)[0]


def _params(base_name):
    decl = rt_params.declarations('srw')
    defaults = rt_params.defaults_from_dict(
        pkunit.data_yaml('sample'),
        'srw',
        decl['root'],
    )
    res = rt_params.init_params(defaults)
    res.wavefront = res.simulation_kind.e.wavefront
    res.simulation_kind = srw_enums.SimulationKind.E
    return res


def _path_length(x,y):
    res = 0
    for i in xrange(0, np.shape(x)[0]-1):
        res += np.sqrt((y[i+1]-y[i])**2*1E-6 + (x[i+1]-x[i])**2)
    return res


def _results(x_vector, y_array):
    x_vec = []
    n = x_vector[2]
    factor = (x_vector[1] - x_vector[0])/(n + 1E-6)
    base = x_vector[0]
    x_vec = map(lambda i: base + i * factor, xrange(n))
    return x_vec, y_array[0:n]
