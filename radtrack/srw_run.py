# -*- coding: utf-8 -*-
"""Multiparticle SRW Pane

:copyright: Copyright (c) 2013-2015 RadiaBeam Technologies LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function

import argparse
import numpy as np

from pykern import pkarray
from pykern.pknamespace import Namespace
from pykern.pkdebug import pkdc, pkdp
from radtrack import srw_params

# After import of srw_params which initializes the backend
import srwlib
import uti_plot
# Initialize so that SRW doesn't generate files
uti_plot.uti_plot_init(backend=uti_plot.DEFAULT_BACKEND, fname_format=None)


def simulate_multi_particle(params, msg_callback=None):
    """Run a multi-particle (thick) simulation and return results

    Args:
        params (dict): canonical RT params to be converted by :mod:`srw_params`
        msg_callback (function): Called at various stages to log output

    Returns:
        Namespace: results and params (see code for format)
    """

    if not msg_callback:
        msg_callback = _msg_callback_none
    p = Namespace()
    p.simulation_kind = params['simulation_kind']
    pkdc('simulation_kind={}', p.simulation_kind)
    p.wavefront = params['wavefront']
    p.update(srw_params.to_undulator_multi_particle(params['undulator']))
    p.beam = srw_params.to_beam(params['beam'])
    p.stkF = srw_params.to_wavefront_multi_particle(p.wavefront)
    p.stkP = srw_params.to_wavefront_multi_particle(p.wavefront)
    p.ar_prec_f = srw_params.to_flux_precision(params['precision'])
    p.ar_prec_p = srw_params.to_power_precision(params['precision'])
    p.plots = []

    #for trajectory calculations:

    #Need to reflect in the GUI:
    p.arPrecPar = [1] #General Precision parameters for Trajectory calculation:
    #[0]: integration method No:
    #1- fourth-order Runge-Kutta (precision is driven by number of points)
    #2- fifth-order Runge-Kutta
    #[1],[2],[3],[4],[5]: absolute precision values for X[m],X'[rad],Y[m],Y'[rad],Z[m] (yet to be tested!!) - to be taken into account only for R-K fifth order or higher
    #[6]: tolerance (default = 1) for R-K fifth order or higher
    #[7]: max. number of auto-steps for R-K fifth order or higher (default = 5000)
    p['fieldInterpMeth'] = 4 #Magnetic Field Interpolation Method, to be entered into 3D field structures below (to be used e.g. for trajectory calculation):
    #1- bi-linear (3D), 2- bi-quadratic (3D), 3- bi-cubic (3D), 4- 1D cubic spline (longitudinal) + 2D bi-cubic
    msg_callback('Performing trajectory calculation')
    _trajectory(p)
    if p.simulation_kind == 'E':
        msg_callback('Performing Electric Field (spectrum vs photon energy) calculation')
        pkdc('ar_prec_f={}', p.ar_prec_f)
        msg_callback('Extracting Intensity from calculated Electric Field')
        srwlib.srwl.CalcStokesUR(p.stkF, p.beam, p.und, p.ar_prec_f)
        p.plots.append([
            uti_plot.uti_plot1d,
            p.stkF.arS,
            [p.stkF.mesh.eStart, p.stkF.mesh.eFin, p.stkF.mesh.ne],
            [
                'Photon Energy [eV]',
                'Flux [ph/s/.1%bw]',
                'Flux through Finite Aperture',
            ],
        ])
    elif p.simulation_kind == 'X':
        msg_callback('Performing Power Density calculation (from field) vs x-coordinate calculation')
        pkdc('stkP={}', p.stkP)
        pkdc('beam={}', p.beam)
        pkdc('und={}', p.und)
        srwlib.srwl.CalcPowDenSR(p.stkP, p.beam, 0, p.magFldCnt, p.ar_prec_p)
        msg_callback('Extracting Intensity from calculated Electric Field')
        p.plotMeshX = [1000*p.stkP.mesh.xStart, 1000*p.stkP.mesh.xFin, p.stkP.mesh.nx]
        p.powDenVsX = pkarray.new_float([0]*p.stkP.mesh.nx)
        for i in xrange(p.stkP.mesh.nx):
            powDenVsX[i] = p.stkP.arS[p.stkP.mesh.nx*int(p.stkP.mesh.ny*0.5) + i]
        pkdc('plotMeshX={}', p.plotMeshX)
        p.plots.append([
            uti_plot.uti_plot1d,
            p.powDenVsX,
            p.plotMeshX,
            [
                'Horizontal Position [mm]',
                'Power Density [W/mm^2]',
                'Power Density\n(horizontal cut at y = 0)',
            ],
        ])
    elif p.simulation_kind == 'Y':
        msg_callback('Performing Power Density calculation (from field) vs x-coordinate calculation')
        pkdc('stkP={}', p.stkP)
        pkdc('beam={}', p.beam)
        pkdc('und={}', p.und)
        srwlib.srwl.CalcPowDenSR(p.stkP, p.beam, 0, p.magFldCnt, p.ar_prec_p)
        msg_callback('Extracting Intensity from calculated Electric Field')
        p.plotMeshY = [1000*p.stkP.mesh.yStart, 1000*p.stkP.mesh.yFin, p.stkP.mesh.ny]
        p.powDenVsY = pkarray.new_float([0]*p.stkP.mesh.ny)
        for i in xrange(p.stkP.mesh.ny):
            p.powDenVsY[i] = p.stkP.arS[p.stkP.mesh.ny*int(p.stkP.mesh.nx*0.5) + i]
        p.plots.append([
            uti_plot.uti_plot1d,
            p.powDenVsY,
            p.plotMeshY,
            [
                'Vertical Position [mm]',
                'Power Density [W/mm^2]',
                'Power Density\n(vertical cut at x = 0)',
            ],
        ])
    elif p.simulation_kind == 'X_AND_Y':
        msg_callback('Performing Electric Field (intensity vs x- and y-coordinate) calculation')
        srwlib.srwl.CalcPowDenSR(p.stkP, p.beam, 0, p.magFldCnt, p.ar_prec_p)
        msg_callback('Extracting Intensity from calculated Electric Field')
        p.plotMeshX = [1000*p.stkP.mesh.xStart, 1000*p.stkP.mesh.xFin, p.stkP.mesh.nx]
        p.plotMeshY = [1000*p.stkP.mesh.yStart, 1000*p.stkP.mesh.yFin, p.stkP.mesh.ny]
        p.plots.append([
            uti_plot.uti_plot2d,
            p.stkP.arS,
            p.plotMeshX,
            p.plotMeshY,
            [
                'Horizontal Position [mm]',
                'Vertical Position [mm]',
                'Power Density',
            ],
        ])
    else:
        raise AssertionError('{}: invalid simulation_kind'.format(p.simulation_kind))
    return p


def _trajectory(p):
    # Done specifying undulator mag field
    # Initial coordinates of particle trajectory through the ID
    part = srwlib.SRWLParticle()
    part.x = p.beam.partStatMom1.x
    part.y = p.beam.partStatMom1.y
    part.xp = p.beam.partStatMom1.xp
    part.yp = p.beam.partStatMom1.yp
    part.gamma = 3/0.51099890221e-03 #Relative Energy self.beam.partStatMom1.gamma #
    part.relE0 = 1
    part.nq = -1
    zcID = 0
    # number of trajectory points along longitudinal axis
    npTraj = 10001
    #Definitions and allocation for the Trajectory waveform
    part.z = zcID #- 0.5*magFldCnt.MagFld[0].rz
    p.partTraj = srwlib.SRWLPrtTrj()
    p.partTraj.partInitCond = part
    p.partTraj.allocate(npTraj, True)
    p.partTraj.ctStart = -0.55 * p.und.nPer * p.und.per
    p.partTraj.ctEnd = 0.55 * p.und.nPer * p.und.per #magFldCnt.MagFld[0].rz
    p.partTraj = srwlib.srwl.CalcPartTraj(p.partTraj, p.magFldCnt, p.arPrecPar)
    p.ctMesh = [p.partTraj.ctStart, p.partTraj.ctEnd, p.partTraj.np]
    for i in range(p.partTraj.np):
        p.partTraj.arX[i] *= 1000
        p.partTraj.arY[i] *= 1000
    p.plots.append([
        uti_plot.uti_plot1d,
        p.partTraj.arX, p.ctMesh, ['ct [m]', 'Horizontal Position [mm]'],
    ])
    p.plots.append([
        uti_plot.uti_plot1d,
        p.partTraj.arY, p.ctMesh, ['ct [m]', 'Vertical Position [mm]'],
    ])


def _msg_callback_none(*args):
    pass
