"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

"""
import sys, os, tempfile, shutil

import argh
import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui
from datetime import datetime

from radtrack.globalgu import Ui_globalgu
from radtrack.LaserTab import LaserTab
from radtrack.rbdcp import RbDcp
from radtrack.RbBunchTransport import RbBunchTransport
from radtrack.RbLaserTransport import RbLaserTransport
from radtrack.RbGenesisTransport import RbGenesisTransport
from radtrack.BunchTab import BunchTab
from radtrack.RbEle import RbEle
from radtrack.RbFEL import RbFEL
from radtrack.RbSimulations import RbSimulations
from radtrack.srw.RbSrwUndulator import srwund
from radtrack.genesis.rbgenesis2 import RbGenesis2
from radtrack.RbSrwsingleA import rbsrw as rbsrwsingle
from radtrack.RbSrwmultiA import rbsrw as rbsrwmulti

class RbGlobal(QtGui.QMainWindow):
    def __init__(self, beta_test=False):
        self.beta_test=beta_test
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_globalgu()
        self.ui.setupUi(self)

        default_font = QtGui.QFont("Times", 10)
        QtGui.QApplication.setFont(default_font)

        self.lastUsedDirectory = os.path.expanduser('~').replace('\\', '/')

        session = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.sessionDirectory = os.path.join(os.path.expanduser('~'), 'RadTrack', session)
        if not os.path.exists(self.sessionDirectory):
            os.makedirs(self.sessionDirectory)

        self.recentfile = None

        self.ui = Ui_globalgu()
        self.ui.setupUi(self)
        self.setWindowTitle('RadTrack')

        self.tabWidget = QtGui.QTabWidget()
        self.ui.verticalLayout.addWidget(self.tabWidget)
        self.tabWidget.setTabsClosable(True)
        self.tabPrefix = '###Tab###' # used to identify files that are the saved data from tabs

        if not beta_test:
            scrollArea = QtGui.QScrollArea(self)
            scrollArea.setWidget(LaserTab(self))
            self.tabWidget.addTab(scrollArea, self.tr('Laser'))

            self.tabWidget.addTab(RbLaserTransport(self), self.tr('Laser Transport'))

        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setWidget(BunchTab(self))
        self.tabWidget.addTab(scrollArea, self.tr('Bunch'))

        self.tabWidget.addTab(RbBunchTransport(self), self.tr('Bunch Transport'))

        #if not beta_test:
        #    scrollArea = QtGui.QScrollArea(self)
        #    scrollArea.setWidget(RbSimulations(self))
        #    self.tabWidget.addTab(scrollArea,self.tr('Interactions'))

        self.tabWidget.addTab(RbEle(self), self.tr('Elegant'))

        self.tabWidget.addTab(RbDcp(self), self.tr('Data Visualization'))
        

        if not beta_test:
            self.tabWidget.addTab(RbFEL(self), self.tr('FEL'))

            scrollArea = QtGui.QScrollArea(self)
            scrollArea.setWidget(RbGenesis2(self))
            self.tabWidget.addTab(scrollArea, self.tr('Genesis'))

            '''scrollArea = QtGui.QScrollArea(self)
            scrollArea.setWidget(rbsrwsingle(self))
            self.tabWidget.addTab(scrollArea, self.tr('SRW-single-electron'))

            scrollArea = QtGui.QScrollArea(self)
            scrollArea.setWidget(rbsrwmulti(self))
            self.tabWidget.addTab(scrollArea, self.tr('SRW-Multi-electron'))'''

            self.tabWidget.addTab(RbGenesisTransport(self), self.tr('Genesis Transport'))
            
            self.stackwidget = QtGui.QStackedWidget(self)
            self.stackwidget.addWidget(rbsrwmulti(self))
            self.stackwidget.addWidget(rbsrwsingle(self))
            self.srw_particle = QtGui.QCheckBox(self)
            self.srw_particle.setText('Single-Particle')
            layout = QtGui.QVBoxLayout(self)
            layout.addWidget(self.srw_particle)
            layout.addWidget(self.stackwidget)
            srwidget = QtGui.QWidget(self)
            srwidget.setLayout(layout)
            self.tabWidget.addTab(srwidget, self.tr('SRW'))
            self.srw_particle.stateChanged.connect(self.togglesrw)


        # Information for making new tabs and importing files
        self.originalNameToTabType = dict()
        self.tabTypeToOriginalName = dict()
        self.usesScrollArea = dict()
        self.widgetChoices = []
        for index in range(self.tabWidget.count()):
            widget = self.tabWidget.widget(index)
            realWidget = getRealWidget(widget)
            widgetType = type(realWidget)
            originalTitle = self.tabWidget.tabText(index)
            self.originalNameToTabType[originalTitle] = widgetType
            self.tabTypeToOriginalName[widgetType] = originalTitle
            self.usesScrollArea[type(realWidget)] = (widget != realWidget)
            self.widgetChoices.append(type(realWidget))

            # populate New Tab Menu
            actionNewTab = QtGui.QAction(self)
            actionNewTab.setObjectName('new ' + originalTitle)
            actionNewTab.setText(originalTitle)

            # The next line has some weirdness that needs explaining:
            #  1. "ignore" is a variable that receives the boolean returned
            #     from QAction.triggered(). This variable is not used, hence
            #     the name. This goes for all "lambda ignore" below.
            #  2. "t = widgetType" sets t to the current widgetType if the
            #     QAction.triggered() doesn't supply it (which it doesn't).
            #     This localizes widgetType to the lambda in this loop iteration.
            #     Just using self.newTab(widgetType) would have the argument
            #     replaced every iteration, so that every selection in the
            #     Tabs->New Tab menu would result in a new copy of the last
            #     tab added.
            actionNewTab.triggered.connect(lambda ignore, t = widgetType : self.newTab(t))

            self.ui.menuNewTab.addAction(actionNewTab)

        self.ui.actionOpen.triggered.connect(lambda : self.openProject())
        self.ui.actionSetLocation.triggered.connect(self.setProjectLocation)
        self.ui.actionNewInstance.triggered.connect(lambda : RbGlobal().show())
        self.ui.actionImport.triggered.connect(lambda : self.importFile())
        self.ui.actionExport.triggered.connect(self.exportCurrentTab)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionRedo.triggered.connect(self.redo)
        self.ui.actionCloseTab.triggered.connect(lambda : self.closeTab(None))
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.ui.actionUndoCloseTab.triggered.connect(self.undoCloseTab)
        self.ui.actionRenameTab.triggered.connect(self.renameTab)
        self.tabWidget.currentChanged.connect(self.checkMenus)

        QtGui.QShortcut(QtGui.QKeySequence.Undo, self).activated.connect(self.undo)
        QtGui.QShortcut(QtGui.QKeySequence.Redo, self).activated.connect(self.redo)

        self.closedTabs = []
        self.globalHasChanged = False

        self.checkMenus()
        
    def togglesrw(self):
        self.stackwidget.setCurrentIndex(int(self.srw_particle.isChecked()))
        print self.stackwidget.currentIndex()
        print int(self.srw_particle.isChecked())

    def populateRecentFile(self):
        action = QtGui.QAction(self)
        action.setObjectName(self.recentfile)
        action.setText(self.recentfile)
        self.ui.menurecent.addAction(action)
        #action.triggered.connect(self.importFile(action.text()))

    def newTab(self, newTabType):
        newTitle = self.uniqueTabTitle(self.tabTypeToOriginalName[newTabType])
        if self.usesScrollArea[newTabType]:
            scrollArea = QtGui.QScrollArea(self)
            scrollArea.setWidget(newTabType(self))
            self.tabWidget.addTab(scrollArea, newTitle)
        else:
            self.tabWidget.addTab(newTabType(self), newTitle)
        self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
        self.checkMenus()
        self.globalHasChanged = True

    def uniqueTabTitle(self, title, ignoreIndex = -1):
        originalTitle = title
        number = 0
        currentTitles = [self.tabWidget.tabText(i).replace("&", "") for i in range(self.tabWidget.count()) if i != ignoreIndex]
        while title in currentTitles:
            number = number + 1
            title = originalTitle + ' ' + str(number)
        return title.strip()

    def closeTab(self, index = None):
        if index == None:
            index = self.tabWidget.currentIndex()
        self.closedTabs.append((self.tabWidget.widget(index),
                                index,
                                self.tabWidget.tabText(index)))
        self.tabWidget.removeTab(index)
        self.checkMenus()
        self.globalHasChanged = True

    def undoCloseTab(self):
        widget, index, title = self.closedTabs.pop()
        self.tabWidget.insertTab(index, widget, title)
        self.checkMenus()
        self.tabWidget.setCurrentIndex(index)
        self.globalHasChanged = True
        self.checkMenus()

    def renameTab(self):
        index = self.tabWidget.currentIndex()
        newName, ok = QtGui.QInputDialog.getText(self, "Rename Tab", 'New name for "' + self.tabWidget.tabText(index) + '"')

        if ok and newName:
            self.tabWidget.setTabText(index, self.uniqueTabTitle(newName, index))
            self.globalHasChanged = True
            self.checkMenus()


    def importFile(self, openFile = None):
        if not openFile:
            openFile = QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.lastUsedDirectory,
                    "All Files (*.*);;" +
                    "Laser Transport (*.rad);;" +
                    "Charged Beam Transport (*.lte);;" +
                    "SDDS (*.sdds);;" +
                    "SRW (*.srw)")
            if openFile == '':
                return
            self.lastUsedDirectory = os.path.dirname(openFile)

        ext = os.path.splitext(openFile)[-1].lower().lstrip(".") # lowercased extension after '.'

        # Find all types of tabs that accept file type "ext"
        choices = []
        for possibleWidget in [widget(self) for widget in self.widgetChoices]:
            try:
                if ext in possibleWidget.acceptsFileTypes:
                    choices.append(type(possibleWidget))
            except AttributeError:
                pass

        if len(choices) == 0:
            QtGui.QMessageBox.warning(self, 'Import Error', 'No suitable tab for file:\n' + openFile)
            return

        elif len(choices) == 1:
            destinationType = choices[0]

        else: # len(choices) > 1
            box = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'Ambiguous Import Destination', 'Multiple tab types can import this file.\nWhich kind of tab should be used?')
            responses = [box.addButton(widgetType.__name__, QtGui.QMessageBox.ActionRole) for widgetType in choices] + [box.addButton(QtGui.QMessageBox.Cancel)]
            box.exec_()
            try:
                destinationType = choices[responses.index(box.clickedButton())]
            except IndexError:
                return # Cancel selected

        # Check if a tab of this type is already open
        openWidgetIndexes = [i for i in range(self.tabWidget.count()) if type(getRealWidget(self.tabWidget.widget(i))) == destinationType]
        if openWidgetIndexes:
            choices = [self.tabWidget.tabText(i) for i in openWidgetIndexes] + ['New Tab']
            box = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'Choose Import Destination', 'Which tab should receive the data?')
            responses = [box.addButton(widgetType, QtGui.QMessageBox.ActionRole) for widgetType in choices] + [box.addButton(QtGui.QMessageBox.Cancel)]

            box.exec_()
            destinationIndex = responses.index(box.clickedButton())
            try:
                if choices[destinationIndex] != 'New Tab': # Pre-existing tab
                    destination = getRealWidget(self.tabWidget.widget(openWidgetIndexes[destinationIndex]))
                    destination.importFile(openFile)
                    self.tabWidget.setCurrentWidget(destination)
                    return
            except IndexError: # Cancel was pressed
                return

        # Make a new tab
        self.newTab(destinationType)
        getRealWidget(self.tabWidget.currentWidget()).importFile(openFile)


    def setProjectLocation(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                'Choose folder to store project',
                self.sessionDirectory)
        if not directory:
            return

        if set(os.listdir(self.sessionDirectory)).intersection(os.listdir(directory)):
            box = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'File Overwrite Warning',
                    'There are files in this directory with the same name\nas files in the original project folder. Do you wish\nto overwrite these files?')
            ok = box.addButton('Continue and overwrite files', QtGui.QMessageBox.ActionRole)
            cancel = box.addButton('Cancel and preserve files', QtGui.QMessageBox.ActionRole)
            box.exec_()
            if box.clickedButton() == cancel:
                return

        for thing in os.listdir(self.sessionDirectory):
            try:
                shutil.move(os.path.join(self.sessionDirectory, thing), directory)
            except shutil.Error:
                shutil.copy2(os.path.join(self.sessionDirectory, thing), directory)
                os.remove(os.path.join(self.sessionDirectory, thing))
        os.rmdir(self.sessionDirectory)
        self.sessionDirectory = directory
        self.saveProjectFile()


    def openProject(self, directory = None):
        if directory is None or directory == '':
            directory = QtGui.QFileDialog.getExistingDirectory(self,
                    'Open project folder',
                    self.lastUsedDirectory)
            if not directory:
                return

        self.saveProjectFile()

        self.sessionDirectory = directory
        self.lastUsedDirectory = directory

        # Load tab data
        self.tabWidget.clear()
        for i, subFileName in enumerate(sorted( \
                [os.path.join(self.sessionDirectory, fn) for fn in os.listdir(self.sessionDirectory) if fn.startswith(self.tabPrefix)])):
            _, _, originalTitle, tabName = os.path.basename(subFileName).split('_')
            tabName = tabName.rsplit(".", 1)[0]
            self.newTab(self.originalNameToTabType[originalTitle])
            getRealWidget(self.tabWidget.widget(i)).importFile(subFileName)
            self.tabWidget.setTabText(i, tabName)

    def saveProjectFile(self):
        # Delete previous tab data in self.sessionDirectory
        for fileName in os.listdir(self.sessionDirectory):
            if fileName.startswith(self.tabPrefix):
                os.remove(os.path.join(self.sessionDirectory, fileName))

        saveProgress = QtGui.QProgressDialog('Saving project ...', 'Cancel', 0, self.tabWidget.count()-1)
        saveProgress.setValue(0)
        padding = len(str(self.tabWidget.count()))
        for i in range(self.tabWidget.count()):
            if saveProgress.wasCanceled():
                return

            widget = getRealWidget(self.tabWidget.widget(i))
            try:
                subExtension = widget.acceptsFileTypes[0]
                subFileName  = os.path.join(self.sessionDirectory,
                    '_'.join([self.tabPrefix,
                              str(i).rjust(padding, '0'),
                              self.tabTypeToOriginalName[type(widget)],
                              self.tabWidget.tabText(i) + '.' + subExtension]))
                widget.exportToFile(subFileName)
                saveProgress.setValue(saveProgress.value()+1)
            except AttributeError as e: # skip tabs without file extensions
                print 'ERROR: Skipping ' + self.tabWidget.tabText(i)
                print e
                saveProgress.setValue(saveProgress.value()+1)
                continue

        self.globalHasChanged = False

    def exportCurrentTab(self):
        getRealWidget(self.tabWidget.currentWidget()).exportToFile()
        self.populateRecentFile()

    def allWidgets(self):
        return [getRealWidget(self.tabWidget.widget(i)) for i in range(self.tabWidget.count())]

    def checkMenus(self):
        menuMap = dict()
        menuMap['exportToFile'] = self.ui.actionExport
        menuMap['undo'] = self.ui.actionUndo
        menuMap['redo'] = self.ui.actionRedo
        for function in menuMap:
            menuMap[function].setEnabled(hasattr(getRealWidget(self.tabWidget.currentWidget()), function))
        self.ui.actionUndoCloseTab.setEnabled(len(self.closedTabs) > 0)

        # Configure Elegant tab to use tabs for simulation input
        for widget in self.allWidgets():
            if type(widget) == RbEle:
                oldBeamlineChoice = widget.ui.beamLineComboBox.currentText()

                oldBunchChoice = widget.ui.bunchSourceComboBox.currentText()
                widget.ui.bunchSourceComboBox.clear()

                oldLatticeChoice = widget.ui.beamLineSourceComboBox.currentText()
                widget.ui.beamLineSourceComboBox.clear()

                widget.ui.bunchSourceComboBox.addItem(widget.noneBunchChoice)
                widget.ui.beamLineSourceComboBox.addItem(widget.noneBeamChoice)

                for index in range(self.tabWidget.count()):
                    if type(getRealWidget(self.tabWidget.widget(index))) == BunchTab:
                        widget.ui.bunchSourceComboBox.addItem(self.tabWidget.tabText(index))
                    elif type(getRealWidget(self.tabWidget.widget(index))) == RbBunchTransport:
                        widget.ui.beamLineSourceComboBox.addItem(self.tabWidget.tabText(index))

                widget.ui.bunchSourceComboBox.addItem(widget.fileBunchChoice)
                widget.ui.beamLineSourceComboBox.addItem(widget.fileBeamChoice)

                # Reselect the previous user's choice
                widget.ui.bunchSourceComboBox.setCurrentIndex(widget.ui.bunchSourceComboBox.findText(oldBunchChoice))
                widget.ui.beamLineSourceComboBox.setCurrentIndex(widget.ui.beamLineSourceComboBox.findText(oldLatticeChoice))
                widget.ui.beamLineComboBox.setCurrentIndex(widget.ui.beamLineComboBox.findText(oldBeamlineChoice))


    def hasChanged(self):
        if self.globalHasChanged:
            return True

        for widget in self.allWidgets():
            try:
                if widget.hasChanged():
                    return True
            except AttributeError:
                print('*** ' + type(widget).__name__ + " has no hasChanged() method")
        return False


    def undo(self):
        getRealWidget(self.tabWidget.currentWidget()).undo()
        self.globalHasChanged = True

    def redo(self):
        getRealWidget(self.tabWidget.currentWidget()).redo()
        self.globalHasChanged = True

    def closeEvent(self, event):
        self.saveProjectFile()
        event.accept()
        QtGui.QMainWindow.closeEvent(self, event)


def getRealWidget(widget):
    try:
        return getRealWidget(widget.widget())
    except AttributeError:
        return widget


@argh.arg('project_file', nargs='?', default=None, help='project file to open at startup')
def main(project_file, beta_test=False):
    """Entry point into RadTrack Application

    Args:
        project_file (str, optional): Name of the project file to open at startup
        beta_test (bool, False): Open only those tabs consider to be Beta ready

    Raises:
        SystemExit: When Qt exits, calls `sys.exit`.
    """
    # We handle arguments with argh so only pass program to Qt
    app = QtGui.QApplication([sys.argv[0]])
    myapp = RbGlobal(beta_test=beta_test)
    if project_file:
        myapp.openProjectFile(project_file)
    myapp.show()
    sys.exit(app.exec_())

def call_main():
    p = argh.ArghParser()
    argh.set_default_command(p, main)
    argh.dispatch(p)

if __name__ == '__main__':
    call_main()
