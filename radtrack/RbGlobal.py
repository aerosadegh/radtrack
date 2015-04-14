"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

"""
import sys, os, tempfile, shutil

import argh
import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui
from datetime import datetime

from radtrack.ui.globalgu import Ui_globalgu, _translate
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
from radtrack.RbUtility import getRealWidget

class RbGlobal(QtGui.QMainWindow):
    def __init__(self, beta_test=False):
        self.beta_test=beta_test
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_globalgu()
        self.ui.setupUi(self)

        default_font = QtGui.QFont("Times", 10)
        QtGui.QApplication.setFont(default_font)

        self.lastUsedDirectory = os.path.expanduser('~').replace('\\', '\\\\')

        if sys.platform == 'win32':
            self.configDirectory = os.path.join(os.getenv('APPDATA'), 'RadTrack')
        else:
            self.configDirectory = os.path.join(os.path.expanduser('~'), '.radtrack')
        try:
            os.makedirs(self.configDirectory)
        except OSError:
            pass

        # Read recent files and projects
        self.recentFile = os.path.join(self.configDirectory, 'recent')
        try:
            with open(self.recentFile) as f:
                for line in f:
                    self.addToRecentMenu(line.strip())
        except IOError: # self.recentFile doesn't exist
            return

        session = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.sessionDirectory = os.path.join(os.path.expanduser('~'), 'RadTrack', session)
        try:
            os.makedirs(self.sessionDirectory)
        except OSError:
            pass

        self.setTitleBar("RadTrack - " + self.sessionDirectory)

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

            self.tabWidget.addTab(RbGenesisTransport(self), self.tr('Genesis Transport'))
            
            self.stackwidget = QtGui.QStackedWidget(self)
            self.stackwidget.addWidget(rbsrwmulti(self))
            self.stackwidget.addWidget(rbsrwsingle(self))
            self.srw_particle = QtGui.QCheckBox(self)
            self.srw_particle.setText('Single-Particle')
            srwidget = QtGui.QWidget(self)
            layout = QtGui.QVBoxLayout(srwidget)
            srwidget.setLayout(layout)
            layout.addWidget(self.srw_particle)
            layout.addWidget(self.stackwidget)
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
            actionNew_Tab = QtGui.QAction(self)
            actionNew_Tab.setObjectName('new ' + originalTitle)
            actionNew_Tab.setText(originalTitle)

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
            actionNew_Tab.triggered.connect(lambda ignore, t = widgetType : self.newTab(t))

            self.ui.menuNew_Tab.addAction(actionNew_Tab)

        self.ui.actionOpen_Project.triggered.connect(lambda : self.openProject())
        self.ui.actionSet_Current_Project_Location.triggered.connect(self.setProjectLocation)
        self.ui.actionOpen_New_RadTrack_Window.triggered.connect(lambda : RbGlobal().show())
        self.ui.actionImport_File.triggered.connect(lambda : self.importFile())
        self.ui.actionExport_Current_Tab.triggered.connect(self.exportCurrentTab)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionRedo.triggered.connect(self.redo)
        self.ui.actionClose_Current_Tab.triggered.connect(lambda : self.closeTab(None))
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.ui.actionReopen_Closed_Tab.triggered.connect(self.undoCloseTab)
        self.ui.actionRename_Current_Tab.triggered.connect(self.renameTab)
        self.tabWidget.currentChanged.connect(self.checkMenus)

        QtGui.QShortcut(QtGui.QKeySequence.Undo, self).activated.connect(self.undo)
        QtGui.QShortcut(QtGui.QKeySequence.Redo, self).activated.connect(self.redo)

        self.closedTabs = []

        self.checkMenus()
        
    def setTitleBar(self, text):
        self.setWindowTitle(_translate("globalgu", text, None))

    def addToRecentMenu(self, name):
        if not name:
            return

        menuSelect = QtGui.QAction(os.path.basename(name), self)
        menuSelect.setObjectName(name)

        if os.path.isdir(name):
            menu = self.ui.menuRecent_Projects
            menuSelect.triggered.connect(lambda ignore, f = name : self.openProject(f))
        elif os.path.isfile(name):
            menu = self.ui.menuRecent_Files
            menuSelect.triggered.connect(lambda ignore, f = name : self.importFile(f))
        else:
            return

        oldList = menu.actions()
        menu.clear()
        menu.addAction(menuSelect)
        for action in [a for a in oldList if a.objectName() != name]:
            menu.addAction(action)

    def togglesrw(self):
        self.stackwidget.setCurrentIndex(int(self.srw_particle.isChecked()))
        print self.stackwidget.currentIndex()
        print int(self.srw_particle.isChecked())

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

    def undoCloseTab(self):
        widget, index, title = self.closedTabs.pop()
        self.tabWidget.insertTab(index, widget, title)
        self.checkMenus()
        self.tabWidget.setCurrentIndex(index)
        self.checkMenus()

    def renameTab(self):
        index = self.tabWidget.currentIndex()
        newName, ok = QtGui.QInputDialog.getText(self, "Rename Tab", 'New name for "' + self.tabWidget.tabText(index) + '"')

        if ok and newName:
            self.tabWidget.setTabText(index, self.uniqueTabTitle(newName, index))
            self.checkMenus()

    def importFile(self, openFile = None):
        if not openFile:
            openFile = QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.lastUsedDirectory,
                    "All Files (*.*);;" +
                    "Laser Transport (*.rad);;" +
                    "Charged Beam Transport (*.lte);;" +
                    "SDDS (*.sdds);;" +
                    "SRW (*.srw)")
            if not openFile:
                return
        self.lastUsedDirectory = os.path.dirname(openFile)

        ext = os.path.splitext(openFile)[-1].lower().lstrip(".") # lowercased extension after '.'

        # Find all types of tabs that accept file type "ext"
        choices = []
        for widgetType in self.widgetChoices:
            try:
                if ext in widgetType().acceptsFileTypes:
                    choices.append(widgetType)
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
                    self.addToRecentMenu(openFile)
                    return
            except IndexError: # Cancel was pressed
                return

        # Make a new tab
        self.newTab(destinationType)
        getRealWidget(self.tabWidget.currentWidget()).importFile(openFile)
        self.addToRecentMenu(openFile)

    def setProjectLocation(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                'Choose folder to store project',
                self.sessionDirectory)
        if not directory:
            return

        if os.listdir(directory):
            box = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'File Overwrite Warning',
                    'The chosen directory is not empty.\n' + \
                    'Do you wish to create a new "RadTrack" folder there?')
            newFolder = box.addButton('Create "RadTrack" folder', QtGui.QMessageBox.ActionRole)
            cancel = box.addButton('Cancel location change', QtGui.QMessageBox.ActionRole)
            box.exec_()
            if box.clickedButton() == cancel:
                return

            directory = os.path.join(directory, 'RadTrack')
            if os.path.lexists(directory):
                count = 1
                while os.path.lexists(directory + '_' + str(count)):
                    count += 1
                directory = directory + '_' + count

        os.makedirs(directory)
        for thing in os.listdir(self.sessionDirectory):
            thingPath = os.path.join(self.sessionDirectory, thing)
            try:
                shutil.move(thingPath, directory)
            except shutil.Error:
                shutil.copy2(thingPath, directory)
                os.remove(thingPath)
        os.rmdir(self.sessionDirectory)
        self.sessionDirectory = directory
        self.saveProject()
        self.setTitleBar('RadTrack - ' + self.sessionDirectory)


    def openProject(self, directory = None):
        if directory is None or directory == '':
            directory = QtGui.QFileDialog.getExistingDirectory(self,
                    'Open project folder',
                    self.lastUsedDirectory)
            if not directory:
                return

        self.saveProject()

        self.addToRecentMenu(self.sessionDirectory)

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

        self.setTitleBar('RadTrack - ' + self.sessionDirectory)


    def saveProject(self):
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

    def exportCurrentTab(self):
        getRealWidget(self.tabWidget.currentWidget()).exportToFile()

    def allWidgets(self):
        return [getRealWidget(self.tabWidget.widget(i)) for i in range(self.tabWidget.count())]

    def checkMenus(self):
        menuMap = dict()
        menuMap['exportToFile'] = self.ui.actionExport_Current_Tab
        menuMap['undo'] = self.ui.actionUndo
        menuMap['redo'] = self.ui.actionRedo
        for function in menuMap:
            menuMap[function].setEnabled(hasattr(getRealWidget(self.tabWidget.currentWidget()), function))
        self.ui.actionReopen_Closed_Tab.setEnabled(len(self.closedTabs) > 0)

        # Configure Elegant tab to use tabs for simulation input
        for widget in self.allWidgets():
            if type(widget) == RbEle:
                widget.update_sources_from_tabs()

    def undo(self):
        getRealWidget(self.tabWidget.currentWidget()).undo()

    def redo(self):
        getRealWidget(self.tabWidget.currentWidget()).redo()

    def closeEvent(self, event):
        self.saveProject()
        event.accept()
        QtGui.QMainWindow.closeEvent(self, event)
        self.addToRecentMenu(self.sessionDirectory)

        with open(self.recentFile, 'w') as f:
            f.write('\n'.join([action.objectName() for action in self.ui.menuRecent_Projects.actions()]))
            f.write('\n')
            f.write('\n'.join([action.objectName() for action in self.ui.menuRecent_Files.actions()]))


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
