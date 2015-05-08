# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'precisionofsrw.ui'
#
# Created: Fri May  8 13:32:39 2015
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
        Dialog.resize(358, 310)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(110, 260, 231, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget_3 = QtGui.QWidget(Dialog)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(30, 20, 311, 241))
        self.formLayoutWidget_3.setObjectName(_fromUtf8("formLayoutWidget_3"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget_3)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_19 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_19)
        self.meth = QtGui.QComboBox(self.formLayoutWidget_3)
        self.meth.setObjectName(_fromUtf8("meth"))
        self.meth.addItem(_fromUtf8(""))
        self.meth.addItem(_fromUtf8(""))
        self.meth.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.meth)
        self.label_20 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_20)
        self.relprec = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.relprec.setObjectName(_fromUtf8("relprec"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.relprec)
        self.label_21 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_21)
        self.label_22 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_22)
        self.label_23 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_23)
        self.label_24 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_24)
        self.usetermin = QtGui.QComboBox(self.formLayoutWidget_3)
        self.usetermin.setObjectName(_fromUtf8("usetermin"))
        self.usetermin.addItem(_fromUtf8(""))
        self.usetermin.addItem(_fromUtf8(""))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.usetermin)
        self.label_25 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_25)
        self.sampfactnxny = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.sampfactnxny.setObjectName(_fromUtf8("sampfactnxny"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.sampfactnxny)
        self.zstartint = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.zstartint.setObjectName(_fromUtf8("zstartint"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.zstartint)
        self.zendint = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.zendint.setObjectName(_fromUtf8("zendint"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.zendint)
        self.nptraj = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.nptraj.setObjectName(_fromUtf8("nptraj"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.nptraj)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Precision", None))
        self.label_19.setText(_translate("Dialog", "SR calculation method", None))
        self.meth.setItemText(0, _translate("Dialog", "Manual", None))
        self.meth.setItemText(1, _translate("Dialog", "Auto-Undulator", None))
        self.meth.setItemText(2, _translate("Dialog", "Auto-Wiggler", None))
        self.label_20.setText(_translate("Dialog", "Relative precision", None))
        self.label_21.setText(_translate("Dialog", "Start integration", None))
        self.label_22.setText(_translate("Dialog", "End integration", None))
        self.label_23.setText(_translate("Dialog", "Number of trajectory points", None))
        self.label_24.setText(_translate("Dialog", "Use terminating terms", None))
        self.usetermin.setItemText(0, _translate("Dialog", "No", None))
        self.usetermin.setItemText(1, _translate("Dialog", "Yes", None))
        self.label_25.setText(_translate("Dialog", "Sampling factor (nx,ny)", None))

