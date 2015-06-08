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

from radtrack.rtpyqt4 import QtCore, QtGui, call_if_main

import jinja2
import xlrd
from pykern.pkdebug import pkdc, pkdi, pkdp

from pykern import pkarray

from radtrack import RbUtility
from radtrack import srw_ui_params
from radtrack.srw import AnalyticCalc
from radtrack.ui import beamforsrw
from radtrack.ui import newsrw
from radtrack.ui import precisionthicksrw
from radtrack.ui import undulatorforthicksrw
from radtrack.util import resource

# TODO(robnagler) remove this once all code migrated
from radtrack.rtsrwlib import srwlib, uti_plot
from radtrack import srw_ui_params
from radtrack import srw_params

class rbsrw(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = newsrw.Ui_Form()
        self.ui.setupUi(self, is_multi_particle=True)

        self.beam = srwlib.SRWLPartBeam()

        self.arPrecF = [0]*5
        self.arPrecP = [0]*5

        #load initial values from excel
        self.workbook = xlrd.open_workbook(resource.filename('SRWinitialvalues.xls'))

        # TODO(robnagler) necessary?
        self.thick(self.ui.deparg.currentIndex())

        self.defaults = srw_params.defaults()['Simulation Complexity']['MULTI_PARTICLE']
        self.declarations = srw_params.declarations()
        self.params = {}
        srw_ui_params.init_params(self, 'Undulator')

        column = self.workbook.sheet_by_name('thick beam').col(0)
        units = self.workbook.sheet_by_name('thick beam').col(1)
        units = self.unitstr(units)
        self.GetBeamParams(DialogB(self,units,column))

        column = self.workbook.sheet_by_name('thick precision').col(0)
        units = self.workbook.sheet_by_name('thick precision').col(1)
        pkdc('column={}', column)
        units = self.unitstr(units)
        self.GetPrecision(DialogP(self,units,column))

        #connections
        self.ui.undulator.clicked.connect(self.makeund)
        self.ui.beam.clicked.connect(self.makebeam)
        self.ui.precision.clicked.connect(self.setprec)
        self.ui.deparg.currentIndexChanged.connect(self.thick)
        self.ui.sim.clicked.connect(self.srwbuttonThick)
        self.ui.analyze.clicked.connect(self.AnalyticA)
        #indicators
        self.ui.status.setText('Initiated')
        self.ui.analytic.setText('No calculations performed...As of Yet')

    def AnalyticA(self):
        params = copy.copy(self.params['Undulator'])
        params['gamma'] = self.beam.partStatMom1.gamma
        params['Iavg'] = self.beam.Iavg
        params = AnalyticCalc.MultiParticle(params)
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
        self.ui.analytic.setText(jt.render(params))

    def UndParamsThick(self):
        #vertical harmonic magnetic field
        harmB = srwlib.SRWLMagFldH() #magnetic field harmonic
        p = self.params['Undulator']
        harmB.n = p['n'] #harmonic number
        # TODO(robnagler) this should be vh
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

    def GetUndParams(self, dialog):
        srw_ui_params.from_dialog(self.params, dialog)
        self.compute_secondary_params('Undulator')

    def compute_secondary_params(self, which):
        p = self.params[which]
        if which == 'Undulator':
            # TODO(robnagler) compute secondaries in srw_params
            if p['vh'].has_name('VERTICAL'):
                p['Bx'] = 0
                p['By'] = p['b']
            else:
                p['Bx'] = p['b']
                p['By'] = 0

    def ShowUndParams(self, dialog):
        srw_ui_params.to_dialog(self.params['Undulator'], dialog)

    def GetBeamParams(self, dialog):
        units = dialog.u
        #this is the beam class

        self.beam.Iavg = RbUtility.convertUnitsStringToNumber(dialog.ui.iavg.text(),units[0])
        self.beam.partStatMom1.x = RbUtility.convertUnitsStringToNumber(dialog.ui.partstatmom1x.text(),units[1])
        self.beam.partStatMom1.y = RbUtility.convertUnitsStringToNumber(dialog.ui.partstatmom1y.text(),units[2])
        self.beam.partStatMom1.z = RbUtility.convertUnitsStringToNumber(dialog.ui.partstatmom1z.text(),units[3])
        self.beam.partStatMom1.xp = RbUtility.convertUnitsStringToNumber(dialog.ui.partstatmom1xp.text(),units[4])
        self.beam.partStatMom1.yp = RbUtility.convertUnitsStringToNumber(dialog.ui.partstatmom1yp.text(),units[5])
        self.beam.partStatMom1.gamma = RbUtility.convertUnitsStringToNumber(dialog.ui.partstatmom1gamma.text(),units[6])
        '''
        sigEperE = 0.00089 #relative RMS energy spread
        sigX = 33.33e-06 #horizontal RMS size of e-beam [m]
        sigXp = 16.5e-06 #horizontal RMS angular divergence [rad]
        sigY = 2.912e-06 #vertical RMS size of e-beam [m]
        sigYp = 2.7472e-06 #vertical RMS angular divergence [rad]
        '''
        sigEperE = RbUtility.convertUnitsStringToNumber(dialog.ui.sige.text(),units[7])
        sigX = RbUtility.convertUnitsStringToNumber(dialog.ui.sigx.text(),units[8])
        sigXp = RbUtility.convertUnitsStringToNumber(dialog.ui.sigxp.text(),units[9])
        sigY = RbUtility.convertUnitsStringToNumber(dialog.ui.sigy.text(),units[10])
        sigYp = RbUtility.convertUnitsStringToNumber(dialog.ui.sigyp.text(),units[11])

        #2nd order stat. moments:
        self.beam.arStatMom2[0] = sigX*sigX #<(x-<x>)^2>
        self.beam.arStatMom2[1] = 0 #<(x-<x>)(x'-<x'>)>
        self.beam.arStatMom2[2] = sigXp*sigXp #<(x'-<x'>)^2>
        self.beam.arStatMom2[3] = sigY*sigY #<(y-<y>)^2>
        self.beam.arStatMom2[4] = 0 #<(y-<y>)(y'-<y'>)>
        self.beam.arStatMom2[5] = sigYp*sigYp #<(y'-<y'>)^2>
        self.beam.arStatMom2[10] = sigEperE*sigEperE #<(E-<E>)^2>/<E>^2

    def ShowBeamParams(self, dialog):
        units = dialog.u
        dialog.ui.iavg.setText(RbUtility.displayWithUnitsNumber(self.beam.Iavg,units[0]))
        dialog.ui.partstatmom1x.setText(RbUtility.displayWithUnitsNumber(self.beam.partStatMom1.x,units[1]))
        dialog.ui.partstatmom1y.setText(RbUtility.displayWithUnitsNumber(self.beam.partStatMom1.y,units[2]))
        dialog.ui.partstatmom1z.setText(RbUtility.displayWithUnitsNumber(self.beam.partStatMom1.z,units[3]))
        dialog.ui.partstatmom1xp.setText(RbUtility.displayWithUnitsNumber(self.beam.partStatMom1.xp,units[4]))
        dialog.ui.partstatmom1yp.setText(RbUtility.displayWithUnitsNumber(self.beam.partStatMom1.yp,units[5]))
        dialog.ui.partstatmom1gamma.setText(RbUtility.displayWithUnitsNumber(self.beam.partStatMom1.gamma,units[6]))
        dialog.ui.sige.setText(RbUtility.displayWithUnitsNumber(math.sqrt(self.beam.arStatMom2[10]),units[7]))
        dialog.ui.sigx.setText(RbUtility.displayWithUnitsNumber(math.sqrt(self.beam.arStatMom2[0]),units[8]))
        dialog.ui.sigy.setText(RbUtility.displayWithUnitsNumber(math.sqrt(self.beam.arStatMom2[3]),units[9]))
        dialog.ui.sigxp.setText(RbUtility.displayWithUnitsNumber(math.sqrt(self.beam.arStatMom2[2]),units[10]))
        dialog.ui.sigyp.setText(RbUtility.displayWithUnitsNumber(math.sqrt(self.beam.arStatMom2[5]),units[11]))

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

    def GetPrecision(self, dialog):
        units = dialog.u
        #for spectral flux vs photon energy
        self.arPrecF[0] = float(dialog.ui.harma.text()) #initial UR harmonic to take into account
        self.arPrecF[1] = float(dialog.ui.harmb.text()) #final UR harmonic to take into account
        self.arPrecF[2] = float(dialog.ui.lip.text()) #longitudinal integration precision parameter
        self.arPrecF[3] = float(dialog.ui.aip.text()) #azimuthal integration precision parameter
        self.arPrecF[4] = dialog.ui.flux.currentIndex()+1 #calculate flux (1) or flux per unit surface (2)

        #for power density
        self.arPrecP[0] = float(dialog.ui.prefact.text()) #precision factor
        self.arPrecP[1] = dialog.ui.field.currentIndex()+1 #power density computation method (1- "near field", 2- "far field")
        self.arPrecP[2] = float(dialog.ui.ilp.text()) #initial longitudinal position (effective if self.arPrecP[2] < self.arPrecP[3])
        self.arPrecP[3] = float(dialog.ui.flp.text()) #final longitudinal position (effective if self.arPrecP[2] < self.arPrecP[3])
        self.arPrecP[4] = int(float(dialog.ui.np.text())) #number of points for (intermediate) trajectory calculation
        #return (self.arPrecF, self.arPrecP)

    def ShowPrecision(self, dialog):
        dialog.ui.harma.setText(str(self.arPrecF[0]))
        dialog.ui.harmb.setText(str(self.arPrecF[1]))
        dialog.ui.lip.setText(str(self.arPrecF[2]))
        dialog.ui.aip.setText(str(self.arPrecF[3]))
        dialog.ui.flux.setCurrentIndex(self.arPrecF[4]-1)

        dialog.ui.prefact.setText(str(self.arPrecP[0]))
        dialog.ui.field.setCurrentIndex(self.arPrecP[1]-1)
        dialog.ui.ilp.setText(str(self.arPrecP[2]))
        dialog.ui.flp.setText(str(self.arPrecP[3]))
        dialog.ui.np.setText(str(self.arPrecP[4]))

    def makeund(self):
        dialog = DialogU(self)
        self.ShowUndParams(dialog)
        if dialog.exec_():
            self.GetUndParams(dialog)

    def setprec(self):
        dialog = DialogP()
        self.ShowPrecision(dialog)
        if dialog.exec_():
            self.GetPrecision(dialog)

    def srwbuttonThick(self):
        (und,magFldCnt)=self.UndParamsThick()

        #self.beam = srwlib.SRWLPartBeam()
        #self.BeamParams(self.beam)

        #self.AnalyticA(self.beam)
        #self.AnalyticA()

        #(self.arPrecF, self.arPrecP)=self.PrecisionThick()

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
            srwlib.srwl.CalcStokesUR(stkF, self.beam, und, self.arPrecF) #####

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
            pkdc('beam={}', self.beam)
            pkdc('und={}', und)
            pkdc('arPrecP={}', self.arPrecP)
            srwlib.srwl.CalcPowDenSR(stkP, self.beam, 0, magFldCnt, self.arPrecP)

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
            pkdc('self.beam={}', self.beam)
            pkdc('und={}', und)
            pkdc('self.arPrecP={}', self.arPrecP)
            srwlib.srwl.CalcPowDenSR(stkP, self.beam, 0, magFldCnt, self.arPrecP)

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
            srwlib.srwl.CalcPowDenSR(stkP, self.beam, 0, magFldCnt, self.arPrecP)

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

    def makebeam(self):
        units = self.workbook.sheet_by_name('thick beam').col(1)
        units = self.unitstr(units)
        dialog = DialogB(self,units)
        self.ShowBeamParams(dialog)
        if dialog.exec_():
            self.GetBeamParams(dialog)

class DialogU(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = undulatorforthicksrw.Ui_Dialog()
        self.ui.setupUi(self, parent.declarations['Undulator'])

class DialogB(QtGui.QDialog):
    def __init__(self, parent=None,units=None,column=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = beamforsrw.Ui_Dialog()
        self.ui.setupUi(self)
        self.u = units
        if column is not None:
            self.ui.iavg.setText(str(column[0].value)+' '+units[0])     #Above is the UP class, this is self.beam.iavg
            self.ui.partstatmom1x.setText(str(column[1].value)+' '+units[1])  #self.beam.partStatMom1.x, initial x-offset
            self.ui.partstatmom1y.setText(str(column[2].value)+' '+units[2])  #self.beam.partStatMom1.y, initial y-offset
            self.ui.partstatmom1z.setText(str(column[3].value)+' '+units[3]) #self.beam.partStatMom1.z, initial z-offset
            self.ui.partstatmom1xp.setText(str(column[4].value)+' '+units[4]) #self.beam.partStatMom1.xp, initial x angle offset
            self.ui.partstatmom1yp.setText(str(column[5].value)+' '+units[5]) #self.beam.partStatMom1.yp, initial y angle offset
            self.ui.partstatmom1gamma.setText(str(column[6].value)+' '+units[6]) # electron beam relative energy, gamma
            self.ui.sige.setText(str(column[7].value)+' '+units[7])
            self.ui.sigx.setText(str(column[8].value)+' '+units[8])
            self.ui.sigy.setText(str(column[9].value)+' '+units[9])
            self.ui.sigxp.setText(str(column[10].value)+' '+units[10])
            self.ui.sigyp.setText(str(column[11].value)+' '+units[11])

class DialogP(QtGui.QDialog):
    def __init__(self, parent=None,units=None,column=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = precisionthicksrw.Ui_Dialog()
        self.ui.setupUi(self)
        self.u = units
        if column is not None:
            self.ui.harma.setText(str(column[0].value))
            self.ui.harmb.setText(str(column[1].value))
            self.ui.lip.setText(str(column[2].value))
            self.ui.aip.setText(str(column[3].value))
            self.ui.flux.setCurrentIndex(int(column[4].value))

            self.ui.prefact.setText(str(column[5].value))
            self.ui.field.setCurrentIndex(column[6].value)
            self.ui.ilp.setText(str(column[7].value))
            self.ui.flp.setText(str(column[8].value))
            self.ui.np.setText(str(column[9].value))

call_if_main(rbsrw)
