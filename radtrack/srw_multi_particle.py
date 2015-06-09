# -*- coding: utf-8 -*-
u"""Multiparticle SRW panel

:copyright: Copyright (c) 2013-2015 RadiaBeam Technologies LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import array
import copy
import math
import os
import re
import sys

from radtrack.rt_pyqt4 import QtCore, QtGui, call_if_main, fromUtf8

from pykern import pkarray
from pykern.pkdebug import pkdc, pkdi, pkdp
import jinja2
import xlrd

from radtrack import RbUtility
from radtrack import rt_params
from radtrack import rt_popup
from radtrack import srw_enums
from radtrack.rtsrwlib import srwlib, uti_plot
from radtrack.srw import AnalyticCalc
from radtrack.ui import newsrw
from radtrack.util import resource

from radtrack.rtsrwlib import srwlib, uti_plot

FILE_PREFIX = 'srw'

class Popup(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = newsrw.Ui_Form()
        self.ui.setupUi(self, is_multi_particle=True)
        # TODO(robnagler) necessary?
        self.declarations = rt_params.declarations(FILE_PREFIX)
        self.params = rt_params.init_params(
            rt_params.defaults(FILE_PREFIX)['Simulation Complexity']['MULTI_PARTICLE'],
            self.declarations,
        )
        self.wavefront_display_params()
        self.ui.undulator.clicked.connect(lambda: self.pop_up('Undulator'))
        self.ui.beam.clicked.connect(lambda: self.pop_up('Beam'))
        self.ui.precision.clicked.connect(lambda: self.pop_up('Precision'))
        self.ui.deparg.currentIndexChanged.connect(self.wavefront_display_params)
        self.ui.sim.clicked.connect(self.simulate)
        self.ui.analyze.clicked.connect(self.analytic_calculations)
        self.ui.analytic.setText('Click Analyze to calculate')
        self.ui.status.setText('Initialized')

    def analytic_calculations(self):
        args = copy.deepcopy(self.params['Undulator'])
        if args['Undulator Orientation'].has_name('VERTICAL'):
            args['Horizontal Magnetic Field'] = 0
            args['Vertical Magnetic Field'] = args['Magnetic Field']
        else:
            args['Horizontal Magnetic Field'] = args['Magnetic Field']
            args['Vertical Magnetic Field'] = 0
        args.update(self.params['Beam'])
        res = AnalyticCalc.multi_particle(args)
        template = '''
            Kx: {{ Kx|f }}
            Ky: {{ Ky|f }}
            Wavelength (m)      Phot. energy (eV)
            1st harmonic: {{ lam_rn|e }}   {{ e_phn|e }}
            3rd harmonic: {{ lam_rn_3|e }}   {{ e_phn_3|e }}
            5th harmonic: {{ lam_rn_5|e }}  {{ e_phn_5|e }}
            Critical energy: {{ E_c|e }} eV
            -----------------------------------
            Rad spot size: {{ RadSpotSize|e }} m
            Rad divergence: {{ RadSpotDivergence|e }} rad
            -----------------------------------
            Length of ID: {{ L_id|f }} m
            Radiated power: {{ P_W|e }} W
            Central Power Density:
            {{ P_Wdc|e }} W/mrad2
            Spectral flux:
            {{ SpectralFluxValue|e }} phot/(sec mrad 0.1% BW)
            Spectral Central Brightness:
            {{ RadBrightness|e }} phot/(sec mrad2 0.1% BW)
            -----------------------------------'''
        template = re.sub(r'^\s+', '', template, flags=re.MULTILINE)
        je = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        je.filters['e'] = lambda v: '{:.3e}'.format(v)
        je.filters['f'] = lambda v: '{:.3f}'.format(v)
        jt = je.from_string(template)
        self.ui.analytic.setText(jt.render(res))

    def beam_inputs(self):
        p = self.params['Beam']
        res = srwlib.SRWLPartBeam()
        res.Iavg = p['Average Current']
        m = res.partStatMom1
        m.x = p['Initial Horizontal Coordinate']
        m.y = p['Initial Vertical Coordinate']
        m.z = p['Initial Longitudinal Coordinate']
        m.xp = p['Initial Horizontal Angle']
        m.yp = p['Initial Vertical Angle']
        m.gamma = p['Relativistic Energy (gamma)']
        res.arStatMom2[0] = p['RMS Horizontal Width'] ** 2
        res.arStatMom2[1] = 0
        res.arStatMom2[2] = p['RMS Horizontal Divergence'] ** 2
        res.arStatMom2[3] = p['RMS Vertical Width'] ** 2
        res.arStatMom2[4] = 0
        res.arStatMom2[5] = p['RMS Vertical Divergence'] ** 2
        res.arStatMom2[10] = p['RMS Energy Spread'] ** 2
        return res

    def ar_prec_f(self):
        return self._ar_prec((
            'Initial Harmonic',
            'Final Harmonic',
            'Longitudinal Integration Precision',
            'Azimuthal Integration Precision',
            'Flux Calculation',
        ))

    def ar_prec_p(self):
        return self._ar_prec((
            'Precision Factor',
            'Density Computation Method',
            'Initial Longitudinal Position',
            'Initial Azimuthal Position',
            'Number of Points along Trajectory',
        ))

    def _ar_prec(self, labels):
        p = self.params['Precision']
        return [_fix_enum_value(p[k]) for k in labels]

    def undulator_inputs(self):
        harmB = srwlib.SRWLMagFldH()
        p = self.params['Undulator']
        harmB.n = p['Harmonic Number']
        if p['Undulator Orientation'].has_name('VERTICAL'):
            harmB.B = p['Magnetic Field']
            harmB.h_or_v = 'v'
        else:
            harmB.B = p['Magnetic Field']
            harmB.h_or_v = 'h'
        und = srwlib.SRWLMagFldU([harmB])
        und.per = p['Period Length']
        und.nPer = p['Number of Periods']
        magFldCnt = srwlib.SRWLMagFldC(
            [und],
            pkarray.new_double([0]),
            pkarray.new_double([0]),
            pkarray.new_double([0]),
        )
        return (und, magFldCnt)

    def wavefront_params(self):
        simulation_kind = srw_enums.SimulationKind(self.ui.deparg.currentIndex())
        return (
            self.params['Simulation Kind'][simulation_kind.name]['Wavefront'],
            simulation_kind,
        )

    def wavefront_inputs(self, p):
        res = srwlib.SRWLStokes()
        res.allocate(
            p['Number of points along Energy'],
            p['Number of points along X'],
            p['Number of points along Y'],
        )
        res.mesh.zStart = p['Distance to Window']
        res.mesh.eStart = p['Initial Photon Energy']
        res.mesh.eFin = p['Final Photon Energy']
        res.mesh.xStart = p['Window Left Edge']
        res.mesh.xFin = p['Window Right Edge']
        res.mesh.yStart = p['Window Top Edge']
        res.mesh.yFin = p['Window Bottom Edge']
        return res

    def wavefront_display_params(self):
        p = self.wavefront_params()[0]
        for i, d in enumerate(
            rt_params.iter_primary_param_declarations(self.declarations['Wavefront'])):
            item = self.ui.tableWidget.verticalHeaderItem(i)
            self.ui.tableWidget.setItem(
                i,
                0,
                QtGui.QTableWidgetItem(str(p[item.text()])),
            )


    def pop_up(self, which):
        p = rt_popup.Window(
            self.declarations[which],
            self.params[which],
            file_prefix=FILE_PREFIX,
            parent=self,
        )
        if p.exec_():
            self.params[which] = p.get_params()

    def simulate(self):
        (und, magFldCnt) = self.undulator_inputs()
        beam = self.beam_inputs()
        (wp, simulation_kind) = self.wavefront_params()
        stkF = self.wavefront_inputs(wp)
        stkP = self.wavefront_inputs(wp)
        pkdc('simulation_kind={}', simulation_kind)
        if simulation_kind.has_name('E'):
            #after setting the text call self.ui.status.repaint() to have it immediately show otherwise it will wait till it exits the block to draw
            str1='* Performing Electric Field (spectrum vs photon energy) calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()
            pkdc('ar_prec_f={}', self.ar_prec_f())
            srwlib.srwl.CalcStokesUR(stkF, beam, und, self.ar_prec_f())
            #pkdp('stkF.arS={}', stkF.arS)

            str2='* Extracting Intensity from calculated Electric Field ... \n \n'
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()

            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            uti_plot.uti_plot1d(stkF.arS, [stkF.mesh.eStart, stkF.mesh.eFin, stkF.mesh.ne], ['Photon Energy [eV]', 'Flux [ph/s/.1%bw]', 'Flux through Finite Aperture'])
        elif simulation_kind.has_name('X'):
            str1='* Performing Power Density calculation (from field) vs x-coordinate calculation ... \n \n'
            self.ui.status.setText(str1)
            pkdc('simulation_kind={}', simulation_kind)
            pkdc('stkP={}', stkP)
            pkdc('beam={}', beam)
            pkdc('und={}', und)
            srwlib.srwl.CalcPowDenSR(stkP, beam, 0, magFldCnt, self.ar_prec_p())

            str2='* Extracting Intensity from calculated Electric Field ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()

            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            plotMeshX = [1000*stkP.mesh.xStart, 1000*stkP.mesh.xFin, stkP.mesh.nx]
            powDenVsX = pkarray.new_float([0]*stkP.mesh.nx)
            for i in range(stkP.mesh.nx): powDenVsX[i] = stkP.arS[stkP.mesh.nx*int(stkP.mesh.ny*0.5) + i]
            pkdc('plotMeshX={}', plotMeshX)
            uti_plot.uti_plot1d(powDenVsX, plotMeshX, ['Horizontal Position [mm]', 'Power Density [W/mm^2]', 'Power Density\n(horizontal cut at y = 0)'])
        elif simulation_kind.has_name('Y'):
            str1='* Performing Power Density calculation (from field) vs x-coordinate calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()
            pkdc('simulation_kind={}', simulation_kind)
            pkdc('stkP={}', stkP)
            pkdc('beam={}', beam)
            pkdc('und={}', und)
            srwlib.srwl.CalcPowDenSR(stkP, beam, 0, magFldCnt, self.ar_prec_p())

            str2='* Extracting Intensity from calculated Electric Field ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()

            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            plotMeshY = [1000*stkP.mesh.yStart, 1000*stkP.mesh.yFin, stkP.mesh.ny]
            powDenVsY = pkarray.new_float([0]*stkP.mesh.ny)
#            for i in range(stkP.mesh.ny): powDenVsY[i] = stkP.arS[int(stkP.mesh.nx*0.5) + i*stkP.mesh.ny]
            for i in range(stkP.mesh.ny): powDenVsY[i] = stkP.arS[stkP.mesh.ny*int(stkP.mesh.nx*0.5) + i]
            uti_plot.uti_plot1d(powDenVsY, plotMeshY, ['Vertical Position [mm]', 'Power Density [W/mm^2]', 'Power Density\n(vertical cut at x = 0)'])
        elif simulation_kind.has_name('X_AND_Y'):
            str1='* Performing Electric Field (intensity vs x- and y-coordinate) calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()
            srwlib.srwl.CalcPowDenSR(stkP, beam, 0, magFldCnt, self.ar_prec_p())

            str2='* Extracting Intensity from calculated Electric Field ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()

            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            plotMeshX = [1000*stkP.mesh.xStart, 1000*stkP.mesh.xFin, stkP.mesh.nx]
            plotMeshY = [1000*stkP.mesh.yStart, 1000*stkP.mesh.yFin, stkP.mesh.ny]
            uti_plot.uti_plot2d(stkP.arS, plotMeshX, plotMeshY, ['Horizontal Position [mm]', 'Vertical Position [mm]', 'Power Density'])
        else:
            raise AssertionError('{}: invalid simulation_kind'.format(simulation_kind))
        uti_plot.uti_plot_show()

def _fix_enum_value(v):
    return v.value if hasattr(v, 'value') else v


call_if_main(Popup)
