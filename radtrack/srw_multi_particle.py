# -*- coding: utf-8 -*-
"""Multiparticle SRW Pane

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

from pykern import pkarray
from pykern import pkcompat
from pykern.pkdebug import pkdc, pkdp
from radtrack import rt_controller
from radtrack import rt_jinja
from radtrack import rt_params
from radtrack import rt_popup
from radtrack import srw_pane
from radtrack import srw_params
from radtrack import srw_run

import srwlib
import uti_plot
# Initialize so that SRW doesn't generate files
uti_plot.uti_plot_init(backend=uti_plot.DEFAULT_BACKEND, fname_format=None)

from radtrack.srw import AnalyticCalc

FILE_PREFIX = 'srw'

class Controller(rt_controller.Controller):
    """Implements contol flow for SRW multiparticle tab"""

    ACTION_NAMES = ('Precision', 'Undulator', 'Beam', 'Analyze', 'Simulate')

    def init(self, parent_widget=None):
        self.defaults = rt_params.defaults(
            FILE_PREFIX + '_multi',
            rt_params.declarations(FILE_PREFIX)['simulation_complexity']['multi_particle'])
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

        self.params['simulation_kind'] = self._view.get_global_param(
            'simulation_kind')
        self.params['wavefront'] = self._view.get_wavefront_params()
        res = srw_run.simulate_multi_particle(self.params, msg)
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
            file_prefix=FILE_PREFIX,
            parent=self._view,
        )
        if pu.exec_():
            self.params[which] = pu.get_params()


Controller.run_if_main()
