# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beamforgenesis.ui'
#
# Created: Sun Mar 15 02:08:20 2015
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
        Dialog.resize(315, 468)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 430, 251, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 261, 395))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.gamma0 = QtGui.QLineEdit(self.formLayoutWidget)
        self.gamma0.setObjectName(_fromUtf8("gamma0"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.gamma0)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.delgam = QtGui.QLineEdit(self.formLayoutWidget)
        self.delgam.setObjectName(_fromUtf8("delgam"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.delgam)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtGui.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_8)
        self.alphax = QtGui.QLineEdit(self.formLayoutWidget)
        self.alphax.setObjectName(_fromUtf8("alphax"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.alphax)
        self.alphay = QtGui.QLineEdit(self.formLayoutWidget)
        self.alphay.setObjectName(_fromUtf8("alphay"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.alphay)
        self.emitx = QtGui.QLineEdit(self.formLayoutWidget)
        self.emitx.setObjectName(_fromUtf8("emitx"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.emitx)
        self.emity = QtGui.QLineEdit(self.formLayoutWidget)
        self.emity.setObjectName(_fromUtf8("emity"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.emity)
        self.xbeam = QtGui.QLineEdit(self.formLayoutWidget)
        self.xbeam.setObjectName(_fromUtf8("xbeam"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.xbeam)
        self.ybeam = QtGui.QLineEdit(self.formLayoutWidget)
        self.ybeam.setObjectName(_fromUtf8("ybeam"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.ybeam)
        self.label_9 = QtGui.QLabel(self.formLayoutWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(12, QtGui.QFormLayout.LabelRole, self.label_9)
        self.curpeak = QtGui.QLineEdit(self.formLayoutWidget)
        self.curpeak.setObjectName(_fromUtf8("curpeak"))
        self.formLayout.setWidget(12, QtGui.QFormLayout.FieldRole, self.curpeak)
        self.label_10 = QtGui.QLabel(self.formLayoutWidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.LabelRole, self.label_10)
        self.rxbeam = QtGui.QLineEdit(self.formLayoutWidget)
        self.rxbeam.setObjectName(_fromUtf8("rxbeam"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.rxbeam)
        self.label_11 = QtGui.QLabel(self.formLayoutWidget)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.formLayout.setWidget(11, QtGui.QFormLayout.LabelRole, self.label_11)
        self.rybeam = QtGui.QLineEdit(self.formLayoutWidget)
        self.rybeam.setObjectName(_fromUtf8("rybeam"))
        self.formLayout.setWidget(11, QtGui.QFormLayout.FieldRole, self.rybeam)
        self.label_12 = QtGui.QLabel(self.formLayoutWidget)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_12)
        self.label_13 = QtGui.QLabel(self.formLayoutWidget)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_13)
        self.pxbeam = QtGui.QLineEdit(self.formLayoutWidget)
        self.pxbeam.setObjectName(_fromUtf8("pxbeam"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.pxbeam)
        self.pybeam = QtGui.QLineEdit(self.formLayoutWidget)
        self.pybeam.setObjectName(_fromUtf8("pybeam"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.pybeam)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Relativistic Factor (beam energy):", None))
        self.label_2.setText(_translate("Dialog", "Energy spread:", None))
        self.label_3.setText(_translate("Dialog", "Alpha - x:", None))
        self.label_4.setText(_translate("Dialog", "Alpha - y:", None))
        self.label_5.setText(_translate("Dialog", "Emittance - x:", None))
        self.label_6.setText(_translate("Dialog", "Emittacne - y:", None))
        self.label_7.setText(_translate("Dialog", "x:", None))
        self.label_8.setText(_translate("Dialog", "y:", None))
        self.label_9.setText(_translate("Dialog", "Peak current:", None))
        self.label_10.setText(_translate("Dialog", "x rms spatial distribution:", None))
        self.label_11.setText(_translate("Dialog", "y rms spatial distribution:", None))
        self.label_12.setText(_translate("Dialog", "x\':", None))
        self.label_13.setText(_translate("Dialog", "y\':", None))

