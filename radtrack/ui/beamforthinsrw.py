# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beamforthinsrw.ui'
#
# Created: Tue Mar 24 19:37:43 2015
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
        Dialog.resize(342, 318)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 270, 271, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget_2 = QtGui.QWidget(Dialog)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(40, 30, 261, 231))
        self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_12 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_12)
        self.iavg = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.iavg.setObjectName(_fromUtf8("iavg"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.iavg)
        self.label_13 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_13)
        self.partstatmom1x = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.partstatmom1x.setObjectName(_fromUtf8("partstatmom1x"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.partstatmom1x)
        self.label_14 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_14)
        self.partstatmom1y = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.partstatmom1y.setObjectName(_fromUtf8("partstatmom1y"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.partstatmom1y)
        self.label_15 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_15)
        self.partstatmom1z = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.partstatmom1z.setObjectName(_fromUtf8("partstatmom1z"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.partstatmom1z)
        self.label_16 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_16)
        self.partstatmom1xp = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.partstatmom1xp.setObjectName(_fromUtf8("partstatmom1xp"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.partstatmom1xp)
        self.label_17 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_17)
        self.partstatmom1yp = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.partstatmom1yp.setObjectName(_fromUtf8("partstatmom1yp"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.partstatmom1yp)
        self.label_18 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_18)
        self.partstatmom1gamma = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.partstatmom1gamma.setObjectName(_fromUtf8("partstatmom1gamma"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.partstatmom1gamma)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_12.setText(_translate("Dialog", "Average Current", None))
        self.label_13.setText(_translate("Dialog", "Initial Horizontal Coordinate", None))
        self.label_14.setText(_translate("Dialog", "Inital Vertical Coordinate", None))
        self.label_15.setText(_translate("Dialog", "Inital Longitudinal Coordinate", None))
        self.label_16.setText(_translate("Dialog", "Initial Relative Horizontal Velocity", None))
        self.label_17.setText(_translate("Dialog", "Initial Relative Vertical Velocity", None))
        self.label_18.setText(_translate("Dialog", "Relativistic Energy(gamma)", None))

