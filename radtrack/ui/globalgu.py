# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'globalgu.ui'
#
# Created: Tue Apr 14 00:00:11 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_globalgu(object):
    def setupUi(self, globalgu):
        globalgu.setObjectName(_fromUtf8("globalgu"))
        globalgu.resize(772, 490)
        self.centralwidget = QtGui.QWidget(globalgu)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout.addLayout(self.verticalLayout)
        globalgu.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(globalgu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 772, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuRecent_Projects = QtGui.QMenu(self.menuFile)
        self.menuRecent_Projects.setObjectName(_fromUtf8("menuRecent_Projects"))
        self.menuRecent_Files = QtGui.QMenu(self.menuFile)
        self.menuRecent_Files.setObjectName(_fromUtf8("menuRecent_Files"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuTabs = QtGui.QMenu(self.menubar)
        self.menuTabs.setObjectName(_fromUtf8("menuTabs"))
        self.menuNew_Tab = QtGui.QMenu(self.menuTabs)
        self.menuNew_Tab.setObjectName(_fromUtf8("menuNew_Tab"))
        self.menuExamples = QtGui.QMenu(self.menubar)
        self.menuExamples.setObjectName(_fromUtf8("menuExamples"))
        self.menuLoad_Example_Project = QtGui.QMenu(self.menuExamples)
        self.menuLoad_Example_Project.setObjectName(_fromUtf8("menuLoad_Example_Project"))
        self.menuImport_Example_File = QtGui.QMenu(self.menuExamples)
        self.menuImport_Example_File.setObjectName(_fromUtf8("menuImport_Example_File"))
        globalgu.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(globalgu)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        globalgu.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(globalgu)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionUndo = QtGui.QAction(globalgu)
        self.actionUndo.setObjectName(_fromUtf8("actionUndo"))
        self.actionRedo = QtGui.QAction(globalgu)
        self.actionRedo.setObjectName(_fromUtf8("actionRedo"))
        self.actionOpen_Project = QtGui.QAction(globalgu)
        self.actionOpen_Project.setObjectName(_fromUtf8("actionOpen_Project"))
        self.actionSet_Current_Project_Location = QtGui.QAction(globalgu)
        self.actionSet_Current_Project_Location.setObjectName(_fromUtf8("actionSet_Current_Project_Location"))
        self.actionOpen_New_RadTrack_Window = QtGui.QAction(globalgu)
        self.actionOpen_New_RadTrack_Window.setObjectName(_fromUtf8("actionOpen_New_RadTrack_Window"))
        self.actionImport_File = QtGui.QAction(globalgu)
        self.actionImport_File.setObjectName(_fromUtf8("actionImport_File"))
        self.actionExport_Current_Tab = QtGui.QAction(globalgu)
        self.actionExport_Current_Tab.setObjectName(_fromUtf8("actionExport_Current_Tab"))
        self.actionClose_Current_Tab = QtGui.QAction(globalgu)
        self.actionClose_Current_Tab.setObjectName(_fromUtf8("actionClose_Current_Tab"))
        self.actionReopen_Closed_Tab = QtGui.QAction(globalgu)
        self.actionReopen_Closed_Tab.setObjectName(_fromUtf8("actionReopen_Closed_Tab"))
        self.actionRename_Current_Tab = QtGui.QAction(globalgu)
        self.actionRename_Current_Tab.setObjectName(_fromUtf8("actionRename_Current_Tab"))
        self.actionExit = QtGui.QAction(globalgu)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuFile.addAction(self.actionSet_Current_Project_Location)
        self.menuFile.addAction(self.actionOpen_New_RadTrack_Window)
        self.menuFile.addAction(self.menuRecent_Projects.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport_File)
        self.menuFile.addAction(self.actionExport_Current_Tab)
        self.menuFile.addAction(self.menuRecent_Files.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuTabs.addAction(self.menuNew_Tab.menuAction())
        self.menuTabs.addSeparator()
        self.menuTabs.addAction(self.actionClose_Current_Tab)
        self.menuTabs.addAction(self.actionReopen_Closed_Tab)
        self.menuTabs.addSeparator()
        self.menuTabs.addAction(self.actionRename_Current_Tab)
        self.menuExamples.addAction(self.menuLoad_Example_Project.menuAction())
        self.menuExamples.addAction(self.menuImport_Example_File.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTabs.menuAction())
        self.menubar.addAction(self.menuExamples.menuAction())

        self.retranslateUi(globalgu)
        QtCore.QMetaObject.connectSlotsByName(globalgu)

    def retranslateUi(self, globalgu):
        globalgu.setWindowTitle(_translate("globalgu", "MainWindow", None))
        self.menuFile.setTitle(_translate("globalgu", "File", None))
        self.menuRecent_Projects.setTitle(_translate("globalgu", "Recent Projects", None))
        self.menuRecent_Files.setTitle(_translate("globalgu", "Recent Files", None))
        self.menuEdit.setTitle(_translate("globalgu", "Edit", None))
        self.menuTabs.setTitle(_translate("globalgu", "Tabs", None))
        self.menuNew_Tab.setTitle(_translate("globalgu", "New Tab", None))
        self.menuExamples.setTitle(_translate("globalgu", "Examples", None))
        self.menuLoad_Example_Project.setTitle(_translate("globalgu", "Load Example Project", None))
        self.menuImport_Example_File.setTitle(_translate("globalgu", "Import Example File", None))
        self.actionOpen.setText(_translate("globalgu", "Open", None))
        self.actionUndo.setText(_translate("globalgu", "Undo", None))
        self.actionRedo.setText(_translate("globalgu", "Redo", None))
        self.actionOpen_Project.setText(_translate("globalgu", "Open Project ...", None))
        self.actionSet_Current_Project_Location.setText(_translate("globalgu", "Set Current Project Location ...", None))
        self.actionOpen_New_RadTrack_Window.setText(_translate("globalgu", "Open New RadTrack Window ...", None))
        self.actionImport_File.setText(_translate("globalgu", "Import File ...", None))
        self.actionExport_Current_Tab.setText(_translate("globalgu", "Export Current Tab ...", None))
        self.actionClose_Current_Tab.setText(_translate("globalgu", "Close Current Tab", None))
        self.actionReopen_Closed_Tab.setText(_translate("globalgu", "Reopen Closed Tab", None))
        self.actionRename_Current_Tab.setText(_translate("globalgu", "Rename Current Tab ...", None))
        self.actionExit.setText(_translate("globalgu", "Exit", None))

