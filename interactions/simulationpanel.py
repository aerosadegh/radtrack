# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulationpanel.ui'
#
# Created: Thu Oct 23 16:43:41 2014
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(918, 625)
        self.programs = QtGui.QListWidget(Form)
        self.programs.setGeometry(QtCore.QRect(20, 40, 161, 111))
        self.programs.setObjectName("programs")
        QtGui.QListWidgetItem(self.programs)
        QtGui.QListWidgetItem(self.programs)
        QtGui.QListWidgetItem(self.programs)
        QtGui.QListWidgetItem(self.programs)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(70, 10, 61, 21))
        self.label.setObjectName("label")
        self.graphicsView = QtGui.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(20, 170, 881, 431))
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(200, 40, 151, 111))
        self.pushButton.setObjectName("pushButton")
        #self.checkBox = QtGui.QCheckBox(Form)
        #self.checkBox.setGeometry(QtCore.QRect(370, 130, 91, 17))
        #self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.programs.isSortingEnabled()
        self.programs.setSortingEnabled(False)
        self.programs.item(0).setText(QtGui.QApplication.translate("Form", "Elegant", None, QtGui.QApplication.UnicodeUTF8))
        self.programs.item(1).setText(QtGui.QApplication.translate("Form", "Genesis", None, QtGui.QApplication.UnicodeUTF8))
        self.programs.item(2).setText(QtGui.QApplication.translate("Form", "Simulation", None, QtGui.QApplication.UnicodeUTF8))
        self.programs.item(3).setText(QtGui.QApplication.translate("Form", "SRW", None, QtGui.QApplication.UnicodeUTF8))
        self.programs.setSortingEnabled(__sortingEnabled)
        self.label.setText(QtGui.QApplication.translate("Form", "Simulations", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Execute", None, QtGui.QApplication.UnicodeUTF8))
        #self.checkBox.setText(QtGui.QApplication.translate("Form", "Toggle", None, QtGui.QApplication.UnicodeUTF8))

