# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbele.ui'
#
# Created: Thu Mar 26 22:23:23 2015
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

class Ui_ELE(object):
    def setupUi(self, ELE):
        ELE.setObjectName(_fromUtf8("ELE"))
        ELE.resize(1043, 364)
        self.horizontalLayoutWidget = QtGui.QWidget(ELE)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1021, 341))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.bunchSourceLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.bunchSourceLabel.setObjectName(_fromUtf8("bunchSourceLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.bunchSourceLabel)
        self.bunchSourceComboBox = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.bunchSourceComboBox.setObjectName(_fromUtf8("bunchSourceComboBox"))
        self.bunchSourceComboBox.addItem(_fromUtf8(""))
        self.bunchSourceComboBox.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.bunchSourceComboBox)
        self.beamLineSourceLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.beamLineSourceLabel.setObjectName(_fromUtf8("beamLineSourceLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.beamLineSourceLabel)
        self.beamLineSourceComboBox = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.beamLineSourceComboBox.setObjectName(_fromUtf8("beamLineSourceComboBox"))
        self.beamLineSourceComboBox.addItem(_fromUtf8(""))
        self.beamLineSourceComboBox.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.beamLineSourceComboBox)
        self.beamLineLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.beamLineLabel.setObjectName(_fromUtf8("beamLineLabel"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.beamLineLabel)
        self.beamLineComboBox = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.beamLineComboBox.setObjectName(_fromUtf8("beamLineComboBox"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.beamLineComboBox)
        self.momentumLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.momentumLabel.setObjectName(_fromUtf8("momentumLabel"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.momentumLabel)
        self.momentumLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.momentumLineEdit.setObjectName(_fromUtf8("momentumLineEdit"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.momentumLineEdit)
        self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.pushButton)
        self.textEdit_2 = QtGui.QTextEdit(self.horizontalLayoutWidget)
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.SpanningRole, self.textEdit_2)
        self.horizontalLayout_2.addLayout(self.formLayout_2)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_4.addWidget(self.label)
        self.line = QtGui.QFrame(self.horizontalLayoutWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_4.addWidget(self.line)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.retranslateUi(ELE)
        QtCore.QMetaObject.connectSlotsByName(ELE)

    def retranslateUi(self, ELE):
        ELE.setWindowTitle(_translate("ELE", "Form", None))
        self.bunchSourceLabel.setText(_translate("ELE", "Bunch Source:", None))
        self.bunchSourceComboBox.setItemText(0, _translate("ELE", "Select bunch source ...", None))
        self.bunchSourceComboBox.setItemText(1, _translate("ELE", "Another file ...", None))
        self.beamLineSourceLabel.setText(_translate("ELE", "Beam Line Source:", None))
        self.beamLineSourceComboBox.setItemText(0, _translate("ELE", "Select beam line source ...", None))
        self.beamLineSourceComboBox.setItemText(1, _translate("ELE", "Another file ...", None))
        self.beamLineLabel.setText(_translate("ELE", "Beam Line:", None))
        self.momentumLabel.setText(_translate("ELE", "Momentum:", None))
        self.pushButton.setText(_translate("ELE", "Simulate", None))
        self.label.setText(_translate("ELE", "Files generated by simulation run. Click to load into RadTrack.", None))

