# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'undulatorforthicksrw.ui'
#
# Created: Tue Apr 21 00:16:56 2015
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
        Dialog.resize(291, 240)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 190, 241, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 231, 151))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.numper = QtGui.QLineEdit(self.formLayoutWidget)
        self.numper.setObjectName(_fromUtf8("numper"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.numper)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.undper = QtGui.QLineEdit(self.formLayoutWidget)
        self.undper.setObjectName(_fromUtf8("undper"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.undper)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.b = QtGui.QLineEdit(self.formLayoutWidget)
        self.b.setObjectName(_fromUtf8("b"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.b)
        self.label_12 = QtGui.QLabel(self.formLayoutWidget)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_12)
        self.n = QtGui.QLineEdit(self.formLayoutWidget)
        self.n.setObjectName(_fromUtf8("n"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.n)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.vh = QtGui.QCheckBox(self.formLayoutWidget)
        self.vh.setObjectName(_fromUtf8("vh"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.vh)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Number of Periods", None))
        self.label_2.setText(_translate("Dialog", "Period Length", None))
        self.label_3.setText(_translate("Dialog", "Magnetic Field", None))
        self.label_12.setText(_translate("Dialog", "Harmonic Number", None))
        self.label_4.setText(_translate("Dialog", "Undulator Orientation", None))
        self.vh.setText(_translate("Dialog", "Vertical", None))

