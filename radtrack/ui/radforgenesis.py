# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'radforgenesis.ui'
#
# Created: Mon Mar 16 15:16:54 2015
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
        Dialog.resize(428, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 260, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 10, 386, 237))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.xlamds = QtGui.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xlamds.sizePolicy().hasHeightForWidth())
        self.xlamds.setSizePolicy(sizePolicy)
        self.xlamds.setObjectName(_fromUtf8("xlamds"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.xlamds)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.prad0 = QtGui.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prad0.sizePolicy().hasHeightForWidth())
        self.prad0.setSizePolicy(sizePolicy)
        self.prad0.setObjectName(_fromUtf8("prad0"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.prad0)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.zrayl = QtGui.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zrayl.sizePolicy().hasHeightForWidth())
        self.zrayl.setSizePolicy(sizePolicy)
        self.zrayl.setObjectName(_fromUtf8("zrayl"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.zrayl)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.zwaist = QtGui.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zwaist.sizePolicy().hasHeightForWidth())
        self.zwaist.setSizePolicy(sizePolicy)
        self.zwaist.setObjectName(_fromUtf8("zwaist"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.zwaist)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.iallharm = QtGui.QPushButton(self.formLayoutWidget)
        self.iallharm.setObjectName(_fromUtf8("iallharm"))
        self.horizontalLayout_2.addWidget(self.iallharm)
        self.nharm = QtGui.QSpinBox(self.formLayoutWidget)
        self.nharm.setObjectName(_fromUtf8("nharm"))
        self.horizontalLayout_2.addWidget(self.nharm)
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_7)
        self.pradh0 = QtGui.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pradh0.sizePolicy().hasHeightForWidth())
        self.pradh0.setSizePolicy(sizePolicy)
        self.pradh0.setObjectName(_fromUtf8("pradh0"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.pradh0)
        self.iharmsc = QtGui.QCheckBox(self.formLayoutWidget)
        self.iharmsc.setObjectName(_fromUtf8("iharmsc"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.iharmsc)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Resonant Radiation Wavelength:", None))
        self.label_2.setText(_translate("Dialog", "Input Radiation Power:", None))
        self.label_3.setText(_translate("Dialog", "Rayleigh length:", None))
        self.label_4.setText(_translate("Dialog", "Position of Input Radiation Waist:", None))
        self.iallharm.setText(_translate("Dialog", "All Harmonics", None))
        self.label_6.setText(_translate("Dialog", "Include Feedback on beam:", None))
        self.label_7.setText(_translate("Dialog", "Harmonic Radiation Power:", None))
        self.iharmsc.setText(_translate("Dialog", "Yes/No", None))
        self.label_5.setText(_translate("Dialog", "Harmonics:", None))

