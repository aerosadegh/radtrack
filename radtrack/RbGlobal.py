"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import sys, os, tempfile, shutil, argh, string, sip, traceback
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
from radtrack.genesis.rbgenesis2 import RbGenesis2
from radtrack.RbSrwTab import RbSrwTab
from radtrack.RbIntroTab import RbIntroTab
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

        # Create configuration directory
        if sys.platform == 'win32': # Windows
            self.configDirectory = os.path.join(os.getenv('APPDATA'), 'RadTrack')
        else: # Mac/Linux
            self.configDirectory = os.path.join(os.path.expanduser('~'), '.radtrack')
        try:
            os.makedirs(self.configDirectory)
        except OSError: # directory already exists or can't be created
            if not os.path.isdir(self.configDirectory):
                raise OSError('Could not find or create configuration directory: ' + self.configDirectory)
        self.logFile = os.path.join(self.configDirectory, 'error_log.txt')
        sys.excepthook = self.exceptionCapture

        # Read recent files and projects
        self.recentFile = os.path.join(self.configDirectory, 'recent')
        try:
            with open(self.recentFile) as f:
                for line in f:
                    self.addToRecentMenu(line.strip())
        except IOError: # self.recentFile doesn't exist
            pass

        session = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.sessionDirectory = os.path.join(os.path.expanduser('~'), 'RadTrack', session)
        try:
            os.makedirs(self.sessionDirectory)
        except OSError:
            pass

        self.setTitleBar("RadTrack - " + self.sessionDirectory)

        # Create tab widget and all tabs
        self.closedTabs = []
        self.tabWidget = QtGui.QTabWidget()
        self.ui.verticalLayout.addWidget(self.tabWidget)
        self.tabWidget.setTabsClosable(True)
        self.tabPrefix = '###Tab###' # used to identify files that are the saved data from tabs

        if self.beta_test:
            self.availableTabTypes = [ RbIntroTab,
                                       RbEle,
                                       BunchTab,
                                       RbBunchTransport,
                                       RbDcp,
                                       RbFEL ]
        else:
            self.availableTabTypes = [ RbIntroTab,
                                       LaserTab,
                                       RbLaserTransport,
                                       BunchTab,
                                       RbBunchTransport,
                                       RbEle,
                                       RbDcp,
                                       RbFEL,
                                       RbGenesis2,
                                       RbGenesisTransport,
                                       RbSrwTab ]

        self.originalNameToTabType = dict()
        for tabType in self.availableTabTypes:
            if not self.beta_test or tabType == RbIntroTab: # For development, show all tabs
                self.newTab(tabType)

            self.originalNameToTabType[tabType.defaultTitle] = tabType

            # populate New Tab Menu
            actionNew_Tab = QtGui.QAction(self)
            actionNew_Tab.setObjectName('new ' + tabType.defaultTitle)
            actionNew_Tab.setText(tabType.defaultTitle)

            # The next line has some weirdness that needs explaining:
            #  1. "ignore" is a variable that receives the boolean returned
            #     from QAction.triggered(). This variable is not used, hence
            #     the name. This goes for all "lambda ignore" below.
            #  2. "t = widgetType" sets t to the current widgetType if the
            #     QAction.triggered() doesn't supply it (which it doesn't).
            #     This localizes widgetType to the lambda in this loop iteration.
            #     Just using self.newTab(widgetType) would only bind the name of
            #     the variable to the argument, not the data contained. This would
            #     result in every menu entry creating a new copy of the last tab added.
            actionNew_Tab.triggered.connect(lambda ignore, t = tabType : self.newTab(t))

            self.ui.menuNew_Tab.addAction(actionNew_Tab)
        self.tabWidget.setCurrentIndex(0)

        self.ui.actionOpen_Project.triggered.connect(lambda : self.openProject())
        self.ui.actionSet_Current_Project_Location.triggered.connect(self.setProjectLocation)
        self.ui.actionOpen_New_RadTrack_Window.triggered.connect(self.openNewWindow)
        self.ui.actionImport_File.triggered.connect(lambda : self.importFile())
        self.ui.actionExport_Current_Tab.triggered.connect(self.exportCurrentTab)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionRedo.triggered.connect(self.redo)
        self.ui.actionClose_Current_Tab.triggered.connect(lambda : self.closeTab(None))
        self.ui.actionOpen_Working_Directory.triggered.connect(self.openSessionDirectory)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.ui.actionReopen_Closed_Tab.triggered.connect(self.undoCloseTab)
        self.ui.actionRename_Current_Tab.triggered.connect(self.renameTab)
        self.tabWidget.currentChanged.connect(self.checkMenus)

        QtGui.QShortcut(QtGui.QKeySequence.Undo, self).activated.connect(self.undo)
        QtGui.QShortcut(QtGui.QKeySequence.Redo, self).activated.connect(self.redo)

        self.checkMenus()

    def exceptionCapture(self, exceptionType, exceptionValue, traceBack):
        # Extract exception information
        exceptionText = 'Traceback (most recent call last):\n'
        for fileName, lineNumber, scope, line in traceback.extract_tb(traceBack):
            exceptionText = exceptionText + '  File "' + fileName + '", line ' + str(lineNumber) + ', in ' + scope + '\n'
            exceptionText = exceptionText + '    ' + line + '\n'
        exceptionText = exceptionText + exceptionType.__name__ + ': ' + str(exceptionValue) + '\n'

        # Log error
        timestamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        with open(self.logFile, 'a') as log:
            log.write(string.center(' ' + timestamp + ' ', 80, '-') + '\n')
            log.write(exceptionText)
            log.write('-'*80 + '\n\n')

        # Make an attempt at saving the user's data.
        # If unsuccessful, skip it to avoid an infinite loop.
        try:
            self.saveProject()
        except Exception:
            pass

        # Present user with dialog box
        box = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                'RadTrack Error',
                                'An unexpected error has occured.\n\nIf you wish to submit a bug report, push "More Details" and copy the information in your report.',
                                QtGui.QMessageBox.Ok, self)
        box.setDetailedText(exceptionText)
        box.exec_()

    def setTitleBar(self, text):
        self.setWindowTitle(_translate("globalgu", text, None))

    def addToRecentMenu(self, name, addToTop = False):
        if not name:
            return

        menuSelect = QtGui.QAction(os.path.basename(name), self)
        menuSelect.setObjectName(name)
        menuSelect.setStatusTip(name)

        if os.path.isdir(name):
            menu = self.ui.menuRecent_Projects
            menuSelect.triggered.connect(lambda ignore, f = name : self.openProject(f))
        elif os.path.isfile(name):
            menu = self.ui.menuRecent_Files
            menuSelect.triggered.connect(lambda ignore, f = name : self.importFile(f))
        else:
            return

        if len(menu.actions()) >= 20:
            return

        if addToTop:
            oldList = menu.actions()
            menu.clear()
            menu.addAction(menuSelect)
            for action in [a for a in oldList if a.objectName() != name]:
                menu.addAction(action)
        else:
            menu.addAction(menuSelect)
        menu.setEnabled(True)

    def newTab(self, newTabType):
        newWidget = newTabType(self)
        newTitle = self.uniqueTabTitle(newWidget.defaultTitle)
        self.tabWidget.addTab(newWidget.container, newTitle)
        self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
        self.checkMenus()

    def uniqueTabTitle(self, title, ignoreIndex = -1):
        originalTitle = title
        number = 0
        currentTitles = [self.tabWidget.tabText(i) for i in range(self.tabWidget.count()) if i != ignoreIndex]
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
                    "Bunch Transport (*.lte);;" +
                    "SDDS (*.sdds);;" +
                    "SRW (*.srw)")
            if not openFile:
                return
        self.lastUsedDirectory = os.path.dirname(openFile)

        ext = os.path.splitext(openFile)[-1].lower().lstrip(".") # lowercased extension after '.'

        # Find all types of tabs that accept file type "ext"
        choices = []
        for tabType in self.availableTabTypes:
            try:
                if ext in tabType.acceptsFileTypes:
                    choices.append(tabType)
            except AttributeError:
                pass

        if len(choices) == 0:
            QtGui.QMessageBox.warning(self, 'Import Error', 'No suitable tab for file:\n' + openFile)
            return
        elif len(choices) == 1:
            destinationType = choices[0]
        else: # len(choices) > 1
            box = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'Ambiguous Import Destination', 'Multiple tab types can import this file.\nWhich kind of tab should be used?')
            responses = [box.addButton(widgetType.defaultTitle, QtGui.QMessageBox.ActionRole) for widgetType in choices] + [box.addButton(QtGui.QMessageBox.Cancel)]
            box.exec_()
            try:
                destinationType = choices[responses.index(box.clickedButton())]
            except IndexError:
                return # Cancel selected

        # Check if a tab of this type is already open
        openWidgetIndexes = [i for i in range(self.tabWidget.count()) if type(getRealWidget(self.tabWidget.widget(i))) == destinationType]
        newTabLabel = 'New ' + box.clickedButton().text() + ' Tab'
        if openWidgetIndexes:
            choices = [self.tabWidget.tabText(i) for i in openWidgetIndexes] + [newTabLabel]
            box = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'Choose Import Destination', 'Which tab should receive the data?')
            responses = [box.addButton(widgetType, QtGui.QMessageBox.ActionRole) for widgetType in choices] + [box.addButton(QtGui.QMessageBox.Cancel)]

            box.exec_()
            destinationIndex = responses.index(box.clickedButton())
            try:
                choice = choices[destinationIndex]
            except IndexError: # Cancel was pressed
                return
        else:
            choice = newTabLabel

        try:
            if choice == newTabLabel: # Make a new tab
                self.newTab(destinationType)
                getRealWidget(self.tabWidget.currentWidget()).importFile(openFile)
            else: # Pre-existing tab
                tabIndex = openWidgetIndexes[destinationIndex]
                destination = getRealWidget(self.tabWidget.widget(tabIndex))
                self.tabWidget.setCurrentIndex(tabIndex)
                destination.importFile(openFile)
            self.addToRecentMenu(openFile, True)
            shutil.copy2(openFile, self.sessionDirectory)
        except IndexError: # Cancel was pressed
            pass


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

        self.addToRecentMenu(self.sessionDirectory, True)

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

        saveProgress = QtGui.QProgressDialog('Saving project ...', 'Cancel', 0, self.tabWidget.count()-1, self)
        saveProgress.setValue(0)
        padding = len(str(self.tabWidget.count()))
        for i in range(self.tabWidget.count()):
            if saveProgress.wasCanceled():
                return

            widget = getRealWidget(self.tabWidget.widget(i))
            saveProgress.setValue(i)
            subExtension = widget.acceptsFileTypes[0] if widget.acceptsFileTypes else 'save'
            subFileName  = os.path.join(self.sessionDirectory,
                '_'.join([self.tabPrefix,
                          unicode(i).rjust(padding, '0'),
                          widget.defaultTitle,
                          self.tabWidget.tabText(i) + '.' + subExtension]))
            widget.exportToFile(subFileName)

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
        if self.ui.actionUndo.isEnabled():
            getRealWidget(self.tabWidget.currentWidget()).undo()

    def redo(self):
        if self.ui.actionRedo.isEnabled():
            getRealWidget(self.tabWidget.currentWidget()).redo()

    def closeEvent(self, event):
        self.saveProject()
        event.accept()
        QtGui.QMainWindow.closeEvent(self, event)
        self.addToRecentMenu(self.sessionDirectory, True)
        self.writeRecentFiles()
        for tab in self.allWidgets():
            tab.close()

    def openNewWindow(self):
        self.writeRecentFiles()
        RbGlobal(self.beta_test).show()

    def writeRecentFiles(self):
        loadedRecentFiles = [action.objectName() for action in \
                             self.ui.menuRecent_Projects.actions() + \
                             self.ui.menuRecent_Files.actions()]
        if self.sessionDirectory not in loadedRecentFiles:
            loadedRecentFiles.insert(0, self.sessionDirectory)

        with open(self.recentFile, 'w') as f:
            f.write('\n'.join(loadedRecentFiles))

    def openSessionDirectory(self):
        openDirectory(self.sessionDirectory)

    def openConfigDirectory(self):
        openDirectory(self.configDirectory)

def openDirectory(directory):
    if sys.platform == 'win32': # Windows
        os.startfile(directory)
    elif sys.platform == 'darwin': # Mac
        subprocess.Popen(['open', directory])
    else: # Linux
        subprocess.Popen(['xdg-open', directory])


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
        myapp.openProject(project_file)
    myapp.show()
    sys.exit(app.exec_())

def call_main():
    p = argh.ArghParser()
    argh.set_default_command(p, main)
    argh.dispatch(p)

if __name__ == '__main__':
    call_main()
