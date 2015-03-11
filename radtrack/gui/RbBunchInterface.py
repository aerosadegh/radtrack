# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RbBunchInterface.ui'
#
# Created: Thu May 08 10:40:22 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_bunchInterface(object):
    def setupUi(self, bunchInterface):
        bunchInterface.setObjectName("bunchInterface")
        bunchInterface.resize(1260, 758)
        self.formLayoutWidget = QtGui.QWidget(bunchInterface)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 120, 231, 74))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.numPtclsLabel = QtGui.QLabel(self.formLayoutWidget)
        self.numPtclsLabel.setObjectName("numPtclsLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.numPtclsLabel)
        self.numPtcls = QtGui.QLineEdit(self.formLayoutWidget)
        self.numPtcls.setObjectName("numPtcls")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.numPtcls)
        self.designMomentumLabel = QtGui.QLabel(self.formLayoutWidget)
        self.designMomentumLabel.setObjectName("designMomentumLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.designMomentumLabel)
        self.designMomentum = QtGui.QLineEdit(self.formLayoutWidget)
        self.designMomentum.setObjectName("designMomentum")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.designMomentum)
        self.charge = QtGui.QLabel(self.formLayoutWidget)
        self.charge.setObjectName("charge")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.charge)
        self.totalCharge = QtGui.QLineEdit(self.formLayoutWidget)
        self.totalCharge.setObjectName("totalCharge")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.totalCharge)
        self.twissTable = QtGui.QTableWidget(bunchInterface)
        self.twissTable.setGeometry(QtCore.QRect(10, 250, 341, 91))
        self.twissTable.setObjectName("twissTable")
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
        self.perpTwissLabel.setGeometry(QtCore.QRect(10, 230, 220, 20))
        self.perpTwissLabel.setObjectName("perpTwissLabel")
        self.highLevelInputsLabel = QtGui.QLabel(bunchInterface)
        self.highLevelInputsLabel.setGeometry(QtCore.QRect(10, 100, 110, 16))
        self.highLevelInputsLabel.setObjectName("highLevelInputsLabel")
        self.offsetLabel = QtGui.QLabel(bunchInterface)
        self.offsetLabel.setGeometry(QtCore.QRect(10, 470, 100, 20))
        self.offsetLabel.setObjectName("offsetLabel")
        self.offsetTable = QtGui.QTableWidget(bunchInterface)
        self.offsetTable.setGeometry(QtCore.QRect(10, 490, 241, 121))
        self.offsetTable.setObjectName("offsetTable")
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
        self.generateBunch.setGeometry(QtCore.QRect(10, 10, 101, 23))
        self.generateBunch.setObjectName("generateBunch")
        self.saveToFile = QtGui.QToolButton(bunchInterface)
        self.saveToFile.setGeometry(QtCore.QRect(130, 10, 81, 23))
        self.saveToFile.setObjectName("saveToFile")
        self.ypyPlot = matplotlibWidget(bunchInterface)
        self.ypyPlot.setGeometry(QtCore.QRect(830, 10, 411, 361))
        self.ypyPlot.setObjectName("ypyPlot")
        self.xyPlot = matplotlibWidget(bunchInterface)
        self.xyPlot.setGeometry(QtCore.QRect(390, 380, 421, 361))
        self.xyPlot.setObjectName("xyPlot")
        self.tpzPlot = matplotlibWidget(bunchInterface)
        self.tpzPlot.setGeometry(QtCore.QRect(830, 380, 411, 361))
        self.tpzPlot.setObjectName("tpzPlot")
        self.xpxPlot = matplotlibWidget(bunchInterface)
        self.xpxPlot.setGeometry(QtCore.QRect(390, 10, 421, 361))
        self.xpxPlot.setObjectName("xpxPlot")
        self.unitsLabel = QtGui.QLabel(bunchInterface)
        self.unitsLabel.setGeometry(QtCore.QRect(280, 100, 81, 16))
        self.unitsLabel.setObjectName("unitsLabel")
        self.formLayoutWidget_2 = QtGui.QWidget(bunchInterface)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(280, 120, 101, 74))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.units = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.units.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.units.setContentsMargins(0, 0, 0, 0)
        self.units.setObjectName("units")
        self.unitsPosLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.unitsPosLabel.setObjectName("unitsPosLabel")
        self.units.setWidget(0, QtGui.QFormLayout.LabelRole, self.unitsPosLabel)
        self.unitsPos = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.unitsPos.setObjectName("unitsPos")
        self.units.setWidget(0, QtGui.QFormLayout.FieldRole, self.unitsPos)
        self.unitsAngleLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.unitsAngleLabel.setObjectName("unitsAngleLabel")
        self.units.setWidget(1, QtGui.QFormLayout.LabelRole, self.unitsAngleLabel)
        self.unitsAngle = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.unitsAngle.setDragEnabled(True)
        self.unitsAngle.setObjectName("unitsAngle")
        self.units.setWidget(1, QtGui.QFormLayout.FieldRole, self.unitsAngle)
        self.ticksLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.ticksLabel.setObjectName("ticksLabel")
        self.units.setWidget(2, QtGui.QFormLayout.LabelRole, self.ticksLabel)
        self.numTicks = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.numTicks.setObjectName("numTicks")
        self.units.setWidget(2, QtGui.QFormLayout.FieldRole, self.numTicks)
        self.importFile = QtGui.QToolButton(bunchInterface)
        self.importFile.setGeometry(QtCore.QRect(130, 40, 81, 23))
        self.importFile.setObjectName("importFile")
        self.calculateTwiss = QtGui.QPushButton(bunchInterface)
        self.calculateTwiss.setGeometry(QtCore.QRect(5, 40, 115, 23))
        self.calculateTwiss.setObjectName("calculateTwiss")
        self.longTwissLabel = QtGui.QLabel(bunchInterface)
        self.longTwissLabel.setGeometry(QtCore.QRect(10, 370, 200, 20))
        self.longTwissLabel.setObjectName("longTwissLabel")
        self.twissTableZ = QtGui.QTableWidget(bunchInterface)
        self.twissTableZ.setGeometry(QtCore.QRect(10, 390, 341, 61))
        self.twissTableZ.setObjectName("twissTableZ")
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
        self.plotType.setGeometry(QtCore.QRect(280, 10, 71, 21))
        self.plotType.setObjectName("plotType")
        self.longTwissSpec = QtGui.QToolButton(bunchInterface)
        self.longTwissSpec.setGeometry(QtCore.QRect(300, 360, 50, 20))
        self.longTwissSpec.setObjectName("longTwissSpec")
        self.perpTwissSpec = QtGui.QToolButton(bunchInterface)
        self.perpTwissSpec.setGeometry(QtCore.QRect(300, 220, 50, 20))
        self.perpTwissSpec.setObjectName("perpTwissSpec")
        self.axisType = QtGui.QToolButton(bunchInterface)
        self.axisType.setGeometry(QtCore.QRect(280, 40, 71, 21))
        self.axisType.setObjectName("axisType")
        self.aspectRatio = QtGui.QToolButton(bunchInterface)
        self.aspectRatio.setGeometry(QtCore.QRect(320, 70, 31, 21))
        self.aspectRatio.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.aspectRatio.setObjectName("aspectRatio")
        self.noTitles = QtGui.QToolButton(bunchInterface)
        self.noTitles.setGeometry(QtCore.QRect(280, 70, 31, 21))
        self.noTitles.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.noTitles.setObjectName("noTitles")

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
        bunchInterface.setWindowTitle(QtGui.QApplication.translate("bunchInterface", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.numPtclsLabel.setText(QtGui.QApplication.translate("bunchInterface", "# macroparticles", None, QtGui.QApplication.UnicodeUTF8))
        self.numPtcls.setToolTip(QtGui.QApplication.translate("bunchInterface", "The number of macro-particles in the distribution.\n"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.designMomentumLabel.setText(QtGui.QApplication.translate("bunchInterface", "<html><head/><body><p>design pC [eV]</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.designMomentum.setToolTip(QtGui.QApplication.translate("bunchInterface", "<html><head/><body><p>Design momentum is the average momentum for zero offset.</p><p>Defaul units can be overridden.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.charge.setText(QtGui.QApplication.translate("bunchInterface", "total Q [C]", None, QtGui.QApplication.UnicodeUTF8))
        self.totalCharge.setToolTip(QtGui.QApplication.translate("bunchInterface", "<html><head/><body><p>Total charge of the beam.</p><p>Default units [C] can be overridden.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.twissTable.setToolTip(QtGui.QApplication.translate("bunchInterface", "Specify the horizontal (x-x\') and vertical (y-y\') Twiss parameters for the bunch.\n"
"Default units for beta [m/rad] can be overridden as follows:\n"
"    mm (implies mm/rad), um (implies um/rad), etc.\n"
"    Note that [m/rad] is equivalent to [mm/mrad]\n"
"Default units for the emittance [m-rad] can also be overridden:\n"
"    microns (implies microns-rad, equivalent to mm-mrad), etc.\n"
"Do not specify units for alpha, which is dimensionless.", None, QtGui.QApplication.UnicodeUTF8))
        self.twissTable.verticalHeaderItem(0).setText(QtGui.QApplication.translate("bunchInterface", "x-x\'", None, QtGui.QApplication.UnicodeUTF8))
        self.twissTable.verticalHeaderItem(1).setText(QtGui.QApplication.translate("bunchInterface", "y-y\'", None, QtGui.QApplication.UnicodeUTF8))
        self.twissTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("bunchInterface", "alpha", None, QtGui.QApplication.UnicodeUTF8))
        self.twissTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("bunchInterface", "beta [m/rad]", None, QtGui.QApplication.UnicodeUTF8))
        self.twissTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("bunchInterface", "eps [m-rad]", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.twissTable.isSortingEnabled()
        self.twissTable.setSortingEnabled(False)
        self.twissTable.setSortingEnabled(__sortingEnabled)
        self.perpTwissLabel.setText(QtGui.QApplication.translate("bunchInterface", "Twiss Parameters (rms, normalized)", None, QtGui.QApplication.UnicodeUTF8))
        self.highLevelInputsLabel.setText(QtGui.QApplication.translate("bunchInterface", "Charge & Energy", None, QtGui.QApplication.UnicodeUTF8))
        self.offsetLabel.setText(QtGui.QApplication.translate("bunchInterface", "beam offsets", None, QtGui.QApplication.UnicodeUTF8))
        self.offsetTable.setToolTip(QtGui.QApplication.translate("bunchInterface", "Specification of the bunch offsets in position and angle.\n"
"In general, these should be small compared to bunch dimensions.\n"
"Default units can be overridden in the usual way.\n"
"    s = ct\n"
"    dp = relative momentum spread with respect to design momentum\n"
"\n"
"The offset in \'s\' can be large, as it represents the full distance\n"
"    propagated by the bunch down the beamline.", None, QtGui.QApplication.UnicodeUTF8))
        self.offsetTable.verticalHeaderItem(0).setText(QtGui.QApplication.translate("bunchInterface", "x-x\'", None, QtGui.QApplication.UnicodeUTF8))
        self.offsetTable.verticalHeaderItem(1).setText(QtGui.QApplication.translate("bunchInterface", "y-y\'", None, QtGui.QApplication.UnicodeUTF8))
        self.offsetTable.verticalHeaderItem(2).setText(QtGui.QApplication.translate("bunchInterface", "s-dp", None, QtGui.QApplication.UnicodeUTF8))
        self.offsetTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("bunchInterface", "position [m]", None, QtGui.QApplication.UnicodeUTF8))
        self.offsetTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("bunchInterface", "angle [rad]", None, QtGui.QApplication.UnicodeUTF8))
        self.generateBunch.setToolTip(QtGui.QApplication.translate("bunchInterface", "Generate a particle beam with the specified parameters.", None, QtGui.QApplication.UnicodeUTF8))
        self.generateBunch.setText(QtGui.QApplication.translate("bunchInterface", "Generate Beam", None, QtGui.QApplication.UnicodeUTF8))
        self.saveToFile.setToolTip(QtGui.QApplication.translate("bunchInterface", "Save particle data to a file.", None, QtGui.QApplication.UnicodeUTF8))
        self.saveToFile.setText(QtGui.QApplication.translate("bunchInterface", "Save to File", None, QtGui.QApplication.UnicodeUTF8))
        self.ypyPlot.setToolTip(QtGui.QApplication.translate("bunchInterface", "The 2D vertical projection (y-y\') of the full 6D phase space.\n"
"Use \'Plot Type\' button to select scatter, contour, combo or to erase.\n"
"Use \'Axis Type\' button to center plot on bunch or on beamline axis.\n"
"Use \'NT\' button to toggle the title on or off (more room for image).\n"
"\n"
"The icons below are standard features of matplotlib, which provide\n"
"full interactivity and allow for saving of publication quality graphics.", None, QtGui.QApplication.UnicodeUTF8))
        self.xyPlot.setToolTip(QtGui.QApplication.translate("bunchInterface", "Transverse cross-section (x-y) of the full 6D bunch distribution.\n"
"Use \'Plot Type\' button to select scatter, contour, combo or to erase.\n"
"Use \'Axis Type\' button to center plot on bunch or on beamline axis.\n"
"Use \'NT\' button to toggle the title on or off (more room for image).\n"
"Use \'AR\' button to toggle aspect ratio between \'square\' and \'tight\',\n"
"    where \'square\' means that a round beam will be seen as round,\n"
"    while \'tight\' uses the plot area most effectively.\n"
"\n"
"The icons below are standard features of matplotlib, which provide\n"
"full interactivity and allow for saving of publication quality graphics.", None, QtGui.QApplication.UnicodeUTF8))
        self.tpzPlot.setToolTip(QtGui.QApplication.translate("bunchInterface", "The 2D longitudinal projection (s-dp) of the full 6D phase space.\n"
"    s = ct  includes the full propagation distance of the bunch\n"
"    dp is the relative momentum spread, with respect to design value.\n"
"Use \'Plot Type\' button to select scatter, contour, combo or to erase.\n"
"Use \'Axis Type\' button to center plot on bunch or on beamline axis.\n"
"Use \'NT\' button to toggle the title on or off (more room for image).\n"
"\n"
"The icons below are standard features of matplotlib, which provide\n"
"full interactivity and allow for saving of publication quality graphics.", None, QtGui.QApplication.UnicodeUTF8))
        self.xpxPlot.setToolTip(QtGui.QApplication.translate("bunchInterface", "The 2D horizontal projection (x-x\') of the full 6D phase space.\n"
"Use \'Plot Type\' button to select scatter, contour, combo or to erase.\n"
"Use \'Axis Type\' button to center plot on bunch or on beamline axis.\n"
"Use \'NT\' button to toggle the title on or off (more room for image).\n"
"\n"
"The icons below are standard features of matplotlib, which provide\n"
"full interactivity and allow for saving of publication quality graphics.", None, QtGui.QApplication.UnicodeUTF8))
        self.unitsLabel.setText(QtGui.QApplication.translate("bunchInterface", "Plotting units", None, QtGui.QApplication.UnicodeUTF8))
        self.unitsPosLabel.setText(QtGui.QApplication.translate("bunchInterface", "position", None, QtGui.QApplication.UnicodeUTF8))
        self.unitsPos.setToolTip(QtGui.QApplication.translate("bunchInterface", "Units to be used for axis labels of position-like variables.\n"
"For example: m, mm, um (or microns), nm ...", None, QtGui.QApplication.UnicodeUTF8))
        self.unitsAngleLabel.setText(QtGui.QApplication.translate("bunchInterface", "<html><head/><body><p>angle</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.unitsAngle.setToolTip(QtGui.QApplication.translate("bunchInterface", "Units to be used for axis labels of angle-like variables.\n"
"For example: rad, mrad, urad (or microrad) ...", None, QtGui.QApplication.UnicodeUTF8))
        self.ticksLabel.setText(QtGui.QApplication.translate("bunchInterface", "# ticks", None, QtGui.QApplication.UnicodeUTF8))
        self.numTicks.setToolTip(QtGui.QApplication.translate("bunchInterface", "Suggest a maximum # of tick marks for the axes.\n"
"Logic for actual # is due to matplotlib library.", None, QtGui.QApplication.UnicodeUTF8))
        self.importFile.setToolTip(QtGui.QApplication.translate("bunchInterface", "Import particle data from a file.", None, QtGui.QApplication.UnicodeUTF8))
        self.importFile.setText(QtGui.QApplication.translate("bunchInterface", "Import File", None, QtGui.QApplication.UnicodeUTF8))
        self.calculateTwiss.setToolTip(QtGui.QApplication.translate("bunchInterface", "<html><head/><body><p>Calculate Twiss parameters directly from particle distribution and overwrite all fields.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.calculateTwiss.setText(QtGui.QApplication.translate("bunchInterface", "Calculate Twiss", None, QtGui.QApplication.UnicodeUTF8))
        self.longTwissLabel.setText(QtGui.QApplication.translate("bunchInterface", "Longitudinal phase space (rms)", None, QtGui.QApplication.UnicodeUTF8))
        self.twissTableZ.setToolTip(QtGui.QApplication.translate("bunchInterface", "Specification of the longitucinal phase space varies widely.\n"
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
"            e.g. 1 mrad = 0.001 rad = 0.1%   (but don\'t use % symbol)", None, QtGui.QApplication.UnicodeUTF8))
        self.twissTableZ.verticalHeaderItem(0).setText(QtGui.QApplication.translate("bunchInterface", "s-dp", None, QtGui.QApplication.UnicodeUTF8))
        self.twissTableZ.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("bunchInterface", "alpha", None, QtGui.QApplication.UnicodeUTF8))
        self.twissTableZ.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("bunchInterface", "bct [m]", None, QtGui.QApplication.UnicodeUTF8))
        self.twissTableZ.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("bunchInterface", "dp/p [rad]", None, QtGui.QApplication.UnicodeUTF8))
        self.plotType.setToolTip(QtGui.QApplication.translate("bunchInterface", "Choose how particle data should be plotted.", None, QtGui.QApplication.UnicodeUTF8))
        self.plotType.setText(QtGui.QApplication.translate("bunchInterface", "Plot Type", None, QtGui.QApplication.UnicodeUTF8))
        self.longTwissSpec.setToolTip(QtGui.QApplication.translate("bunchInterface", "Choose how longitudinal Twiss parameters are to be specified.", None, QtGui.QApplication.UnicodeUTF8))
        self.longTwissSpec.setText(QtGui.QApplication.translate("bunchInterface", "Spec", None, QtGui.QApplication.UnicodeUTF8))
        self.perpTwissSpec.setToolTip(QtGui.QApplication.translate("bunchInterface", "Choose how transverse Twiss parameters are to be specified.", None, QtGui.QApplication.UnicodeUTF8))
        self.perpTwissSpec.setText(QtGui.QApplication.translate("bunchInterface", "Spec", None, QtGui.QApplication.UnicodeUTF8))
        self.axisType.setToolTip(QtGui.QApplication.translate("bunchInterface", "Choose a convention for the axis limits.", None, QtGui.QApplication.UnicodeUTF8))
        self.axisType.setText(QtGui.QApplication.translate("bunchInterface", "Axis Type", None, QtGui.QApplication.UnicodeUTF8))
        self.aspectRatio.setToolTip(QtGui.QApplication.translate("bunchInterface", "Toggle the aspect ratio of the x-y plot.", None, QtGui.QApplication.UnicodeUTF8))
        self.aspectRatio.setText(QtGui.QApplication.translate("bunchInterface", "AR", None, QtGui.QApplication.UnicodeUTF8))
        self.noTitles.setToolTip(QtGui.QApplication.translate("bunchInterface", "Toggle plot titles on/off.", None, QtGui.QApplication.UnicodeUTF8))
        self.noTitles.setStatusTip(QtGui.QApplication.translate("bunchInterface", "Toggle plot titles on/off.", None, QtGui.QApplication.UnicodeUTF8))
        self.noTitles.setText(QtGui.QApplication.translate("bunchInterface", "NT", None, QtGui.QApplication.UnicodeUTF8))

from matplotlibwidget import matplotlibWidget
