# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'undulatorforthinsrw.ui'
#
# Created: Wed Mar 25 13:11:12 2015
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
        Dialog.resize(400, 426)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 380, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 341, 341))
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
        self.by = QtGui.QLineEdit(self.formLayoutWidget)
        self.by.setObjectName(_fromUtf8("by"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.by)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.bx = QtGui.QLineEdit(self.formLayoutWidget)
        self.bx.setObjectName(_fromUtf8("bx"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.bx)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.phbx = QtGui.QLineEdit(self.formLayoutWidget)
        self.phbx.setObjectName(_fromUtf8("phbx"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.phbx)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.phby = QtGui.QLineEdit(self.formLayoutWidget)
        self.phby.setObjectName(_fromUtf8("phby"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.phby)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_7)
        self.sbx = QtGui.QLineEdit(self.formLayoutWidget)
        self.sbx.setObjectName(_fromUtf8("sbx"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.sbx)
        self.label_8 = QtGui.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_8)
        self.sby = QtGui.QLineEdit(self.formLayoutWidget)
        self.sby.setObjectName(_fromUtf8("sby"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.sby)
        self.label_9 = QtGui.QLabel(self.formLayoutWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_9)
        self.xcid = QtGui.QLineEdit(self.formLayoutWidget)
        self.xcid.setObjectName(_fromUtf8("xcid"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.xcid)
        self.label_10 = QtGui.QLabel(self.formLayoutWidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_10)
        self.ycid = QtGui.QLineEdit(self.formLayoutWidget)
        self.ycid.setObjectName(_fromUtf8("ycid"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.ycid)
        self.label_11 = QtGui.QLabel(self.formLayoutWidget)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.LabelRole, self.label_11)
        self.zcid = QtGui.QLineEdit(self.formLayoutWidget)
        self.zcid.setObjectName(_fromUtf8("zcid"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.zcid)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Number of Periods", None))
        self.label_2.setText(_translate("Dialog", "Period Length", None))
        self.label_3.setText(_translate("Dialog", "Peak Vertical Field", None))
        self.label_4.setText(_translate("Dialog", "Peak Horizontal Field", None))
        self.label_5.setText(_translate("Dialog", "Inital Phase of Horizontal Field Component", None))
        self.label_6.setText(_translate("Dialog", "Inital Phase of Vertical Field Componenent", None))
        self.label_7.setText(_translate("Dialog", "Symmetry of Horizontal Field Component", None))
        self.label_8.setText(_translate("Dialog", "Symmetry of Vertical Field Component", None))
        self.label_9.setText(_translate("Dialog", "Horizontal Coordinate of Undulator Center ", None))
        self.label_10.setText(_translate("Dialog", "Vertical Coordinate of Undulator Center", None))
        self.label_11.setText(_translate("Dialog", "Longitudinal Coordinate of Undulator Center", None))

