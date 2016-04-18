# -*- coding: utf-8 -*-
"""Creates SRW pane, and runs SRW simulation

:copyright: Copyright (c) 2013-2016 RadiaBeam Technologies LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function

import numpy as np

from pykern import pkarray
from pykern import pkcompat

from pykern import pkcollections
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
from radtrack.util.plotTools import scatConPlot

class Base(rt_controller.Controller):
    """Implements contol flow for SRW multiparticle tab"""

    ACTION_NAMES = ('Precision', 'Beam', 'Analyze', 'Simulate')


    FILE_PREFIX = 'srw'

    def init(self, parent_widget=None):
        self._static_widgets = []
        self.complexity_widget = parent_widget.complexity_widget
        decl = rt_params.declarations(self.FILE_PREFIX)
        self.defaults = rt_params.defaults(self.FILE_PREFIX, decl['root'])
        self.params = rt_params.init_params(self.defaults)
        self._view = srw_pane.View(self, parent_widget)
        self.complexity_widget.stateChanged.connect(self.toggle_complexity)
        self._view.plot.canvas.fig.set_facecolor('w')
        return self._view

    def action_analyze(self):
        self.params['source'] = self._view.get_source_params()
        for k in 'wavefront', 'simulation_kind', 'polarization', 'intensity','radiation_source':
            self.params[k] = self._view.get_global_param(k)
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
        self.params['source'] = self._view.get_source_params()
        for k in 'wavefront', 'simulation_kind', 'polarization', 'intensity','radiation_source':
            self.params[k] = self._view.get_global_param(k)

        res = self.simulate(msg)
        msg('Plotting the results')
        self._view.plot.canvas.ax.clear()
        for plot in res.plots:
            dataXLimits = plot[-2]
            dataX = np.linspace(dataXLimits[0], dataXLimits[1], dataXLimits[2])
            xLabel = plot[-1][0]

            dataY = np.array(plot[0][0:dataXLimits[2]])
            yLabel = plot[-1][1]

            title = plot[-1][2]

            scatConPlot('line', 'linear', dataX, dataY, self._view.plot.canvas.ax)
            self._view.plot.canvas.ax.set_xlabel(xLabel)
            self._view.plot.canvas.ax.set_ylabel(yLabel)
            self._view.plot.canvas.ax.set_title(title)
            self._view.plot.canvas.fig.tight_layout()
            self._view.plot.canvas.draw()

    def action_undulator(self):
        self._pop_up('undulator')

    def decl_is_visible(self, decl):
        r = decl.required
        if self.is_single_particle():
            if not 'srw_single' in r:
                return False
        elif not 'srw_multi' in r:
            return False
        return True

    def is_single_particle(self):
        return self.complexity_widget.isChecked()

    def name_to_action(self, name):
        """Returns button action"""
        return getattr(self, 'action_' + name.lower())

    def register_static_widget(self, widget):
        if widget not in self._static_widgets:
            self._static_widgets.append(widget)

    def simulate(self, msg_callback):
        if self.is_single_particle():
            return srw_single_particle.simulate(self.params, msg_callback)
        return srw_multi_particle.simulate(self.params, msg_callback)

    def toggle_complexity(self):
        for w in self._static_widgets:
            w.update_visibility()

    def _pop_up(self, which):
        if which in ['beam']:
            fromtab=True
        else:
            fromtab=False
        pu = rt_popup.Window(
            self.defaults[which],
            self.params[which],
            controller=self,
            parent=self._view,
        )
        if pu.exec_():
            self.params[which] = pu.get_params()
