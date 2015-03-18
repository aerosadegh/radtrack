# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ploadforgenesis.ui'
#
# Created: Sun Mar 15 02:10:31 2015
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
        Dialog.resize(279, 439)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 400, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(30, 20, 221, 211))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(6)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 240, 222, 145))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.itgaus = QtGui.QComboBox(self.formLayoutWidget)
        self.itgaus.setObjectName(_fromUtf8("itgaus"))
        self.itgaus.addItem(_fromUtf8(""))
        self.itgaus.addItem(_fromUtf8(""))
        self.itgaus.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.itgaus)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.itgamgaus = QtGui.QComboBox(self.formLayoutWidget)
        self.itgamgaus.setObjectName(_fromUtf8("itgamgaus"))
        self.itgamgaus.addItem(_fromUtf8(""))
        self.itgamgaus.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.itgamgaus)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.iall = QtGui.QLineEdit(self.formLayoutWidget)
        self.iall.setObjectName(_fromUtf8("iall"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.iall)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.ipspeed = QtGui.QLineEdit(self.formLayoutWidget)
        self.ipspeed.setObjectName(_fromUtf8("ipspeed"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.ipspeed)
        self.nbins = QtGui.QLineEdit(self.formLayoutWidget)
        self.nbins.setObjectName(_fromUtf8("nbins"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.nbins)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "particle phase", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Dialog", "energy distribution", None))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Dialog", "x", None))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Dialog", "y", None))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("Dialog", "px", None))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("Dialog", "py", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Hammersley Base", None))
        self.label.setText(_translate("Dialog", "Distribution Profile:", None))
        self.itgaus.setItemText(0, _translate("Dialog", "Gaussian", None))
        self.itgaus.setItemText(1, _translate("Dialog", "Uniform", None))
        self.itgaus.setItemText(2, _translate("Dialog", "Parabolic", None))
        self.label_2.setText(_translate("Dialog", "Energy Profile:", None))
        self.itgamgaus.setItemText(0, _translate("Dialog", "Gaussian", None))
        self.itgamgaus.setItemText(1, _translate("Dialog", "Uniform", None))
        self.label_3.setText(_translate("Dialog", "IALL:", None))
        self.label_4.setText(_translate("Dialog", "IPSEED:", None))
        self.label_5.setText(_translate("Dialog", "NBINS:", None))

