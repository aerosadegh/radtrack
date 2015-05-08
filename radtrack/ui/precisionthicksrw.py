# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'precisionthicksrw.ui'
#
# Created: Fri May  8 13:33:10 2015
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
        Dialog.resize(380, 468)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 420, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 30, 321, 181))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.harma = QtGui.QLineEdit(self.formLayoutWidget)
        self.harma.setObjectName(_fromUtf8("harma"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.harma)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.harmb = QtGui.QLineEdit(self.formLayoutWidget)
        self.harmb.setObjectName(_fromUtf8("harmb"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.harmb)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lip = QtGui.QLineEdit(self.formLayoutWidget)
        self.lip.setObjectName(_fromUtf8("lip"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lip)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.aip = QtGui.QLineEdit(self.formLayoutWidget)
        self.aip.setObjectName(_fromUtf8("aip"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.aip)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.flux = QtGui.QComboBox(self.formLayoutWidget)
        self.flux.setObjectName(_fromUtf8("flux"))
        self.flux.addItem(_fromUtf8(""))
        self.flux.addItem(_fromUtf8(""))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.flux)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 10, 161, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(110, 230, 161, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayoutWidget_2 = QtGui.QWidget(Dialog)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(30, 250, 318, 161))
        self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_8 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_8)
        self.prefact = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.prefact.setObjectName(_fromUtf8("prefact"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.prefact)
        self.label_9 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_9)
        self.field = QtGui.QComboBox(self.formLayoutWidget_2)
        self.field.setObjectName(_fromUtf8("field"))
        self.field.addItem(_fromUtf8(""))
        self.field.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.field)
        self.label_10 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_10)
        self.ilp = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.ilp.setObjectName(_fromUtf8("ilp"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.ilp)
        self.label_11 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_11)
        self.flp = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.flp.setObjectName(_fromUtf8("flp"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.flp)
        self.label_12 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_12)
        self.np = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.np.setObjectName(_fromUtf8("np"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.np)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Precision", None))
        self.label_2.setText(_translate("Dialog", "Initial Harmonic:", None))
        self.label_3.setText(_translate("Dialog", "Final Harmonic:", None))
        self.label_4.setText(_translate("Dialog", "Longitudinal Integration Precision:", None))
        self.label_5.setText(_translate("Dialog", "Azimuthal Integration Precision:", None))
        self.label_6.setText(_translate("Dialog", "Flux Calculation:", None))
        self.flux.setItemText(0, _translate("Dialog", "Total", None))
        self.flux.setItemText(1, _translate("Dialog", "Per Unit Surface", None))
        self.label.setText(_translate("Dialog", "Spectral Flux Calculation", None))
        self.label_7.setText(_translate("Dialog", "Power Density Calculation", None))
        self.label_8.setText(_translate("Dialog", "Precision Factor:", None))
        self.label_9.setText(_translate("Dialog", "Density Computation Method:", None))
        self.field.setItemText(0, _translate("Dialog", "Near Field", None))
        self.field.setItemText(1, _translate("Dialog", "Far Field", None))
        self.label_10.setText(_translate("Dialog", "Initial Longitudinal Position:", None))
        self.label_11.setText(_translate("Dialog", "Final Longitudinal Position:", None))
        self.label_12.setText(_translate("Dialog", "Number of Points along Trajectory:", None))

