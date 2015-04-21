"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

"""

import sys, os
import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui, QtCore
from ui.newsrw import Ui_Form as Ui_newsrw
from ui.undulatorforthicksrw import Ui_Dialog as und_dlg
from ui.beamforsrw import Ui_Dialog as beam_dlg
from ui.precisionthicksrw import Ui_Dialog as prec_dlg
from srw.uti_plot import *
from srw.AnalyticCalc import *
from srw.srwlib import *
from xlrd import *
import radtrack.util.resource as resource
from RbUtility import *

class rbsrw(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_newsrw()
        self.ui.setupUi(self)
        self.up = UP()
        self.beam = SRWLPartBeam()
        #self.precis = Precis()
        self.arPrecF = [0]*5
        self.arPrecP = [0]*5 
        #load initial values from excel
        self.workbook = open_workbook(resource.filename('SRWinitialvalues.xls'))
        self.thick(self.ui.deparg.currentIndex())
        #disable/remove broken simulation argument
        self.ui.deparg.removeItem(6)
        self.ui.deparg.removeItem(5)
        self.ui.deparg.removeItem(4)
        #set srw initial values
        column = self.workbook.sheet_by_name('thick undulator').col(0)
        units = self.workbook.sheet_by_name('thick undulator').col(1)
        units = self.unitstr(units)
        self.GetUndParams(DialogU(self,units,column))
        column = self.workbook.sheet_by_name('thick beam').col(0)
        units = self.workbook.sheet_by_name('thick beam').col(1)
        units = self.unitstr(units)
        self.GetBeamParams(DialogB(self,units,column))
        column = self.workbook.sheet_by_name('thick precision').col(0)
        units = self.workbook.sheet_by_name('thick precision').col(1)
        print column
        units = self.unitstr(units)
        self.GetPrecision(DialogP(self,units,column))
        
        #connections
        self.ui.undulator.clicked.connect(self.makeund)
        self.ui.beam.clicked.connect(self.makebeam)
        self.ui.precision.clicked.connect(self.setprec)
        self.ui.deparg.currentIndexChanged.connect(self.thick)
        self.ui.sim.clicked.connect(self.srwbuttonThick)
        self.ui.plot.clicked.connect(self.check)
        #indicators
        self.ui.status.setText('Initiated')
        self.ui.analytic.setText('No calculations performed...Yet')
        
    def AnalyticA(self):
#        (Kx,Ky,lam_rn,e_phn)=IDWaveLengthPhotonEnergy(self.up.undPer,self.up.Bx,self.up.By,self.beam.partStatMom1.gamma)
        (Kx,Ky,lam_rn,e_phn)=IDWaveLengthPhotonEnergy(self.up.undPer,0,self.up.By,self.beam.partStatMom1.gamma)
        #Outputs: (UP.Kx=0.934*UP.By*UP.undPer, UP.K, RAD.ephn, UP.WorU)=
        #1. derived Kx from UP.By and UP.undPer
        #2. Introduced new class RAD.ephn = radiation class, variable phot energy of nth harmonics
        #3. UP.WorU=flag indicating wiggler or undulator situation
        #Inputs: (harmB.n, UP.undPer, UP.Bx, UP.By, self.beam.partStatMom1.gamma)
        stri='# Ky:'+'{:.3f}'.format(Kx)+\
        ' # Kx:'+'{:.3f}'.format(Ky)+'\n'+\
        '# Wavelength, m           Phot. energy, eV'+'\n'+\
        '1st harmonic '+'{:.3e}'.format(lam_rn)+' '+'{:.3f}'.format(e_phn)+'\n'+\
        '3rd harmonic '+'{:.3e}'.format(lam_rn/3.0)+' '+'{:.3f}'.format(e_phn*3.0)+'\n'+\
        '5th harmonic '+'{:.3e}'.format(lam_rn/5.0)+' '+'{:.3f}'.format(e_phn*5.0)+'\n' 
        
        E_c=CriticalEnergyWiggler(self.up.By,self.beam.partStatMom1.gamma)
        #Outputs: (RAD.Ecrit,UPWorU) where RAD.Ecrit is critical energy of Wiggler Radiation
        #Inputs: (UP.Bx, self.beam.partStatMom1.gamma,UP.Kx)
        stra=stri+'# Critical energy:'+'{:.3e}'.format(E_c)+', eV'+'\n'+\
        '-----------------------------------'+'\n'
        
        (P_W, L_id)=RadiatedPowerPlanarWiggler(self.up.undPer,self.up.By,self.up.numPer,self.beam.partStatMom1.gamma,self.beam.Iavg)
        #Outputs: (RAD.PowW,UP.L) where RAD.PowW is radiated power of Wiggler Radiation, UP.L=length of ID
        #Inputs: (UP.undPer,UP.Bx,UP.numPer,self.beam.partStatMom1.gamma,self.beam.Iavg) standart SRW class variables
        #RadiatedPowerPlanarWiggler(lam_u,Bx,N_u,Gam,I_b):
        
        (RadSpotSize,RadSpotDivergence)=UndulatorSourceSizeDivergence(lam_rn,L_id)
        stre=stra+'# Rad spot size: '+'{:.3e}'.format(RadSpotSize)+', m'+'\n'
        strf=stre+'# Rad divergence: '+'{:.3e}'.format(RadSpotDivergence)+', rad'+'\n'+\
        '-----------------------------------'+'\n'
        
        strb=strf+'# Length of ID:'+'{:.3f}'.format(L_id)+', m'+'\n' + \
        '# Radiated power:'+'{:.3e}'.format(P_W)+', W'+'\n'
        
        P_Wdc=CentralPowerDensityPlanarWiggler(self.up.By,self.up.numPer,self.beam.partStatMom1.gamma,self.beam.Iavg)
        #Outputs: (RAD.PowCPD) where RAD.PowCPD is radiated central cone power density of Wiggler Radiation
        #Inputs: (UP.undPer,UP.Bx,UP.numPer,self.beam.partStatMom1.gamma,self.beam.Iavg) standart SRW class variables
        strc=strb+'# Central Power Density: '+'{:.3e}'.format(P_Wdc)+', W/mrad2'+'\n'
        
        SpectralFluxValue=SpectralFLux(self.up.numPer,self.beam.partStatMom1.gamma,1,self.beam.Iavg,Kx)
        strd=strc+'# Spectral flux: '+'{:.3e}'.format(SpectralFluxValue)+', phot/(sec mrad 0.1% BW)'+'\n'
        
        RadBrightness=SpectralCenBrightness(self.up.numPer,self.beam.partStatMom1.gamma,self.beam.Iavg)
        strw=strd+'# Spectral Central Brightness: '+'{:.3e}'.format(RadBrightness)+', phot/(sec mrad2 0.1% BW)'+'\n'+\
        '-----------------------------------'+'\n'
        
        self.ui.analytic.setText(strw)
        
    def UndParamsThick(self):
        #vertical harmonic magnetic field
        harmB = SRWLMagFldH() #magnetic field harmonic
        harmB.n = self.up.n #harmonic number
        if self.up.By is None:
            harmB.B = self.up.Bx #magnetic field amplitude [T] 
            harmB.h_or_v = 'h'   #magnetic field plane: horzontal ('h')
        else:
            harmB.B = self.up.By #magnetic field amplitude[T]
            harmB.h_or_v = 'v'   #magnetic field plane: vertical ('v')
        
        und = SRWLMagFldU([harmB])
        und.per = self.up.undPer #period length [m]
        und.nPer = self.up.numPer #number of periods (will be rounded to integer)
        magFldCnt = SRWLMagFldC([und], array('d', [0]), array('d', [0]), array('d', [0])) #Container of all magnetic field elements
        return (und, magFldCnt) 
        
    def GetUndParams(self, dialog):
        units = dialog.u
        self.up.numPer = convertUnitsStringToNumber(dialog.ui.numper.text(),units[0])
        self.up.undPer = convertUnitsStringToNumber(dialog.ui.undper.text(),units[1])
        self.up.n = int(float(dialog.ui.n.text()))

        if dialog.ui.vh.isChecked():
            self.up.By = convertUnitsStringToNumber(dialog.ui.b.text(),units[2])
            self.up.Bx = 0
        else:
            self.up.Bx = convertUnitsStringToNumber(dialog.ui.b.text(),units[2])
            self.up.By = 0

        
    def ShowUndParams(self, dialog):
        units = dialog.u
        dialog.ui.numper.setText(displayWithUnitsNumber(self.up.numPer,units[0]))
        dialog.ui.undper.setText(displayWithUnitsNumber(self.up.undPer,units[1]))
        if self.up.By is 0:
            dialog.ui.b.setText(displayWithUnitsNumber(self.up.Bx,units[2]))
            dialog.ui.vh.setChecked(False)
        else:
            dialog.ui.b.setText(displayWithUnitsNumber(self.up.By,units[2]))
            dialog.ui.vh.setChecked(True)
        dialog.ui.n.setText(str(self.up.n))   
        
    def GetBeamParams(self,dialog):
        units = dialog.u
        #this is the beam class
        self.beam.Iavg = convertUnitsStringToNumber(dialog.ui.iavg.text(),units[0])
        self.beam.partStatMom1.x = convertUnitsStringToNumber(dialog.ui.partstatmom1x.text(),units[1])
        self.beam.partStatMom1.y = convertUnitsStringToNumber(dialog.ui.partstatmom1y.text(),units[2])
        self.beam.partStatMom1.z = convertUnitsStringToNumber(dialog.ui.partstatmom1z.text(),units[3])
        self.beam.partStatMom1.xp = convertUnitsStringToNumber(dialog.ui.partstatmom1xp.text(),units[4])
        self.beam.partStatMom1.yp = convertUnitsStringToNumber(dialog.ui.partstatmom1yp.text(),units[5]) 
        self.beam.partStatMom1.gamma = convertUnitsStringToNumber(dialog.ui.partstatmom1gamma.text(),units[6])
        '''
        sigEperE = 0.00089 #relative RMS energy spread
        sigX = 33.33e-06 #horizontal RMS size of e-beam [m]
        sigXp = 16.5e-06 #horizontal RMS angular divergence [rad]
        sigY = 2.912e-06 #vertical RMS size of e-beam [m]
        sigYp = 2.7472e-06 #vertical RMS angular divergence [rad]
        '''
        sigEperE = convertUnitsStringToNumber(dialog.ui.sige.text(),units[7])
        sigX = convertUnitsStringToNumber(dialog.ui.sigx.text(),units[8])
        sigXp = convertUnitsStringToNumber(dialog.ui.sigxp.text(),units[9])
        sigY = convertUnitsStringToNumber(dialog.ui.sigy.text(),units[10])
        sigYp = convertUnitsStringToNumber(dialog.ui.sigyp.text(),units[11])
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
        dialog.ui.iavg.setText(displayWithUnitsNumber(self.beam.Iavg,units[0]))
        dialog.ui.partstatmom1x.setText(displayWithUnitsNumber(self.beam.partStatMom1.x,units[1]))
        dialog.ui.partstatmom1y.setText(displayWithUnitsNumber(self.beam.partStatMom1.y,units[2]))
        dialog.ui.partstatmom1z.setText(displayWithUnitsNumber(self.beam.partStatMom1.z,units[3]))
        dialog.ui.partstatmom1xp.setText(displayWithUnitsNumber(self.beam.partStatMom1.xp,units[4]))
        dialog.ui.partstatmom1yp.setText(displayWithUnitsNumber(self.beam.partStatMom1.yp,units[5]))
        dialog.ui.partstatmom1gamma.setText(displayWithUnitsNumber(self.beam.partStatMom1.gamma,units[6]))
        dialog.ui.sige.setText(displayWithUnitsNumber(sqrt(self.beam.arStatMom2[10]),units[7]))
        dialog.ui.sigx.setText(displayWithUnitsNumber(sqrt(self.beam.arStatMom2[0]),units[8]))
        dialog.ui.sigy.setText(displayWithUnitsNumber(sqrt(self.beam.arStatMom2[3]),units[9]))
        dialog.ui.sigxp.setText(displayWithUnitsNumber(sqrt(self.beam.arStatMom2[2]),units[10]))
        dialog.ui.sigyp.setText(displayWithUnitsNumber(sqrt(self.beam.arStatMom2[5]),units[11]))
        
    def WfrSetUpE(self,wfrE):
        #wfrE = SRWLWfr() this is the waveform class
#        Nenergy = float(self.ui.tableWidget.item(0,0).text())#float?
        Nenergy = int(convertUnitsStringToNumber(self.ui.tableWidget.item(0,0).text(),''))
#        Nx = int(self.ui.tableWidget.item(1,0).text())
        Nx = int(convertUnitsStringToNumber(self.ui.tableWidget.item(1,0).text(),''))
#        Ny = int(self.ui.tableWidget.item(2,0).text())
        Ny = int(convertUnitsStringToNumber(self.ui.tableWidget.item(2,0).text(),''))
        wfrE.allocate(Nenergy,Nx,Ny)
        wfrE.mesh.zStart = float(self.ui.tableWidget.item(3,0).text())
        wfrE.mesh.eStart = float(self.ui.tableWidget.item(4,0).text())
        wfrE.mesh.eFin = float(self.ui.tableWidget.item(5,0).text())
        wfrE.mesh.xStart = float(self.ui.tableWidget.item(6,0).text())
        wfrE.mesh.xFin = float(self.ui.tableWidget.item(8,0).text())
        wfrE.mesh.yStart = float(self.ui.tableWidget.item(7,0).text())
        wfrE.mesh.yFin = float(self.ui.tableWidget.item(9,0).text())   
        
    def GetPrecision(self,dialog):
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
        
    def ShowPrecision(self,dialog):
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
        
    def unitstr(self,units):
        for n,u in enumerate(units):
            units[n]=str(u.value)
            
        return units
        
    def makeund(self):
        units = self.workbook.sheet_by_name('thick undulator').col(1)
        units = self.unitstr(units)
        dialog = DialogU(self,units)
        self.ShowUndParams(dialog)
        if dialog.exec_():
            self.GetUndParams(dialog)
            
    def makebeam(self):
        units = self.workbook.sheet_by_name('thick undulator').col(1)
        units = self.unitstr(units)
        dialog = DialogB(self,units)
        self.ShowBeamParams(dialog)
        if dialog.exec_():
            self.GetBeamParams(dialog)
            
    def setprec(self):
        dialog = DialogP()
        self.ShowPrecision(dialog)
        if dialog.exec_():
            self.GetPrecision(dialog)
        
    def srwbuttonThick(self):     
        if 'srwl' not in globals():
            msg = ' !Warning --'
            msg += 'SRW not installed on this system.'
            self.ui.status.setText(msg)
            raise Exception(msg)

        (und,magFldCnt)=self.UndParamsThick()
        
        #self.beam = SRWLPartBeam()
        #self.BeamParams(self.beam)

        #self.AnalyticA(self.beam)
        self.AnalyticA()

        #(self.arPrecF, self.arPrecP)=self.PrecisionThick()     
        
        stkF = SRWLStokes() #for spectrum
        self.WfrSetUpE(stkF)
        stkP = SRWLStokes() #for power density
        self.WfrSetUpE(stkP)
        
        Polar = self.ui.polar.currentIndex()
        Intens = self.ui.intensity.currentIndex()
        DependArg = self.ui.deparg.currentIndex()
        print (Polar, Intens, DependArg)
         
        if DependArg == 0:
            #after setting the text call self.ui.status.repaint() to have it immediately show otherwise it will wait till it exits the block to draw
            str1='* Performing Electric Field (spectrum vs photon energy) calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()
            srwl.CalcStokesUR(stkF, self.beam, und, self.arPrecF) #####
            
            str2='* Extracting Intensity from calculated Electric Field ... \n \n'
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()

            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            uti_plot1d(stkF.arS, [stkF.mesh.eStart, stkF.mesh.eFin, stkF.mesh.ne], ['Photon Energy [eV]', 'Flux [ph/s/.1%bw]', 'Flux through Finite Aperture'])

        elif DependArg == 1: 
            str1='* Performing Power Density calculation (from field) vs x-coordinate calculation ... \n \n'
            self.ui.status.setText(str1)
            print DependArg
            print(stkP)
            print(self.beam)
            print(und)
            print(self.arPrecP)
            srwl.CalcPowDenSR(stkP, self.beam, 0, magFldCnt, self.arPrecP)
            print 'yes'
                
            str2='* Extracting Intensity from calculated Electric Field ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()
            
            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            plotMeshX = [1000*stkP.mesh.xStart, 1000*stkP.mesh.xFin, stkP.mesh.nx]
            powDenVsX = array('f', [0]*stkP.mesh.nx)
            for i in range(stkP.mesh.nx): powDenVsX[i] = stkP.arS[stkP.mesh.nx*int(stkP.mesh.ny*0.5) + i]
            print plotMeshX
            uti_plot1d(powDenVsX, plotMeshX, ['Horizontal Position [mm]', 'Power Density [W/mm^2]', 'Power Density\n(horizontal cut at y = 0)'])


        elif DependArg == 2:
            str1='* Performing Power Density calculation (from field) vs x-coordinate calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()
#            print DependArg
#            print(stkP)
#            print(self.beam)
#            print(und)
#            print(self.arPrecP)
            srwl.CalcPowDenSR(stkP, self.beam, 0, magFldCnt, self.arPrecP)
#            print 'yes'
                
            str2='* Extracting Intensity from calculated Electric Field ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()
            
            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            plotMeshY = [1000*stkP.mesh.yStart, 1000*stkP.mesh.yFin, stkP.mesh.ny]
            powDenVsY = array('f', [0]*stkP.mesh.ny)
#            for i in range(stkP.mesh.ny): powDenVsY[i] = stkP.arS[int(stkP.mesh.nx*0.5) + i*stkP.mesh.ny]
            for i in range(stkP.mesh.ny): powDenVsY[i] = stkP.arS[stkP.mesh.ny*int(stkP.mesh.nx*0.5) + i]
            uti_plot1d(powDenVsY, plotMeshY, ['Vertical Position [mm]', 'Power Density [W/mm^2]', 'Power Density\n(vertical cut at x = 0)'])

        elif DependArg == 3:
            str1='* Performing Electric Field (intensity vs x- and y-coordinate) calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()
            srwl.CalcPowDenSR(stkP, self.beam, 0, magFldCnt, self.arPrecP)

            str2='* Extracting Intensity from calculated Electric Field ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()

            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            plotMeshX = [1000*stkP.mesh.xStart, 1000*stkP.mesh.xFin, stkP.mesh.nx]
            plotMeshY = [1000*stkP.mesh.yStart, 1000*stkP.mesh.yFin, stkP.mesh.ny]
            uti_plot2d(stkP.arS, plotMeshX, plotMeshY, ['Horizontal Position [mm]', 'Vertical Position [mm]', 'Power Density'])

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
            print 'Error'
    
        uti_plot_show()

                     
    def thick(self,i):
        thicksheet = self.workbook.sheet_by_name('thick table')
        for n,c in enumerate(thicksheet.col(i)):
            self.ui.tableWidget.setItem(n,0,QtGui.QTableWidgetItem(str(c.value)))
            
    def unitstr(self,units):
        for n,u in enumerate(units):
            units[n]=str(u.value)
            
        return units
        
    def makeund(self):
        units = self.workbook.sheet_by_name('thick undulator').col(1)
        units = self.unitstr(units)
        dialog = DialogU(self,units)
        self.ShowUndParams(dialog)
        if dialog.exec_():
            self.GetUndParams(dialog)
            
    def makebeam(self):
        units = self.workbook.sheet_by_name('thick beam').col(1)
        units = self.unitstr(units)
        dialog = DialogB(self,units)
        self.ShowBeamParams(dialog)
        if dialog.exec_():
            self.GetBeamParams(dialog)
            
    def setprec(self):
        dialog = DialogP()
        self.ShowPrecision(dialog)
        if dialog.exec_():
            self.GetPrecision(dialog)
            
    def check(self):
        print self.arPrecF
        
        
class DialogU(QtGui.QDialog):
    def __init__(self, parent=None,units=None,column=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = und_dlg()
        self.ui.setupUi(self)
        self.u = units
        if column is not None:
            self.ui.numper.setText(str(column[0].value)+' '+units[0])  #Number of ID Periods (without accounting for terminations)
            self.ui.undper.setText(str(column[1].value)) #Period Length
            self.ui.n.setText(str(column[3].value))
            self.ui.b.setText(str(column[2].value)+' '+units[2])
            self.ui.vh.setChecked(column[4].value is unicode('v'))             
            
                
class DialogB(QtGui.QDialog):
    def __init__(self, parent=None,units=None,column=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = beam_dlg()
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
        self.ui = prec_dlg()
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
        
class UP:
     def __init__(self): 
         UP.numPer = [] 
         UP.undPer = [] 
         UP.Bx = [] 
         UP.By = [] 
         UP.phBx = [] 
         UP.phBy = [] 
         UP.sBx = [] 
         UP.sBy = [] 
         UP.xcID = [] 
         UP.ycID = [] 
         UP.zcID = []
         UP.n = []

class Precis:
     def __init__(self):
        Precis.meth = [] 
        Precis.relPrec = [] 
        Precis.zStartInteg = [] 
        Precis.zEndInteg = [] 
        Precis.npTraj = [] 
        Precis.useTermin = [] 
        Precis.sampFactNxNyForProp = []
        
        
                
def main():
    app = QtGui.QApplication(sys.argv)
    myapp = rbsrw()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

