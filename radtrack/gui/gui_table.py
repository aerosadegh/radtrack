# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_table.ui'
#
# Created: Mon Jan 28 14:37:00 2013
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_EvgSoftSeq(object):
    def setupUi(self, EvgSoftSeq):
        EvgSoftSeq.setObjectName("EvgSoftSeq")
        EvgSoftSeq.resize(482, 499)
        self.tableWidget = QtGui.QTableWidget(EvgSoftSeq)
        self.tableWidget.setGeometry(QtCore.QRect(40, 10, 251, 281))
        self.tableWidget.setRowCount(100)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(100)
        self.pb_setSequence = QtGui.QPushButton(EvgSoftSeq)
        self.pb_setSequence.setGeometry(QtCore.QRect(300, 290, 75, 23))
        self.pb_setSequence.setObjectName("pb_setSequence")

        self.retranslateUi(EvgSoftSeq)
        QtCore.QMetaObject.connectSlotsByName(EvgSoftSeq)

    def retranslateUi(self, EvgSoftSeq):
        EvgSoftSeq.setWindowTitle(QtGui.QApplication.translate("EvgSoftSeq", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_setSequence.setText(QtGui.QApplication.translate("EvgSoftSeq", "set", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4.Qwt5 import * 