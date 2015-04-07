"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
version 2
"""
import sys, os, subprocess, glob, time

from PyQt4 import QtCore, QtGui
from radtrack.ui.rbele import Ui_ELE
from  radtrack.RbBunchTransport import RbBunchTransport
from  radtrack.BunchTab import BunchTab
from  radtrack.RbUtility import stripComments, convertUnitsNumber, convertUnitsStringToNumber
import radtrack.util.resource as resource

class RbEle(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_ELE()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.simulate)
        self.ui.beamLineSourceComboBox.currentIndexChanged.connect(self.getLTE)
        self.ui.bunchSourceComboBox.currentIndexChanged.connect(self.getBUN)
        self.fileExtension = '.ele'
        self.parent = parent

        self.noneBeamChoice = 'Select beamline source ...'
        self.fileBeamChoice = 'Use another file ...'

        self.noneBunchChoice = 'Select beam bunch source ...'
        self.fileBunchChoice = 'Use another file ...'

        self.generatedFileButtons = []

        if self.parent is None:
            self.parent = self
            self.parent.lastUsedDirectory = os.path.expanduser('~')

        self.loaderCache = dict() # saves the elements from beamline files chosen
                                  # so they don't have to be reloaded every time
                                  # the user chooses that file

    def getBUN(self):
        if self.ui.bunchSourceComboBox.currentText() == self.noneBunchChoice:
            return

        if self.ui.bunchSourceComboBox.currentText() == self.fileBunchChoice:
            sddsfileName = QtGui.QFileDialog.getOpenFileName(self, 'Open',
                    self.parent.lastUsedDirectory, '*.sdds')
            if sddsfileName == '':
                self.ui.bunchSourceComboBox.setCurrentIndex(self.ui.bunchSourceComboBox.findText(self.noneBunchChoice))
                return
            self.parent.lastUsedDirectory = os.path.dirname(sddsfileName)
            # Check if file has already been selected
            index = self.ui.bunchSourceComboBox.findText(sddsfileName)
            if index != -1:
                self.ui.bunchSourceComboBox.setCurrentIndex(index)
            else:
                self.ui.bunchSourceComboBox.addItem(sddsfileName)
                self.ui.bunchSourceComboBox.setCurrentIndex(self.ui.bunchSourceComboBox.count()-1)
        elif self.ui.bunchSourceComboBox.currentText() in self.tabTitles():
            self.ui.momentumLabel.setHidden(True)
            self.ui.momentumLineEdit.setHidden(True)
        else:
            self.ui.momentumLabel.setHidden(False)
            self.ui.momentumLineEdit.setHidden(False)


    def getLTE(self):
        self.ui.beamLineComboBox.clear()

        if self.ui.beamLineSourceComboBox.currentText() in [self.noneBeamChoice, '']:
            return

        elif self.ui.beamLineSourceComboBox.currentText() in self.tabTitles():
            for tabIndex in range(self.parent.tabWidget.count()):
                if self.parent.tabWidget.tabText(tabIndex) == self.ui.beamLineSourceComboBox.currentText():
                    loader = self.parent.tabWidget.widget(tabIndex)

        elif self.ui.beamLineSourceComboBox.currentText() == self.fileBeamChoice:
            fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open',
                    self.parent.lastUsedDirectory, '*.lte')
            if fileName == '':
                self.ui.beamLineSourceComboBox.setCurrentIndex(self.ui.beamLineSourceComboBox.findText(self.noneBeamChoice))
                return
            self.parent.lastUsedDirectory = os.path.dirname(fileName)
            # Check if user already selected a file previously
            if fileName not in self.loaderCache:
                loader = RbBunchTransport()
                loader.importFile(fileName)
                self.loaderCache[fileName] = loader
                self.ui.beamLineSourceComboBox.addItem(fileName)
            self.ui.beamLineSourceComboBox.setCurrentIndex(self.ui.beamLineSourceComboBox.findText(fileName))

            return
            # Setting the currentIndex triggers another signal that runs
            # the else clause below

        else: # previously loaded file
            loader = self.loaderCache[self.ui.beamLineSourceComboBox.currentText()]

        allBeamLines = []
        for element in loader.elementDictionary.values():
            if element.isBeamline() and not element.name.startswith('-'):
                allBeamLines.append(element.name)

        # Reset available beamlines
        self.ui.beamLineComboBox.addItems(allBeamLines)
        self.ui.beamLineComboBox.setCurrentIndex(self.ui.beamLineComboBox.findText(loader.defaultBeamline))

    def tabTitles(self):
        return [self.parent.tabWidget.tabText(i) for i in range(self.parent.tabWidget.count())]

    def simulate(self):
        errMsg = ''
        self.ui.textEdit_2.clear()

        # Get beamline file
        if self.ui.beamLineSourceComboBox.currentText() == self.noneBeamChoice:
            errMsg += '  - No beamline lattice specified.\n'

        elif self.ui.beamLineSourceComboBox.currentText() in self.tabTitles():
            self.ui.textEdit_2.append('Generating beam lattice file ...')
            latticeFileName = os.path.join(self.parent.sessionDirectory, 'elegantSimulation.lte')
            for tabIndex in range(self.parent.tabWidget.count()):
                if self.ui.beamLineSourceComboBox.currentText() == self.parent.tabWidget.tabText(tabIndex):
                    self.parent.tabWidget.widget(tabIndex).exportToFile(latticeFileName)
                    break
            else:
                errMsg += "  - Could not find tab with name: " + self.ui.beamLineSourceComboBox.currentText() + '\n'
            deleteLatticeFile = True

        else: # Separate file chosen
            latticeFileName = self.ui.beamLineSourceComboBox.currentText()
            deleteLatticeFile = False

        beamlineName = self.ui.beamLineComboBox.currentText()
        if not beamlineName:
            errMsg += "  - No beamline selected.\n"

        # Get bunch file
        if self.ui.bunchSourceComboBox.currentText() == self.noneBunchChoice:
            errMsg += '  - No bunch file specified.\n'
        elif self.ui.bunchSourceComboBox.currentText() in self.tabTitles():
            self.ui.textEdit_2.append('Generating beam bunch file ...')
            bunchFileName = os.path.join(self.parent.sessionDirectory, 'elegantSimulation.sdds')
            for index in range(self.parent.tabWidget.count()):
                if self.parent.tabWidget.tabText(index) == self.ui.bunchSourceComboBox.currentText():
                    self.parent.tabWidget.widget(index).widget().saveToSDDS(bunchFileName)
                    deleteBunchFile = True
                    break
        else:
            bunchFileName = self.ui.bunchSourceComboBox.currentText()
            deleteBunchFile = False

        if self.ui.momentumLineEdit.isHidden():
            bunchTabIndex = self.tabTitles().index(self.ui.bunchSourceComboBox.currentText())
            momentum = convertUnitsNumber(self.parent.tabWidget.widget(bunchTabIndex).widget().myBunch.getDesignMomentumEV(), 'eV', 'MeV')
        else:
            if self.ui.momentumLineEdit.text() == '':
                errMsg += '  - No momentum specified.\n'
            else:
                try:
                    momentum = float(self.ui.momentumLineEdit.text())
                except ValueError:
                    try:
                        momentum = convertUnitsStringToNumber(self.ui.momentumLineEdit.text(), 'MeV')
                    except ValueError:
                        errMsg += '  - Unable to parse momentum.\n'

        if errMsg:
            errMsg = 'Cannot start simulation due to:\n' + errMsg
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'RadTrack', errMsg)
            msgBox.exec_()
            return

        #generate ele file
        self.ui.textEdit_2.append('Writing Elegant simulation file ...')
        outputFileName = os.path.join(self.parent.sessionDirectory, 'elegantSimulation.ele')
        with open(outputFileName, 'w') as outputFile:
            s = '    '
            outputFile.write('&run_setup\n')
            outputFile.write(s+'lattice = "'+latticeFileName+'",'+'\n')
            outputFile.write(s+'use_beamline = '+beamlineName+','+'\n')
            outputFile.write(s+'default_order = 2\n')
            outputFile.write(s+'p_central_mev = '+str(momentum)+','+'\n')
            outputFile.write(s+'output = %s.out, \n')
            outputFile.write(s+'centroid = %s.cen, \n')
            outputFile.write(s+'sigma = %s.sig,\n')
            outputFile.write(s+'final = %s.fin,\n')
            outputFile.write(s+'parameters = %s.param,\n')
            outputFile.write(s+'magnets = %s.mag,\n')
            outputFile.write(s+'random_number_seed = 987654321,\n')
            outputFile.write(s+'combine_bunch_statistics = 0,\n')
            outputFile.write(s+'concat_order = 2,\n')
            outputFile.write(s+'tracking_updates = 1,\n') #0
            outputFile.write(s+'echo_lattice = 0 \n')
            outputFile.write('&end \n\n')
            outputFile.write('&run_control \n')
            outputFile.write(s+'n_steps = 1\n')
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
                
        if not os.getenv('RPN_DEFNS', None):
            os.environ['RPN_DEFNS'] = resource.filename('defns.rpn')

        self.ui.textEdit_2.append('Running simulation ...')

        elegantRun = ElegantRunner(outputFileName)
        self.elegantOutputFileName = elegantRun.outputFileName
        self.elegantErrorFileName = elegantRun.errorFileName
        elegantThread = QtCore.QThread(self)
        elegantRun.moveToThread(elegantThread)

        elegantThread.started.connect(elegantRun.start)
        elegantThread.finished.connect(lambda : self.postSimulationResults(outputFileName))
        elegantRun.runFinished.connect(elegantThread.quit)

        elegantThread.start()

        # Sleep for 10 ms to allow thread to run.
        # This is not for allowing time for the simulation to finish, but to get
        # the GUI thread to give up control to allow the simulation thread
        # to proceed. Python doesn't actually have multithreaded capabilities,
        # so hacks like these are necessary.
        time.sleep(0.01)

    def postSimulationResults(self, inputFileName):
        if os.stat(self.elegantErrorFileName).st_size > 0:
            self.ui.textEdit_2.append('Errors reported:')
            with open(self.elegantErrorFileName) as err:
                for line in err:
                    self.ui.textEdit_2.append(line)
        self.ui.textEdit_2.append('Simulation complete!\n')

        while self.generatedFileButtons:
            self.ui.verticalLayout_4.removeWidget(self.generatedFileButtons.pop())

        for i, fileName in enumerate(glob.glob(os.path.splitext(inputFileName)[0] + '*')):
            newButton = QtGui.QPushButton()
            self.generatedFileButtons.append(newButton)
            newButton.setText(os.path.basename(fileName))
            newButton.clicked.connect(lambda ignore, name = newButton.text() : \
                    self.parent.importFile(os.path.join(self.parent.sessionDirectory, name)))
            self.ui.verticalLayout_4.insertWidget(i + 2, newButton)


# This class essentially runs the elegant command line. Wrapping
# it in a class that inherits GObject allows for handing the
# process off to another thread.
class ElegantRunner(QtCore.QObject):
    runFinished = QtCore.pyqtSignal(int)

    def __init__(self, inputFileName):
        QtCore.QObject.__init__(self)
        
        # Required so Elegant will interpret the file name correctly
        self.inputFileName = os.path.realpath(inputFileName).replace('\\', '\\\\')

        self.outputFileName = os.path.join(os.path.dirname(self.inputFileName), 'elegant_output.txt')
        self.errorFileName = os.path.join(os.path.dirname(self.inputFileName), 'elegant_errors.txt')

    def start(self):
        elegantProcess = QtCore.QProcess()
        elegantProcess.setStandardOutputFile(self.outputFileName)
        elegantProcess.setStandardErrorFile(self.errorFileName)
        elegantProcess.start('elegant', [self.inputFileName])
        elegantProcess.waitForFinished()
        self.runFinished.emit(elegantProcess.exitCode())

        
def run():
    app = QtGui.QApplication(sys.argv)
    ex = RbEle()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()               
