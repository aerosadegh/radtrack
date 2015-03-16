# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simcongenesis.ui'
#
# Created: Sun Mar 15 02:15:37 2015
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
        Dialog.resize(322, 280)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 240, 231, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 20, 281, 203))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.delz = QtGui.QLineEdit(self.formLayoutWidget)
        self.delz.setObjectName(_fromUtf8("delz"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.delz)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.zstop = QtGui.QLineEdit(self.formLayoutWidget)
        self.zstop.setObjectName(_fromUtf8("zstop"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.zstop)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.iorb = QtGui.QPushButton(self.formLayoutWidget)
        self.iorb.setObjectName(_fromUtf8("iorb"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.iorb)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.isravg = QtGui.QPushButton(self.formLayoutWidget)
        self.isravg.setObjectName(_fromUtf8("isravg"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.isravg)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.isrsig = QtGui.QPushButton(self.formLayoutWidget)
        self.isrsig.setObjectName(_fromUtf8("isrsig"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.isrsig)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.eloss = QtGui.QLineEdit(self.formLayoutWidget)
        self.eloss.setObjectName(_fromUtf8("eloss"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.eloss)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Integration Step Size:", None))
        self.label_2.setText(_translate("Dialog", "Integration Length:", None))
        self.label_3.setText(_translate("Dialog", "Orbit Correction:", None))
        self.iorb.setText(_translate("Dialog", "Yes/No", None))
        self.label_4.setText(_translate("Dialog", "Include spontaneous synchrotron \n"
"energy loss:", None))
        self.isravg.setText(_translate("Dialog", "Yes/No", None))
        self.label_5.setText(_translate("Dialog", "Include energy spread from \n"
"quantum fluctuations", None))
        self.isrsig.setText(_translate("Dialog", "Yes/No", None))
        self.label_6.setText(_translate("Dialog", "Externally Applied energy loss:", None))

