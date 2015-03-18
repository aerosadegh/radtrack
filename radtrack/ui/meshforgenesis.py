# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'meshforgenesis.ui'
#
# Created: Mon Mar 16 15:23:22 2015
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
        Dialog.resize(341, 352)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 310, 271, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 281, 278))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.ncar = QtGui.QLineEdit(self.formLayoutWidget)
        self.ncar.setObjectName(_fromUtf8("ncar"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.ncar)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.rmax0 = QtGui.QLineEdit(self.formLayoutWidget)
        self.rmax0.setObjectName(_fromUtf8("rmax0"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.rmax0)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.dgrid = QtGui.QLineEdit(self.formLayoutWidget)
        self.dgrid.setObjectName(_fromUtf8("dgrid"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.dgrid)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.nscz = QtGui.QSpinBox(self.formLayoutWidget)
        self.nscz.setObjectName(_fromUtf8("nscz"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.nscz)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.nscr = QtGui.QLineEdit(self.formLayoutWidget)
        self.nscr.setObjectName(_fromUtf8("nscr"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.nscr)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_7)
        self.nptr = QtGui.QLineEdit(self.formLayoutWidget)
        self.nptr.setObjectName(_fromUtf8("nptr"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.nptr)
        self.label_8 = QtGui.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_8)
        self.rmax0sc = QtGui.QLineEdit(self.formLayoutWidget)
        self.rmax0sc.setObjectName(_fromUtf8("rmax0sc"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.rmax0sc)
        self.label_9 = QtGui.QLabel(self.formLayoutWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_9)
        self.lbc = QtGui.QCheckBox(self.formLayoutWidget)
        self.lbc.setObjectName(_fromUtf8("lbc"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lbc)
        self.iscrkup = QtGui.QCheckBox(self.formLayoutWidget)
        self.iscrkup.setObjectName(_fromUtf8("iscrkup"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.iscrkup)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Number of Grid Points:", None))
        self.label_2.setText(_translate("Dialog", "Boundary Condition:", None))
        self.label_3.setText(_translate("Dialog", "RMAX0:", None))
        self.label_4.setText(_translate("Dialog", "Grid Size:", None))
        self.label_5.setText(_translate("Dialog", "Number of Fourier Components:", None))
        self.label_6.setText(_translate("Dialog", "Number of Azimuthal Modes:", None))
        self.label_7.setText(_translate("Dialog", "Number of Radial Grid Points:", None))
        self.label_8.setText(_translate("Dialog", "RMAX0SC:", None))
        self.label_9.setText(_translate("Dialog", "Runge-Kutta:", None))
        self.lbc.setText(_translate("Dialog", "Neumann", None))
        self.iscrkup.setText(_translate("Dialog", "Yes/No", None))

