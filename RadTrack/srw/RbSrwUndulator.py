#Library for SRW-Radtrack interface
#steven seung

import numpy as np
from srwlib import *
import sys, os
import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui, QtCore
from undulator import ui_form
from uti_plot import *
from AnalyticCalc import *

class srwund(QtGui.QWidget):

    def AnalyticA(self,elecBeam):
        n_har=1
        (Kx,Ky,lam_rn,e_phn,w_or_id)=IDWaveLengthPhotonEnergy(n_har,UP.undPer,UP.Bx,UP.By,elecBeam.partStatMom1.gamma)
        stri='# K vertical:'+'{:.3f}'.format(Kx)+'\n'+\
        '# K horizontal:'+'{:.3f}'.format(Ky)+'\n'+\
        '# Wavelength, m         Photon energy, eV'+'\n'+\
        '1st harmonic '+'{:.3e}'.format(lam_rn)+' '+'{:.3e}'.format(e_phn)+'\n'+\
        '3rd harmonic '+'{:.3e}'.format(lam_rn/3.0)+' '+'{:.3e}'.format(e_phn*3.0)+'\n'+\
        '5th harmonic '+'{:.3e}'.format(lam_rn/5.0)+' '+'{:.3e}'.format(e_phn*5.0)+'\n' 
        
        (E_c,w_or_id)=CriticalEnergyWiggler(UP.Bx,elecBeam.partStatMom1.gamma,Kx)
        stra=stri+'# If wiggler: critical energy:'+'{:.3e}'.format(E_c)+', eV'+'\n'
        
        (P_W, L_id)=RadiatedPowerPlanarWiggler(UP.undPer,UP.Bx,UP.numPer,elecBeam.partStatMom1.gamma,elecBeam.Iavg)
        strb=stra+'# Length of ID:'+'{:.3e}'.format(L_id)+', m'+'\n' + \
        '# Radiated power:'+'{:.3e}'.format(P_W)+', W'+'\n'
        
        P_Wdc=CentralPowerDensityPlanarWiggler(UP.Bx,UP.numPer,elecBeam.partStatMom1.gamma,elecBeam.Iavg)
        strc=strb+'# Central Power Density: '+'{:.3e}'.format(P_Wdc)+', W/mrad2'+'\n'
        
        self.ui.analytic.setText(strc)
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = ui_form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.srwbutton)

        #default values
        self.ui.numper.setText('40.5')
        self.ui.undper.setText('0.049')
        self.ui.bx.setText('0.0')
        self.ui.by.setText('0.57')
        self.ui.phbx.setText('0')
        self.ui.phby.setText('0')
        self.ui.sbx.setText('-1')
        self.ui.sby.setText('1')
        self.ui.xcid.setText('0')
        self.ui.ycid.setText('0')
        self.ui.zcid.setText('0')
        self.ui.iavg.setText('0.5')
        self.ui.partstatmom1x.setText('0')
        self.ui.partstatmom1y.setText('0')
        self.ui.partstatmom1z.setText('0.0')
        self.ui.partstatmom1xp.setText('0')
        self.ui.partstatmom1yp.setText('0')
        self.ui.partstatmom1gamma.setText('5870.925')
        self.ui.meth.setCurrentIndex(1)
        self.ui.relprec.setText('0.01')
        self.ui.zstartint.setText('0')
        self.ui.zendint.setText('0')
        self.ui.nptraj.setText('20000')
        self.ui.usetermin.setCurrentIndex(1)
        self.ui.sampfactnxnyprop.setText('0')
        self.ui.tableWidget.setItem(0,0,QtGui.QTableWidgetItem('10000'))
        self.ui.tableWidget.setItem(1,0,QtGui.QTableWidgetItem('1'))
        self.ui.tableWidget.setItem(2,0,QtGui.QTableWidgetItem('1'))
        self.ui.tableWidget.setItem(3,0,QtGui.QTableWidgetItem('20'))
        self.ui.tableWidget.setItem(4,0,QtGui.QTableWidgetItem('10'))
        self.ui.tableWidget.setItem(5,0,QtGui.QTableWidgetItem('3000'))
        self.ui.tableWidget.setItem(6,0,QtGui.QTableWidgetItem('0'))
        self.ui.tableWidget.setItem(7,0,QtGui.QTableWidgetItem('0'))
        self.ui.tableWidget.setItem(8,0,QtGui.QTableWidgetItem('0'))
        self.ui.tableWidget.setItem(9,0,QtGui.QTableWidgetItem('0'))
        
