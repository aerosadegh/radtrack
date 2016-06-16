# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'radtrack/ui/rbcbt.ui'
#
# Created: Thu Jun 16 05:40:41 2016
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_RBCBT(object):
    def setupUi(self, RBCBT):
        RBCBT.setObjectName(_fromUtf8("RBCBT"))
        RBCBT.resize(644, 938)
        self.verticalLayout_4 = QtGui.QVBoxLayout(RBCBT)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label = QtGui.QLabel(RBCBT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_4.addWidget(self.label)
        self.elementButtonLayout = QtGui.QHBoxLayout()
        self.elementButtonLayout.setObjectName(_fromUtf8("elementButtonLayout"))
        self.verticalLayout_4.addLayout(self.elementButtonLayout)
        self.splitter = QtGui.QSplitter(RBCBT)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.elementListLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.elementListLayout.setMargin(0)
        self.elementListLayout.setObjectName(_fromUtf8("elementListLayout"))
        self.elementListLabel = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.elementListLabel.setFont(font)
        self.elementListLabel.setObjectName(_fromUtf8("elementListLabel"))
        self.elementListLayout.addWidget(self.elementListLabel)
        self.treeWidget = dtreeWidget(self.layoutWidget)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.elementListLayout.addWidget(self.treeWidget)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.beamlineEditorLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.beamlineEditorLayout.setMargin(0)
        self.beamlineEditorLayout.setObjectName(_fromUtf8("beamlineEditorLayout"))
        self.beamlineEditorLabel = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.beamlineEditorLabel.setFont(font)
        self.beamlineEditorLabel.setObjectName(_fromUtf8("beamlineEditorLabel"))
        self.beamlineEditorLayout.addWidget(self.beamlineEditorLabel)
        self.beamlineEditorLayout_2 = QtGui.QHBoxLayout()
        self.beamlineEditorLayout_2.setObjectName(_fromUtf8("beamlineEditorLayout_2"))
        self.workingBeamline = dlistWidget(self.layoutWidget1)
        self.workingBeamline.setObjectName(_fromUtf8("workingBeamline"))
        self.beamlineEditorLayout_2.addWidget(self.workingBeamline)
        self.saveBeamlineButton = QtGui.QPushButton(self.layoutWidget1)
        self.saveBeamlineButton.setObjectName(_fromUtf8("saveBeamlineButton"))
        self.beamlineEditorLayout_2.addWidget(self.saveBeamlineButton)
        self.clearBeamlineButton = QtGui.QPushButton(self.layoutWidget1)
        self.clearBeamlineButton.setObjectName(_fromUtf8("clearBeamlineButton"))
        self.beamlineEditorLayout_2.addWidget(self.clearBeamlineButton)
        self.beamlineEditorLayout.addLayout(self.beamlineEditorLayout_2)
        self.layoutWidget2 = QtGui.QWidget(self.splitter)
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.graphicsLayout = QtGui.QVBoxLayout(self.layoutWidget2)
        self.graphicsLayout.setMargin(0)
        self.graphicsLayout.setObjectName(_fromUtf8("graphicsLayout"))
        self.graphicsLabel = QtGui.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.graphicsLabel.setFont(font)
        self.graphicsLabel.setObjectName(_fromUtf8("graphicsLabel"))
        self.graphicsLayout.addWidget(self.graphicsLabel)
        self.graphicsView = beamGraphicsWindow(self.layoutWidget2)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.graphicsLayout.addWidget(self.graphicsView)
        self.verticalLayout_4.addWidget(self.splitter)

        self.retranslateUi(RBCBT)
        QtCore.QMetaObject.connectSlotsByName(RBCBT)

    def retranslateUi(self, RBCBT):
        RBCBT.setWindowTitle(_translate("RBCBT", "Widget", None))
        self.label.setText(_translate("RBCBT", "New Beamline Elements", None))
        self.elementListLabel.setText(_translate("RBCBT", "Beamline Element List", None))
        self.beamlineEditorLabel.setText(_translate("RBCBT", "Beamline Editor - Drag elements here to create beamlines", None))
        self.saveBeamlineButton.setText(_translate("RBCBT", "Save Beamline", None))
        self.clearBeamlineButton.setText(_translate("RBCBT", "Clear Beamline", None))
        self.graphicsLabel.setText(_translate("RBCBT", "Graphical Preview", None))

from cbt import beamGraphicsWindow, dlistWidget, dtreeWidget
