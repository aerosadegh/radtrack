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

from radtrack.rt_pyqt4 import QtCore, QtGui, call_if_main

import jinja2
import xlrd
from pykern.pkdebug import pkdc, pkdi, pkdp

from pykern import pkarray

from radtrack import RbUtility
from radtrack import rt_popup
from radtrack.srw import AnalyticCalc
from radtrack.ui import newsrw
from radtrack.ui import precisionthicksrw
from radtrack.util import resource


from radtrack import rt_params

from radtrack.rtsrwlib import srwlib, uti_plot

FILE_PREFIX = 'srw'

class rbsrw(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = newsrw.Ui_Form()
        self.ui.setupUi(self, is_multi_particle=True)
        self.workbook = xlrd.open_workbook(resource.filename('SRWinitialvalues.xls'))
        # TODO(robnagler) necessary?
        self.thick(self.ui.deparg.currentIndex())
        self.defaults = rt_params.defaults(FILE_PREFIX) \
            ['Simulation Complexity']['MULTI_PARTICLE']
        self.declarations = rt_params.declarations(FILE_PREFIX)
        self._init_params('Undulator')
        self._init_params('Beam')
        self._init_params('Precision')
        self.ui.undulator.clicked.connect(lambda: self.pop_up('Undulator'))
        self.ui.beam.clicked.connect(lambda: self.pop_up('Beam'))
        self.ui.precision.clicked.connect(lambda: self.pop_up('Precision'))
        self.ui.deparg.currentIndexChanged.connect(self.thick)
        self.ui.sim.clicked.connect(self.srwbuttonThick)
        self.ui.analyze.clicked.connect(self.AnalyticA)
        #indicators
        self.ui.status.setText('Initiated')
        self.ui.analytic.setText('No calculations performed...As of Yet')

    def _init_params(self, which):
        """Initialize ``params`` from declarations and defaults.

        widget must have fields `params`, `defaults`, and `declarations`.

        Args:
            widget (QWidget): params, defaults, ec.
            declarations (dict): parameter spec
            defaults (dict): values

        Returns:
            dict: name to value
        """
        if not hasattr(self, 'params'):
            self.params = {}
        res = {}
        dflt = self.defaults[which]
        for i, d in enumerate(self.declarations[which].values()):
            #TODO(robnagler) this should be a list, perhaps (e.g. fields)
            if not isinstance(d, dict):
                continue
            if d['rt_old']:
                res[d['rt_old']] = dflt[d['label']]
        self.params[which] = res


    def AnalyticA(self):
        args = copy.copy(self.params['Undulator'])
        if args['vh'].has_name('VERTICAL'):
            args['Bx'] = 0
            args['By'] = args['b']
        else:
            args['Bx'] = args['b']
            args['By'] = 0
        args['gamma'] = self.params['Beam']['partstatmom1gamma']
        args['Iavg'] = self.params['Beam']['iavg']
        args = AnalyticCalc.MultiParticle(args)
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
        self.ui.analytic.setText(jt.render(args))

    def beam_params(self):
        p = self.params['Beam']
        res = srwlib.SRWLPartBeam()
        res.Iavg = p['iavg']
        res.partStatMom1.x = p['partstatmom1x']
        res.partStatMom1.y = p['partstatmom1y']
        res.partStatMom1.z = p['partstatmom1z']
        res.partStatMom1.xp = p['partstatmom1xp']
        res.partStatMom1.yp = p['partstatmom1yp']
        res.partStatMom1.gamma = p['partstatmom1gamma']
        sigEperE = p['sige']
        sigX = p['sigx']
        sigXp = p['sigxp']
        sigY = p['sigy']
        sigYp = p['sigyp']
        res.arStatMom2[0] = sigX*sigX #<(x-<x>)^2>
        res.arStatMom2[1] = 0 #<(x-<x>)(x'-<x'>)>
        res.arStatMom2[2] = sigXp*sigXp #<(x'-<x'>)^2>
        res.arStatMom2[3] = sigY*sigY #<(y-<y>)^2>
        res.arStatMom2[4] = 0 #<(y-<y>)(y'-<y'>)>
        res.arStatMom2[5] = sigYp*sigYp #<(y'-<y'>)^2>
        res.arStatMom2[10] = sigEperE*sigEperE #<(E-<E>)^2>/<E>^2
        return res

    def ar_prec_f(self):
        return self._ar_prec(('harma', 'harmb', 'lip', 'aip', 'flux'))

    def ar_prec_p(self):
        return self._ar_prec(('prefact', 'field', 'ilp', 'flp', 'np'))

    def _ar_prec(self, short_names):
        p = self.params['Precision']
        return [_fix_enum_value(p[k]) for k in short_names]

    def undulator_params(self):
        #vertical harmonic magnetic field
        harmB = srwlib.SRWLMagFldH() #magnetic field harmonic
        p = self.params['Undulator']
        harmB.n = p['n'] #harmonic number
        # TODO(robnagler) this should be vh
        # TODO(robnagler) compute secondaries in rt_params
        if p['vh'].has_name('VERTICAL'):
            harmB.B = p['b'] #magnetic field amplitude[T]
            harmB.h_or_v = 'v'   #magnetic field plane: vertical ('v')
        else:
            harmB.B = p['b'] #magnetic field amplitude [T]
            harmB.h_or_v = 'h'   #magnetic field plane: horzontal ('h')
        und = srwlib.SRWLMagFldU([harmB])
        und.per = p['undPer'] #period length [m]
        und.nPer = p['numPer'] #number of periods (will be rounded to integer)
        # Container of all magnetic field elements
        magFldCnt = srwlib.SRWLMagFldC(
            [und],
            pkarray.new_double([0]),
            pkarray.new_double([0]),
            pkarray.new_double([0]),
        )
        return (und, magFldCnt)

    def WfrSetUpE(self,wfrE):
        #wfrE = srwlib.SRWLWfr() this is the waveform class
#        Nenergy = float(self.ui.tableWidget.item(0,0).text())#float?
        Nenergy = int(RbUtility.convertUnitsStringToNumber(self.ui.tableWidget.item(0,0).text(),''))
#        Nx = int(self.ui.tableWidget.item(1,0).text())
        Nx = int(RbUtility.convertUnitsStringToNumber(self.ui.tableWidget.item(1,0).text(),''))
#        Ny = int(self.ui.tableWidget.item(2,0).text())
        Ny = int(RbUtility.convertUnitsStringToNumber(self.ui.tableWidget.item(2,0).text(),''))
        wfrE.allocate(Nenergy,Nx,Ny)
        wfrE.mesh.zStart = float(self.ui.tableWidget.item(3,0).text())
        wfrE.mesh.eStart = float(self.ui.tableWidget.item(4,0).text())
        wfrE.mesh.eFin = float(self.ui.tableWidget.item(5,0).text())
        wfrE.mesh.xStart = float(self.ui.tableWidget.item(6,0).text())
        wfrE.mesh.xFin = float(self.ui.tableWidget.item(8,0).text())
        wfrE.mesh.yStart = float(self.ui.tableWidget.item(7,0).text())
        wfrE.mesh.yFin = float(self.ui.tableWidget.item(9,0).text())


    def pop_up(self, which):
        p = rt_popup.Window(
            self.declarations[which],
            self.params[which],
            file_prefix=FILE_PREFIX,
            parent=self,
        )
        if p.exec_():
            self.params[which] = p.get_params()

    def srwbuttonThick(self):
        (und, magFldCnt) = self.undulator_params()
        beam = self.beam_params()
        stkF = srwlib.SRWLStokes() #for spectrum
        self.WfrSetUpE(stkF)
        stkP = srwlib.SRWLStokes() #for power density
        self.WfrSetUpE(stkP)

        DependArg = self.ui.deparg.currentIndex()
        pkdc('DependArg={}', DependArg)

        if DependArg == 0:
            #after setting the text call self.ui.status.repaint() to have it immediately show otherwise it will wait till it exits the block to draw
            str1='* Performing Electric Field (spectrum vs photon energy) calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()
            pkdc('ar_prec_f={}', self.ar_prec_f())
            srwlib.srwl.CalcStokesUR(stkF, beam, und, self.ar_prec_f())

            str2='* Extracting Intensity from calculated Electric Field ... \n \n'
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()

            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            uti_plot.uti_plot1d(stkF.arS, [stkF.mesh.eStart, stkF.mesh.eFin, stkF.mesh.ne], ['Photon Energy [eV]', 'Flux [ph/s/.1%bw]', 'Flux through Finite Aperture'])

        elif DependArg == 1:
            str1='* Performing Power Density calculation (from field) vs x-coordinate calculation ... \n \n'
            self.ui.status.setText(str1)
            pkdc('DependArg={}', DependArg)
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


        elif DependArg == 2:
            str1='* Performing Power Density calculation (from field) vs x-coordinate calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()
            pkdc('DependArg={}', DependArg)
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

        elif DependArg == 3:
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

        elif DependArg == 4:
            str1='* Performing Electric Field (intensity vs energy- and x-coordinate) calculation ... \n \n '
            self.ui.status.setText(str1)
            self.ui.status.repaint()

            str2='* Un der construction ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()

            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()

        elif DependArg == 5:
            str1='* Performing Electric Field (intensity vs energy- and y-coordinate) calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()

            str2='* Un der construction ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()

            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()

        else:
            raise AssertionError('{}: invalid DependArg'.format(DependArg))

        uti_plot.uti_plot_show()


    def thick(self,i):
        thicksheet = self.workbook.sheet_by_name('thick table')
        for n,c in enumerate(thicksheet.col(i)):
            self.ui.tableWidget.setItem(n,0,QtGui.QTableWidgetItem(str(c.value)))

    def unitstr(self,units):
        for n,u in enumerate(units):
            units[n]=str(u.value)

        return units


def _fix_enum_value(v):
    return v.value if hasattr(v, 'value') else v

call_if_main(rbsrw)
