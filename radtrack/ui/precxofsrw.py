# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'precisionofsrw.ui'
#
# Created: Tue Feb 24 15:23:51 2015
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
        Dialog.resize(320, 322)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 270, 231, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget_3 = QtGui.QWidget(Dialog)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(30, 20, 261, 241))
        self.formLayoutWidget_3.setObjectName(_fromUtf8("formLayoutWidget_3"))
        self.formLayout_3 = QtGui.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setMargin(0)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label_19 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_19)
        self.comboBox = QtGui.QComboBox(self.formLayoutWidget_3)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.label_20 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_20)
        self.lineEdit_19 = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_19.setObjectName(_fromUtf8("lineEdit_19"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_19)
        self.label_21 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_21)
        self.label_22 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_22)
        self.label_23 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_23)
        self.label_24 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_24)
        self.comboBox_2 = QtGui.QComboBox(self.formLayoutWidget_3)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.FieldRole, self.comboBox_2)
        self.label_25 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.formLayout_3.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_25)
        self.lineEdit_20 = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_20.setObjectName(_fromUtf8("lineEdit_20"))
        self.formLayout_3.setWidget(6, QtGui.QFormLayout.FieldRole, self.lineEdit_20)
        self.lineEdit_21 = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_21.setObjectName(_fromUtf8("lineEdit_21"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_21)
        self.lineEdit_22 = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_22.setObjectName(_fromUtf8("lineEdit_22"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_22)
        self.lineEdit_23 = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_23.setObjectName(_fromUtf8("lineEdit_23"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_23)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_19.setText(_translate("Dialog", "SR calculation method", None))
        self.comboBox.setItemText(0, _translate("Dialog", "Manual", None))
        self.comboBox.setItemText(1, _translate("Dialog", "Auto-Undulator", None))
        self.comboBox.setItemText(2, _translate("Dialog", "Auto-Wiggler", None))
        self.label_20.setText(_translate("Dialog", "Relative precision", None))
        self.label_21.setText(_translate("Dialog", "Start integration", None))
        self.label_22.setText(_translate("Dialog", "End integration", None))
        self.label_23.setText(_translate("Dialog", "Number of trajectory points", None))
        self.label_24.setText(_translate("Dialog", "Use terminating terms", None))
        self.comboBox_2.setItemText(0, _translate("Dialog", "No", None))
        self.comboBox_2.setItemText(1, _translate("Dialog", "Yes", None))
        self.label_25.setText(_translate("Dialog", "Sampling factor (nx,ny)", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

