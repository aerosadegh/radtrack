"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved

"""
import sys, os, tempfile, shutil
from zipfile import ZipFile

from PySide import QtGui

from globalgu import Ui_globalgu
from RbLaserWindow import RbLaserWindow
from rbdcp import RbDcp
from RbBunchTransport import RbBunchTransport
from RbLaserTransport import RbLaserTransport
from RbBunchWindow import RbBunchWindow
from RbEle import RbEle
from RbFEL import RbFEL
from RbSimulations import RbSimulations
from RadTrack.srw.RbSrwUndulator import srwund
from RadTrack.genesis.rbgenesis import RbGenesis
from RadTrack.genesis.rbgenesis2 import RbGenesis2

class RbGlobal(QtGui.QMainWindow):
    #Constructor
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.lastUsedDirectory = os.path.expanduser('~')
        self.fileExtension = '.radtrack'

        self.ui = Ui_globalgu()
        self.ui.setupUi(self)
        self.setWindowTitle('RadTrack')

        self.tabWidget = QtGui.QTabWidget()

        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setWidget(RbLaserWindow(self))
        self.tabWidget.addTab(scrollArea, self.tr('Laser'))

        self.tabWidget.addTab(RbLaserTransport(self), self.tr('Laser Transport'))

        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setWidget(RbBunchWindow(self))
        self.tabWidget.addTab(scrollArea, self.tr('Bunch'))

        self.tabWidget.addTab(RbBunchTransport(self), self.tr('Bunch Transport'))

        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setWidget(RbSimulations(self))
        self.tabWidget.addTab(scrollArea,self.tr('Interactions'))
        
        self.tabWidget.addTab(RbEle(self), self.tr('Elegant'))
        self.tabWidget.addTab(RbDcp(self), self.tr('Data Visualization'))
        self.tabWidget.addTab(RbFEL(self), self.tr('FEL'))

        scrollArea3 = QtGui.QScrollArea(self)
        scrollArea3.setWidget(srwund(self))
        self.tabWidget.addTab(scrollArea3,self.tr('SRW'))

        newscrollarea = QtGui.QScrollArea(self)
        newscrollarea.setWidget(RbGenesis2(self))
        self.tabWidget.addTab(newscrollarea, self.tr('Genesis'))
        

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

        self.ui.verticalLayout.addWidget(self.tabWidget)
        self.setLayout(self.ui.verticalLayout)
        self.ui.actionOpen.triggered.connect(self.openProjectFile)
        self.ui.actionSave.triggered.connect(self.saveProjectFile)
        self.ui.actionImport.triggered.connect(self.importFile)
        self.ui.actionExport.triggered.connect(self.exportCurrentTab)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionRedo.triggered.connect(self.redo)
        self.ui.actionCloseTab.triggered.connect(self.closeCurrentTab)
        self.ui.actionUndoCloseTab.triggered.connect(self.undoCloseTab)
        self.ui.actionRenameTab.triggered.connect(self.renameTab)
        self.tabWidget.currentChanged.connect(self.checkMenus)

        QtGui.QShortcut(QtGui.QKeySequence.Undo, self).activated.connect(self.undo)
        QtGui.QShortcut(QtGui.QKeySequence.Redo, self).activated.connect(self.redo)

        self.closedTabs = []
        self.globalHasChanged = False

        self.populateNewTabMenu()
        self.checkMenus()

    def populateNewTabMenu(self):
        for i in range(self.tabWidget.count()):
            actionNewTab = QtGui.QAction(self)
            actionNewTab.setObjectName('new' + self.tabWidget.tabText(i))
            actionNewTab.setText(self.tabWidget.tabText(i))
            self.ui.menuNewTab.addAction(actionNewTab)
            tabType = type(getRealWidget(self.tabWidget.widget(i)))
            actionNewTab.triggered.connect(lambda tabType = tabType : self.newTab(tabType))

    def newTab(self, newTabType):
        if self.usesScrollArea[newTabType]:
            scrollArea = QtGui.QScrollArea(self)
            scrollArea.setWidget(newTabType())
            self.tabWidget.addTab(scrollArea, self.uniqueTabTitle(self.tabTypeToOriginalName[newTabType]))
        else:
            self.tabWidget.addTab(newTabType(), self.uniqueTabTitle(self.tabTypeToOriginalName[newTabType]))
        self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
        self.globalHasChanged = True

    def uniqueTabTitle(self, title, ignoreIndex = -1):
        originalTitle = title
        number = 0
        currentTitles = [self.tabWidget.tabText(i).replace("&", "") for i in range(self.tabWidget.count()) if i != ignoreIndex]
        while title in currentTitles:
            number = number + 1
            title = originalTitle + ' ' + str(number)
        return title.strip()

    def closeCurrentTab(self):
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

    def renameTab(self):
        index = self.tabWidget.currentIndex()
        newName, ok = QtGui.QInputDialog.getText(self, "Rename Tab", 'New name for "' + self.tabWidget.tabText(index) + '"')

        if ok and newName:
            self.tabWidget.setTabText(index, self.uniqueTabTitle(newName, index))
            self.globalHasChanged = True


    def importFile(self, openFile = None):
        if openFile is None or openFile == '':
            openFile, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.lastUsedDirectory,
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
            box = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'Ambiguous Import Destination', 'Which tab should receive the data?')
            responses = [box.addButton(widgetType, QtGui.QMessageBox.ActionRole) for widgetType in choices] + [box.addButton(QtGui.QMessageBox.Cancel)]

            box.exec_()
            destinationIndex = responses.index(box.clickedButton())
            try:
                if choices[destinationIndex] != 'New Tab':
                    destination = getRealWidget(self.tabWidget.widget(openWidgetIndexes[destinationIndex]))
                    destination.importFile(openFile)
                    self.tabWidget.setCurrentWidget(destination)
                else:
                    self.newTab(destinationType)
                    getRealWidget(self.tabWidget.currentWidget()).importFile(openFile)
            except IndexError: # Cancel was pressed
                return


    def openProjectFile(self, fileName = None):
        print "Opening: ", fileName
        if fileName is None or fileName == '':
            fileName, _ = QtGui.QFileDialog.getOpenFileName(self, 
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
                zf.extract(subFileName)
                _, originalTitle, tabName = os.path.basename(subFileName).split('_')
                tabName = os.path.basename(subFileName).split("_", 1)[1].rsplit(".", 1)[0]
                dest.newTab(self.originalNameToTabType[originalTitle])
                getRealWidget(dest.tabWidget.widget(i)).importFile(subFileName)
                dest.tabWidget.setTabText(i, tabName)
                tabName = os.path.basename(subFileName).split('_', 1)[1].rsplit('.', 1)[0]
                dest.tabWidget.setTabText(i, tabName)
                os.remove(subFileName)
        dest.lastUsedDirectory = os.path.dirname(fileName)

    def saveProjectFile(self):
        fileName, _ = QtGui.QFileDialog.getSaveFileName(self,
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

    def checkMenus(self):
        menuMap = dict()
        menuMap['exportToFile'] = self.ui.actionExport
        menuMap['undo'] = self.ui.actionUndo
        menuMap['redo'] = self.ui.actionRedo
        for function in menuMap.keys():
            menuMap[function].setEnabled(hasattr(getRealWidget(self.tabWidget.currentWidget()), function))
        self.ui.actionUndoCloseTab.setEnabled(len(self.closedTabs) > 0)

    def hasChanged(self):
        if self.globalHasChanged:
            return True

        for widget in [getRealWidget(self.tabWidget.widget(i)) for i in range(self.tabWidget.count())]:
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

def getRealWidget(widget):
    try:
        return getRealWidget(widget.widget())
    except AttributeError:
        return widget



def main(argv):
    app = QtGui.QApplication(argv)
    myapp = RbGlobal()
    if len(argv) > 1:
        myapp.openProjectFile(argv[1])
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
