"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
version 2
"""
#base imports
import sys
import os
import subprocess
import tempfile

from PySide.QtCore import *
from PySide.QtGui import *
from RadTrack.interactions.rbele import *
from rbcbt import RbCbt
from RbUtility import stripComments

class RbEle(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.ui = Ui_ELE()
        self.ui.setupUi(self)
        self.ui.sim.clicked.connect(self.execsim)
        self.ui.latticeChoice.currentIndexChanged.connect(self.getLTE)
        self.ui.bunchChoice.currentIndexChanged.connect(self.getBUN)
        self.ui.orderLineEdit.setText('2')
        self.ui.stepsLineEdit.setText('1')
        self.fileExtension = '.ele'
        self.parent = parent
        
        if self.parent is None:
            self.parent = self
            self.parent.lastUsedDirectory = os.path.expanduser('~')

        self.loaderCache = [] # saves the elements from beamline files chosen
                              # so they don't have to be reloaded every time
                              # the user chooses that file
        
    def getBUN(self):
        if self.ui.bunchChoice.currentText() == self.ui.fileBunchChoice:
            sddsfileName, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open',
                    self.parent.lastUsedDirectory, '*.sdds')
            if sddsfileName == '':
                return
            self.parent.lastUsedDirectory = os.path.dirname(sddsfileName)
            # Check if file has already been selected
            index = self.ui.bunchChoice.findText(sddsfileName)
            if index != -1:
                self.ui.bunchChoice.setCurrentIndex(index)
            else:
                self.ui.bunchChoice.addItem(sddsfileName)
                self.ui.bunchChoice.setCurrentIndex(self.ui.bunchChoice.count()-1)

        elif self.ui.bunchChoice.currentIndex() == 1:
            print 'Feature Coming Soon'
		
        
    def getLTE(self):
        self.ui.beamlineDropDown.clear()

        if self.ui.latticeChoice.currentText() == self.ui.noneBeamChoice:
            return
        elif self.ui.latticeChoice.currentText() == self.ui.tabBeamChoice:
            loader = self.parent.chargedBeamTransportTab
        elif self.ui.latticeChoice.currentText() == self.ui.fileBeamChoice:
            fileName, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open',
                    self.parent.lastUsedDirectory, '*.lte')
            if fileName == '':
                return
            self.parent.lastUsedDirectory = os.path.dirname(fileName)
            # Check if user already selected a file previously
            index = self.ui.latticeChoice.findText(fileName)
            if index != -1:
                self.ui.latticeChoice.setCurrentIndex(index)
            else:
                self.ui.latticeChoice.addItem(fileName)
                self.ui.latticeChoice.setCurrentIndex(self.ui.latticeChoice.count()-1)
            return
            # Setting the currentIndex triggers another signal that runs
            # the else clause below 

        else: # previously loaded file

            # There are three choices in the lattice dropdown menu before
            # any files are selected, hence the loaders created from files
            # are offset by three in the dropdown list compared to the 
            # loaderCache.
            if len(self.loaderCache) <= self.ui.latticeChoice.currentIndex()-3:
                loader = RbCbt('particle', parent=None)
                loader.importLattice(self.ui.latticeChoice.currentText())
                self.loaderCache.append(loader)
            else:
                loader = self.loaderCache[self.ui.latticeChoice.currentIndex()-3]


        allBeamLines = \
                [bl.name for bl in loader.elementDictionary.values() \
                if bl.isBeamline() and not bl.name.startswith('-')]

        # Reset available beamlines
        self.ui.beamlineDropDown.addItems(allBeamLines)
        self.ui.beamlineDropDown.setCurrentIndex(self.ui.beamlineDropDown.findText(loader.defaultBeamline))
        
    
    def simulate(self):
        # Define start of error message
        errMsg = 'Cannot start simulation due to:\n'
        errStartLength = len(errMsg)

        # Get beamline file
        if self.ui.latticeChoice.currentText() == self.ui.noneBeamChoice:
            errMsg += '  - No beamline lattice specified.\n'
        elif self.ui.latticeChoice.currentText() == self.ui.tabBeamChoice:
            fileHandle, latticeFileName = tempfile.mkstemp('.lte')
            os.close(fileHandle)
            self.parent.chargedBeamTransportTab.outBeam(latticeFileName)
            deleteLatticeFile = True
        else:
            latticeFileName = self.ui.latticeChoice.currentText()
            deleteLatticeFile = False

        # Get bunch file
        if self.ui.bunchChoice.currentText() == self.ui.noneBunchChoice:
            errMsg += '  - No bunch file specified.\n'
        elif self.ui.bunchChoice.currentText() == self.ui.tabBunchChoice:
            fileHandle, bunchFileName = tempfile.mkstemp('.sdds')
            os.close(fileHandle)
            self.parent.bunchTab.saveToSDDS(bunchFileName)
            deleteBunchFile = True
        else:
            bunchFileName = self.ui.bunchChoice.currentText()
            deleteBunchFile = False

        if self.ui.beamlineDropDown.currentText() == '':
            errMsg += '  - No beamline specified.\n'
        if self.ui.orderLineEdit.text() == '':
            errMsg += '  - No default order specified.\n'
        if self.ui.momentumLineEdit.text() == '':
            errMsg += '  - No momentum specified.\n'
        if self.ui.stepsLineEdit.text() == '':
            errMsg += '  - No step number specified.\n'

        if len(errMsg) > errStartLength:
            msgBox = QMessageBox(QMessageBox.Warning, 'RadTrack', errMsg)
            msgBox.exec_()
            return

        #generate ele file
        outputFileName, _ = QFileDialog.getSaveFileName(self, 'Save As',
                self.parent.lastUsedDirectory, '*' + self.fileExtension)
        if outputFileName == '':
            return
        if not outputFileName.endswith(self.fileExtension):
            outputFileName = outputFileName + self.fileExtension

        self.parent.lastUsedDirectory = os.path.dirname(outputFileName)
                
        with open(outputFileName, 'w') as outputFile:
            # Copyright statement
            #outputFile.write('/*\n')
            #outputFile.write('This Elegant file was created by RadTrack\n')
            #outputFile.write('RadTrack (c) 2013, RadiaBeam Technologies, LLC\n')
            #outputFile.write('*/\n\n\n')
            s = '    '
            outputFile.write('&run_setup\n')
            outputFile.write(s+'lattice = "'+latticeFileName+'",'+'\n')
            outputFile.write(s+'use_beamline = '+self.ui.beamlineDropDown.currentText()+','+'\n')
            outputFile.write(s+'default_order = '+self.ui.orderLineEdit.text()+','+'\n')
            outputFile.write(s+'p_central = '+self.ui.momentumLineEdit.text()+','+'\n')
            outputFile.write(s+'output = %s.out, \n')
            outputFile.write(s+'centroid = %s.cen, \n')
            outputFile.write(s+'sigma = %s.sig,\n')
            outputFile.write(s+'final = %s.fin,\n')
            outputFile.write(s+'parameters = %s.param,\n')
            outputFile.write(s+'magnets = %s.mag,\n')
            outputFile.write(s+'random_number_seed = 987654321,\n')
            outputFile.write(s+'combine_bunch_statistics = 0,\n')
            outputFile.write(s+'concat_order = 2,\n')
            outputFile.write(s+'print_statistics = 0,\n')
            outputFile.write(s+'tracking_updates = 1,\n') #0
            outputFile.write(s+'echo_lattice = 0 \n')
            outputFile.write('&end \n\n')
            outputFile.write('&run_control \n')
            outputFile.write(s+'n_steps = '+self.ui.stepsLineEdit.text()+','+'\n')
            outputFile.write(s+'reset_rf_for_each_step = 1 \n')
            outputFile.write('&end \n\n')
            outputFile.write('&twiss_output \n')
            outputFile.write(s+'matched = 0, \n') #****
            outputFile.write(s+'concat_order = 3, \n')
            outputFile.write(s+'beta_x=5, alpha_x=0, \n')
            outputFile.write(s+'beta_y=5, alpha_y=0, \n')
            #outputFile.write(s+'eta_x=0, eta_y=0, etap_x=0, etap_y=0 \n')
            outputFile.write(s+'output_at_each_step=1, \n')
            outputFile.write(s+'statistics =1, concat_order=3, \n')
            outputFile.write(s+'filename = %s.twi \n')
            outputFile.write('&end \n\n')
            outputFile.write('&sdds_beam \n')
            outputFile.write(s+'input = "'+bunchFileName+'",'+'\n')
            outputFile.write('&end \n\n')
            #outputFile.write('&bunched_beam \n')
            #outputFile.write(s+'n_particles_per_bunch = 200000, \n')
            #outputFile.write(s+'bunch = %s.bun,use_twiss_command_values = 1,beta_x=5,beta_y=5, alpha_x=0,alpha_y=0, \n')
            #outputFile.write(s+'sigma_dp= 1E-4,\n')
            #outputFile.write(s+'sigma_s = 20E-6, \n')
            #outputFile.write(s+'emit_nx = 1E-6, \n')
            #outputFile.write(s+'emit_ny = 1E-6, distribution_type[0] = 3*\"gaussian\", \n')
            #outputFile.write(s+'distribution_cutoff[0]=3*3, \n')
            #outputFile.write(s+'enforce_rms_values[0] = 1,1,1, \n')
            #outputFile.write('&end \n\n')
            outputFile.write('&matrix_output \n')
            outputFile.write(s+'SDDS_output = %s.mat, SDDS_output_order = 3, output_at_each_step = 1 \n')
            outputFile.write('&end \n\n')
            outputFile.write('&track \n')
            outputFile.write('&end \n\n')
            outputFile.write('&stop \n')
            outputFile.write('&end \n\n')
                
        with open(outputFileName,'r') as f:
            self.ui.textEdit.setText(f.read())

        
        #run elegant simulation
        simulationPackage = 'Elegant'
        #configfile = self.ui.lineEdit.text()
        #runfile = outputFileName
        runsim = [simulationPackage, outputFileName]

        #return(runsim)
        return(outputFileName)

        #import tempfile    
        #subprocess.call(runsim)

    def execsim(self):
        ofile = self.simulate()
        subprocess.call(['Elegant',ofile])
        

        '''proc = subprocess.Popen(runsim, bufsize=1, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        print 'output:/n', out


        #with open(f, 'r') as F:
            #self.ui.textEdit.setText(F.read())
        if deleteLatticeFile:
            os.remove(latticeFileName)
        #if deleteBunchFile:
        #    os.remove(bunchFileName)'''
            
        
def run():

    app = QtGui.QApplication(sys.argv)
    ex = RbEle()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()               
               
               
               
