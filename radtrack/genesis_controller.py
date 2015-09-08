# -*- coding: utf-8 -*-
"""
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

class Base(rt_controller.Controller):
    """Implements contol flow for Genesis tab"""
    ACTION_NAMES = ('Undulator', 'Beam', 'Radiation', 'Particle Loading','Mesh','Focusing', 'Time Dependence',
        'Simulation Control','Scan','I/O','Simulate')
    
    FILE_PREFIX = 'genesis'
    
    def init(self, parent_widget=None):
        decl = rt_params.declarations(self.FILE_PREFIX)
        self.defaults = rt_params.defaults(self.FILE_PREFIX, decl)
        self.params = rt_params.init_params(self.defaults)
        self._view = genesis_pane.View(self, parent_widget)
        return self._view
        
    def action_beam(self):
        self._pop_up('beam')
        
    def action_undulator(self):
        self._pop_up('undulator')
        
    def action_radiation(self):
        self._pop_up('radiation')
        
    def action_particle_loading(self):
        self._pop_up('particle_loading')
        
    def action_mesh(self):
        self._pop_up('mesh')
        
    def action_focusing(self):
        self._pop_up('focusing')
        
    def action_time_dependence(self):
        self._pop_up('time_dependence')
        
    def action_simulation_control(self):
        self._pop_up('simulation_control')
        
    def action_scan(self):
        self._pop_up('scan')
        
    def action_IO_control(self):
        self._pop_up('IO_control')
        
    def action_simulate(self):
        pass
        
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
        