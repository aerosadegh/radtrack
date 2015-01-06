# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'average.ui'
#
# Created: Thu Mar 20 10:10:57 2014
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_average(object):
    def setupUi(self, average):
        average.setObjectName("average")
        average.resize(225, 99)
        self.formLayout = QtGui.QFormLayout(average)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(average)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.label)
        self.label_2 = QtGui.QLabel(average)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit = QtGui.QLineEdit(average)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit)
        self.buttonBox = QtGui.QDialogButtonBox(average)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.buttonBox)

        self.retranslateUi(average)
        QtCore.QMetaObject.connectSlotsByName(average)

    def retranslateUi(self, average):
        average.setWindowTitle(QtGui.QApplication.translate("average", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("average", "Averaging", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("average", "bin:", None, QtGui.QApplication.UnicodeUTF8))

