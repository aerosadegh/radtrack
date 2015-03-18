# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'timeforgenesis.ui'
#
# Created: Mon Mar 16 15:36:27 2015
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
        Dialog.resize(308, 282)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 230, 211, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 251, 201))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.curlen = QtGui.QLineEdit(self.formLayoutWidget)
        self.curlen.setObjectName(_fromUtf8("curlen"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.curlen)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.zsep = QtGui.QLineEdit(self.formLayoutWidget)
        self.zsep.setObjectName(_fromUtf8("zsep"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.zsep)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.nslice = QtGui.QLineEdit(self.formLayoutWidget)
        self.nslice.setObjectName(_fromUtf8("nslice"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.nslice)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.ntail = QtGui.QLineEdit(self.formLayoutWidget)
        self.ntail.setObjectName(_fromUtf8("ntail"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.ntail)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.shotnoise = QtGui.QLineEdit(self.formLayoutWidget)
        self.shotnoise.setObjectName(_fromUtf8("shotnoise"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.shotnoise)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_7)
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label)
        self.itdp = QtGui.QCheckBox(self.formLayoutWidget)
        self.itdp.setObjectName(_fromUtf8("itdp"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.itdp)
        self.isntyp = QtGui.QCheckBox(self.formLayoutWidget)
        self.isntyp.setObjectName(_fromUtf8("isntyp"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.isntyp)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_2.setText(_translate("Dialog", "Bunch Length:", None))
        self.label_3.setText(_translate("Dialog", "Slice Separation:", None))
        self.label_4.setText(_translate("Dialog", "Total Slices:", None))
        self.label_5.setText(_translate("Dialog", "Position of First Slice:", None))
        self.label_6.setText(_translate("Dialog", "Shotnoise:", None))
        self.label_7.setText(_translate("Dialog", "ISNTYP:", None))
        self.label.setText(_translate("Dialog", "Time Dependence:", None))
        self.itdp.setText(_translate("Dialog", "Yes/No", None))
        self.isntyp.setText(_translate("Dialog", "Fawley", None))

