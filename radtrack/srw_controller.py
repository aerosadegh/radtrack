# -*- coding: utf-8 -*-
"""Multiparticle SRW Pane

:copyright: Copyright (c) 2013-2015 RadiaBeam Technologies LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function

from pykern import pkarray
from pykern import pkcompat
from pykern.pkdebug import pkdc, pkdp

from radtrack import rt_controller
from radtrack import rt_jinja
from radtrack import rt_params
from radtrack import rt_popup
from radtrack import srw_pane
from radtrack import srw_params
from radtrack import srw_multi_particle
from radtrack import srw_single_particle
from radtrack.srw import AnalyticCalc

# Must be last, because srw_params initializes srwlib and uti_plot
import uti_plot


class Base(rt_controller.Controller):
    """Implements contol flow for SRW multiparticle tab"""

    ACTION_NAMES = ('Precision', 'Beam', 'Analyze', 'Simulate')


    FILE_PREFIX = 'srw'

    def init(self, parent_widget=None):
        decl = rt_params.declarations(self.FILE_PREFIX)
        self.defaults = rt_params.defaults(
            self.FILE_PREFIX + '_' + self.SRW_MODE,
            decl['simulation_complexity'][self.SRW_MODE + '_particle'])
        self.params = rt_params.init_params(self.defaults)
        self._view = srw_pane.View(self, parent_widget)
        return self._view

    def action_analyze(self):
        values = AnalyticCalc.compute_all(self.params)
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

    def action_simulate(self):
        msg_list = []
        def msg(m):
            msg_list.append(m + '... \n \n')
            self._view.set_result_text('simulation', ''.join(msg_list))
        self.params['wavefront'] = self._view.get_wavefront_params()
        for k in 'wavefront', 'simulation_kind', 'polarization', 'intensity':
            self.params[k] = self._view.get_global_param(k)
        res = self.simulate(msg)
        msg('Plotting the results')
        for plot in res.plots:
            plot[0](*plot[1:])
        msg('NOTE: Close all graph windows to proceed')
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
            file_prefix=self.FILE_PREFIX,
            parent=self._view,
        )
        if pu.exec_():
            self.params[which] = pu.get_params()


class MultiParticle(Base):

    SRW_MODE = 'multi'

    def simulate(self, msg_callback):
        return srw_multi_particle.simulate(self.params, msg_callback)


class SingleParticle(Base):

    SRW_MODE = 'single'

    def simulate(self, msg_callback):
        return srw_single_particle.simulate(self.params, msg_callback)
