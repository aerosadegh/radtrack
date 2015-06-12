"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

"""

import sys, os
from numpy import sqrt
import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui, QtCore
from ui.newsrw import Ui_Form as Ui_newsrw
from ui.undulatorforthinsrw import Ui_Dialog as und_dlg
from ui.beamforthinsrw import Ui_Dialog as beam_dlg
from ui.precisionofsrw import Ui_Dialog as prec_dlg
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
        self.precis = Precis()
        #load initial values from excel
        self.workbook = open_workbook(resource.filename('SRWinitialvalues.xls'))
        self.thin(self.ui.deparg.currentIndex())
        #set srw initial values 
        column = self.workbook.sheet_by_name('thin undulator').col(0)
        units = self.workbook.sheet_by_name('thin undulator').col(1)
        units =self.unitstr(units)
        self.GetUndParams(DialogU(self,units,column))
        column = self.workbook.sheet_by_name('thin beam').col(0)
        units = self.workbook.sheet_by_name('thin beam').col(1)
        units =self.unitstr(units)
        self.GetBeamParams(DialogB(self,units,column))
        column = self.workbook.sheet_by_name('thin precision').col(0)
        units = self.workbook.sheet_by_name('thin precision').col(1)
        units =self.unitstr(units)
        self.GetPrecision(DialogP(self,units,column))
        #removed exy option
        self.ui.deparg.removeItem(6)
        
        #connections
        self.ui.undulator.clicked.connect(self.makeund)
        self.ui.beam.clicked.connect(self.makebeam)
        self.ui.precision.clicked.connect(self.setprec)
        self.ui.deparg.currentIndexChanged.connect(self.thin)
        self.ui.sim.clicked.connect(self.srwbuttonThin)
        self.ui.analyze.clicked.connect(self.AnalyticA)
        #indicators
        self.ui.status.setText('Initiated')
        self.ui.analytic.setText('No calculations performed...As of Yet')
        
        
    def AnalyticA(self):
        (Kx,Ky,lam_rn,e_phn)=IDWaveLengthPhotonEnergy(self.up.undPer,self.up.Bx,self.up.By,self.beam.partStatMom1.gamma)
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
        
        E_c=CriticalEnergyWiggler(self.up.By,self.up.Bx,self.beam.partStatMom1.gamma)
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
        
    def GetUndParams(self, dialog):
        units = dialog.u
        self.up.numPer = convertUnitsStringToNumber(dialog.ui.numper.text(),units[0])
        self.up.undPer = convertUnitsStringToNumber(dialog.ui.undper.text(),units[1])
        self.up.Bx = convertUnitsStringToNumber(dialog.ui.bx.text(),units[2])
        self.up.By = convertUnitsStringToNumber(dialog.ui.by.text(),units[3])
        self.up.phBx = convertUnitsStringToNumber(dialog.ui.phbx.text(),units[4])
        self.up.phBy = convertUnitsStringToNumber(dialog.ui.phby.text(),units[5])
        self.up.sBx = convertUnitsStringToNumber(dialog.ui.sbx.text(),units[6])
        self.up.sBy = convertUnitsStringToNumber(dialog.ui.sby.text(),units[7])
        self.up.xcID = convertUnitsStringToNumber(dialog.ui.xcid.text(),units[8])
        self.up.ycID = convertUnitsStringToNumber(dialog.ui.ycid.text(),units[9])
        self.up.zcID = convertUnitsStringToNumber(dialog.ui.zcid.text(),units[10])
        
    def ShowUndParams(self, dialog):
        units = dialog.u
        dialog.ui.numper.setText(displayWithUnitsNumber(self.up.numPer,units[0]))
        dialog.ui.undper.setText(displayWithUnitsNumber(self.up.undPer,units[1]))
        dialog.ui.bx.setText(displayWithUnitsNumber(self.up.Bx,units[2]))
        dialog.ui.by.setText(displayWithUnitsNumber(self.up.By,units[3]))
        dialog.ui.phbx.setText(displayWithUnitsNumber(self.up.phBx,units[4]))
        dialog.ui.phby.setText(displayWithUnitsNumber(self.up.phBy,units[5]))
        dialog.ui.sbx.setText(displayWithUnitsNumber(self.up.sBx,units[6]))
        dialog.ui.sby.setText(displayWithUnitsNumber(self.up.sBy,units[7]))
        dialog.ui.xcid.setText(displayWithUnitsNumber(self.up.xcID,units[8]))
        dialog.ui.ycid.setText(displayWithUnitsNumber(self.up.ycID,units[9]))
        dialog.ui.zcid.setText(displayWithUnitsNumber(self.up.zcID,units[10]))
        
        
    def GetBeamParams(self,dialog):
        units = dialog.u
#        (P_W, L_id)=RadiatedPowerPlanarWiggler(self.up.undPer,self.up.By,self.up.numPer,self.beam.partStatMom1.gamma,self.beam.Iavg)
#        self.beam.partStatMom1.z=-L_id
        self.beam.Iavg = convertUnitsStringToNumber(dialog.ui.iavg.text(),units[0])
        self.beam.partStatMom1.x = convertUnitsStringToNumber(dialog.ui.partstatmom1x.text(),units[1])
        self.beam.partStatMom1.y = convertUnitsStringToNumber(dialog.ui.partstatmom1y.text(),units[2])
        self.beam.partStatMom1.z = convertUnitsStringToNumber(dialog.ui.partstatmom1z.text(),units[3])
        self.beam.partStatMom1.xp = convertUnitsStringToNumber(dialog.ui.partstatmom1xp.text(),units[4])
        self.beam.partStatMom1.yp = convertUnitsStringToNumber(dialog.ui.partstatmom1yp.text(),units[5]) 
        self.beam.partStatMom1.gamma = convertUnitsStringToNumber(dialog.ui.partstatmom1gamma.text(),units[6])

        
    def ShowBeamParams(self, dialog):
        units = dialog.u
        dialog.ui.iavg.setText(displayWithUnitsNumber(self.beam.Iavg,units[0]))
        dialog.ui.partstatmom1x.setText(displayWithUnitsNumber(self.beam.partStatMom1.x,units[1]))
        dialog.ui.partstatmom1y.setText(displayWithUnitsNumber(self.beam.partStatMom1.y,units[2]))
        dialog.ui.partstatmom1z.setText(displayWithUnitsNumber(self.beam.partStatMom1.z,units[3]))
        dialog.ui.partstatmom1xp.setText(displayWithUnitsNumber(self.beam.partStatMom1.xp,units[4]))
        dialog.ui.partstatmom1yp.setText(displayWithUnitsNumber(self.beam.partStatMom1.yp,units[5]))
        dialog.ui.partstatmom1gamma.setText(displayWithUnitsNumber(self.beam.partStatMom1.gamma,units[6]))
        
    def WfrSetUpE(self,wfrE):
        #wfrE = SRWLWfr() this is the waveform class
        Nenergy = int(float(self.ui.tableWidget.item(0,0).text()))#float?
        Nx = int(float(self.ui.tableWidget.item(1,0).text()))
        Ny = int(float(self.ui.tableWidget.item(2,0).text()))
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
        self.precis.meth = dialog.ui.meth.currentIndex()
        self.precis.relPrec = convertUnitsStringToNumber(dialog.ui.relprec.text(),units[1])
        self.precis.zStartInteg = convertUnitsStringToNumber(dialog.ui.zstartint.text(),units[2])
        self.precis.zEndInteg = convertUnitsStringToNumber(dialog.ui.zendint.text(),units[3])
        self.precis.npTraj = convertUnitsStringToNumber(dialog.ui.nptraj.text(),units[4])
        self.precis.useTermin = dialog.ui.usetermin.currentIndex()
        self.precis.sampFactNxNyForProp = convertUnitsStringToNumber(dialog.ui.sampfactnxny.text(),units[6])
        
    def ShowPrecision(self,dialog):
        units = dialog.u
        dialog.ui.meth.setCurrentIndex(self.precis.meth)
        dialog.ui.relprec.setText(displayWithUnitsNumber(self.precis.relPrec,units[1]))
        dialog.ui.zstartint.setText(displayWithUnitsNumber(self.precis.zStartInteg,units[2]))
        dialog.ui.zendint.setText(displayWithUnitsNumber(self.precis.zEndInteg,units[3]))
        dialog.ui.nptraj.setText(displayWithUnitsNumber(self.precis.npTraj,units[4]))
        dialog.ui.usetermin.setCurrentIndex(self.precis.useTermin)
        dialog.ui.sampfactnxny.setText(displayWithUnitsNumber(self.precis.sampFactNxNyForProp,units[6]))
    
         
    def srwbuttonThin(self):
        if 'srwl' not in globals():
            msg = ' !Warning --'
            msg += 'SRW not installed on this system.'
            self.ui.status.setText(msg)
            raise Exception(msg)
        #UP = self.UndParams()
        und = SRWLMagFldU([SRWLMagFldH(1, 'v', self.up.By, self.up.phBy, self.up.sBy, 1), SRWLMagFldH(1, 'h', self.up.Bx, self.up.phBx, self.up.sBx, 1)], self.up.undPer, self.up.numPer)
        magFldCnt = SRWLMagFldC([und], array('d', [self.up.xcID]), array('d', [self.up.ycID]), array('d', [self.up.zcID]))
        #elecBeam = SRWLPartBeam()
        #self.BeamParams(elecBeam)

        #self.AnalyticA()

        #precis = self.Precision()
        arPrecPar = [self.precis.meth, self.precis.relPrec, self.precis.zStartInteg, self.precis.zEndInteg, self.precis.npTraj, self.precis.useTermin, self.precis.sampFactNxNyForProp]

        wfrE = SRWLWfr()
        self.WfrSetUpE(wfrE)
        wfrE.partBeam = self.beam

        wfrXY = SRWLWfr()
        self.WfrSetUpE(wfrXY)
        wfrXY.partBeam = self.beam
        
        mesh=deepcopy(wfrE.mesh)
        wfrIn=deepcopy(wfrE)

        Polar = self.ui.polar.currentIndex()
        Intens = self.ui.intensity.currentIndex()
        DependArg = self.ui.deparg.currentIndex()
#       print (Polar, Intens, DependArg)
      
        if DependArg == 0:
            #after setting the text call self.ui.status.repaint() to have it immediately show otherwise it will wait till it exits the block to draw
            str1='* Performing Electric Field (spectrum vs photon energy) calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()
            srwl.CalcElecFieldSR(wfrE, 0, magFldCnt, arPrecPar)
            str2='* Extracting Intensity from calculated Electric Field ... \n \n'
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()
            arI1 = array('f',[0]*wfrE.mesh.ne)
            srwl.CalcIntFromElecField(arI1, wfrE, Polar, Intens, DependArg, wfrE.mesh.eStart, 0, 0)
            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            #time.sleep(1)
            self.ui.status.repaint()
            uti_plot1d(arI1, [wfrE.mesh.eStart, wfrE.mesh.eFin, wfrE.mesh.ne],
            ['Photon energy, eV','Spectral intensity, ph/s/0.1%BW','Intensity vs photon energy'])

        elif DependArg == 1:
            str1='* Performing Electric Field (intensity vs x-coordinate) calculation ... \n \n'
            self.ui.status.setText(str1)
            srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
            str2='* Extracting Intensity from calculated Electric Field ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()
            arI1 = array('f',[0]*wfrXY.mesh.nx)
            srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, 0, wfrXY.mesh.xStart, 0)
            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            uti_plot1d(arI1, [wfrXY.mesh.xStart, wfrXY.mesh.xFin, wfrXY.mesh.nx],
            ['Horizontal Position [m]','Spectral intensity, ph/s/0.1%BW','Intensity vs x-coordinate'])

        elif DependArg == 2:
            str1='* Performing Electric Field (intensity vs y-coordinate) calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()
            srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
            str2='* Extracting Intensity from calculated Electric Field ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()
            arI1 = array('f',[0]*wfrXY.mesh.ny)
            srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, 0, wfrXY.mesh.yStart, 0)
            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            uti_plot1d(arI1, [wfrXY.mesh.yStart, wfrXY.mesh.yFin, wfrXY.mesh.ny],
            ['Vertical Position [m]','Spectral intensity, ph/s/0.1%BW','Intensity vs y-coordinate'])
       
        elif DependArg == 3:
            str1='* Performing Electric Field (intensity vs x- and y-coordinate) calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()
            srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
            str2='* Extracting Intensity from calculated Electric Field ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()
            arI1 = array('f', [0]*wfrXY.mesh.nx*wfrXY.mesh.ny)
            srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, wfrXY.mesh.eStart, wfrXY.mesh.xStart, wfrXY.mesh.yStart)
            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            uti_plot2d(arI1, [1*wfrXY.mesh.xStart, 1*wfrXY.mesh.xFin, wfrXY.mesh.nx], 
            [1*wfrXY.mesh.yStart, 1*wfrXY.mesh.yFin, wfrXY.mesh.ny], 
            ['Horizontal Position [m]', 'Vertical Position [m]', 'Intensity at ' + str(wfrXY.mesh.eStart) + ' eV'])

        elif DependArg == 4:
            str1='* Performing Electric Field (intensity vs energy- and x-coordinate) calculation ... \n \n '
            self.ui.status.setText(str1)
            self.ui.status.repaint()
            srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
            str2='* Extracting Intensity from calculated Electric Field ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()
            arI1 = array('f', [0]*wfrXY.mesh.ne*wfrXY.mesh.nx)
            srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, wfrXY.mesh.eStart, wfrXY.mesh.xStart, wfrXY.mesh.yStart)
            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            uti_plot2d(arI1, [1*wfrXY.mesh.eStart, 1*wfrXY.mesh.eFin, wfrXY.mesh.ne], 
            [1*wfrXY.mesh.xStart, 1*wfrXY.mesh.xFin, wfrXY.mesh.nx], 
            ['Energy [eV]', 'Horizontal Position [m]', 'Intensity integrated from ' + str(wfrXY.mesh.yStart) + ' to ' + str(wfrXY.mesh.yFin) + ' ,m in y-coordinate'])

        elif DependArg == 5:
            str1='* Performing Electric Field (intensity vs energy- and y-coordinate) calculation ... \n \n'
            self.ui.status.setText(str1)
            self.ui.status.repaint()
            srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
            str2='* Extracting Intensity from calculated Electric Field ... \n \n '
            self.ui.status.setText(str1+str2)
            self.ui.status.repaint()
            arI1 = array('f', [0]*wfrXY.mesh.ne*wfrXY.mesh.ny)
            srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, wfrXY.mesh.eStart, wfrXY.mesh.xStart, wfrXY.mesh.yStart)
            str3='* Plotting the results ...\n'
            self.ui.status.setText(str1+str2+str3)
            self.ui.status.repaint()
            uti_plot2d(arI1, [1*wfrXY.mesh.eStart, 1*wfrXY.mesh.eFin, wfrXY.mesh.ne], 
            [1*wfrXY.mesh.yStart, 1*wfrXY.mesh.yFin, wfrXY.mesh.ny], 
            ['Energy [eV]', 'Vertical Position [m]', 'Intensity integrated from ' + str(wfrXY.mesh.xStart) + ' to ' + str(wfrXY.mesh.xFin)+ ' ,m in x-coordinate'])
        else:
            print 'Error'
    
        uti_plot_show()
          
    def thin(self,i):
        thinsheet = self.workbook.sheet_by_name('thin table')
            
        for n,c in enumerate(thinsheet.col(i)):
            self.ui.tableWidget.setItem(n,0,QtGui.QTableWidgetItem(str(c.value)))
            
    def unitstr(self,units):
        for n,u in enumerate(units):
            units[n]=str(u.value)
            
        return units
        
    def makeund(self):
        units = self.workbook.sheet_by_name('thin undulator').col(1)
        units = self.unitstr(units)
        dialog = DialogU(self,units)
        self.ShowUndParams(dialog)
        if dialog.exec_():
            self.GetUndParams(dialog)
            
    def makebeam(self):
        units = self.workbook.sheet_by_name('thin beam').col(1)
        units = self.unitstr(units)
        dialog = DialogB(self,units)
        self.ShowBeamParams(dialog)
        if dialog.exec_():
            self.GetBeamParams(dialog)
            
    def setprec(self):
        units = self.workbook.sheet_by_name('thin precision').col(1)
        units = self.unitstr(units)
        dialog = DialogP(self,units)
        self.ShowPrecision(dialog)
        if dialog.exec_():
            self.GetPrecision(dialog)
        
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
        
        
class DialogU(QtGui.QDialog):
    def __init__(self, parent=None,units=None,column=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = und_dlg()
        self.ui.setupUi(self)
        self.u = units
        if column is not None:
            self.ui.numper.setText(str(column[0].value)+' '+units[0])  #Number of ID Periods (without accounting for terminations)
            self.ui.undper.setText(str(column[1].value)+' '+units[1]) #Period Length
            self.ui.bx.setText(str(column[2].value)+' '+units[2])       #Peak Vertical field
            self.ui.by.setText(str(column[3].value)+' '+units[3])      #Peak Horizontal field
            self.ui.phbx.setText(str(column[4].value)+' '+units[4])       #Initial Phase of the Horizontal field component
            self.ui.phby.setText(str(column[5].value)+' '+units[5])       #Initial Phase of the Vertical field component
            self.ui.sbx.setText(str(column[6].value)+' '+units[6])       #Symmetry of the Horizontal field component vs Longitudinal position
            self.ui.sby.setText(str(column[7].value)+' '+units[7])        #Symmetry of the Vertical field component vs Longitudinal position
            self.ui.xcid.setText(str(column[8].value)+' '+units[8])       #Misaligment. Horizontal Coordinate of Undulator Center 
            self.ui.ycid.setText(str(column[9].value)+' '+units[9])       #Misaligment. Vertical Coordinate of Undulator Center 
            self.ui.zcid.setText(str(column[10].value)+' '+units[10])      #Misaligment. Longitudinal Coordinate of Undulator Center
                
class DialogB(QtGui.QDialog):
    def __init__(self, parent=None, units = None, column=None):
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

class DialogP(QtGui.QDialog):
    def __init__(self, parent=None, units=None,column=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = prec_dlg()
        self.ui.setupUi(self)
        self.u = units
        if column is not None:
            self.ui.meth.setCurrentIndex(int(column[0].value)) #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
            self.ui.relprec.setText(str(column[1].value)+' '+units[1]) #relative precision
            self.ui.zstartint.setText(str(column[2].value)+' '+units[2]) #longitudinal position to start integration (effective if < zEndInteg)
            self.ui.zendint.setText(str(column[3].value)+' '+units[3]) #longitudinal position to finish integration (effective if > zStartInteg)
            self.ui.nptraj.setText(str(column[4].value)+' '+units[4]) #Number of points for trajectory calculation
            self.ui.usetermin.setCurrentIndex(int(column[5].value)) #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
            self.ui.sampfactnxny.setText(str(column[6].value)+' '+units[6]) #sampling factor for adjusting nx, ny (effective if > 0)
        
        
                
def main():
    app = QtGui.QApplication(sys.argv)
    myapp = rbsrw()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
