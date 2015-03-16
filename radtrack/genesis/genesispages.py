
from PyQt4 import QtGui, QtCore
import os, sys

from radtrack.ui.beamforgenesis import Ui_Dialog as Ui_genbeam
from radtrack.ui.fodoforgenesis import Ui_Dialog as Ui_genfodo
from radtrack.ui.iogenesis import Ui_Dialog as Ui_io
from radtrack.ui.meshforgenesis import Ui_Dialog as Ui_Mesh
from radtrack.ui.ploadforgenesis import Ui_Dialog as  Ui_ploading
from radtrack.ui.radforgenesis import Ui_Dialog as Ui_radiation
from radtrack.ui.scanforgenesis import Ui_Dialog as Ui_scan
from radtrack.ui.simcongenesis import Ui_Dialog as Ui_simcon
from radtrack.ui.timeforgenesis import Ui_Dialog as Ui_timeparams
from radtrack.ui.undulatorforgenesis import Ui_Dialog as Ui_genund
        

class undulator_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_genund()
        self.ui.setupUi(self)
        self.ui.aw0.setText('2.4749')
        self.ui.iwityp.setCheckable(True)
        self.ui.iwityp.setChecked(False)
        #self.ui.xkx.setText('0')
        #self.ui.xky.setText('1')
        self.ui.xlamd.setText('0.03')
        self.ui.nwig.setText('144')
        self.ui.nsec.setText('30')
        self.ui.delaw.setText('0')
        self.ui.awx.setText('0')
        self.ui.awy.setText('0')
        self.ui.seed.setText('20')
        self.ui.iertyp.setRange(-2,2)
        

class fodo_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_genfodo()
        self.ui.setupUi(self)
        self.ui.quadf.setText('12.7')
        self.ui.quadd.setText('12.7')
        self.ui.fl.setText('8.0')
        self.ui.dl.setText('8.0')
        self.ui.drl.setText('112')
        self.ui.f1st.setText('0')
        self.ui.qfdx.setText('0')
        self.ui.qfdy.setText('0')
        self.ui.solen.setText('0')
        self.ui.sl.setText('0')        
        

class beam_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_genbeam()
        self.ui.setupUi(self)
        self.ui.gamma0.setText('26700')
        self.ui.delgam.setText('2.8')
        self.ui.rxbeam.setText('34.71e-6')
        self.ui.rybeam.setText('28.63e-6')
        self.ui.alphax.setText('1.2268')
        self.ui.alphay.setText('-0.8375')
        self.ui.emitx.setText('1.2e-6')
        self.ui.emity.setText('1.2e-6')
        self.ui.xbeam.setText('0')
        self.ui.ybeam.setText('0')
        self.ui.pxbeam.setText('0')
        self.ui.pybeam.setText('0')
        self.ui.curpeak.setText('250')
        

class radiation_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_radiation()
        self.ui.setupUi(self)
        self.ui.xlamds.setText('1.50e-10')
        self.ui.prad0.setText('3000')
        self.ui.zrayl.setText('50')
        self.ui.zwaist.setText('0')
        self.ui.iallharm.setCheckable(True)
        self.ui.iallharm.setChecked(False)
        self.ui.nharm.setText('1')
        self.ui.iharmsc.setCheckable(True)
        self.ui.iharmsc.setChecked(False)
        self.ui.pradh0.setText('0')   
        

class ploading_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_ploading()
        self.ui.setupUi(self)
        self.ui.tableWidget.setItem(0,0,QtGui.QTableWidgetItem('7'))
        self.ui.tableWidget.setItem(1,0,QtGui.QTableWidgetItem('5'))
        self.ui.tableWidget.setItem(2,0,QtGui.QTableWidgetItem('1'))
        self.ui.tableWidget.setItem(3,0,QtGui.QTableWidgetItem('2'))
        self.ui.tableWidget.setItem(4,0,QtGui.QTableWidgetItem('3'))
        self.ui.tableWidget.setItem(5,0,QtGui.QTableWidgetItem('4'))
        #self.ui.itgaus.setCurrentIndex(0)
        self.ui.itgamgaus.setCurrentIndex((1))
        self.ui.iall.setText('0')
        self.ui.ipspeed.setText('-1')
        self.ui.nbins.setText('4') 
        

class mesh_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Mesh()
        self.ui.setupUi(self)
        self.ui.ncar.setText('139')
        self.ui.lbc.setCheckable(True)
        self.ui.lbc.setChecked(False)
        self.ui.rmax0.setText('11')
        self.ui.dgrid.setText('0')
        #self.ui.nscz.setRange(0,10)
        self.ui.nscr.setText('1')
        self.ui.nptr.setText('40')
        self.ui.rmax0sc.setText('0')
        self.ui.iscrkup.setCheckable(True)
        self.ui.iscrkup.setChecked(False)
        

class time_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_timeparams()
        self.ui.setupUi(self)
        self.ui.itdp.setCheckable(True)
        self.ui.itdp.setChecked(False)
        self.ui.curlen.setText('1.0e-3')
        self.ui.zsep.setText('32')
        self.ui.nslice.setText('13302')
        self.ui.ntail.setText('25')
        self.ui.shotnoise.setText('1')
        self.ui.isntyp.setCheckable(True)
        self.ui.isntyp.setChecked(False)
        

class sim_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_simcon()
        self.ui.setupUi(self)
        self.ui.delz.setText('8')
        self.ui.zstop.setText('132')
        self.ui.iorb.setCheckable(True)
        self.ui.isravg.setCheckable(True)
        self.ui.isrsig.setCheckable(True)
        self.ui.iorb.setChecked(False)
        self.ui.isravg.setChecked(False)
        self.ui.isrsig.setChecked(True)
        self.ui.eloss.setText('0')

class scan_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_scan()
        self.ui.setupUi(self)
        #self.ui.iscan.setCurrentIndex(0)
        self.ui.nscan.setText('3')
        self.ui.svar.setText('0.01')

class io_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_io()
        self.ui.setupUi(self)
        self.ui.iphsty.setCheckable(True)
        self.ui.ishsty.setCheckable(True)
        self.ui.ippart.setCheckable(True)
        self.ui.ispart.setCheckable(True)
        self.ui.ipradi.setCheckable(True)
        self.ui.isradi.setCheckable(True)
        self.ui.iotail.setCheckable(True)
        self.ui.ndcut.setCheckable(True)
        self.ui.aligngradf.setCheckable(True)
        self.ui.ilog.setCheckable(True)
        self.ui.trama.setCheckable(True)
        self.ui.iphsty.setChecked(True)
        self.ui.ishsty.setChecked(True)
        self.ui.ippart.setChecked(False)
        self.ui.ispart.setChecked(True)
        self.ui.ipradi.setChecked(False)
        self.ui.isradi.setChecked(False)
        self.ui.iotail.setChecked(True)
        self.ui.ndcut.setChecked(False)
        self.ui.aligngradf.setChecked(False)
        self.ui.ilog.setChecked(False)
        self.ui.trama.setChecked(False)

        #outputfile = 'lcls.out'
        #maginfile = 'lcls.lat'
        self.ui.dump.setCurrentIndex(0)
        #idmpfld=1
        #distfile='lcls_resonant.dist'
        self.ui.offsetradf.setText('0')
        self.ui.convharm.setText('1')
        self.ui.multiconv.setText('0')
        self.ui.ibfield.setText('0')
        self.ui.imagl.setText('0')
        self.ui.idril.setText('0')
        #LOUT=1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 0 0 0 0 1 0 0
        self.ui.ffspec.setText('0')
        

        

        
        
