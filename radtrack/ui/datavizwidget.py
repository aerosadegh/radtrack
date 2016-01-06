# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'datavizwidget.ui'
#
# Created: Wed Jan  6 02:49:14 2016
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(983, 692)
        self.files = QtGui.QListWidget(Form)
        self.files.setGeometry(QtCore.QRect(20, 30, 201, 251))
        self.files.setObjectName(_fromUtf8("files"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(80, 10, 91, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.data = QtGui.QTableWidget(Form)
        self.data.setGeometry(QtCore.QRect(240, 30, 511, 251))
        self.data.setObjectName(_fromUtf8("data"))
        self.data.setColumnCount(0)
        self.data.setRowCount(3)
        item = QtGui.QTableWidgetItem()
        self.data.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.data.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.data.setVerticalHeaderItem(2, item)
        self.legend = QtGui.QTextBrowser(Form)
        self.legend.setGeometry(QtCore.QRect(770, 30, 191, 251))
        self.legend.setObjectName(_fromUtf8("legend"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(840, 10, 56, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(470, 10, 56, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.widget = matplotlibWidget(Form)
        self.widget.setGeometry(QtCore.QRect(241, 300, 721, 391))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(590, 290, 56, 13))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(50, 290, 141, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.selectplot = QtGui.QComboBox(Form)
        self.selectplot.setGeometry(QtCore.QRect(20, 320, 201, 26))
        self.selectplot.setObjectName(_fromUtf8("selectplot"))
        self.line = QtGui.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(30, 360, 191, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(40, 370, 151, 31))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayoutWidget = QtGui.QWidget(Form)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 410, 201, 61))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_7)
        self.xaxis = QtGui.QComboBox(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xaxis.sizePolicy().hasHeightForWidth())
        self.xaxis.setSizePolicy(sizePolicy)
        self.xaxis.setObjectName(_fromUtf8("xaxis"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.xaxis)
        self.label_8 = QtGui.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_8)
        self.yaxis = QtGui.QComboBox(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yaxis.sizePolicy().hasHeightForWidth())
        self.yaxis.setSizePolicy(sizePolicy)
        self.yaxis.setObjectName(_fromUtf8("yaxis"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.yaxis)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(60, 521, 101, 71))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Available Files", None))
        item = self.data.verticalHeaderItem(0)
        item.setText(_translate("Form", "Description", None))
        item = self.data.verticalHeaderItem(1)
        item.setText(_translate("Form", "Name", None))
        item = self.data.verticalHeaderItem(2)
        item.setText(_translate("Form", "Units", None))
        self.label_2.setText(_translate("Form", "Legend", None))
        self.label_3.setText(_translate("Form", "Data", None))
        self.label_4.setText(_translate("Form", "Plots", None))
        self.label_5.setText(_translate("Form", "Quick Select Plot Data", None))
        self.label_6.setText(_translate("Form", "Custom Select Plot Data", None))
        self.label_7.setText(_translate("Form", "X-axis", None))
        self.label_8.setText(_translate("Form", "Y-axis", None))
        self.pushButton.setText(_translate("Form", "PushButton", None))

from radtrack.ui.matplotlibwidget import matplotlibWidget
