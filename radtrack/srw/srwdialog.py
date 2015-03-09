# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'srwdialog.ui'
#
# Created: Fri Oct 17 17:02:53 2014
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

import sip
sip.setapi('QString', 2)
from PyQt4 import QtCore, QtGui

class Ui_srwdialog(object):
    def setupUi(self, srwdialog):
        srwdialog.setObjectName("srwdialog")
        srwdialog.resize(640, 480)
        self.buttonBox = QtGui.QDialogButtonBox(srwdialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 440, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(srwdialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), srwdialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), srwdialog.reject)
        QtCore.QMetaObject.connectSlotsByName(srwdialog)

    def retranslateUi(self, srwdialog):
        srwdialog.setWindowTitle(QtGui.QApplication.translate("srwdialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