##         self.ui.tableWidget.setItem(0,0,QtGui.QTableWidgetItem('3'))
##         self.ui.tableWidget.setItem(1,0,QtGui.QTableWidgetItem('30'))
##         self.ui.tableWidget.setItem(2,0,QtGui.QTableWidgetItem('30'))
##         self.ui.tableWidget.setItem(3,0,QtGui.QTableWidgetItem('20'))
##         self.ui.tableWidget.setItem(4,0,QtGui.QTableWidgetItem('10'))
##         self.ui.tableWidget.setItem(5,0,QtGui.QTableWidgetItem('3000'))
##         self.ui.tableWidget.setItem(6,0,QtGui.QTableWidgetItem('-0.01'))
##         self.ui.tableWidget.setItem(7,0,QtGui.QTableWidgetItem('-0.01'))
##         self.ui.tableWidget.setItem(8,0,QtGui.QTableWidgetItem('0.01'))
##         self.ui.tableWidget.setItem(9,0,QtGui.QTableWidgetItem('0.01'))
                            
        #this is how you write to the status and calculations windows
        self.ui.analytic.setText('hello')
        self.ui.status.setText('hi')

    def UndParams(self,UP):
        #U = UP()
        UP.numPer = float(self.ui.numper.text())
        UP.undPer = float(self.ui.undper.text())
        UP.Bx = float(self.ui.bx.text())
        UP.By = float(self.ui.by.text())
        UP.phBx = float(self.ui.phbx.text())
        UP.phBy = float(self.ui.phby.text())
        UP.sBx = float(self.ui.sbx.text())
        UP.sBy = float(self.ui.sby.text())
        UP.xcID = float(self.ui.xcid.text())
        UP.ycID = float(self.ui.ycid.text())
        UP.zcID = float(self.ui.zcid.text())
        #return (UP)

    def BeamParams(self,elecBeam):
        elecBeam.Iavg = float(self.ui.iavg.text())
        elecBeam.partStatMom1.x = float(self.ui.partstatmom1x.text())
        elecBeam.partStatMom1.y = float(self.ui.partstatmom1y.text())
        elecBeam.partStatMom1.z = float(self.ui.partstatmom1z.text())
        elecBeam.partStatMom1.xp = float(self.ui.partstatmom1xp.text())
        elecBeam.partStatMom1.yp = float(self.ui.partstatmom1yp.text()) 
        elecBeam.partStatMom1.gamma = float(self.ui.partstatmom1gamma.text())
        sigEperE = 0.89E-2 #relative RMS energy spread
        sigX = 33.33e-04 #horizontal RMS size of e-beam [m]
        sigXp = 16.5e-09 #horizontal RMS angular divergence [rad]
        sigY = 2.912e-09 #vertical RMS size of e-beam [m]
        sigYp = 2.7472e-09 #vertical RMS angular divergence [rad]
        #2nd order stat. moments:
        elecBeam.arStatMom2[0] = sigX*sigX #<(x-<x>)^2> 
        elecBeam.arStatMom2[1] = 0 #<(x-<x>)(x'-<x'>)>
        elecBeam.arStatMom2[2] = sigXp*sigXp #<(x'-<x'>)^2> 
        elecBeam.arStatMom2[3] = sigY*sigY #<(y-<y>)^2>
        elecBeam.arStatMom2[4] = 0 #<(y-<y>)(y'-<y'>)>
        elecBeam.arStatMom2[5] = sigYp*sigYp #<(y'-<y'>)^2>
        elecBeam.arStatMom2[10] = sigEperE*sigEperE #<(E-<E>)^2>/<E>^2

    def WfrSetUpE(self,wfrE):
        #wfrE = SRWLWfr()
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
        #return(wfrE)

    def Precision(self,Precis):
        Precis.meth = self.ui.meth.currentIndex()
        Precis.relPrec = float(self.ui.relprec.text())
        Precis.zStartInteg = float(self.ui.zstartint.text())
        Precis.zEndInteg = float(self.ui.zendint.text())
        Precis.npTraj = float(self.ui.nptraj.text())
        Precis.useTermin = float(self.ui.usetermin.currentIndex())
        Precis.sampFactNxNyForProp = float(self.ui.sampfactnxnyprop.text())
        #return(Precis)

    def srwbutton(self):
        if 'srwl' not in globals():
            msg = ' !Warning --'
            msg += 'SRW not installed on this system.'
            self.ui.status.setText(msg)
            raise Exception(msg)
        Up = UP()
        #UP =
        self.UndParams(UP)
        und = SRWLMagFldU([SRWLMagFldH(1, 'v', Up.By, Up.phBy, Up.sBy, 1), SRWLMagFldH(1, 'h', Up.Bx, Up.phBx, Up.sBx, 1)], Up.undPer, Up.numPer)
        magFldCnt = SRWLMagFldC([und], array('d', [Up.xcID]), array('d', [Up.ycID]), array('d', [Up.zcID]))
        elecBeam = SRWLPartBeam()
        self.BeamParams(elecBeam)

        self.AnalyticA(elecBeam)

        precis = Precis()
        self.Precision(Precis)
        arPrecPar = [precis.meth, precis.relPrec, precis.zStartInteg, precis.zEndInteg, precis.npTraj, precis.useTermin, precis.sampFactNxNyForProp]

        wfrE = SRWLWfr()
        self.WfrSetUpE(wfrE)
        wfrE.partBeam = elecBeam

        wfrXY = SRWLWfr()
        self.WfrSetUpE(wfrXY)
        wfrXY.partBeam = elecBeam
        
        mesh=deepcopy(wfrE.mesh)
        wfrIn=deepcopy(wfrE)

        Polar = self.ui.polar.currentIndex()
        Intens = self.ui.intensity.currentIndex()
        DependArg = self.ui.deparg.currentIndex()
