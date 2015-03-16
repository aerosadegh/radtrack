# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fodoforgenesis.ui'
#
# Created: Sun Mar 15 02:08:43 2015
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
        Dialog.resize(289, 392)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 350, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 231, 311))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.quadf = QtGui.QLineEdit(self.formLayoutWidget)
        self.quadf.setObjectName(_fromUtf8("quadf"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.quadf)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.quadd = QtGui.QLineEdit(self.formLayoutWidget)
        self.quadd.setObjectName(_fromUtf8("quadd"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.quadd)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.fl = QtGui.QLineEdit(self.formLayoutWidget)
        self.fl.setObjectName(_fromUtf8("fl"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.fl)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.dl = QtGui.QLineEdit(self.formLayoutWidget)
        self.dl.setObjectName(_fromUtf8("dl"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.dl)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.drl = QtGui.QLineEdit(self.formLayoutWidget)
        self.drl.setObjectName(_fromUtf8("drl"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.drl)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.f1st = QtGui.QLineEdit(self.formLayoutWidget)
        self.f1st.setObjectName(_fromUtf8("f1st"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.f1st)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtGui.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_8)
        self.qfdx = QtGui.QLineEdit(self.formLayoutWidget)
        self.qfdx.setObjectName(_fromUtf8("qfdx"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.qfdx)
        self.qfdy = QtGui.QLineEdit(self.formLayoutWidget)
        self.qfdy.setObjectName(_fromUtf8("qfdy"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.qfdy)
        self.label_9 = QtGui.QLabel(self.formLayoutWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_9)
        self.label_10 = QtGui.QLabel(self.formLayoutWidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_10)
        self.solen = QtGui.QLineEdit(self.formLayoutWidget)
        self.solen.setObjectName(_fromUtf8("solen"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.solen)
        self.sl = QtGui.QLineEdit(self.formLayoutWidget)
        self.sl.setObjectName(_fromUtf8("sl"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.sl)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Focusing Quad strength:", None))
        self.label_2.setText(_translate("Dialog", "Defocusing Quad strength:", None))
        self.label_3.setText(_translate("Dialog", "Focusing Quad length:", None))
        self.label_4.setText(_translate("Dialog", "Defocusing Quad length:", None))
        self.label_5.setText(_translate("Dialog", "Drift between Quads:", None))
        self.label_6.setText(_translate("Dialog", "Starting point:", None))
        self.label_7.setText(_translate("Dialog", "Offset - x:", None))
        self.label_8.setText(_translate("Dialog", "Offset - y:", None))
        self.label_9.setText(_translate("Dialog", "Solenoid field component:", None))
        self.label_10.setText(_translate("Dialog", "Solenoid component length:", None))

