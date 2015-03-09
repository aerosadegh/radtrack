# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbele.ui'
#
# Created: Thu Feb 20 16:12:26 2014
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ELE(object):
    def setupUi(self, ELE):
        ELE.setObjectName("ELE")
        ELE.resize(568, 364)
        self.formLayoutWidget = QtGui.QWidget(ELE)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 341, 211))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.latticeChoice = QtGui.QComboBox(self.formLayoutWidget)
        self.noneBeamChoice = 'Select beamline source ...'
        self.fileBeamChoice = 'Use another file ...'
        self.latticeChoice.addItem(self.noneBeamChoice)
        self.latticeChoice.addItem(self.fileBeamChoice)
        self.latticeChoice.setObjectName("latticeChoice")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.latticeChoice)
        self.bunchChoice = QtGui.QComboBox(self.formLayoutWidget)
        self.noneBunchChoice = 'Select beam bunch source ...'
        self.fileBunchChoice = 'Use another file ...'
        self.bunchChoice.addItem(self.noneBunchChoice)
        self.bunchChoice.addItem(self.fileBunchChoice)
        self.bunchChoice.setObjectName("bunchChoice")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.bunchChoice)
        self.beamlineLabel = QtGui.QLabel(self.formLayoutWidget)
        self.beamlineLabel.setObjectName("beamlineLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.beamlineLabel)
        self.orderLabel = QtGui.QLabel(self.formLayoutWidget)
        self.orderLabel.setObjectName("orderLabel")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.orderLabel)
        self.orderLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.orderLineEdit.setObjectName("orderLineEdit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.orderLineEdit)
        self.momentumLabel = QtGui.QLabel(self.formLayoutWidget)
        self.momentumLabel.setObjectName("momentumLabel")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.momentumLabel)
        self.momentumLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.momentumLineEdit.setObjectName("momentumLineEdit")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.momentumLineEdit)
        self.stepLabel = QtGui.QLabel(self.formLayoutWidget)
        self.stepLabel.setObjectName("stepLabel")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.stepLabel)
        self.stepsLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.stepsLineEdit.setObjectName("stepsLineEdit")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.stepsLineEdit)
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.bunchChoice)
        self.lte = QtGui.QLabel(self.formLayoutWidget)
        self.lte.setObjectName("lte")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lte)
        self.bun = QtGui.QLabel(self.formLayoutWidget)
        self.bun.setObjectName("bun")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.bun)
        self.beamlineDropDown = QtGui.QComboBox(self.formLayoutWidget)
        self.beamlineDropDown.setObjectName("beamlineDropDown")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.beamlineDropDown)
        self.sim = QtGui.QPushButton(ELE)
        self.sim.setGeometry(QtCore.QRect(80, 220, 211, 101))
        self.sim.setObjectName("sim")
        self.textEdit = QtGui.QTextEdit(ELE)
        self.textEdit.setGeometry(QtCore.QRect(360, 10, 201, 211))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(ELE)
        QtCore.QMetaObject.connectSlotsByName(ELE)

    def retranslateUi(self, ELE):
        ELE.setWindowTitle(QtGui.QApplication.translate("ELE", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.beamlineLabel.setText(QtGui.QApplication.translate("ELE", "beamline:", None, QtGui.QApplication.UnicodeUTF8))
        self.orderLabel.setText(QtGui.QApplication.translate("ELE", "default order:", None, QtGui.QApplication.UnicodeUTF8))
        self.momentumLabel.setText(QtGui.QApplication.translate("ELE", "momentum:", None, QtGui.QApplication.UnicodeUTF8))
        self.stepLabel.setText(QtGui.QApplication.translate("ELE", "step number:", None, QtGui.QApplication.UnicodeUTF8))
        self.lte.setText(QtGui.QApplication.translate("ELE", "Lattice File:", None, QtGui.QApplication.UnicodeUTF8))
        self.bun.setText(QtGui.QApplication.translate("ELE", "Bunch File:", None, QtGui.QApplication.UnicodeUTF8))
        self.sim.setText(QtGui.QApplication.translate("ELE", "SIMULATE", None, QtGui.QApplication.UnicodeUTF8))

