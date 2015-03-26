"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

"""
import sys, os, tempfile, shutil
from zipfile import ZipFile

import argh
import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui
from datetime import datetime

from  radtrack.globalgu import Ui_globalgu
from  radtrack.RbLaserWindow import RbLaserWindow
from  radtrack.rbdcp import RbDcp
from  radtrack.RbBunchTransport import RbBunchTransport
from  radtrack.RbLaserTransport import RbLaserTransport
from  radtrack.RbGenesisTransport import RbGenesisTransport
from  radtrack.RbBunchWindow import RbBunchWindow
from  radtrack.RbEle import RbEle
from  radtrack.RbFEL import RbFEL
from  radtrack.RbSimulations import RbSimulations
from radtrack.srw.RbSrwUndulator import srwund
from radtrack.genesis.rbgenesis2 import RbGenesis2
from  radtrack.RbSrwsingle import rbsrw as rbsrwsingle
from  radtrack.RbSrwmulti import rbsrw as rbsrwmulti

class RbGlobal(QtGui.QMainWindow):
    #Constructor
    def __init__(self, beta_test=False):
        self.beta_test=beta_test
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_globalgu()
        self.ui.setupUi(self)

        self.lastUsedDirectory = os.path.expanduser('~').replace('\\', '/')
        session = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.sessionDirectory = os.path.join(os.path.expanduser('~'), 'RadTrack', session).replace('\\', '/')
        if not os.path.exists(self.sessionDirectory):
            os.makedirs(self.sessionDirectory)
        self.fileExtension = '.radtrack'
        self.recentfile = None

        self.ui = Ui_globalgu()
        self.ui.setupUi(self)
        self.setWindowTitle('RadTrack')

        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.setTabsClosable(True)

        if not beta_test:
            scrollArea = QtGui.QScrollArea(self)
            scrollArea.setWidget(RbLaserWindow(self))
            self.tabWidget.addTab(scrollArea, self.tr('Laser'))

            self.tabWidget.addTab(RbLaserTransport(self), self.tr('Laser Transport'))

        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setWidget(RbBunchWindow(self))
        self.tabWidget.addTab(scrollArea, self.tr('Bunch'))

        self.tabWidget.addTab(RbBunchTransport(self), self.tr('Bunch Transport'))

        if not beta_test:
            scrollArea = QtGui.QScrollArea(self)
            scrollArea.setWidget(RbSimulations(self))
            self.tabWidget.addTab(scrollArea,self.tr('Interactions'))

        self.tabWidget.addTab(RbEle(self), self.tr('Elegant'))

        self.tabWidget.addTab(RbDcp(self), self.tr('Data Visualization'))

        if not beta_test:
            self.tabWidget.addTab(RbFEL(self), self.tr('FEL'))

            scrollArea3 = QtGui.QScrollArea(self)
            scrollArea3.setWidget(srwund(self))
            self.tabWidget.addTab(scrollArea3,self.tr('SRW'))

            scrollArea = QtGui.QScrollArea(self)
            scrollArea.setWidget(RbGenesis2(self))
            self.tabWidget.addTab(scrollArea, self.tr('Genesis'))

            scrollArea = QtGui.QScrollArea(self)
            scrollArea.setWidget(rbsrwsingle(self))
            self.tabWidget.addTab(scrollArea, self.tr('SRW-single-electron'))

            scrollArea = QtGui.QScrollArea(self)
            scrollArea.setWidget(rbsrwmulti(self))
            self.tabWidget.addTab(scrollArea, self.tr('SRW-Multi-electron'))

            self.tabWidget.addTab(RbGenesisTransport(self), self.tr('Genesis Transport'))


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

        self.ui.verticalLayout.addWidget(self.tabWidget)
        self.ui.actionOpen.triggered.connect(lambda : self.openProjectFile())
        self.ui.actionSave.triggered.connect(self.saveProjectFile)
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


    def openProjectFile(self, fileName = None):
        if fileName is None or fileName == '':
            fileName = QtGui.QFileDialog.getOpenFileName(self,
                    'Open file',
                    self.lastUsedDirectory,
                    '*' + self.fileExtension)
            if fileName == '':
                return

        # Open a new window if user has worked in the current one
        if self.hasChanged():
            dest = RbGlobal()
            dest.show()
        else:
            dest = self

        dest.tabWidget.clear()

        with ZipFile(fileName, 'r') as zf:
            for i, subFileName in enumerate(zf.namelist()):
                print subFileName
                zf.extract(subFileName)
                _, originalTitle, tabName = os.path.basename(subFileName).split('_')
                tabName = tabName.rsplit(".", 1)[0]
                dest.newTab(self.originalNameToTabType[originalTitle])
                getRealWidget(dest.tabWidget.widget(i)).importFile(subFileName)
                dest.tabWidget.setTabText(i, tabName)
                os.remove(subFileName)
        dest.lastUsedDirectory = os.path.dirname(fileName)

    def saveProjectFile(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                'Save Project',
                self.lastUsedDirectory,
                '*' + self.fileExtension)
        if fileName == '':
            return
        if not fileName.endswith(self.fileExtension):
            fileName = fileName + self.fileExtension

        tempFileName = fileName + '.partial'
        with ZipFile(tempFileName, 'w') as zf:
            saveProgress = QtGui.QProgressDialog('Saving as ' + fileName + ' ...',
                    'Cancel',
                    0,
                    self.tabWidget.count()-1)
            saveProgress.setValue(0)
            padding = len(str(self.tabWidget.count()))
            for i in range(self.tabWidget.count()):
                if saveProgress.wasCanceled():
                    return

                widget = getRealWidget(self.tabWidget.widget(i))
                try:
                    subExtension = widget.acceptsFileTypes[0]
                    subFileHandle, subFileName = tempfile.mkstemp(subExtension)
                except AttributeError as e: # skip tabs without file extensions
                    print 'ERROR: Skipping ' + self.tabWidget.tabText(i)
                    print e
                    saveProgress.setValue(saveProgress.value()+1)
                    continue
                os.close(subFileHandle)

                try:
                    print self.tabWidget.tabText(i)
                    widget.exportToFile(subFileName)
                    zf.write(subFileName, str(i).rjust(padding, '0')
                                          + '_'
                                          + self.tabTypeToOriginalName[type(widget)]
                                          + '_'
                                          + self.tabWidget.tabText(i)
                                          + "."
                                          + subExtension)
                    saveProgress.setValue(saveProgress.value()+1)
                except Exception as e:
                    print 'Error saving ' + widget.__class__.__name__
                    print e
                    saveProgress.reset()
                    if type(e) is not AttributeError:
                        raise
                finally:
                    os.remove(subFileName)

        shutil.move(tempFileName, fileName)
        self.globalHasChanged = False
        print 'Done.'

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
                oldBeamlineChoice = widget.ui.beamlineDropDown.currentText()

                oldBunchChoice = widget.ui.bunchChoice.currentText()
                widget.ui.bunchChoice.clear()

                oldLatticeChoice = widget.ui.latticeChoice.currentText()
                widget.ui.latticeChoice.clear()

                widget.ui.bunchChoice.addItem(widget.ui.noneBunchChoice)
                widget.ui.latticeChoice.addItem(widget.ui.noneBeamChoice)

                for index in range(self.tabWidget.count()):
                    if type(getRealWidget(self.tabWidget.widget(index))) == RbBunchWindow:
                        widget.ui.bunchChoice.addItem(self.tabWidget.tabText(index))
                    elif type(getRealWidget(self.tabWidget.widget(index))) == RbBunchTransport:
                        widget.ui.latticeChoice.addItem(self.tabWidget.tabText(index))

                widget.ui.bunchChoice.addItem(widget.ui.fileBunchChoice)
                widget.ui.latticeChoice.addItem(widget.ui.fileBeamChoice)

                # Reselect the previous user's choice
                widget.ui.bunchChoice.setCurrentIndex(widget.ui.bunchChoice.findText(oldBunchChoice))
                widget.ui.latticeChoice.setCurrentIndex(widget.ui.latticeChoice.findText(oldLatticeChoice))
                widget.ui.beamlineDropDown.setCurrentIndex(widget.ui.beamlineDropDown.findText(oldBeamlineChoice))


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
        if self.hasChanged():
            saveBox = QtGui.QMessageBox(QtGui.QMessageBox.Question,
                    'RadTrack',
                    'Do you want to save the current project?',
                    QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                    QtGui.QMessageBox.Cancel)
            answer = saveBox.exec_()

            if answer == QtGui.QMessageBox.Save:
                self.saveProjectFile()
            elif answer == QtGui.QMessageBox.Cancel:
                event.ignore()
                return
        event.accept()
        QtGui.QMainWindow.closeEvent(self, event)
        try:
            os.rmdir(self.sessionDirectory) # delete sessionDirectory if it's empty
        except OSError, WindowsError:
            pass # files exist in sessionDirectory, so don't delete


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
