"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
version 2
"""
import sys, os, subprocess, tempfile, glob

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from radtrack.interactions.rbele import *
from  radtrack.RbBunchTransport import RbBunchTransport
from  radtrack.RbBunchWindow import RbBunchWindow
from  radtrack.RbUtility import stripComments
import radtrack.util.resource as resource

class RbEle(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.ui = Ui_ELE()
        self.ui.setupUi(self)
        self.ui.sim.clicked.connect(self.simulate)
        self.ui.latticeChoice.currentIndexChanged.connect(self.getLTE)
        self.ui.bunchChoice.currentIndexChanged.connect(self.getBUN)
        self.ui.orderLineEdit.setText('2')
        self.ui.stepsLineEdit.setText('1')
        self.fileExtension = '.ele'
        self.parent = parent

        if self.parent is None:
            self.parent = self
            self.parent.lastUsedDirectory = os.path.expanduser('~')

        self.loaderCache = dict() # saves the elements from beamline files chosen
                                  # so they don't have to be reloaded every time
                                  # the user chooses that file

    def getBUN(self):
        if self.ui.bunchChoice.currentText() == self.ui.noneBunchChoice:
            return

        if self.ui.bunchChoice.currentText() == self.ui.fileBunchChoice:
            sddsfileName = QtGui.QFileDialog.getOpenFileName(self, 'Open',
                    self.parent.lastUsedDirectory, '*.sdds')
            if sddsfileName == '':
                self.ui.bunchChoice.setCurrentIndex(self.ui.bunchChoice.findText(self.ui.noneBunchChoice))
                return
            self.parent.lastUsedDirectory = os.path.dirname(sddsfileName)
            # Check if file has already been selected
            index = self.ui.bunchChoice.findText(sddsfileName)
            if index != -1:
                self.ui.bunchChoice.setCurrentIndex(index)
            else:
                self.ui.bunchChoice.addItem(sddsfileName)
                self.ui.bunchChoice.setCurrentIndex(self.ui.bunchChoice.count()-1)


    def getLTE(self):
        self.ui.beamlineDropDown.clear()

        if self.ui.latticeChoice.currentText() in [self.ui.noneBeamChoice, '']:
            return

        elif self.ui.latticeChoice.currentText() in self.tabTitles():
            for tabIndex in range(self.parent.tabWidget.count()):
                if self.parent.tabWidget.tabText(tabIndex) == self.ui.latticeChoice.currentText():
                    loader = self.parent.tabWidget.widget(tabIndex)

        elif self.ui.latticeChoice.currentText() == self.ui.fileBeamChoice:
            fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open',
                    self.parent.lastUsedDirectory, '*.lte')
            if fileName == '':
                self.ui.latticeChoice.setCurrentIndex(self.ui.latticeChoice.findText(self.ui.noneLatticeChoice))
                return
            self.parent.lastUsedDirectory = os.path.dirname(fileName)
            # Check if user already selected a file previously
            if fileName not in self.loaderCache:
                loader = RbBunchTransport()
                loader.importFile(fileName)
                self.loaderCache[fileName] = loader
                self.ui.latticeChoice.addItem(fileName)
            self.ui.latticeChoice.setCurrentIndex(self.ui.latticeChoice.findText(fileName))

            return
            # Setting the currentIndex triggers another signal that runs
            # the else clause below

        else: # previously loaded file
            loader = self.loaderCache[self.ui.latticeChoice.currentText()]

        allBeamLines = []
        for element in loader.elementDictionary.values():
            if element.isBeamline() and not element.name.startswith('-'):
                allBeamLines.append(element.name)

        # Reset available beamlines
        self.ui.beamlineDropDown.addItems(allBeamLines)
        self.ui.beamlineDropDown.setCurrentIndex(self.ui.beamlineDropDown.findText(loader.defaultBeamline))

    def tabTitles(self):
        return [self.parent.tabWidget.tabText(i) for i in range(self.parent.tabWidget.count())]

    def simulate(self):
        self.ui.textEdit.append('Starting simulation ...')

        errMsg = ''

        # Get beamline file
        if self.ui.latticeChoice.currentText() == self.ui.noneBeamChoice:
            errMsg += '  - No beamline lattice specified.\n'

        elif self.ui.latticeChoice.currentText() in self.tabTitles():
            fileHandle, latticeFileName = tempfile.mkstemp('.lte')
            os.close(fileHandle)
            for tabIndex in range(self.parent.tabWidget.count()):
                if self.ui.latticeChoice.currentText() == self.parent.tabWidget.tabText(tabIndex):
                    self.parent.tabWidget.widget(tabIndex).exportToFile(latticeFileName)
                    break
            else:
                errMsg += "  - Could not find tab with name: " + self.ui.latticeChoice.currentText() + '\n'
            deleteLatticeFile = True

        else: # Separate file chosen
            latticeFileName = self.ui.latticeChoice.currentText()
            deleteLatticeFile = False

        beamlineName = self.ui.beamlineDropDown.currentText()
        if not beamlineName:
            errMsg += "  - No beamline selected.\n"

        # Get bunch file
        if self.ui.bunchChoice.currentText() == self.ui.noneBunchChoice:
            errMsg += '  - No bunch file specified.\n'
        elif self.ui.bunchChoice.currentText() in self.tabTitles():
            fileHandle, bunchFileName = tempfile.mkstemp('.sdds')
            os.close(fileHandle)
            for index in range(self.parent.tabWidget.count()):
                if self.parent.tabWidget.tabText(index) == self.ui.bunchChoice.currentText():
                    self.parent.tabWidget.widget(index).widget().saveToSDDS(bunchFileName)
                    deleteBunchFile = True
                    break
        else:
            bunchFileName = self.ui.bunchChoice.currentText()
            deleteBunchFile = False

        if self.ui.orderLineEdit.text() == '':
            errMsg += '  - No default order specified.\n'
        if self.ui.momentumLineEdit.text() == '':
            errMsg += '  - No momentum specified.\n'
        if self.ui.stepsLineEdit.text() == '':
            errMsg += '  - No step number specified.\n'

        if errMsg:
            errMsg = 'Cannot start simulation due to:\n' + errMsg
            msgBox = QMessageBox(QMessageBox.Warning, 'RadTrack', errMsg)
            msgBox.exec_()
            return

        #generate ele file
        self.ui.textEdit.append('Writing .ele file ...')
        outputFileName = os.path.join(self.parent.sessionDirectory, 'elegantFile.ele')
        with open(outputFileName, 'w') as outputFile:
            s = '    '
            outputFile.write('&run_setup\n')
            outputFile.write(s+'lattice = "'+latticeFileName+'",'+'\n')
            outputFile.write(s+'use_beamline = '+beamlineName+','+'\n')
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
            outputFile.write(s+'output_at_each_step=1, \n')
            outputFile.write(s+'statistics =1, concat_order=3, \n')
            outputFile.write(s+'filename = %s.twi \n')
            outputFile.write('&end \n\n')
            outputFile.write('&sdds_beam \n')
            outputFile.write(s+'input = "'+bunchFileName+'",'+'\n')
            outputFile.write('&end \n\n')
            outputFile.write('&matrix_output \n')
            outputFile.write(s+'SDDS_output = %s.mat, SDDS_output_order = 3, output_at_each_step = 1 \n')
            outputFile.write('&end \n\n')
            outputFile.write('&track \n')
            outputFile.write('&end \n\n')
            outputFile.write('&stop \n')
            outputFile.write('&end \n\n')

        self.ui.textEdit.append('Running simulations ...')

        if not os.getenv('RPN_DEFNS', None):
            os.environ['RPN_DEFNS'] = resource.filename('defns.rpn')

        subprocess.call(['elegant', outputFileName])

        self.ui.textEdit.append('Simulation complete!\n')

        self.ui.textEdit.append('Generated files:')
        for fileName in glob.glob(os.path.splitext(outputFileName)[0] + '*'):
            self.ui.textEdit.append(fileName)


def run():

    app = QtGui.QApplication(sys.argv)
    ex = RbEle()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
