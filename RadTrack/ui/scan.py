# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scan.ui'
#
# Created: Tue Jan 13 16:30:56 2015
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_scan(object):
    def setupUi(self, scan):
        scan.setObjectName("scan")
        scan.resize(313, 163)
        self.formLayoutWidget = QtGui.QWidget(scan)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 30, 251, 101))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.comboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.nscan = QtGui.QLineEdit(self.formLayoutWidget)
        self.nscan.setObjectName("nscan")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.nscan)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.svar = QtGui.QLineEdit(self.formLayoutWidget)
        self.svar.setObjectName("svar")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.svar)

        self.retranslateUi(scan)
        QtCore.QMetaObject.connectSlotsByName(scan)

    def retranslateUi(self, scan):
        scan.setWindowTitle(QtGui.QApplication.translate("scan", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("scan", "Target Parameter to Scan:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("scan", "gamma0", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("scan", "delgam", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("scan", "curpeak", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(3, QtGui.QApplication.translate("scan", "xlamds", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(4, QtGui.QApplication.translate("scan", "aw0", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(5, QtGui.QApplication.translate("scan", "iseed", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(6, QtGui.QApplication.translate("scan", "pxbeam", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(7, QtGui.QApplication.translate("scan", "pybeam", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(8, QtGui.QApplication.translate("scan", "xbeam", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(9, QtGui.QApplication.translate("scan", "ybeam", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(10, QtGui.QApplication.translate("scan", "rxbeam", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(11, QtGui.QApplication.translate("scan", "rybeam", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(12, QtGui.QApplication.translate("scan", "xlamd", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(13, QtGui.QApplication.translate("scan", "delaw", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(14, QtGui.QApplication.translate("scan", "alphax", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(15, QtGui.QApplication.translate("scan", "alphay", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(16, QtGui.QApplication.translate("scan", "emitx", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(17, QtGui.QApplication.translate("scan", "emity", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(18, QtGui.QApplication.translate("scan", "prad0", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(19, QtGui.QApplication.translate("scan", "zrayl", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(20, QtGui.QApplication.translate("scan", "zwaist", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(21, QtGui.QApplication.translate("scan", "awd", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(22, QtGui.QApplication.translate("scan", "beamfile", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(23, QtGui.QApplication.translate("scan", "beamopt", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(24, QtGui.QApplication.translate("scan", "beamgam", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("scan", "Steps per Scan:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("scan", "Scan Range:", None, QtGui.QApplication.UnicodeUTF8))
