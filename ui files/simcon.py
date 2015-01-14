# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simcon.ui'
#
# Created: Tue Jan 13 16:27:28 2015
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_simcon(object):
    def setupUi(self, simcon):
        simcon.setObjectName("simcon")
        simcon.resize(341, 249)
        self.formLayoutWidget = QtGui.QWidget(simcon)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 30, 281, 191))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.delz = QtGui.QLineEdit(self.formLayoutWidget)
        self.delz.setObjectName("delz")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.delz)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.zstop = QtGui.QLineEdit(self.formLayoutWidget)
        self.zstop.setObjectName("zstop")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.zstop)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.iorb = QtGui.QPushButton(self.formLayoutWidget)
        self.iorb.setObjectName("iorb")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.iorb)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.isravg = QtGui.QPushButton(self.formLayoutWidget)
        self.isravg.setObjectName("isravg")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.isravg)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.isrsig = QtGui.QPushButton(self.formLayoutWidget)
        self.isrsig.setObjectName("isrsig")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.isrsig)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.eloss = QtGui.QLineEdit(self.formLayoutWidget)
        self.eloss.setObjectName("eloss")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.eloss)

        self.retranslateUi(simcon)
        QtCore.QMetaObject.connectSlotsByName(simcon)

    def retranslateUi(self, simcon):
        simcon.setWindowTitle(QtGui.QApplication.translate("simcon", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("simcon", "Integration Step Size:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("simcon", "Integration Length:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("simcon", "Orbit Correction:", None, QtGui.QApplication.UnicodeUTF8))
        self.iorb.setText(QtGui.QApplication.translate("simcon", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("simcon", "Include spontaneous synchrotron \n"
"energy loss:", None, QtGui.QApplication.UnicodeUTF8))
        self.isravg.setText(QtGui.QApplication.translate("simcon", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("simcon", "Include energy spread from \n"
"quantum fluctuations", None, QtGui.QApplication.UnicodeUTF8))
        self.isrsig.setText(QtGui.QApplication.translate("simcon", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("simcon", "Externally Applied energy loss:", None, QtGui.QApplication.UnicodeUTF8))

