# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'math.ui'
#
# Created: Thu Mar 20 10:10:44 2014
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_four(object):
    def setupUi(self, four):
        four.setObjectName("four")
        four.resize(225, 96)
        self.formLayout = QtGui.QFormLayout(four)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtGui.QLabel(four)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_3)
        self.label = QtGui.QLabel(four)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.n = QtGui.QLineEdit(four)
        self.n.setObjectName("n")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.n)
        self.buttonBox = QtGui.QDialogButtonBox(four)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.buttonBox)

        self.retranslateUi(four)
        QtCore.QMetaObject.connectSlotsByName(four)

    def retranslateUi(self, four):
        four.setWindowTitle(QtGui.QApplication.translate("math", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("math", "FFT", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("math", "N:", None, QtGui.QApplication.UnicodeUTF8))

