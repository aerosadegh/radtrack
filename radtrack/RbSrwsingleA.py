"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

"""

import sys, os
from numpy import sqrt
from PyQt4 import QtGui, QtCore
from ui.newsrw import Ui_Form as Ui_newsrw
from ui.undulatorforthinsrw import Ui_Dialog as und_dlg
from ui.beamforthinsrw import Ui_Dialog as beam_dlg
from ui.precisionofsrw import Ui_Dialog as prec_dlg
from srw.uti_plot import *
from srw.AnalyticCalc import *
from srw.srwlib import *
from xlrd import *

class rbsrw(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_newsrw()
        self.ui.setupUi(self)
        self.up = UP()
        self.beam = SRWLPartBeam()
        self.precis = Precis()
        #load initial values from excel
        workbook = open_workbook('/Users/stevenseung/Desktop/radtrack/radtrack/srw/SRWinitialvalues.xls')
        self.thinsheet = workbook.sheet_by_name('thin table')
        self.thin(self.ui.deparg.currentIndex())
        #set srw initial values 
        column = workbook.sheet_by_name('thin undulator').col(0)
        self.GetUndParams(DialogU(self,column))
        column = workbook.sheet_by_name('thin beam').col(0)
        self.GetBeamParams(DialogB(self,column))
        column = workbook.sheet_by_name('thin precision').col(0)
        self.GetPrecision(DialogP(self,column))
        
        #connections
        self.ui.undulator.clicked.connect(self.makeund)
        self.ui.beam.clicked.connect(self.makebeam)
        self.ui.precision.clicked.connect(self.setprec)
        self.ui.deparg.currentIndexChanged.connect(self.thin)
        self.ui.sim.clicked.connect(self.srwbuttonThin)
        #self.ui.plot.clicked.connect(self.check)
        #indicators
        self.ui.status.setText('Initiated')
        self.ui.analytic.setText('No calculations performed...Yet')
        
        
    def AnalyticA(self):
        n_har=1 #harmB.n harmonic number from SRWTestCases(2)\UndC
        (Kx,Ky,lam_rn,e_phn,w_or_id)=IDWaveLengthPhotonEnergy(n_har,self.up.undPer,self.up.Bx,self.up.By,self.beam.partStatMom1.gamma)
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
        
        (E_c,w_or_id)=CriticalEnergyWiggler(self.up.Bx,self.beam.partStatMom1.gamma,Kx)
        #Outputs: (RAD.Ecrit,UPWorU) where RAD.Ecrit is critical energy of Wiggler Radiation
        #Inputs: (UP.Bx, self.beam.partStatMom1.gamma,UP.Kx)
        stra=stri+'# If wiggler: critical energy:'+'{:.3e}'.format(E_c)+', eV'+'\n'
        
        (P_W, L_id)=RadiatedPowerPlanarWiggler(self.up.undPer,self.up.Bx,self.up.numPer,self.beam.partStatMom1.gamma,self.beam.Iavg)
        #Outputs: (RAD.PowW,UP.L) where RAD.PowW is radiated power of Wiggler Radiation, UP.L=length of ID
        #Inputs: (UP.undPer,UP.Bx,UP.numPer,self.beam.partStatMom1.gamma,self.beam.Iavg) standart SRW class variables
        strb=stra+'# Length of ID:'+'{:.3e}'.format(L_id)+', m'+'\n' + \
        '# Radiated power:'+'{:.3e}'.format(P_W)+', W'+'\n'
        
        P_Wdc=CentralPowerDensityPlanarWiggler(self.up.Bx,self.up.numPer,self.beam.partStatMom1.gamma,self.beam.Iavg)
        #Outputs: (RAD.PowCPD) where RAD.PowCPD is radiated central cone power density of Wiggler Radiation
        #Inputs: (UP.undPer,UP.Bx,UP.numPer,self.beam.partStatMom1.gamma,self.beam.Iavg) standart SRW class variables
        strc=strb+'# Central Power Density: '+'{:.3e}'.format(P_Wdc)+', W/mrad2'+'\n'
        
        self.ui.analytic.setText(strc)
        
    def GetUndParams(self, dialog):
        self.up.numPer = float(dialog.ui.numper.text())
        self.up.undPer = float(dialog.ui.undper.text())
        self.up.Bx = float(dialog.ui.bx.text())
        self.up.By = float(dialog.ui.by.text())
        self.up.phBx = float(dialog.ui.phbx.text())
        self.up.phBy = float(dialog.ui.phby.text())
        self.up.sBx = float(dialog.ui.sbx.text())
        self.up.sBy = float(dialog.ui.sby.text())
        self.up.xcID = float(dialog.ui.xcid.text())
        self.up.ycID = float(dialog.ui.ycid.text())
        self.up.zcID = float(dialog.ui.zcid.text())
        
    def ShowUndParams(self, dialog):
        dialog.ui.numper.setText(str(self.up.numPer))
        dialog.ui.undper.setText(str(self.up.undPer))
        dialog.ui.bx.setText(str(self.up.Bx))
        dialog.ui.by.setText(str(self.up.By))
        dialog.ui.phbx.setText(str(self.up.phBx))
        dialog.ui.phby.setText(str(self.up.phBy))
        dialog.ui.sbx.setText(str(self.up.sBx))
        dialog.ui.sby.setText(str(self.up.sBy))
        dialog.ui.xcid.setText(str(self.up.xcID))
        dialog.ui.ycid.setText(str(self.up.ycID))
        dialog.ui.zcid.setText(str(self.up.zcID))
        
        
    def GetBeamParams(self,dialog):
        #this is the self.beam class
        self.beam.Iavg = float(dialog.ui.iavg.text())
        self.beam.partStatMom1.x = float(dialog.ui.partstatmom1x.text())
        self.beam.partStatMom1.y = float(dialog.ui.partstatmom1y.text())
        self.beam.partStatMom1.z = float(dialog.ui.partstatmom1z.text())
        self.beam.partStatMom1.xp = float(dialog.ui.partstatmom1xp.text())
        self.beam.partStatMom1.yp = float(dialog.ui.partstatmom1yp.text()) 
        self.beam.partStatMom1.gamma = float(dialog.ui.partstatmom1gamma.text())

        
    def ShowBeamParams(self, dialog):
        dialog.ui.iavg.setText(str(self.beam.Iavg))
        dialog.ui.partstatmom1x.setText(str(self.beam.partStatMom1.x))
        dialog.ui.partstatmom1y.setText(str(self.beam.partStatMom1.y))
        dialog.ui.partstatmom1z.setText(str(self.beam.partStatMom1.z))
        dialog.ui.partstatmom1xp.setText(str(self.beam.partStatMom1.xp))
        dialog.ui.partstatmom1yp.setText(str(self.beam.partStatMom1.yp))
        dialog.ui.partstatmom1gamma.setText(str(self.beam.partStatMom1.gamma))
        
    def WfrSetUpE(self,wfrE):
        #wfrE = SRWLWfr() this is the waveform class
        Nenergy = int(self.ui.tableWidget.item(0,0).text())#float?
        Nx = int(self.ui.tableWidget.item(1,0).text())
        Ny = int(self.ui.tableWidget.item(2,0).text())
        wfrE.allocate(Nenergy,Nx,Ny)
        wfrE.mesh.zStart = float(self.ui.tableWidget.item(3,0).text())
        wfrE.mesh.eStart = float(self.ui.tableWidget.item(4,0).text())
        wfrE.mesh.eFin = float(self.ui.tableWidget.item(5,0).text())
        wfrE.mesh.xStart = float(self.ui.tableWidget.item(6,0).text())
        wfrE.mesh.xFin = float(self.ui.tableWidget.item(8,0).text())
        wfrE.mesh.yStart = float(self.ui.tableWidget.item(7,0).text())
        wfrE.mesh.yFin = float(self.ui.tableWidget.item(9,0).text())
        
    def GetPrecision(self,dialog):
        self.precis.meth = dialog.ui.meth.currentIndex()
        self.precis.relPrec = float(dialog.ui.relprec.text())
        self.precis.zStartInteg = float(dialog.ui.zstartint.text())
        self.precis.zEndInteg = float(dialog.ui.zendint.text())
        self.precis.npTraj = float(dialog.ui.nptraj.text())
        self.precis.useTermin = dialog.ui.usetermin.currentIndex()
        self.precis.sampFactNxNyForProp = float(dialog.ui.sampfactnxny.text())
        
    def ShowPrecision(self,dialog):
        dialog.ui.meth.setCurrentIndex(self.precis.meth)
        dialog.ui.relprec.setText(str(self.precis.relPrec))
        dialog.ui.zstartint.setText(str(self.precis.zStartInteg))
        dialog.ui.zendint.setText(str(self.precis.zEndInteg))
        dialog.ui.nptraj.setText(str(self.precis.npTraj))
        dialog.ui.usetermin.setCurrentIndex(self.precis.useTermin)
        dialog.ui.sampfactnxny.setText(str(self.precis.sampFactNxNyForProp))
    
         
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

        self.AnalyticA()

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
        '''
        r = self.thinsheet.nrows
        c = self.thinsheet.ncols
        thintable = []
        for k in range(c):
            l = []
            for j in range(r):
                l.append(self.thinsheet.cell(j,k).value)
            thintable.append(l)
                     
        for n,x in enumerate(thintable[i]):
            self.ui.tableWidget.setItem(n,0,QtGui.QTableWidgetItem(str(x)))'''
            
        for n,c in enumerate(self.thinsheet.col(i)):
            self.ui.tableWidget.setItem(n,0,QtGui.QTableWidgetItem(str(c.value)))
        
        
    def makeund(self):
        dialog = DialogU()
        self.ShowUndParams(dialog)
        if dialog.exec_():
            self.GetUndParams(dialog)
            
    def makebeam(self):
        dialog = DialogB()
        self.ShowBeamParams(dialog)
        if dialog.exec_():
            self.GetBeamParams(dialog)
            
    def setprec(self):
        dialog = DialogP()
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
    def __init__(self, parent=None,column=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = und_dlg()
        self.ui.setupUi(self)
        if column is not None:
            self.ui.numper.setText(str(column[0].value))  #Number of ID Periods (without accounting for terminations)
            self.ui.undper.setText(str(column[1].value)) #Period Length
            self.ui.bx.setText(str(column[2].value))       #Peak Vertical field
            self.ui.by.setText(str(column[3].value))      #Peak Horizontal field
            self.ui.phbx.setText(str(column[4].value))       #Initial Phase of the Horizontal field component
            self.ui.phby.setText(str(column[5].value))       #Initial Phase of the Vertical field component
            self.ui.sbx.setText(str(column[6].value))       #Symmetry of the Horizontal field component vs Longitudinal position
            self.ui.sby.setText(str(column[7].value))        #Symmetry of the Vertical field component vs Longitudinal position
            self.ui.xcid.setText(str(column[8].value))       #Misaligment. Horizontal Coordinate of Undulator Center 
            self.ui.ycid.setText(str(column[9].value))       #Misaligment. Vertical Coordinate of Undulator Center 
            self.ui.zcid.setText(str(column[10].value))      #Misaligment. Longitudinal Coordinate of Undulator Center
                
class DialogB(QtGui.QDialog):
    def __init__(self, parent=None, column=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = beam_dlg()
        self.ui.setupUi(self)
        if column is not None:
            self.ui.iavg.setText(str(column[0].value))     #Above is the UP class, this is self.beam.iavg
            self.ui.partstatmom1x.setText(str(column[1].value))  #self.beam.partStatMom1.x, initial x-offset    
            self.ui.partstatmom1y.setText(str(column[2].value))  #self.beam.partStatMom1.y, initial y-offset
            self.ui.partstatmom1z.setText(str(column[3].value)) #self.beam.partStatMom1.z, initial z-offset
            self.ui.partstatmom1xp.setText(str(column[4].value)) #self.beam.partStatMom1.xp, initial x angle offset
            self.ui.partstatmom1yp.setText(str(column[5].value)) #self.beam.partStatMom1.yp, initial y angle offset
            self.ui.partstatmom1gamma.setText(str(column[6].value)) # electron beam relative energy, gamma

class DialogP(QtGui.QDialog):
    def __init__(self, parent=None, column=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = prec_dlg()
        self.ui.setupUi(self)
        if column is not None:
            self.ui.meth.setCurrentIndex(int(column[0].value)) #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
            self.ui.relprec.setText(str(column[1].value)) #relative precision
            self.ui.zstartint.setText(str(column[2].value)) #longitudinal position to start integration (effective if < zEndInteg)
            self.ui.zendint.setText(str(column[3].value)) #longitudinal position to finish integration (effective if > zStartInteg)
            self.ui.nptraj.setText(str(column[4].value)) #Number of points for trajectory calculation
            self.ui.usetermin.setCurrentIndex(int(column[5].value)) #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
            self.ui.sampfactnxny.setText(str(column[6].value)) #sampling factor for adjusting nx, ny (effective if > 0)
        
        
                
def main():
    app = QtGui.QApplication(sys.argv)
    myapp = rbsrw()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

