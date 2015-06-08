# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'undulatorforthicksrw.ui'
#
# Created: Fri May  8 13:35:33 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

from radtrack.rtpyqt4 import QtCore, QtGui, fromUtf8, translate

from radtrack import srw_ui_params

class Ui_Dialog(object):
    def setupUi(self, Dialog, declarations):
        Dialog.setObjectName(fromUtf8("Dialog"))
        Dialog.resize(291, 240)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 190, 241, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 231, 151))
        self.formLayoutWidget.setObjectName(fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(fromUtf8("formLayout"))

        srw_ui_params.setup_ui(self, Dialog, declarations)
        srw_ui_params.retranslate_dialog(self, Dialog, declarations)

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
