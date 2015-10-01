# -*- coding: utf-8 -*-
"""
:copyright: Copyright (c) 2013-2015 RadiaBeam Technologies LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function

from pykern import pkarray
from pykern import pkcompat
from pykern.pkdebug import pkdc, pkdp

from radtrack import genesis_pane
from radtrack import genesis_params
from radtrack import rt_controller
from radtrack import rt_jinja
from radtrack import rt_params
from radtrack import rt_popup
from radtrack import rt_enum

class Base(rt_controller.Controller):
    """Implements contol flow for Genesis tab"""
    ACTION_NAMES = ('Undulator', 'Beam', 'Radiation', 'Particle_Loading','Mesh','Focusing', 'Time_Dependence',
        'Simulation_Control','Scan','IO_Control','Simulate')
    
    FILE_PREFIX = 'genesis'
    
    def init(self, parent_widget=None):
        decl = rt_params.declarations(self.FILE_PREFIX)
        self.defaults = rt_params.defaults(self.FILE_PREFIX, decl)
        self.params = rt_params.init_params(self.defaults)
        self._view = genesis_pane.View(self, parent_widget)
        self.w = {}
        return self._view
        
    def action_beam(self):
        self._pop_up('beam')
        self.w.update(genesis_params.to_beam(self.params.beam))
        
    def action_undulator(self):
        self._pop_up('undulator')
        self.w.update(genesis_params.to_undulator(self.params.undulator))
        
    def action_radiation(self):
        self._pop_up('radiation')
        self.w.update(genesis_params.to_radiation(self.params.radiation))
        
    def action_particle_loading(self):
        self._pop_up('particle_loading')
        self.w.update(genesis_params.to_particle_loading(self.params.particle_loading))
        
    def action_mesh(self):
        self._pop_up('mesh')
        self.w.update(genesis_params.to_mesh(self.params.mesh))
        
    def action_focusing(self):
        self._pop_up('focusing')
        self.w.update(genesis_params.to_focusing(self.params.focusing))
        
    def action_time_dependence(self):
        self._pop_up('time_dependence')
        self.w.update(genesis_params.to_time(self.params.time_dependence))
        
    def action_simulation_control(self):
        self._pop_up('simulation_control')
        self.w.update(genesis_params.to_sim_control(self.params.simulation_control))
        
    def action_scan(self):
        self._pop_up('scan')
        self.w.update(genesis_params.to_scan(self.params.scan))
        
    def action_io_control(self):
        self._pop_up('io_control')
        self.w.update(genesis_params.to_io_control(self.params.io_control))
        
    def action_simulate(self):
        msg_list = []
        def msg(m):
            msg_list.append(m + '... \n \n')
            self._view.set_result_text('simulation', ''.join(msg_list))
            
        msg('Writing Genesis IN file')
        with open('test.in','w') as f:
            f.write('$newrun \n')
            for i in self.w:
                if isinstance(self.w[i], rt_enum.Enum):
                    f.write('{}={}\n'.format(i, self.w[i].value))
                else:
                    f.write(i+'='+str(self.w[i])+'\n')
            f.write('$end')
        '''
        for i in self.w:
            if isinstance(self.w[i], rt_enum.Enum):
                print(self.w[i])
                print('{}={}\n'.format(i, self.w[i].value))'''
        msg('Finished')
        
        
        
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
        