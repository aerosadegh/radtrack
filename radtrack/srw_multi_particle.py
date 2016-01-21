# -*- coding: utf-8 -*-
"""Multiparticle SRW Pane

:copyright: Copyright (c) 2013-2015 RadiaBeam Technologies LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function

from pykern.pkdebug import pkdc, pkdp
from pykern import pkarray
from pykern import pkcollections

from radtrack import srw_params

# Must be after srw_params import
import srwlib
import uti_plot

def simulate(params, msg_callback=lambda _: _):
    """Run a multi-particle (thick) simulation and return results

    Args:
        params (OrderedMapping): configuration parameters
        msg_callback (function): Called at various stages to log output

    Returns:
        OrderedMapping: results and params (see code for format)
    """
    p = pkcollections.OrderedMapping()
    for k in 'simulation_kind', 'wavefront','intensity','polarization':
        v = params[k]
        p[k] = v.value if hasattr(v, 'value') else v
    if params.radiation_source.name.lower() == 'wiggler':
        pkcollections.mapping_merge(
        p, srw_params.to_undulator_multi_particle(params.source))
    elif params.radiation_source.name.lower() == 'dual_dipole':
        pkcollections.mapping_merge(
        p,srw_params.to_dipoles(params.source))
    elif params.radiation_source.name.lower() == 'multipole':
        pkcollections.mapping_merge(
        p,srw_params.to_multipole(params.source))
    
    p.beam = srw_params.to_beam(params.beam)
    p.stkF = srw_params.to_wavefront_multi_particle(p.wavefront) #flux
    p.stkP = srw_params.to_wavefront_multi_particle(p.wavefront) #power
    p.wfrXY = srw_params.to_wavefront_single_particle(p.wavefront)
    p.ar_prec_f = srw_params.to_flux_precision(params.precision)
    p.ar_prec_p = srw_params.to_power_precision(params.precision)
    p.arPrecPar = [2,0.01,-0.1,0.1,8000,1,0] #General Precision parameters for Trajectory calculation:
    p.fieldInterpMeth = 4
    
    p.wfrE = srw_params.to_wavefront_single_particle(p.wavefront)
    p.wfrE.partBeam = srw_params.to_beam(params.beam)
    p.wfrXY = srw_params.to_wavefront_single_particle(p.wavefront)
    p.wfrXY.partBeam = srw_params.to_beam(params.beam)
    
    p.plots = []
    skv = p.simulation_kind
    
    msg_callback('Performing trajectory calculation')
    #if params.radiation_source.name.lower() == 'wiggler': _trajectory(p)
    if params.simulation_kind == 'E':
        msg_callback('Performing Electric Field (spectrum vs photon energy) calculation')
        msg_callback('Extracting Intensity from calculated Electric Field')
        if params.radiation_source == 'wiggler':
            srwlib.srwl.CalcStokesUR(p.stkF, p.beam, p.und, p.ar_prec_f)
        else:
            srwlib.srwl.SRWLStokes()
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
    elif params.simulation_kind == 'X':
        msg_callback('Performing Power Density calculation (from field) vs x-coordinate calculation')
        srwlib.srwl.CalcPowDenSR(p.stkP, p.beam, 0, p.magFldCnt, p.ar_prec_p)
        msg_callback('Extracting Intensity from calculated Electric Field')
        p.plotMeshX = [1000*p.stkP.mesh.xStart, 1000*p.stkP.mesh.xFin, p.stkP.mesh.nx]
        p.powDenVsX = pkarray.new_float([0]*p.stkP.mesh.nx)
        for i in xrange(p.stkP.mesh.nx):
            p.powDenVsX[i] = p.stkP.arS[p.stkP.mesh.nx*int(p.stkP.mesh.ny*0.5) + i]
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
    elif params.simulation_kind == 'Y':
        msg_callback('Performing Power Density calculation (from field) vs x-coordinate calculation')
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
    elif params.simulation_kind == 'X_AND_Y':
        if params.radiation_source.name.lower() == 'wiggler':
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
            msg_callback('Performing Electric Field (intensity vs x- and y-coordinate) calculation')
            srwlib.srwl.CalcElecFieldSR(p.wfrXY,p.beam,p.magFldCnt, p.arPrecPar)
            #'''
            msg_callback('Extracting Intensity from calculated Electric Field')
            p.arI1 = pkarray.new_float([0]*p.wfrXY.mesh.nx*p.wfrXY.mesh.ny)
            srwlib.srwl.CalcIntFromElecField(p.arI1, p.wfrXY, p.polarization, p.intensity, skv, p.wfrXY.mesh.eStart, p.wfrXY.mesh.xStart, p.wfrXY.mesh.yStart)
            p.plots.append([
                uti_plot.uti_plot2d,
                p.arI1,
                [1*p.wfrXY.mesh.xStart, 1*p.wfrXY.mesh.xFin, p.wfrXY.mesh.nx],
                [1*p.wfrXY.mesh.yStart, 1*p.wfrXY.mesh.yFin, p.wfrXY.mesh.ny],
                ['Horizontal Position [m]', 'Vertical Position [m]', 'Intensity at ' + str(p.wfrXY.mesh.eStart) + ' eV'],
            ])#'''
        
    else:
        raise AssertionError('{}: invalid simulation_kind'.format(params.simulation_kind))
    return p

def _trajectory(p):
    # Done specifying undulator mag field
    # Initial coordinates of particle trajectory through the ID
    part = srwlib.SRWLParticle()
    part.x = p.beam.partStatMom1.x
    part.y = p.beam.partStatMom1.y
    part.xp = p.beam.partStatMom1.xp
    part.yp = p.beam.partStatMom1.yp
    part.gamma = 3/0.51099890221e-03 #Relative Energy beam.partStatMom1.gamma #
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
    
def _trajectorys(p):
    # Done specifying undulator mag field
    # Initial coordinates of particle trajectory through the ID
    part = srwlib.SRWLParticle()
    part.x = p.beam.partStatMom1.x
    part.y = p.beam.partStatMom1.y
    part.xp = p.beam.partStatMom1.xp
    part.yp = p.beam.partStatMom1.yp
    part.gamma = p.beam.partStatMom1.gamma #3/0.51099890221e-03 #Relative Energy beam.partStatMom1.gamma 
    part.relE0 = 1
    part.nq = -1
    #zcID = 0
    # number of trajectory points along longitudinal axis
    npTraj = 1000
    #Definitions and allocation for the Trajectory waveform
    part.z = 0 #zcID #- 0.5*magFldCnt.MagFld[0].rz
    p.partTraj = srwlib.SRWLPrtTrj()
    p.partTraj.partInitCond = part
    p.partTraj.allocate(npTraj, True)
    p.partTraj.ctStart = -0.1 #-0.55 * p.und.nPer * p.und.per
    p.partTraj.ctEnd = 0.1    #0.55 * p.und.nPer * p.und.per #magFldCnt.MagFld[0].rz
    p.partTraj = srwlib.srwl.CalcPartTraj(p.partTraj, p.magFldCnt, p.arPrecPar)
    p.ctMesh = [p.partTraj.ctStart, p.partTraj.ctEnd, p.partTraj.np]
    
    uti_plot.uti_plot1d(p.partTraj.arX, p.ctMesh, ['ct [m]', 'Horizontal Position [m]'])
    #uti_plot.uti_plot1d(p.partTraj.arY, p.ctMesh, ['ct [m]', 'Vertical Position [m]'])
    uti_plot.uti_plot1d(p.partTraj.arXp, p.ctMesh, ['ct [m]', 'Horizontal angle [rad]'])
    uti_plot.uti_plot_show()    
