# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'globalgu.ui'
#
# Created: Thu Jan 16 14:37:36 2014
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_globalgu(object):
    def setupUi(self, globalgu):
        globalgu.setObjectName("globalgu")
        globalgu.resize(772, 490)
        self.centralwidget = QtGui.QWidget(globalgu)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout.addLayout(self.verticalLayout)
        globalgu.setCentralWidget(self.centralwidget)

        self.menuFile = QtGui.QMenu()
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtGui.QMenu()
        self.menuEdit.setObjectName("menuEdit")
        self.menuTab = QtGui.QMenu()
        self.menuTab.setObjectName("menuTab")

        self.statusbar = QtGui.QStatusBar(globalgu)
        self.statusbar.setObjectName("statusbar")
        globalgu.setStatusBar(self.statusbar)

        self.actionOpen = QtGui.QAction(globalgu)
        self.actionOpen.setObjectName("actionOpen")
        self.actionImport = QtGui.QAction(globalgu)
        self.actionImport.setObjectName("actionImport")
        self.actionExport = QtGui.QAction(globalgu)
        self.actionExport.setObjectName("actionExport")
        self.actionSave = QtGui.QAction(globalgu)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtGui.QAction(globalgu)
        self.actionExit.setObjectName("actionExit")
        self.actionUndo = QtGui.QAction(globalgu)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtGui.QAction(globalgu)
        self.actionRedo.setObjectName("actionRedo")
        self.menuNewTab = QtGui.QMenu(globalgu)
        self.menuNewTab.setObjectName("menuNewTab")
        self.menurecent = QtGui.QMenu(globalgu)
        self.menurecent.setObjectName("menurecent")
        self.actionDupeTab = QtGui.QAction(globalgu)
        self.actionDupeTab.setObjectName("actionDupeTab")
        self.actionCloseTab = QtGui.QAction(globalgu)
        self.actionCloseTab.setObjectName("actionCloseTab")
        self.actionUndoCloseTab = QtGui.QAction(globalgu)
        self.actionUndoCloseTab.setObjectName("actionUndoCloseTab")
        self.actionRenameTab = QtGui.QAction(globalgu)
        self.actionRenameTab.setObjectName("actionRenameTab")
        
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addMenu(self.menurecent)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)

        self.menuTab.addMenu(self.menuNewTab)
        self.menuTab.addSeparator()
        self.menuTab.addAction(self.actionCloseTab)
        self.menuTab.addAction(self.actionUndoCloseTab)
        self.menuTab.addSeparator()
        self.menuTab.addAction(self.actionRenameTab)

        self.menubar = QtGui.QMenuBar(globalgu)
        self.menubar.setNativeMenuBar(False)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTab.menuAction())
        self.menubar.setGeometry(QtCore.QRect(0, 0, 772, 21))
        self.menubar.setObjectName("menubar")
        globalgu.setMenuBar(self.menubar)

        self.retranslateUi(globalgu)
        QtCore.QMetaObject.connectSlotsByName(globalgu)

    def retranslateUi(self, globalgu):
        globalgu.setWindowTitle(QtGui.QApplication.translate("globalgu", "RadTrack", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("globalgu", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("globalgu", "Open Project ...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("globalgu", "Save Project ...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setText(QtGui.QApplication.translate("globalgu", "Import File ...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setText(QtGui.QApplication.translate("globalgu", "Export Current Tab ...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("globalgu", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("globalgu", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUndo.setText(QtGui.QApplication.translate("globalgu", "Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRedo.setText(QtGui.QApplication.translate("globalgu", "Redo", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTab.setTitle(QtGui.QApplication.translate("globalgu", "Tabs", None, QtGui.QApplication.UnicodeUTF8))
        self.menuNewTab.setTitle(QtGui.QApplication.translate("globalgu", "New Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDupeTab.setText(QtGui.QApplication.translate("globalgu", "Duplicate Current Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCloseTab.setText(QtGui.QApplication.translate("globalgu", "Close Current Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUndoCloseTab.setText(QtGui.QApplication.translate("globalgu", "Reopen Closed Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRenameTab.setText(QtGui.QApplication.translate("globalgu", "Rename Current Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.menurecent.setTitle(QtGui.QApplication.translate("globalgu", "Recent Files", None, QtGui.QApplication.UnicodeUTF8))
