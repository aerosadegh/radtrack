# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'io.ui'
#
# Created: Tue Jan 13 16:33:19 2015
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_io(object):
    def setupUi(self, io):
        io.setObjectName("io")
        io.resize(401, 921)
        self.formLayoutWidget = QtGui.QWidget(io)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 30, 343, 791))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.iphsty = QtGui.QPushButton(self.formLayoutWidget)
        self.iphsty.setObjectName("iphsty")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.iphsty)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.ishsty = QtGui.QPushButton(self.formLayoutWidget)
        self.ishsty.setObjectName("ishsty")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.ishsty)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.ippart = QtGui.QPushButton(self.formLayoutWidget)
        self.ippart.setObjectName("ippart")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.ippart)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.ispart = QtGui.QPushButton(self.formLayoutWidget)
        self.ispart.setObjectName("ispart")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.ispart)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.ipradi = QtGui.QPushButton(self.formLayoutWidget)
        self.ipradi.setObjectName("ipradi")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.ipradi)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.isradi = QtGui.QPushButton(self.formLayoutWidget)
        self.isradi.setObjectName("isradi")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.isradi)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_7)
        self.iotail = QtGui.QPushButton(self.formLayoutWidget)
        self.iotail.setObjectName("iotail")
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.iotail)
        self.label_8 = QtGui.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_8)
        self.outputfile = QtGui.QPushButton(self.formLayoutWidget)
        self.outputfile.setObjectName("outputfile")
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.outputfile)
        self.label_9 = QtGui.QLabel(self.formLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_9)
        self.magin = QtGui.QPushButton(self.formLayoutWidget)
        self.magin.setObjectName("magin")
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.magin)
        self.label_10 = QtGui.QLabel(self.formLayoutWidget)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_10)
        self.magout = QtGui.QPushButton(self.formLayoutWidget)
        self.magout.setObjectName("magout")
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.magout)
        self.label_11 = QtGui.QLabel(self.formLayoutWidget)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(10, QtGui.QFormLayout.LabelRole, self.label_11)
        self.dump = QtGui.QComboBox(self.formLayoutWidget)
        self.dump.setObjectName("dump")
        self.dump.addItem("")
        self.dump.addItem("")
        self.dump.addItem("")
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.dump)
        self.label_12 = QtGui.QLabel(self.formLayoutWidget)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(11, QtGui.QFormLayout.LabelRole, self.label_12)
        self.beamfile = QtGui.QPushButton(self.formLayoutWidget)
        self.beamfile.setObjectName("beamfile")
        self.formLayout.setWidget(11, QtGui.QFormLayout.FieldRole, self.beamfile)
        self.label_13 = QtGui.QLabel(self.formLayoutWidget)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(12, QtGui.QFormLayout.LabelRole, self.label_13)
        self.radfile = QtGui.QPushButton(self.formLayoutWidget)
        self.radfile.setObjectName("radfile")
        self.formLayout.setWidget(12, QtGui.QFormLayout.FieldRole, self.radfile)
        self.label_14 = QtGui.QLabel(self.formLayoutWidget)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(13, QtGui.QFormLayout.LabelRole, self.label_14)
        self.distfile = QtGui.QPushButton(self.formLayoutWidget)
        self.distfile.setObjectName("distfile")
        self.formLayout.setWidget(13, QtGui.QFormLayout.FieldRole, self.distfile)
        self.label_15 = QtGui.QLabel(self.formLayoutWidget)
        self.label_15.setObjectName("label_15")
        self.formLayout.setWidget(14, QtGui.QFormLayout.LabelRole, self.label_15)
        self.ndcut = QtGui.QPushButton(self.formLayoutWidget)
        self.ndcut.setObjectName("ndcut")
        self.formLayout.setWidget(14, QtGui.QFormLayout.FieldRole, self.ndcut)
        self.label_16 = QtGui.QLabel(self.formLayoutWidget)
        self.label_16.setObjectName("label_16")
        self.formLayout.setWidget(15, QtGui.QFormLayout.LabelRole, self.label_16)
        self.fieldfile = QtGui.QPushButton(self.formLayoutWidget)
        self.fieldfile.setObjectName("fieldfile")
        self.formLayout.setWidget(15, QtGui.QFormLayout.FieldRole, self.fieldfile)
        self.label_17 = QtGui.QLabel(self.formLayoutWidget)
        self.label_17.setObjectName("label_17")
        self.formLayout.setWidget(16, QtGui.QFormLayout.LabelRole, self.label_17)
        self.aligngradf = QtGui.QPushButton(self.formLayoutWidget)
        self.aligngradf.setObjectName("aligngradf")
        self.formLayout.setWidget(16, QtGui.QFormLayout.FieldRole, self.aligngradf)
        self.label_18 = QtGui.QLabel(self.formLayoutWidget)
        self.label_18.setObjectName("label_18")
        self.formLayout.setWidget(17, QtGui.QFormLayout.LabelRole, self.label_18)
        self.offsetradf = QtGui.QLineEdit(self.formLayoutWidget)
        self.offsetradf.setObjectName("offsetradf")
        self.formLayout.setWidget(17, QtGui.QFormLayout.FieldRole, self.offsetradf)
        self.label_19 = QtGui.QLabel(self.formLayoutWidget)
        self.label_19.setObjectName("label_19")
        self.formLayout.setWidget(18, QtGui.QFormLayout.LabelRole, self.label_19)
        self.partfile = QtGui.QPushButton(self.formLayoutWidget)
        self.partfile.setObjectName("partfile")
        self.formLayout.setWidget(18, QtGui.QFormLayout.FieldRole, self.partfile)
        self.label_20 = QtGui.QLabel(self.formLayoutWidget)
        self.label_20.setObjectName("label_20")
        self.formLayout.setWidget(19, QtGui.QFormLayout.LabelRole, self.label_20)
        self.convharm = QtGui.QLineEdit(self.formLayoutWidget)
        self.convharm.setObjectName("convharm")
        self.formLayout.setWidget(19, QtGui.QFormLayout.FieldRole, self.convharm)
        self.label_21 = QtGui.QLabel(self.formLayoutWidget)
        self.label_21.setObjectName("label_21")
        self.formLayout.setWidget(20, QtGui.QFormLayout.LabelRole, self.label_21)
        self.multiconv = QtGui.QLineEdit(self.formLayoutWidget)
        self.multiconv.setObjectName("multiconv")
        self.formLayout.setWidget(20, QtGui.QFormLayout.FieldRole, self.multiconv)
        self.label_22 = QtGui.QLabel(self.formLayoutWidget)
        self.label_22.setObjectName("label_22")
        self.formLayout.setWidget(21, QtGui.QFormLayout.LabelRole, self.label_22)
        self.ibfield = QtGui.QLineEdit(self.formLayoutWidget)
        self.ibfield.setObjectName("ibfield")
        self.formLayout.setWidget(21, QtGui.QFormLayout.FieldRole, self.ibfield)
        self.label_23 = QtGui.QLabel(self.formLayoutWidget)
        self.label_23.setObjectName("label_23")
        self.formLayout.setWidget(22, QtGui.QFormLayout.LabelRole, self.label_23)
        self.imagl = QtGui.QLineEdit(self.formLayoutWidget)
        self.imagl.setObjectName("imagl")
        self.formLayout.setWidget(22, QtGui.QFormLayout.FieldRole, self.imagl)
        self.label_24 = QtGui.QLabel(self.formLayoutWidget)
        self.label_24.setObjectName("label_24")
        self.formLayout.setWidget(23, QtGui.QFormLayout.LabelRole, self.label_24)
        self.idril = QtGui.QLineEdit(self.formLayoutWidget)
        self.idril.setObjectName("idril")
        self.formLayout.setWidget(23, QtGui.QFormLayout.FieldRole, self.idril)
        self.label_25 = QtGui.QLabel(self.formLayoutWidget)
        self.label_25.setObjectName("label_25")
        self.formLayout.setWidget(24, QtGui.QFormLayout.LabelRole, self.label_25)
        self.trama = QtGui.QPushButton(self.formLayoutWidget)
        self.trama.setObjectName("trama")
        self.formLayout.setWidget(24, QtGui.QFormLayout.FieldRole, self.trama)
        self.label_26 = QtGui.QLabel(self.formLayoutWidget)
        self.label_26.setObjectName("label_26")
        self.formLayout.setWidget(25, QtGui.QFormLayout.LabelRole, self.label_26)
        self.ilog = QtGui.QPushButton(self.formLayoutWidget)
        self.ilog.setObjectName("ilog")
        self.formLayout.setWidget(25, QtGui.QFormLayout.FieldRole, self.ilog)
        self.label_27 = QtGui.QLabel(self.formLayoutWidget)
        self.label_27.setObjectName("label_27")
        self.formLayout.setWidget(26, QtGui.QFormLayout.LabelRole, self.label_27)
        self.ffspec = QtGui.QLineEdit(self.formLayoutWidget)
        self.ffspec.setObjectName("ffspec")
        self.formLayout.setWidget(26, QtGui.QFormLayout.FieldRole, self.ffspec)

        self.retranslateUi(io)
        QtCore.QMetaObject.connectSlotsByName(io)

    def retranslateUi(self, io):
        io.setWindowTitle(QtGui.QApplication.translate("io", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("io", "Output at each integration step:", None, QtGui.QApplication.UnicodeUTF8))
        self.iphsty.setText(QtGui.QApplication.translate("io", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("io", "Output at each Slice:", None, QtGui.QApplication.UnicodeUTF8))
        self.ishsty.setText(QtGui.QApplication.translate("io", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("io", "Output Particle Distribution at \n"
"each integration step", None, QtGui.QApplication.UnicodeUTF8))
        self.ippart.setText(QtGui.QApplication.translate("io", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("io", "Output Particle Distribution at\n"
"each slice:", None, QtGui.QApplication.UnicodeUTF8))
        self.ispart.setText(QtGui.QApplication.translate("io", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("io", "Output Field Distribution at \n"
"each integration step:", None, QtGui.QApplication.UnicodeUTF8))
        self.ipradi.setText(QtGui.QApplication.translate("io", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("io", "Output Field Distribution at\n"
"each slice:", None, QtGui.QApplication.UnicodeUTF8))
        self.isradi.setText(QtGui.QApplication.translate("io", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("io", "IOTAIL:", None, QtGui.QApplication.UnicodeUTF8))
        self.iotail.setText(QtGui.QApplication.translate("io", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("io", "Output File:", None, QtGui.QApplication.UnicodeUTF8))
        self.outputfile.setText(QtGui.QApplication.translate("io", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("io", "Magnetic Field Input:", None, QtGui.QApplication.UnicodeUTF8))
        self.magin.setText(QtGui.QApplication.translate("io", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("io", "Magnetic Field Output:", None, QtGui.QApplication.UnicodeUTF8))
        self.magout.setText(QtGui.QApplication.translate("io", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("io", "DUMP:", None, QtGui.QApplication.UnicodeUTF8))
        self.dump.setItemText(0, QtGui.QApplication.translate("io", "Field", None, QtGui.QApplication.UnicodeUTF8))
        self.dump.setItemText(1, QtGui.QApplication.translate("io", "Distribution", None, QtGui.QApplication.UnicodeUTF8))
        self.dump.setItemText(2, QtGui.QApplication.translate("io", "Field & Distribuition", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("io", "Beam Input File:", None, QtGui.QApplication.UnicodeUTF8))
        self.beamfile.setText(QtGui.QApplication.translate("io", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("io", "Seeding Radiation Input:", None, QtGui.QApplication.UnicodeUTF8))
        self.radfile.setText(QtGui.QApplication.translate("io", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("io", "6D Phase Space:", None, QtGui.QApplication.UnicodeUTF8))
        self.distfile.setText(QtGui.QApplication.translate("io", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("io", "NDCUT:", None, QtGui.QApplication.UnicodeUTF8))
        self.ndcut.setText(QtGui.QApplication.translate("io", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("io", "Field File:", None, QtGui.QApplication.UnicodeUTF8))
        self.fieldfile.setText(QtGui.QApplication.translate("io", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("io", "Align Radiation Field:", None, QtGui.QApplication.UnicodeUTF8))
        self.aligngradf.setText(QtGui.QApplication.translate("io", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("io", "Offset Radiation:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("io", "PARTFILE:", None, QtGui.QApplication.UnicodeUTF8))
        self.partfile.setText(QtGui.QApplication.translate("io", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("io", "CONVHARM:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("io", "MULTICONV:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("io", "IBFIELD:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("io", "IMAGL:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_24.setText(QtGui.QApplication.translate("io", "IDRIL:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_25.setText(QtGui.QApplication.translate("io", "Transport Matrix:", None, QtGui.QApplication.UnicodeUTF8))
        self.trama.setText(QtGui.QApplication.translate("io", "define matrix", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setText(QtGui.QApplication.translate("io", "Log:", None, QtGui.QApplication.UnicodeUTF8))
        self.ilog.setText(QtGui.QApplication.translate("io", "Yes/No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_27.setText(QtGui.QApplication.translate("io", "FFSPEC:", None, QtGui.QApplication.UnicodeUTF8))
