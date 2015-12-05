# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BunchInterface.ui'
#
# Created: Sat May 02 21:02:17 2015
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
        bunchInterface.resize(1260, 761)
        self.formLayoutWidget = QtGui.QWidget(bunchInterface)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 120, 231, 85))
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
        self.twissTable.setGeometry(QtCore.QRect(10, 250, 341, 91))
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
        self.perpTwissLabel.setGeometry(QtCore.QRect(10, 230, 221, 20))
        self.perpTwissLabel.setObjectName(_fromUtf8("perpTwissLabel"))
        self.highLevelInputsLabel = QtGui.QLabel(bunchInterface)
        self.highLevelInputsLabel.setGeometry(QtCore.QRect(10, 100, 131, 16))
        self.highLevelInputsLabel.setObjectName(_fromUtf8("highLevelInputsLabel"))
        self.offsetLabel = QtGui.QLabel(bunchInterface)
        self.offsetLabel.setGeometry(QtCore.QRect(10, 480, 101, 20))
        self.offsetLabel.setObjectName(_fromUtf8("offsetLabel"))
        self.offsetTable = QtGui.QTableWidget(bunchInterface)
        self.offsetTable.setGeometry(QtCore.QRect(10, 500, 241, 121))
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
        self.distribType = QtGui.QToolButton(bunchInterface)
        self.distribType.setGeometry(QtCore.QRect(10, 10, 111, 23))
        self.distribType.setObjectName(_fromUtf8("distribType"))
        self.ypyPlot = matplotlibWidget(bunchInterface)
        self.ypyPlot.setGeometry(QtCore.QRect(830, 10, 411, 361))
        self.ypyPlot.setObjectName(_fromUtf8("ypyPlot"))
        self.xyPlot = matplotlibWidget(bunchInterface)
        self.xyPlot.setGeometry(QtCore.QRect(390, 380, 421, 361))
        self.xyPlot.setObjectName(_fromUtf8("xyPlot"))
        self.tpzPlot = matplotlibWidget(bunchInterface)
        self.tpzPlot.setGeometry(QtCore.QRect(830, 380, 411, 361))
        self.tpzPlot.setObjectName(_fromUtf8("tpzPlot"))
        self.xpxPlot = matplotlibWidget(bunchInterface)
        self.xpxPlot.setGeometry(QtCore.QRect(390, 10, 421, 361))
        self.xpxPlot.setObjectName(_fromUtf8("xpxPlot"))
        self.unitsLabel = QtGui.QLabel(bunchInterface)
        self.unitsLabel.setGeometry(QtCore.QRect(280, 100, 81, 16))
        self.unitsLabel.setObjectName(_fromUtf8("unitsLabel"))
        self.formLayoutWidget_2 = QtGui.QWidget(bunchInterface)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(260, 120, 101, 74))
        self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
        self.gridLayout = QtGui.QGridLayout(self.formLayoutWidget_2)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.unitsPosLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.unitsPosLabel.setObjectName(_fromUtf8("unitsPosLabel"))
        self.gridLayout.addWidget(self.unitsPosLabel, 0, 0, 1, 1)
        self.unitsPos = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.unitsPos.setObjectName(_fromUtf8("unitsPos"))
        self.gridLayout.addWidget(self.unitsPos, 0, 1, 1, 1)
        self.unitsAngleLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.unitsAngleLabel.setObjectName(_fromUtf8("unitsAngleLabel"))
        self.gridLayout.addWidget(self.unitsAngleLabel, 1, 0, 1, 1)
        self.unitsAngle = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.unitsAngle.setDragEnabled(True)
        self.unitsAngle.setObjectName(_fromUtf8("unitsAngle"))
        self.gridLayout.addWidget(self.unitsAngle, 1, 1, 1, 1)
        self.ticksLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.ticksLabel.setObjectName(_fromUtf8("ticksLabel"))
        self.gridLayout.addWidget(self.ticksLabel, 2, 0, 1, 1)
        self.numTicks = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.numTicks.setObjectName(_fromUtf8("numTicks"))
        self.gridLayout.addWidget(self.numTicks, 2, 1, 1, 1)
        self.longTwissLabel = QtGui.QLabel(bunchInterface)
        self.longTwissLabel.setGeometry(QtCore.QRect(10, 370, 191, 20))
        self.longTwissLabel.setObjectName(_fromUtf8("longTwissLabel"))
        self.twissTableZ = QtGui.QTableWidget(bunchInterface)
        self.twissTableZ.setGeometry(QtCore.QRect(10, 390, 341, 61))
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
        self.plotType.setGeometry(QtCore.QRect(280, 10, 71, 21))
        self.plotType.setObjectName(_fromUtf8("plotType"))
        self.longTwissSpec = QtGui.QToolButton(bunchInterface)
        self.longTwissSpec.setGeometry(QtCore.QRect(290, 360, 51, 20))
        self.longTwissSpec.setObjectName(_fromUtf8("longTwissSpec"))
        self.perpTwissSpec = QtGui.QToolButton(bunchInterface)
        self.perpTwissSpec.setGeometry(QtCore.QRect(290, 220, 51, 20))
        self.perpTwissSpec.setObjectName(_fromUtf8("perpTwissSpec"))
        self.axisType = QtGui.QToolButton(bunchInterface)
        self.axisType.setGeometry(QtCore.QRect(280, 40, 71, 21))
        self.axisType.setObjectName(_fromUtf8("axisType"))
        self.aspectRatio = QtGui.QToolButton(bunchInterface)
        self.aspectRatio.setGeometry(QtCore.QRect(320, 70, 31, 21))
        self.aspectRatio.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.aspectRatio.setObjectName(_fromUtf8("aspectRatio"))
        self.noTitles = QtGui.QToolButton(bunchInterface)
        self.noTitles.setGeometry(QtCore.QRect(280, 70, 31, 21))
        self.noTitles.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.noTitles.setObjectName(_fromUtf8("noTitles"))

        self.retranslateUi(bunchInterface)
        QtCore.QMetaObject.connectSlotsByName(bunchInterface)
        bunchInterface.setTabOrder(self.numPtcls, self.designMomentum)
        bunchInterface.setTabOrder(self.designMomentum, self.distribType)
        bunchInterface.setTabOrder(self.distribType, self.unitsPos)
        bunchInterface.setTabOrder(self.unitsPos, self.unitsAngle)
        bunchInterface.setTabOrder(self.unitsAngle, self.twissTable)
        bunchInterface.setTabOrder(self.twissTable, self.twissTableZ)
        bunchInterface.setTabOrder(self.twissTableZ, self.offsetTable)

    def retranslateUi(self, bunchInterface):
        bunchInterface.setWindowTitle(_translate("bunchInterface", "Form", None))
        self.numPtclsLabel.setText(_translate("bunchInterface", "# macroparticles   ", None))
        self.numPtcls.setToolTip(_translate("bunchInterface", "The number of macro-particles in the distribution.", None))
        self.designMomentumLabel.setText(_translate("bunchInterface", "momentum [eV]", None))
        self.designMomentum.setToolTip(_translate("bunchInterface", "Design momentum is the average momentum for zero offset.\nDefaul units can be overridden.", None))
        self.charge.setText(_translate("bunchInterface", "total Q [C]", None))
        self.totalCharge.setToolTip(_translate("bunchInterface", "Total charge of the beam.\nDefault units [C] can be overridden.", None))
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
        self.distribType.setToolTip(_translate("bunchInterface", "Select the desired particle distribution type.", None))
        self.distribType.setText(_translate("bunchInterface", "Distribution", None))
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
        self.unitsPosLabel.setText(_translate("bunchInterface", "position     ", None))
        self.unitsPos.setToolTip(_translate("bunchInterface", "Units to be used for axis labels of position-like variables.\n"
"For example: m, mm, um (or microns), nm ...", None))
        self.unitsAngleLabel.setText(_translate("bunchInterface", "angle", None))
        self.unitsAngle.setToolTip(_translate("bunchInterface", "Units to be used for axis labels of angle-like variables.\n"
"For example: rad, mrad, urad (or microrad) ...", None))
        self.ticksLabel.setText(_translate("bunchInterface", "# ticks", None))
        self.numTicks.setToolTip(_translate("bunchInterface", "Suggest a maximum # of tick marks for the axes.\n"
"Logic for actual # is due to matplotlib library.", None))
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

from radtrack.gui.matplotlibwidget import matplotlibWidget
