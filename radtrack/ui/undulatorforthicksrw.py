# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'undulatorforthicksrw.ui'
#
# Created: Fri May  8 13:35:33 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

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
        Dialog.resize(291, 240)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 190, 241, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 231, 151))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))

        self.fields = {}
        for i, c in enumerate(Dialog.cfg[1]):
            n, t, _, u, _ = c
            label = QtGui.QLabel(self.formLayoutWidget)
            label.setObjectName(_fromUtf8(n + ' label'))
            self.formLayout.setWidget(i, QtGui.QFormLayout.LabelRole, label)
            if t == bool:
                value = QtGui.QCheckBox(self.formLayoutWidget)
            else:
                value = QtGui.QLineEdit(self.formLayoutWidget)
            value.setObjectName(_fromUtf8(n))
            self.formLayout.setWidget(i, QtGui.QFormLayout.FieldRole, value)
            self.fields[n] = {
                # Not good to denormalize
                'cfg': c,
                'label': label,
                'value': value,
            }
        self.retranslateUi(Dialog)

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", Dialog.cfg[0], None))
        for f in self.fields.values():
            f['label'].setText(_translate("Dialog", f['cfg'][0], None))
            # Encapsulate in a widget based on type
            if f['cfg'][1] == bool:
                f['value'].setText(_translate("Dialog", f['cfg'][3], None))
