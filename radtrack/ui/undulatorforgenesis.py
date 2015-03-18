# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'undulatorforgenesis.ui'
#
# Created: Mon Mar 16 15:14:26 2015
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
        Dialog.resize(299, 372)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 330, 251, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 241, 281))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.aw0 = QtGui.QLineEdit(self.formLayoutWidget)
        self.aw0.setObjectName(_fromUtf8("aw0"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.aw0)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.xlamd = QtGui.QLineEdit(self.formLayoutWidget)
        self.xlamd.setObjectName(_fromUtf8("xlamd"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.xlamd)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.nwig = QtGui.QLineEdit(self.formLayoutWidget)
        self.nwig.setObjectName(_fromUtf8("nwig"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.nwig)
        self.label_8 = QtGui.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_8)
        self.nsec = QtGui.QLineEdit(self.formLayoutWidget)
        self.nsec.setObjectName(_fromUtf8("nsec"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.nsec)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.delaw = QtGui.QLineEdit(self.formLayoutWidget)
        self.delaw.setObjectName(_fromUtf8("delaw"))
        self.horizontalLayout.addWidget(self.delaw)
        self.iertyp = QtGui.QSpinBox(self.formLayoutWidget)
        self.iertyp.setObjectName(_fromUtf8("iertyp"))
        self.horizontalLayout.addWidget(self.iertyp)
        self.formLayout.setLayout(5, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_6)
        self.awx = QtGui.QLineEdit(self.formLayoutWidget)
        self.awx.setObjectName(_fromUtf8("awx"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.awx)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_7)
        self.awy = QtGui.QLineEdit(self.formLayoutWidget)
        self.awy.setObjectName(_fromUtf8("awy"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.awy)
        self.label_9 = QtGui.QLabel(self.formLayoutWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_9)
        self.seed = QtGui.QLineEdit(self.formLayoutWidget)
        self.seed.setObjectName(_fromUtf8("seed"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.seed)
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.iwityp = QtGui.QCheckBox(self.formLayoutWidget)
        self.iwityp.setObjectName(_fromUtf8("iwityp"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.iwityp)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_2.setText(_translate("Dialog", "Undulator Parameter:", None))
        self.label_3.setText(_translate("Dialog", "Period Length:", None))
        self.label_4.setText(_translate("Dialog", "Number of Periods:", None))
        self.label_8.setText(_translate("Dialog", "Sections:", None))
        self.label_5.setText(_translate("Dialog", "Field Errors:", None))
        self.label_6.setText(_translate("Dialog", "Offset - x:", None))
        self.label_7.setText(_translate("Dialog", "Offset - y:", None))
        self.label_9.setText(_translate("Dialog", "seed:", None))
        self.label.setText(_translate("Dialog", "Undulator Type:", None))
        self.iwityp.setText(_translate("Dialog", "Planar/Helical", None))

