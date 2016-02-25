# -*- coding: utf-8 -*-
"""
:copyright: Copyright (c) 2013-2015 RadiaBeam Technologies LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function
import subprocess

from pykern import pkarray
from pykern import pkcompat
from pykern.pkdebug import pkdc, pkdp
from PyQt4 import QtCore, QtGui

from radtrack import genesis_pane
from radtrack import genesis_params
from radtrack import rt_controller
from radtrack import rt_jinja
from radtrack import rt_params
from radtrack import rt_popup
from radtrack import rt_enum
from enum import Enum

class Base(rt_controller.Controller):
    """Implements contol flow for Genesis tab"""
    ACTION_NAMES = ('Undulator', 'Beam', 'Radiation', 'Particle_Loading','Mesh','Focusing', 'Time_Dependence',
        'Simulation_Control','Scan','IO_Control','Simulate')

    FILE_PREFIX = 'genesis'

    def init(self, parent_widget=None):
        self.decl = rt_params.declarations(self.FILE_PREFIX)
        self.defaults = rt_params.defaults(self.FILE_PREFIX, self.decl)
        self.params = rt_params.init_params(self.defaults)
        self._view = genesis_pane.View(self, parent_widget)
        self.process = QtCore.QProcess()
        self.process.readyReadStandardOutput.connect(self.newStdInfo)
        self.process.readyReadStandardError.connect(self.newStdError)
        self._in_file = None
        self.msg_list = []
        self.w = {}
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

    def action_io_control(self):
        self._pop_up('io_control')

    def action_simulate(self):
        def msg(m):
            self.msg_list.append(m + '... \n \n')
            self._view.set_result_text('simulation', ''.join(self.msg_list))

        self.w.update(genesis_params.to_beam(self.params.beam))
        self.w.update(genesis_params.to_undulator(self.params.undulator))
        self.w.update(genesis_params.to_radiation(self.params.radiation))
        self.w.update(genesis_params.to_particle_loading(self.params.particle_loading))
        self.w.update(genesis_params.to_mesh(self.params.mesh))
        self.w.update(genesis_params.to_focusing(self.params.focusing))
        self.w.update(genesis_params.to_time(self.params.time_dependence))
        self.w.update(genesis_params.to_sim_control(self.params.simulation_control))
        self.w.update(genesis_params.to_scan(self.params.scan))
        self.w.update(genesis_params.to_io_control(self.params.io_control))

        msg('Writing Genesis IN file')
        with open('genesis_run.in','w') as f:
            f.write(' $newrun \n')
            for i in self.w:
                if isinstance(self.w[i], rt_enum.Enum):
                    f.write(' {}={}\n'.format(i, self.w[i].value))
                elif isinstance(self.w[i], bool):
                    f.write(' '+i+'='+str(int(self.w[i]))+'\n')
                elif isinstance(self.w[i], str) or isinstance(self.w[i],unicode):
                    if not self.w[i]:
                        pass
                    else:
                        f.write(" "+i+"='"+str(self.w[i])+"' \n")
                elif isinstance(self.w[i], list):
                    l = str()
                    for j in self.w[i]:
                        l += str(j)
                        l += ' '
                    f.write(' '+i+'='+l+'\n')
                else:
                    f.write(' '+i+'='+str(self.w[i])+'\n')
            f.write(' $end \n')
        msg('Finished \nRunning Genesis\n')

        '''
        self.process.start('genesis',['genesis_run.in']) # add option so files start with common name
        for output_file in glob.glob('genesis_run.*'):
        	listwidget.addItem(output_file)
        '''

        self.process.start('genesis',['genesis_run.in'])

    def decl_is_visible(self, decl):
        return True

    def iter_default_children(self, defaults):
        res = pkcollections.map_values(defaults)
        return iter(res)

    def newStdInfo(self):
        """Callback with simulation stdout text"""
        newString = str(self.process.readAllStandardOutput())
        self.msg_list.append(newString)
        self._view.set_result_text('simulation', ''.join(self.msg_list))
        self._view._result_text['simulation'].moveCursor(QtGui.QTextCursor.End)

    def newStdError(self):
        """Callback with simulation stderr text"""
        newString = str(self.process.readAllStandardError())
        self.msg_list.append(newString)
        self._view.set_result_text('simulation', ''.join(self.msg_list))
        self._view._result_text['simulation'].moveCursor(QtGui.QTextCursor.End)



    def name_to_action(self, name):
        """Returns button action"""
        return getattr(self, 'action_' + name.lower())

    def register_static_widget(self, widget):
        pass

    def _pop_up(self, which):
        pu = rt_popup.Window(
            self.defaults[which],
            self.params[which],
            file_prefix=self.FILE_PREFIX,
            parent=self._view,
        )
        if pu.exec_():
            self.params[which] = pu.get_params()
            
    def get_in(self,phile):
        def param_update(key,value):
            D=genesis_params.to_genesis()
            for i in self.decl:
                if D[key] in self.decl[i].children:
                    #compares to both rt_enum and Enum unsure of what radtrack enumerated type is so compare to both
                    if self.decl[i][D[key]].py_type in [str,int,float,bool] or isinstance(self.params[i][D[key]],rt_enum.Enum) or isinstance(self.params[i][D[key]],Enum):  
                        self.params[i][D[key]]=self.decl[i][D[key]].py_type(value)
                    elif self.decl[i][D[key]].py_type is list:
                        op_children=value.split()
                        for n,j in enumerate(self.params[i][D[key]]):
                            self.params[i][D[key]][j]=bool(int(op_children[n]))                           
                       
                    
        dollar = 0    
        for line in phile:
            if '$' not in line:
                name,val=line.split('=')
                name = name.strip()
                val = val.strip().strip(',')
                param_update(name,val)
            else:
                dollar+=1
                if dollar == 2:
                    break
