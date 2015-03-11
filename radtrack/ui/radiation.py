# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'radiation.ui'
#
# Created: Wed Feb 04 09:40:01 2015
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_radiation(object):
    def setupUi(self, radiation):
        radiation.setObjectName("radiation")
        radiation.resize(371, 281)
        self.formLayoutWidget = QtGui.QWidget(radiation)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 30, 311, 221))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.xlamds = QtGui.QLineEdit(self.formLayoutWidget)
        self.xlamds.setObjectName("xlamds")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.xlamds)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.prad0 = QtGui.QLineEdit(self.formLayoutWidget)
        self.prad0.setObjectName("prad0")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.prad0)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.zrayl = QtGui.QLineEdit(self.formLayoutWidget)
        self.zrayl.setObjectName("zrayl")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.zrayl)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.zwaist = QtGui.QLineEdit(self.formLayoutWidget)
        self.zwaist.setObjectName("zwaist")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.zwaist)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.iallharm = QtGui.QPushButton(self.formLayoutWidget)
        self.iallharm.setObjectName("iallharm")
        self.horizontalLayout_2.addWidget(self.iallharm)
        self.nharm = QtGui.QLineEdit(self.formLayoutWidget)
        self.nharm.setObjectName("nharm")
        self.horizontalLayout_2.addWidget(self.nharm)
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.pushButton_2 = QtGui.QPushButton(self.formLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.pushButton_2)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_7)
        self.pradh0 = QtGui.QLineEdit(self.formLayoutWidget)
        self.pradh0.setObjectName("pradh0")
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.pradh0)

        self.retranslateUi(radiation)
        QtCore.QMetaObject.connectSlotsByName(radiation)

    def retranslateUi(self, radiation):
        radiation.setWindowTitle(QtGui.QApplication.translate("radiation", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("radiation", "Resonant Radiation Wavelength:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("radiation", "Input Radiation Power:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("radiation", "Rayleigh length:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("radiation", "Position of Input Radiation Waist:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("radiation", "Harmonics:", None, QtGui.QApplication.UnicodeUTF8))
        self.iallharm.setText(QtGui.QApplication.translate("radiation", "All Harmonics", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("radiation", "Include Feedback on beam:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("radiation", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("radiation", "Harmonic Radiation Power:", None, QtGui.QApplication.UnicodeUTF8))

