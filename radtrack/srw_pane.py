# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newsrw.ui'
#
# Created: Fri May  8 14:02:42 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from radtrack.rt_pyqt4 import QtCore, QtGui, fromUtf8, translate

from pykern.pkdebug import pkdc, pkdi, pkdp
from pykern import pkio
from pykern import pkresource

from radtrack import rt_params
from radtrack import srw_enums

def _size_expanding(w):
    if hasattr(w, 'setSizePolicy'):
        w.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    else:
        w.addStretch(1)

class Pane(object):
    def setupUi(self, calculation_pane, is_multi_particle=False):
        self.is_multi_particle = is_multi_particle

        calculation_pane.setStyleSheet(pkio.read_text(pkresource.filename('srw_pane.css')))
        main = QtGui.QHBoxLayout()

        button_widget = QtGui.QWidget(calculation_pane)
        button_vbox = QtGui.QVBoxLayout()
        button_widget.setLayout(button_vbox)
        self.action_box = {}
        for n in ('Precision', 'Undulator', 'Beam', 'Analyze', 'Simulate'):
            a = QtGui.QPushButton(n, button_widget)
            a.setObjectName(n)
            a.setDefault(False)
            a.setAutoDefault(False)
            button_vbox.addWidget(a)
            policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
            #a.setSizePolicy(policy)
            self.action_box[n] = a
        main.addWidget(button_widget)
        pkdp('main.sizeHint={}', main.sizeHint())


        param_vbox = QtGui.QVBoxLayout()
        param_widget = QtGui.QWidget(calculation_pane)
        main.addLayout(param_vbox, stretch=4)

        hb = QtGui.QHBoxLayout()

        label = QtGui.QLabel(param_widget)
        label.setText('Simulation Kind: ')
        label.setObjectName('simulation_kind')
        hb.addWidget(label, alignment=QtCore.Qt.AlignRight)
        self.simulation_kind_value = QtGui.QComboBox(param_widget)
        hb.addWidget(self.simulation_kind_value)
        param_vbox.addLayout(hb)

        params = calculation_pane.params['Simulation Kind']
        self.wavefront_param_models = {}
        self.wavefront_param_view = QtGui.QTableView(param_widget)
        param_vbox.addWidget(self.wavefront_param_view)

        self.wavefront_param_view.horizontalHeader().setVisible(0)
        #self.wavefront_param_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.wavefront_param_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.wavefront_param_view.verticalHeader().setVisible(0)
        decl = list(rt_params.iter_primary_param_declarations(calculation_pane.declarations['Wavefront']))



        for sk in srw_enums.SimulationKind:
            if sk.name not in params:
                continue
            item = QtGui.QStandardItem()
            self.simulation_kind_value.addItem(
                fromUtf8(sk.display_name),
                userData=sk,
            )
            m = QtGui.QStandardItemModel(len(decl), 2);
            p = params[sk.name]['Wavefront']
            for (row, d) in enumerate(decl):
                item = QtGui.QStandardItem()
                item.setText(fromUtf8(str(d['label'])))
                m.setItem(row, 0, item)
                item = QtGui.QStandardItem()
                item.setText(fromUtf8(str(p[d['label']])))
                m.setItem(row, 1, item)
            self.wavefront_param_models[sk.name] = m
        self.wavefront_param_view.setModel(self.wavefront_param_models['E'])

        pkdp('param_vbox.sizeHint={}', param_vbox.sizeHint())
        pkdp('main.sizeHint={}', main.sizeHint())



        #### Simulation Results

        simulation_vbox = QtGui.QVBoxLayout()
        main.addLayout(simulation_vbox, stretch=3)
        label = QtGui.QLabel(calculation_pane)
        label.setMinimumHeight(self.simulation_kind_value.sizeHint().height())
        label.setText('Simulation Results')
        label.setObjectName('simulation_results')
        simulation_vbox.addWidget(label, alignment=QtCore.Qt.AlignCenter)
        self.simulation = QtGui.QTextEdit(calculation_pane)
        simulation_vbox.addWidget(self.simulation)

        #### Analysis Results

        analysis_vbox = QtGui.QVBoxLayout()
        analysis_vbox.setObjectName('analysis_vbox')
        main.addLayout(analysis_vbox, stretch=3)
        label = QtGui.QLabel(calculation_pane)
        label.setText('Analysis Results')
        label.setObjectName('analysis_results')
        label.setMinimumHeight(self.simulation_kind_value.sizeHint().height())
        analysis_vbox.addWidget(label, alignment=QtCore.Qt.AlignCenter)
        self.analysis = QtGui.QTextEdit(calculation_pane)
        self.analysis.setObjectName('analysis_results')
        analysis_vbox.addWidget(self.analysis)

        pkdp('param_vbox.sizeHint={}', param_vbox.sizeHint())
        pkdp('main.sizeHint={}', main.sizeHint())
        pkdp('simulation_kind.sizeHint={}', self.simulation_kind_value.sizeHint())

        pkdp('label.sizeHint={}', label.sizeHint())

        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)





        param_widget.setSizePolicy(policy)

        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        button_widget.setSizePolicy(policy)

        policy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.wavefront_param_view.setSizePolicy(policy)
        self.wavefront_param_view.horizontalHeader().setSizePolicy(
            QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)

        calculation_pane.setLayout(main)

        fill_vbox = QtGui.QVBoxLayout()
        fill_widget = QtGui.QWidget(calculation_pane)
        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        fill_widget.setSizePolicy(policy)

        button_vbox.addStretch()
        # Adding either forces scrollbars
        #param_vbox.addStretch()
        #main.addStretch()

        pkdp('param_vbox.sizeHint={}', param_vbox.sizeHint())
        pkdp('main.sizeHint={}', main.sizeHint())

        return















        self.tableWidget = QtGui.QTableWidget(calculation_pane)
        self.tableWidget.setGeometry(QtCore.QRect(210, 130, 271, 321))
        self.tableWidget.setObjectName(fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(10)
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
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.status = QtGui.QTextEdit(calculation_pane)
        self.status.setGeometry(QtCore.QRect(500, 40, 251, 411))
        self.status.setObjectName(fromUtf8("status"))
        self.analytic = QtGui.QTextEdit(calculation_pane)
        self.analytic.setGeometry(QtCore.QRect(780, 40, 251, 411))
        self.analytic.setObjectName(fromUtf8("analytic"))
        self.label = QtGui.QLabel(calculation_pane)
        self.label.setGeometry(QtCore.QRect(600, 20, 71, 16))
        self.label.setObjectName(fromUtf8("label"))
        self.label_2 = QtGui.QLabel(calculation_pane)
        self.label_2.setGeometry(QtCore.QRect(850, 20, 161, 16))
        self.label_2.setObjectName(fromUtf8("label_2"))

        self.retranslateUi(calculation_pane)
        QtCore.QMetaObject.connectSlotsByName(calculation_pane)

    def retranslateUi(self, calculation_pane):
        calculation_pane.setWindowTitle(translate("calculation_pane", "calculation_pane", None))
        self.precision.setText(translate("calculation_pane", "Precision", None))
        self.undulator.setText(translate("calculation_pane", "Undulator", None))
        self.beam.setText(translate("calculation_pane", "Beam", None))
        self.analyze.setText(translate("calculation_pane", "Analyze", None))
        self.sim.setText(translate("calculation_pane", "Simulate", None))
        if not self.is_multi_particle:
            self.label_31.setText(translate("calculation_pane", "Polarization", None))
            self.label_32.setText(translate("calculation_pane", "Intensity", None))
            self.intensity.setItemText(0, translate("calculation_pane", "Single Electron Intensity", None))
            self.intensity.setItemText(1, translate("calculation_pane", "Single Electron Flux", None))
            self.intensity.setItemText(2, translate("calculation_pane", "Real Part of Electron E-Field", None))
            self.intensity.setItemText(3, translate("calculation_pane", "Imaginary Part of Electron E-Field", None))
        self.label_33.setText(translate("calculation_pane", "Dependent Argument", None))
        self.deparg.setItemText(0, translate("calculation_pane", "e (energy)", None))
        self.deparg.setItemText(1, translate("calculation_pane", "x (horizontal)", None))
        self.deparg.setItemText(2, translate("calculation_pane", "y (vertical)", None))
        self.deparg.setItemText(3, translate("calculation_pane", "x & y", None))
        if not self.is_multi_particle:
            self.deparg.setItemText(4, translate("calculation_pane", "e & x", None))
            self.deparg.setItemText(5, translate("calculation_pane", "e & y", None))
            self.deparg.setItemText(6, translate("calculation_pane", "e & x & y", None))
            self.polar.setItemText(0, translate("calculation_pane", "Linear Horizontal", None))
            self.polar.setItemText(1, translate("calculation_pane", "Linear Vertical", None))
            self.polar.setItemText(2, translate("calculation_pane", "Linear 45 Degrees", None))
            self.polar.setItemText(3, translate("calculation_pane", "Linear 135 Degrees", None))
            self.polar.setItemText(4, translate("calculation_pane", "Circular Right", None))
            self.polar.setItemText(5, translate("calculation_pane", "Circular Left", None))
            self.polar.setItemText(6, translate("calculation_pane", "Total", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(translate("calculation_pane", "Number of points along Energy", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(translate("calculation_pane", "Number of points along X", None))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(translate("calculation_pane", "Number of points along Y", None))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(translate("calculation_pane", "Distance to Window", None))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(translate("calculation_pane", "Initial Photon Energy", None))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(translate("calculation_pane", "Final Photon Energy", None))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(translate("calculation_pane", "Window Left Edge", None))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(translate("calculation_pane", "Window Top Edge", None))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(translate("calculation_pane", "Window Right Edge", None))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(translate("calculation_pane", "Window Bottom Edge", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(translate("calculation_pane", "sampling", None))
        self.label.setText(translate("calculation_pane", "Status", None))
        self.label_2.setText(translate("calculation_pane", "Analytic Calculations", None))