#        print (Polar, Intens, DependArg)
      
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
            uti_plot1d(arI1, [wfrE.mesh.eStart, wfrE.mesh.eFin, wfrE.mesh.ne],['label','label','label'])

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
            uti_plot1d(arI1, [wfrXY.mesh.xStart, wfrXY.mesh.xFin, wfrXY.mesh.nx],['label','label','label'])

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
            uti_plot1d(arI1, [wfrXY.mesh.yStart, wfrXY.mesh.yFin, wfrXY.mesh.ny],['label','label','label'])
       
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
            uti_plot2d(arI1, [1000*wfrXY.mesh.xStart, 1000*wfrXY.mesh.xFin, wfrXY.mesh.nx], 
            [1000*wfrXY.mesh.yStart, 1000*wfrXY.mesh.yFin, wfrXY.mesh.ny], 
            ['Horizontal Position [mm]', 'Vertical Position [mm]', 'Intensity at ' + str(wfrXY.mesh.eStart) + ' eV'])

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
            uti_plot2d(arI1, [1000*wfrXY.mesh.eStart, 1000*wfrXY.mesh.eFin, wfrXY.mesh.ne], 
            [1000*wfrXY.mesh.xStart, 1000*wfrXY.mesh.xFin, wfrXY.mesh.nx], 
            ['Energy [eV]', 'Horizontal Position [mm]', 'Intensity at ' + str(wfrXY.mesh.eStart) + ' eV'])

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
            uti_plot2d(arI1, [1000*wfrXY.mesh.eStart, 1000*wfrXY.mesh.eFin, wfrXY.mesh.ne], 
            [1000*wfrXY.mesh.yStart, 1000*wfrXY.mesh.yFin, wfrXY.mesh.ny], 
            ['Energy [eV]', 'Vertical Position [mm]', 'Intensity at ' + str(wfrXY.mesh.eStart) + ' eV'])

        else:
            print 'Error'
    
        uti_plot_show()
        

class UP:
     def __init__(self): #,index
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
    myapp = srwund()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
