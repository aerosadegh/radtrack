# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beamforsrw.ui'
#
# Created: Mon Feb 23 01:43:57 2015
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(342, 306)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 260, 271, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget_2 = QtGui.QWidget(Dialog)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(40, 30, 261, 221))
        self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_12 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_12)
        self.label_13 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_13)
        self.label_14 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_14)
        self.label_15 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_15)
        self.label_16 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_16)
        self.label_17 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_17)
        self.label_18 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_18)
        self.lineEdit_12 = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_12.setObjectName(_fromUtf8("lineEdit_12"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_12)
        self.lineEdit_13 = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_13.setObjectName(_fromUtf8("lineEdit_13"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_13)
        self.lineEdit_14 = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_14.setObjectName(_fromUtf8("lineEdit_14"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_14)
        self.lineEdit_15 = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_15.setObjectName(_fromUtf8("lineEdit_15"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_15)
        self.lineEdit_16 = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_16.setObjectName(_fromUtf8("lineEdit_16"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_16)
        self.lineEdit_17 = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_17.setObjectName(_fromUtf8("lineEdit_17"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.lineEdit_17)
        self.lineEdit_18 = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_18.setObjectName(_fromUtf8("lineEdit_18"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.FieldRole, self.lineEdit_18)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_12.setText(_translate("Dialog", "Avergae Current", None))
        self.label_13.setText(_translate("Dialog", "Initial Horizontal Coordinate", None))
        self.label_14.setText(_translate("Dialog", "Inital Vertical Coordinate", None))
        self.label_15.setText(_translate("Dialog", "Inital Longitudinal Coordinate", None))
        self.label_16.setText(_translate("Dialog", "Initial Relative Horizontal Velocity", None))
        self.label_17.setText(_translate("Dialog", "Initial Relative Vertical Velocity", None))
        self.label_18.setText(_translate("Dialog", "Relative Energy", None))

