# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'timeparams.ui'
#
# Created: Tue Jan 13 16:23:28 2015
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_timeparams(object):
    def setupUi(self, timeparams):
        timeparams.setObjectName("timeparams")
        timeparams.resize(271, 258)
        self.formLayoutWidget = QtGui.QWidget(timeparams)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 30, 211, 211))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.itdp = QtGui.QPushButton(self.formLayoutWidget)
        self.itdp.setObjectName("itdp")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.itdp)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.curlen = QtGui.QLineEdit(self.formLayoutWidget)
        self.curlen.setObjectName("curlen")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.curlen)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.zsep = QtGui.QLineEdit(self.formLayoutWidget)
        self.zsep.setObjectName("zsep")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.zsep)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.nslice = QtGui.QLineEdit(self.formLayoutWidget)
        self.nslice.setObjectName("nslice")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.nslice)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.ntail = QtGui.QLineEdit(self.formLayoutWidget)
        self.ntail.setObjectName("ntail")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.ntail)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.shotnoise = QtGui.QLineEdit(self.formLayoutWidget)
        self.shotnoise.setObjectName("shotnoise")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.shotnoise)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_7)
        self.isntyp = QtGui.QPushButton(self.formLayoutWidget)
        self.isntyp.setObjectName("isntyp")
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.isntyp)

        self.retranslateUi(timeparams)
        QtCore.QMetaObject.connectSlotsByName(timeparams)

    def retranslateUi(self, timeparams):
        timeparams.setWindowTitle(QtGui.QApplication.translate("timeparams", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("timeparams", "Time Dependence:", None, QtGui.QApplication.UnicodeUTF8))
        self.itdp.setText(QtGui.QApplication.translate("timeparams", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("timeparams", "Bunch Length:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("timeparams", "Slice Separation:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("timeparams", "Total Slices:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("timeparams", "Position of First Slice:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("timeparams", "Shotnoise:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("timeparams", "ISNTYP:", None, QtGui.QApplication.UnicodeUTF8))
        self.isntyp.setText(QtGui.QApplication.translate("timeparams", "Pennman/Fawley", None, QtGui.QApplication.UnicodeUTF8))

