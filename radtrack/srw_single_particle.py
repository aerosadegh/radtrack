# -*- coding: utf-8 -*-
u"""Multiparticle SRW Pane

:copyright: Copyright (c) 2013-2015 RadiaBeam Technologies LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open
import copy
import math
import os
import re
import sys
import numpy as np

from radtrack.rt_qt import QtGui

from pykern import pkarray
from pykern import pkcompat
from pykern.pkdebug import pkdc, pkdp
from radtrack import rt_controller
from radtrack import rt_jinja
from radtrack import rt_params
from radtrack import rt_popup
from radtrack import srw_pane
from radtrack import srw_params

import srwlib
import uti_plot
# Initialize so that SRW doesn't generate files
uti_plot.uti_plot_init(backend=uti_plot.DEFAULT_BACKEND, fname_format=None)

from radtrack.srw import AnalyticCalc

FILE_PREFIX = 'srw'

class Controller(rt_controller.Controller):
    """Implements contol flow for SRW single-particle tab"""

    ACTION_NAMES = ('Precision', 'Undulator', 'Beam', 'Analyze', 'Simulate')

    def init(self, parent_widget=None):
        self.defaults = rt_params.defaults(
            FILE_PREFIX + '_single',
            rt_params.declarations(FILE_PREFIX)['simulation_complexity']['single_particle'])
        self.params = rt_params.init_params(self.defaults)
        self._view = srw_pane.View(self, parent_widget)
        return self._view

    def action_analyze(self):
        args = copy.deepcopy(self.params['undulator'])
        args.update(self.params['beam'])
        values = AnalyticCalc.compute_all(args)
        res = rt_jinja.render(
            '''
            Kx: $Kx
            Ky: $Ky
            Wavelength (m)      Phot. energy (eV)
            1st harmonic: $lam_rn   $e_phn
            3rd harmonic: $lam_rn_3   $e_phn_3
            5th harmonic: $lam_rn_5  $e_phn_5
            Critical energy: $E_c eV
            -----------------------------------
            Rad spot size: $RadSpotSize m
            Rad divergence: $RadSpotDivergence rad
            -----------------------------------
            Length of ID: $L_id m
            Radiated power: $P_W W
            Central Power Density:
            $P_Wdc W/mrad2
            Spectral flux:
            $SpectralFluxValue phot/(sec mrad 0.1% BW)
            Spectral Central Brightness:
            $RadBrightness phot/(sec mrad2 0.1% BW)
            -----------------------------------
            ''',
            values,
        )
        self._view.set_result_text('analysis', res)

    def action_beam(self):
        self._pop_up('beam')

    def action_precision(self):
        self._pop_up('precision')

    def save_results(self,file_name,x_vector,y_array):
	x_vec=[]
	for i in xrange(0,x_vector[2]):
            x_vec.append(x_vector[0]+i*(x_vector[1] - x_vector[0])/(x_vector[2]+1E-6))
	AA=np.vstack((x_vec, y_array))
	np.savetxt(file_name, np.transpose(AA)) #, fmt=("%5.4f","%5.4f","%5.4f"))

    def action_simulate(self):
        msg_list = []

        def msg(m):
            msg_list.append(m + '... \n \n')
            self._view.set_result_text('simulation', ''.join(msg_list))

        (und, magFldCnt) = srw_params.to_undulator_single_particle(
            self.params['undulator'])
        arPrecPar = srw_params.to_precision_single_particle(self.params['precision'])
        wfrE = srw_params.to_wavefront_single_particle(self._view.get_wavefront_params())
        wfrE.partBeam = srw_params.to_beam(self.params['beam'])
        wfrXY = srw_params.to_wavefront_single_particle(self._view.get_wavefront_params())
        wfrXY.partBeam = srw_params.to_beam(self.params['beam'])
        simulation_kind = self._view.get_global_param('simulation_kind')
        Polar = self._view.get_global_param('polarization').value
        Intens = self._view.get_global_param('intensity').value
        skv = simulation_kind.value
        if simulation_kind == 'E':
            msg('Performing Electric Field (spectrum vs photon energy) calculation')
            srwlib.srwl.CalcElecFieldSR(wfrE, 0, magFldCnt, arPrecPar)
            msg('Extracting Intensity from calculated Electric Field')
            arI1 = pkarray.new_float([0]*wfrE.mesh.ne)
            srwlib.srwl.CalcIntFromElecField(arI1, wfrE, Polar, Intens, skv, wfrE.mesh.eStart, 0, 0)
            msg('Plotting the results')
            uti_plot.uti_plot1d(
                arI1,
                [wfrE.mesh.eStart, wfrE.mesh.eFin, wfrE.mesh.ne],
                ['Photon energy, eV','Spectral intensity, ph/s/0.1%BW','Intensity vs photon energy'],
            )
        elif simulation_kind == 'X':
            msg('Performing Electric Field (intensity vs x-coordinate) calculation')
            srwlib.srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
            msg('Extracting Intensity from calculated Electric Field')
            arI1 = pkarray.new_float([0]*wfrXY.mesh.nx)
            srwlib.srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, skv, 0, wfrXY.mesh.xStart, 0)
            msg('Plotting the results')
            uti_plot.uti_plot1d(
                arI1,
                [wfrXY.mesh.xStart, wfrXY.mesh.xFin, wfrXY.mesh.nx],
                ['Horizontal Position [m]','Spectral intensity, ph/s/0.1%BW','Intensity vs x-coordinate'],
            )
        elif simulation_kind == 'Y':
            msg('Performing Electric Field (intensity vs y-coordinate) calculation')
            srwlib.srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
            msg('Extracting Intensity from calculated Electric Field')
            arI1 = pkarray.new_float([0]*wfrXY.mesh.ny)
            srwlib.srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, skv, 0, wfrXY.mesh.yStart, 0)
            msg('Plotting the results')
            uti_plot.uti_plot1d(
                arI1,
                [wfrXY.mesh.yStart, wfrXY.mesh.yFin, wfrXY.mesh.ny],
                ['Vertical Position [m]','Spectral intensity, ph/s/0.1%BW','Intensity vs y-coordinate'],
            )
        elif simulation_kind == 'X_AND_Y':
            msg('Performing Electric Field (intensity vs x- and y-coordinate) calculation')
            srwlib.srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
            msg('Extracting Intensity from calculated Electric Field')
            arI1 = pkarray.new_float([0]*wfrXY.mesh.nx*wfrXY.mesh.ny)
            srwlib.srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, skv, wfrXY.mesh.eStart, wfrXY.mesh.xStart, wfrXY.mesh.yStart)
            msg('Plotting the results')
            uti_plot.uti_plot2d(
                arI1,
                [1*wfrXY.mesh.xStart, 1*wfrXY.mesh.xFin, wfrXY.mesh.nx],
                [1*wfrXY.mesh.yStart, 1*wfrXY.mesh.yFin, wfrXY.mesh.ny],
                ['Horizontal Position [m]', 'Vertical Position [m]', 'Intensity at ' + str(wfrXY.mesh.eStart) + ' eV'])

        elif simulation_kind == 'E_AND_X':
            msg('Performing Electric Field (intensity vs energy- and x-coordinate) calculation')
            srwlib.srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
            msg('* Extracting Intensity from calculated Electric Field')
            arI1 = pkarray.new_float([0]*wfrXY.mesh.ne*wfrXY.mesh.nx)
            srwlib.srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, skv, wfrXY.mesh.eStart, wfrXY.mesh.xStart, wfrXY.mesh.yStart)
            msg('Plotting the results')
            uti_plot.uti_plot2d(
                arI1,
                [1*wfrXY.mesh.eStart, 1*wfrXY.mesh.eFin, wfrXY.mesh.ne],
                [1*wfrXY.mesh.xStart, 1*wfrXY.mesh.xFin, wfrXY.mesh.nx],
                ['Energy [eV]', 'Horizontal Position [m]', 'Intensity integrated from ' + str(wfrXY.mesh.yStart) + ' to ' + str(wfrXY.mesh.yFin) + ' ,m in y-coordinate'])

        elif simulation_kind == 'E_AND_Y':
            msg('Performing Electric Field (intensity vs energy- and y-coordinate) calculation')
            srwlib.srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
            msg('Extracting Intensity from calculated Electric Field')
            arI1 = pkarray.new_float([0]*wfrXY.mesh.ne*wfrXY.mesh.ny)
            srwlib.srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, skv, wfrXY.mesh.eStart, wfrXY.mesh.xStart, wfrXY.mesh.yStart)
            msg('Plotting the results')
            uti_plot.uti_plot2d(
                arI1,
                [1*wfrXY.mesh.eStart, 1*wfrXY.mesh.eFin, wfrXY.mesh.ne],
                [1*wfrXY.mesh.yStart, 1*wfrXY.mesh.yFin, wfrXY.mesh.ny],
                ['Energy [eV]', 'Vertical Position [m]', 'Intensity integrated from ' + str(wfrXY.mesh.xStart) + ' to ' + str(wfrXY.mesh.xFin)+ ' ,m in x-coordinate'])
        else:
            raise AssertionError('{}: invalid simulation_kind'.format(simulation_kind))
        uti_plot.uti_plot_show()

    def action_undulator(self):
        self._pop_up('undulator')

    def name_to_action(self, name):
        """Returns button action"""
        return getattr(self, 'action_' + name.lower())

    def _pop_up(self, which):
        pu = rt_popup.Window(
            self.defaults[which],
            self.params[which],
            file_prefix=FILE_PREFIX,
            parent=self._view,
        )
        if pu.exec_():
            self.params[which] = pu.get_params()

    def _trajectory(self,und,magFldCnt,arPrecPar,fieldInterpMeth,beam):
        # Done specifying undulator mag field
        # Initial coordinates of particle trajectory through the ID
        part = srwlib.SRWLParticle()
        part.x = beam.partStatMom1.x
        part.y = beam.partStatMom1.y
        part.xp = beam.partStatMom1.xp
        part.yp = beam.partStatMom1.yp
        part.gamma = 3/0.51099890221e-03 #Relative Energy self.beam.partStatMom1.gamma #
        part.relE0 = 1
        part.nq = -1
        zcID=0

        # number of trajectory points along longitudinal axis
        npTraj = 10001

        #Definitions and allocation for the Trajectory waveform
        part.z = zcID #- 0.5*magFldCnt.MagFld[0].rz
        partTraj = srwlib.SRWLPrtTrj()
        partTraj.partInitCond = part
        partTraj.allocate(npTraj, True)
        partTraj.ctStart = -0.55*und.nPer*und.per
        partTraj.ctEnd = 0.55*und.nPer*und.per #magFldCnt.MagFld[0].rz
        partTraj = srwlib.srwl.CalcPartTraj(partTraj, magFldCnt, arPrecPar)

        ctMesh = [partTraj.ctStart, partTraj.ctEnd, partTraj.np]
        for i in range(partTraj.np):
            partTraj.arX[i] *= 1000
            partTraj.arY[i] *= 1000
        uti_plot.uti_plot1d(partTraj.arX, ctMesh, ['ct [m]', 'Horizontal Position [mm]'])
        uti_plot.uti_plot1d(partTraj.arY, ctMesh, ['ct [m]', 'Vertical Position [mm]'])
        return (partTraj.arX,partTraj.arY,ctMesh)


Controller.run_if_main()
