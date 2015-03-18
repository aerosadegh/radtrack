# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scanforgenesis.ui'
#
# Created: Sun Mar 15 02:11:30 2015
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
        Dialog.resize(327, 176)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(100, 130, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 268, 101))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.comboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.nscan = QtGui.QLineEdit(self.formLayoutWidget)
        self.nscan.setObjectName(_fromUtf8("nscan"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.nscan)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.svar = QtGui.QLineEdit(self.formLayoutWidget)
        self.svar.setObjectName(_fromUtf8("svar"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.svar)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Target Parameter to Scan:", None))
        self.comboBox.setItemText(0, _translate("Dialog", "gamma0", None))
        self.comboBox.setItemText(1, _translate("Dialog", "delgam", None))
        self.comboBox.setItemText(2, _translate("Dialog", "curpeak", None))
        self.comboBox.setItemText(3, _translate("Dialog", "xlamds", None))
        self.comboBox.setItemText(4, _translate("Dialog", "aw0", None))
        self.comboBox.setItemText(5, _translate("Dialog", "iseed", None))
        self.comboBox.setItemText(6, _translate("Dialog", "pxbeam", None))
        self.comboBox.setItemText(7, _translate("Dialog", "pybeam", None))
        self.comboBox.setItemText(8, _translate("Dialog", "xbeam", None))
        self.comboBox.setItemText(9, _translate("Dialog", "ybeam", None))
        self.comboBox.setItemText(10, _translate("Dialog", "rxbeam", None))
        self.comboBox.setItemText(11, _translate("Dialog", "rybeam", None))
        self.comboBox.setItemText(12, _translate("Dialog", "xlamd", None))
        self.comboBox.setItemText(13, _translate("Dialog", "delaw", None))
        self.comboBox.setItemText(14, _translate("Dialog", "alphax", None))
        self.comboBox.setItemText(15, _translate("Dialog", "alphay", None))
        self.comboBox.setItemText(16, _translate("Dialog", "emitx", None))
        self.comboBox.setItemText(17, _translate("Dialog", "emity", None))
        self.comboBox.setItemText(18, _translate("Dialog", "prad0", None))
        self.comboBox.setItemText(19, _translate("Dialog", "zrayl", None))
        self.comboBox.setItemText(20, _translate("Dialog", "zwaist", None))
        self.comboBox.setItemText(21, _translate("Dialog", "awd", None))
        self.comboBox.setItemText(22, _translate("Dialog", "beamfile", None))
        self.comboBox.setItemText(23, _translate("Dialog", "beamopt", None))
        self.comboBox.setItemText(24, _translate("Dialog", "beamgam", None))
        self.label_2.setText(_translate("Dialog", "Steps per Scan:", None))
        self.label_3.setText(_translate("Dialog", "Scan Range:", None))

