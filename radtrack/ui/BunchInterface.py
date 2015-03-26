# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BunchInterface.ui'
#
# Created: Fri Mar 20 17:26:24 2015
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

class Ui_bunchInterface(object):
    def setupUi(self, bunchInterface):
        bunchInterface.setObjectName(_fromUtf8("bunchInterface"))
        bunchInterface.resize(1260, 791)
        self.formLayoutWidget = QtGui.QWidget(bunchInterface)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 160, 231, 85))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.numPtclsLabel = QtGui.QLabel(self.formLayoutWidget)
        self.numPtclsLabel.setObjectName(_fromUtf8("numPtclsLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.numPtclsLabel)
        self.numPtcls = QtGui.QLineEdit(self.formLayoutWidget)
        self.numPtcls.setObjectName(_fromUtf8("numPtcls"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.numPtcls)
        self.designMomentumLabel = QtGui.QLabel(self.formLayoutWidget)
        self.designMomentumLabel.setObjectName(_fromUtf8("designMomentumLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.designMomentumLabel)
        self.designMomentum = QtGui.QLineEdit(self.formLayoutWidget)
        self.designMomentum.setObjectName(_fromUtf8("designMomentum"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.designMomentum)
        self.charge = QtGui.QLabel(self.formLayoutWidget)
        self.charge.setObjectName(_fromUtf8("charge"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.charge)
        self.totalCharge = QtGui.QLineEdit(self.formLayoutWidget)
        self.totalCharge.setObjectName(_fromUtf8("totalCharge"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.totalCharge)
        self.twissTable = QtGui.QTableWidget(bunchInterface)
        self.twissTable.setGeometry(QtCore.QRect(10, 290, 341, 91))
        self.twissTable.setObjectName(_fromUtf8("twissTable"))
        self.twissTable.setColumnCount(3)
        self.twissTable.setRowCount(2)
        item = QtGui.QTableWidgetItem()
        self.twissTable.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.twissTable.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.twissTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.twissTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.twissTable.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.twissTable.setItem(0, 0, item)
        self.perpTwissLabel = QtGui.QLabel(bunchInterface)
        self.perpTwissLabel.setGeometry(QtCore.QRect(10, 270, 221, 20))
        self.perpTwissLabel.setObjectName(_fromUtf8("perpTwissLabel"))
        self.highLevelInputsLabel = QtGui.QLabel(bunchInterface)
        self.highLevelInputsLabel.setGeometry(QtCore.QRect(10, 140, 131, 16))
        self.highLevelInputsLabel.setObjectName(_fromUtf8("highLevelInputsLabel"))
        self.offsetLabel = QtGui.QLabel(bunchInterface)
        self.offsetLabel.setGeometry(QtCore.QRect(10, 520, 101, 20))
        self.offsetLabel.setObjectName(_fromUtf8("offsetLabel"))
        self.offsetTable = QtGui.QTableWidget(bunchInterface)
        self.offsetTable.setGeometry(QtCore.QRect(10, 540, 241, 121))
        self.offsetTable.setObjectName(_fromUtf8("offsetTable"))
        self.offsetTable.setColumnCount(2)
        self.offsetTable.setRowCount(3)
        item = QtGui.QTableWidgetItem()
        self.offsetTable.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.offsetTable.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.offsetTable.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.offsetTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.offsetTable.setHorizontalHeaderItem(1, item)
        self.generateBunch = QtGui.QToolButton(bunchInterface)
        self.generateBunch.setGeometry(QtCore.QRect(10, 50, 101, 23))
        self.generateBunch.setObjectName(_fromUtf8("generateBunch"))
        self.saveToFile = QtGui.QToolButton(bunchInterface)
        self.saveToFile.setGeometry(QtCore.QRect(130, 50, 81, 23))
        self.saveToFile.setObjectName(_fromUtf8("saveToFile"))
        self.ypyPlot = matplotlibWidget(bunchInterface)
        self.ypyPlot.setGeometry(QtCore.QRect(830, 50, 411, 361))
        self.ypyPlot.setObjectName(_fromUtf8("ypyPlot"))
        self.xyPlot = matplotlibWidget(bunchInterface)
        self.xyPlot.setGeometry(QtCore.QRect(390, 420, 421, 361))
        self.xyPlot.setObjectName(_fromUtf8("xyPlot"))
        self.tpzPlot = matplotlibWidget(bunchInterface)
        self.tpzPlot.setGeometry(QtCore.QRect(830, 420, 411, 361))
        self.tpzPlot.setObjectName(_fromUtf8("tpzPlot"))
        self.xpxPlot = matplotlibWidget(bunchInterface)
        self.xpxPlot.setGeometry(QtCore.QRect(390, 50, 421, 361))
        self.xpxPlot.setObjectName(_fromUtf8("xpxPlot"))
        self.unitsLabel = QtGui.QLabel(bunchInterface)
        self.unitsLabel.setGeometry(QtCore.QRect(280, 140, 81, 16))
        self.unitsLabel.setObjectName(_fromUtf8("unitsLabel"))
        self.formLayoutWidget_2 = QtGui.QWidget(bunchInterface)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(270, 160, 111, 85))
        self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
        self.units = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.units.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.units.setMargin(0)
        self.units.setObjectName(_fromUtf8("units"))
        self.unitsPosLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.unitsPosLabel.setObjectName(_fromUtf8("unitsPosLabel"))
        self.units.setWidget(0, QtGui.QFormLayout.LabelRole, self.unitsPosLabel)
        self.unitsPos = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.unitsPos.setObjectName(_fromUtf8("unitsPos"))
        self.units.setWidget(0, QtGui.QFormLayout.FieldRole, self.unitsPos)
        self.unitsAngleLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.unitsAngleLabel.setObjectName(_fromUtf8("unitsAngleLabel"))
        self.units.setWidget(1, QtGui.QFormLayout.LabelRole, self.unitsAngleLabel)
        self.unitsAngle = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.unitsAngle.setDragEnabled(True)
        self.unitsAngle.setObjectName(_fromUtf8("unitsAngle"))
        self.units.setWidget(1, QtGui.QFormLayout.FieldRole, self.unitsAngle)
        self.ticksLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.ticksLabel.setObjectName(_fromUtf8("ticksLabel"))
        self.units.setWidget(2, QtGui.QFormLayout.LabelRole, self.ticksLabel)
        self.numTicks = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.numTicks.setObjectName(_fromUtf8("numTicks"))
        self.units.setWidget(2, QtGui.QFormLayout.FieldRole, self.numTicks)
        self.importFile = QtGui.QToolButton(bunchInterface)
        self.importFile.setGeometry(QtCore.QRect(130, 80, 81, 23))
        self.importFile.setObjectName(_fromUtf8("importFile"))
        self.calculateTwiss = QtGui.QPushButton(bunchInterface)
        self.calculateTwiss.setGeometry(QtCore.QRect(5, 80, 115, 23))
        self.calculateTwiss.setObjectName(_fromUtf8("calculateTwiss"))
        self.longTwissLabel = QtGui.QLabel(bunchInterface)
        self.longTwissLabel.setGeometry(QtCore.QRect(10, 410, 191, 20))
        self.longTwissLabel.setObjectName(_fromUtf8("longTwissLabel"))
        self.twissTableZ = QtGui.QTableWidget(bunchInterface)
        self.twissTableZ.setGeometry(QtCore.QRect(10, 430, 341, 71))
        self.twissTableZ.setObjectName(_fromUtf8("twissTableZ"))
        self.twissTableZ.setColumnCount(3)
        self.twissTableZ.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.twissTableZ.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.twissTableZ.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.twissTableZ.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.twissTableZ.setHorizontalHeaderItem(2, item)
        self.plotType = QtGui.QToolButton(bunchInterface)
        self.plotType.setGeometry(QtCore.QRect(280, 50, 71, 21))
        self.plotType.setObjectName(_fromUtf8("plotType"))
        self.longTwissSpec = QtGui.QToolButton(bunchInterface)
        self.longTwissSpec.setGeometry(QtCore.QRect(290, 400, 51, 20))
        self.longTwissSpec.setObjectName(_fromUtf8("longTwissSpec"))
        self.perpTwissSpec = QtGui.QToolButton(bunchInterface)
        self.perpTwissSpec.setGeometry(QtCore.QRect(290, 260, 51, 20))
        self.perpTwissSpec.setObjectName(_fromUtf8("perpTwissSpec"))
        self.axisType = QtGui.QToolButton(bunchInterface)
        self.axisType.setGeometry(QtCore.QRect(280, 80, 71, 21))
        self.axisType.setObjectName(_fromUtf8("axisType"))
        self.aspectRatio = QtGui.QToolButton(bunchInterface)
        self.aspectRatio.setGeometry(QtCore.QRect(320, 110, 31, 21))
        self.aspectRatio.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.aspectRatio.setObjectName(_fromUtf8("aspectRatio"))
        self.noTitles = QtGui.QToolButton(bunchInterface)
        self.noTitles.setGeometry(QtCore.QRect(280, 110, 31, 21))
        self.noTitles.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.noTitles.setObjectName(_fromUtf8("noTitles"))
        self.noTitles_2 = QtGui.QToolButton(bunchInterface)
        self.noTitles_2.setGeometry(QtCore.QRect(310, 520, 31, 21))
        self.noTitles_2.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.noTitles_2.setObjectName(_fromUtf8("noTitles_2"))
        self.toggleToolTips = QtGui.QToolButton(bunchInterface)
        self.toggleToolTips.setGeometry(QtCore.QRect(220, 110, 51, 21))
        self.toggleToolTips.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.toggleToolTips.setObjectName(_fromUtf8("toggleToolTips"))
        self.overview = QtGui.QTextBrowser(bunchInterface)
        self.overview.setGeometry(QtCore.QRect(10, 10, 1241, 31))
        self.overview.setObjectName(_fromUtf8("overview"))

        self.retranslateUi(bunchInterface)
        QtCore.QMetaObject.connectSlotsByName(bunchInterface)
        bunchInterface.setTabOrder(self.numPtcls, self.designMomentum)
        bunchInterface.setTabOrder(self.designMomentum, self.generateBunch)
        bunchInterface.setTabOrder(self.generateBunch, self.calculateTwiss)
        bunchInterface.setTabOrder(self.calculateTwiss, self.saveToFile)
        bunchInterface.setTabOrder(self.saveToFile, self.importFile)
        bunchInterface.setTabOrder(self.importFile, self.unitsPos)
        bunchInterface.setTabOrder(self.unitsPos, self.unitsAngle)
        bunchInterface.setTabOrder(self.unitsAngle, self.twissTable)
        bunchInterface.setTabOrder(self.twissTable, self.twissTableZ)
        bunchInterface.setTabOrder(self.twissTableZ, self.offsetTable)

    def retranslateUi(self, bunchInterface):
        bunchInterface.setWindowTitle(_translate("bunchInterface", "Form", None))
        self.numPtclsLabel.setText(_translate("bunchInterface", "# macroparticles", None))
        self.numPtcls.setToolTip(_translate("bunchInterface", "The number of macro-particles in the distribution.\n"
"", None))
        self.designMomentumLabel.setText(_translate("bunchInterface", "<html><head/><body><p>design pC [eV]</p></body></html>", None))
        self.designMomentum.setToolTip(_translate("bunchInterface", "<html><head/><body><p>Design momentum is the average momentum for zero offset.</p><p>Defaul units can be overridden.</p></body></html>", None))
        self.charge.setText(_translate("bunchInterface", "total Q [C]", None))
        self.totalCharge.setToolTip(_translate("bunchInterface", "<html><head/><body><p>Total charge of the beam.</p><p>Default units [C] can be overridden.</p></body></html>", None))
        self.twissTable.setToolTip(_translate("bunchInterface", "Specify the horizontal (x-x\') and vertical (y-y\') Twiss parameters for the bunch.\n"
"Default units for beta [m/rad] can be overridden as follows:\n"
"    mm (implies mm/rad), um (implies um/rad), etc.\n"
"    Note that [m/rad] is equivalent to [mm/mrad]\n"
"Default units for the emittance [m-rad] can also be overridden:\n"
"    microns (implies microns-rad, equivalent to mm-mrad), etc.\n"
"Do not specify units for alpha, which is dimensionless.", None))
        item = self.twissTable.verticalHeaderItem(0)
        item.setText(_translate("bunchInterface", "x-x\'", None))
        item = self.twissTable.verticalHeaderItem(1)
        item.setText(_translate("bunchInterface", "y-y\'", None))
        item = self.twissTable.horizontalHeaderItem(0)
        item.setText(_translate("bunchInterface", "alpha", None))
        item = self.twissTable.horizontalHeaderItem(1)
        item.setText(_translate("bunchInterface", "beta [m/rad]", None))
        item = self.twissTable.horizontalHeaderItem(2)
        item.setText(_translate("bunchInterface", "eps [m-rad]", None))
        __sortingEnabled = self.twissTable.isSortingEnabled()
        self.twissTable.setSortingEnabled(False)
        self.twissTable.setSortingEnabled(__sortingEnabled)
        self.perpTwissLabel.setText(_translate("bunchInterface", "Twiss Parameters (rms, normalized)", None))
        self.highLevelInputsLabel.setText(_translate("bunchInterface", "Charge & Energy", None))
        self.offsetLabel.setText(_translate("bunchInterface", "beam offsets", None))
        self.offsetTable.setToolTip(_translate("bunchInterface", "Specification of the bunch offsets in position and angle.\n"
"In general, these should be small compared to bunch dimensions.\n"
"Default units can be overridden in the usual way.\n"
"    s = ct\n"
"    dp = relative momentum spread with respect to design momentum\n"
"\n"
"The offset in \'s\' can be large, as it represents the full distance\n"
"    propagated by the bunch down the beamline.", None))
        item = self.offsetTable.verticalHeaderItem(0)
        item.setText(_translate("bunchInterface", "x-x\'", None))
        item = self.offsetTable.verticalHeaderItem(1)
        item.setText(_translate("bunchInterface", "y-y\'", None))
        item = self.offsetTable.verticalHeaderItem(2)
        item.setText(_translate("bunchInterface", "s-dp", None))
        item = self.offsetTable.horizontalHeaderItem(0)
        item.setText(_translate("bunchInterface", "position [m]", None))
        item = self.offsetTable.horizontalHeaderItem(1)
        item.setText(_translate("bunchInterface", "angle [rad]", None))
        self.generateBunch.setToolTip(_translate("bunchInterface", "Generate a particle beam with the specified parameters.", None))
        self.generateBunch.setText(_translate("bunchInterface", "Generate Beam", None))
        self.saveToFile.setToolTip(_translate("bunchInterface", "Save particle data to a file.", None))
        self.saveToFile.setText(_translate("bunchInterface", "Save to File", None))
        self.ypyPlot.setToolTip(_translate("bunchInterface", "The 2D vertical projection (y-y\') of the full 6D phase space.\n"
"Use \'Plot Type\' button to select scatter, contour, combo or to erase.\n"
"Use \'Axis Type\' button to center plot on bunch or on beamline axis.\n"
"Use \'NT\' button to toggle the title on or off (more room for image).\n"
"\n"
"The icons below are standard features of matplotlib, which provide\n"
"full interactivity and allow for saving of publication quality graphics.", None))
        self.xyPlot.setToolTip(_translate("bunchInterface", "Transverse cross-section (x-y) of the full 6D bunch distribution.\n"
"Use \'Plot Type\' button to select scatter, contour, combo or to erase.\n"
"Use \'Axis Type\' button to center plot on bunch or on beamline axis.\n"
"Use \'NT\' button to toggle the title on or off (more room for image).\n"
"Use \'AR\' button to toggle aspect ratio between \'square\' and \'tight\',\n"
"    where \'square\' means that a round beam will be seen as round,\n"
"    while \'tight\' uses the plot area most effectively.\n"
"\n"
"The icons below are standard features of matplotlib, which provide\n"
"full interactivity and allow for saving of publication quality graphics.", None))
        self.tpzPlot.setToolTip(_translate("bunchInterface", "The 2D longitudinal projection (s-dp) of the full 6D phase space.\n"
"    s = ct  includes the full propagation distance of the bunch\n"
"    dp is the relative momentum spread, with respect to design value.\n"
"Use \'Plot Type\' button to select scatter, contour, combo or to erase.\n"
"Use \'Axis Type\' button to center plot on bunch or on beamline axis.\n"
"Use \'NT\' button to toggle the title on or off (more room for image).\n"
"\n"
"The icons below are standard features of matplotlib, which provide\n"
"full interactivity and allow for saving of publication quality graphics.", None))
        self.xpxPlot.setToolTip(_translate("bunchInterface", "The 2D horizontal projection (x-x\') of the full 6D phase space.\n"
"Use \'Plot Type\' button to select scatter, contour, combo or to erase.\n"
"Use \'Axis Type\' button to center plot on bunch or on beamline axis.\n"
"Use \'NT\' button to toggle the title on or off (more room for image).\n"
"\n"
"The icons below are standard features of matplotlib, which provide\n"
"full interactivity and allow for saving of publication quality graphics.", None))
        self.unitsLabel.setText(_translate("bunchInterface", "Plotting units", None))
        self.unitsPosLabel.setText(_translate("bunchInterface", "position", None))
        self.unitsPos.setToolTip(_translate("bunchInterface", "Units to be used for axis labels of position-like variables.\n"
"For example: m, mm, um (or microns), nm ...", None))
        self.unitsAngleLabel.setText(_translate("bunchInterface", "<html><head/><body><p>angle</p></body></html>", None))
        self.unitsAngle.setToolTip(_translate("bunchInterface", "Units to be used for axis labels of angle-like variables.\n"
"For example: rad, mrad, urad (or microrad) ...", None))
        self.ticksLabel.setText(_translate("bunchInterface", "# ticks", None))
        self.numTicks.setToolTip(_translate("bunchInterface", "Suggest a maximum # of tick marks for the axes.\n"
"Logic for actual # is due to matplotlib library.", None))
        self.importFile.setToolTip(_translate("bunchInterface", "Import particle data from a file.", None))
        self.importFile.setText(_translate("bunchInterface", "Import File", None))
        self.calculateTwiss.setToolTip(_translate("bunchInterface", "<html><head/><body><p>Calculate Twiss parameters directly from particle distribution and overwrite all fields.</p></body></html>", None))
        self.calculateTwiss.setText(_translate("bunchInterface", "Calculate Twiss", None))
        self.longTwissLabel.setText(_translate("bunchInterface", "Longitudinal phase space (rms)", None))
        self.twissTableZ.setToolTip(_translate("bunchInterface", "Specification of the longitucinal phase space varies widely.\n"
"Use the \'Spec\' button to the upper right to choose a convention.\n"
"RMS values are specified, with default units shown in the label.\n"
"\n"
"Default units can be overridden in the usual way.\n"
"Default units for the emittance [m-rad] can also be overridden:\n"
"    microns (implies microns-rad, equivalent to mm-mrad), etc.\n"
"Do not specify units for alpha, which is dimensionless.\n"
"\n"
"    s = ct\n"
"    bct = beta0*s  (beta0 is relativistic factor; not Twiss beta)\n"
"    dp = relative momentum spread with respect to design momentum\n"
"            units (rad, mrad, etc.) represent the fractional value\n"
"            e.g. 1 mrad = 0.001 rad = 0.1%   (but don\'t use % symbol)", None))
        item = self.twissTableZ.verticalHeaderItem(0)
        item.setText(_translate("bunchInterface", "s-dp", None))
        item = self.twissTableZ.horizontalHeaderItem(0)
        item.setText(_translate("bunchInterface", "alpha", None))
        item = self.twissTableZ.horizontalHeaderItem(1)
        item.setText(_translate("bunchInterface", "bct [m]", None))
        item = self.twissTableZ.horizontalHeaderItem(2)
        item.setText(_translate("bunchInterface", "dp/p [rad]", None))
        self.plotType.setToolTip(_translate("bunchInterface", "Choose how particle data should be plotted.", None))
        self.plotType.setText(_translate("bunchInterface", "Plot Type", None))
        self.longTwissSpec.setToolTip(_translate("bunchInterface", "Choose how longitudinal Twiss parameters are to be specified.", None))
        self.longTwissSpec.setText(_translate("bunchInterface", "Spec", None))
        self.perpTwissSpec.setToolTip(_translate("bunchInterface", "Choose how transverse Twiss parameters are to be specified.", None))
        self.perpTwissSpec.setText(_translate("bunchInterface", "Spec", None))
        self.axisType.setToolTip(_translate("bunchInterface", "Choose a convention for the axis limits.", None))
        self.axisType.setText(_translate("bunchInterface", "Axis Type", None))
        self.aspectRatio.setToolTip(_translate("bunchInterface", "Toggle the aspect ratio of the x-y plot.", None))
        self.aspectRatio.setText(_translate("bunchInterface", "AR", None))
        self.noTitles.setToolTip(_translate("bunchInterface", "Toggle plot titles on/off.", None))
        self.noTitles.setStatusTip(_translate("bunchInterface", "Toggle plot titles on/off.", None))
        self.noTitles.setText(_translate("bunchInterface", "NT", None))
        self.noTitles_2.setToolTip(_translate("bunchInterface", "Toggle plot titles on/off.", None))
        self.noTitles_2.setStatusTip(_translate("bunchInterface", "Toggle plot titles on/off.", None))
        self.noTitles_2.setText(_translate("bunchInterface", "NT", None))
        self.toggleToolTips.setToolTip(_translate("bunchInterface", "Toggle plot titles on/off.", None))
        self.toggleToolTips.setStatusTip(_translate("bunchInterface", "Toggle plot titles on/off.", None))
        self.toggleToolTips.setText(_translate("bunchInterface", "Tool Tips", None))
        self.overview.setHtml(_translate("bunchInterface", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">The bunch tab is used to create a 3D charged particle distribution.</span></p></body></html>", None))

from radtrack.gui.matplotlibwidget import matplotlibWidget
