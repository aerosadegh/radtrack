"""
Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
version 2
"""
import os, re, cgi
from PyQt4 import QtCore, QtGui

from pybivio.trace import trace
from radtrack.BunchTab import BunchTab
from radtrack.RbBunchTransport import RbBunchTransport
from radtrack.RbUtility import convertUnitsStringToNumber, convertUnitsNumber
from radtrack.rbdcp import RbDcp
from radtrack.ui.rbele import Ui_ELE
from radtrack.RbUtility import getRealWidget
import radtrack.util.resource as resource

class RbEle(QtGui.QWidget):

    ERROR_FILE_NAME = 'elegant_errors.txt'
    OUTPUT_FILE_NAME = 'elegant_output.txt'
    ELEGANT_BASE_NAME = 'elegantSimulation'
    ELEGANT_TEMPLATE = '''
&run_setup
    lattice = "{latticeFileName}",
    use_beamline = {beamlineName},
    default_order = 2,
    p_central_mev = {momentum},
    output = %s.out,
    centroid = %s.cen,
    sigma = %s.sig,
    parameters = %s.param,
    random_number_seed = 987654321,
    combine_bunch_statistics = 0,
    concat_order = 2,
    tracking_updates = 1,
    echo_lattice = 0,
&end

&run_control
    n_steps = 1,
    reset_rf_for_each_step = 1,
&end

&twiss_output
    matched = 0,
    concat_order = 3,
    beta_x = 5, alpha_x = 0,
    beta_y = 5, alpha_y = 0,
    output_at_each_step = 1,
    statistics = 1,
    concat_order = 3,
    filename = %s.twi,
&end

&sdds_beam
    input = "{bunchFileName}",
&end

&track
&end

&stop
&end
'''

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_ELE()
        self.ui.setupUi(self)
        self.parent = parent
        self.fileExtension = '.ele'
        self._setup_widgets()
        self.update_widget_state()
        self.process = QtCore.QProcess(self)
        self.process.readyReadStandardOutput.connect(self._process_stdout)
        self.process.readyReadStandardError.connect(self._process_stderr)
        self.process.started.connect(self._process_started)
        self.process.finished.connect(self._process_finished)
        # states: 'summary' or 'full'
        self.status_mode = 'summary'
        self.summary_html = ''

        self.container = self
        self.defaultTitle = self.parent.tr('Elegant')

        self.acceptsFileTypes = ['']

    # This tab only pulls together data from other sources.
    # It has no information to save. exportToFile() creates
    # an empty file to signal to RadTrack to create a new
    # tab when a project is opened that had this tab.
    def exportToFile(self, fileName):
        with open(fileName, 'w'):
            pass

    def importFile(self, fileName):
        pass

    def append_status(self, line):
        """Formats and appends the line to the status field"""
        status = self.ui.simulationStatusTextEdit
        line += '\n'
        if self._is_error_text(line):
            html = '<strong>{}</strong>'.format(cgi.escape(line))
        else:
            html = cgi.escape(line)
        html = re.sub(r'\n', '<br>', html)
        status.moveCursor(QtGui.QTextCursor.End)
        status.insertHtml(html)
        scroll_bar = status.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())
        self.summary_html += html

    def clear_beam_lines(self):
        self.ui.beamLineComboBox.clear()

    def get_tab_by_name(self, tab_name):
        """Returns an app tab widget by text value"""
        tab = self.parent.tabWidget
        for i in range(tab.count()):
            if tab.tabText(i) == tab_name:
                return getRealWidget(tab.widget(i))
        return None

    def get_tab_names_for_type(self, tab_type):
        """Returns a list of app tab names with the specified type"""
        tab_names = []
        for i in range(self.parent.tabWidget.count()):
            name = self.parent.tabWidget.tabText(i)
            if type(self.get_tab_by_name(name)) == tab_type:
                tab_names.append(name)
        return tab_names

    def session_file(self, file_name=None, suffix=None):
        """Creates a file path in the sessionDirectory."""
        if not file_name:
            file_name = '{}.{}'.format(self.ELEGANT_BASE_NAME, suffix)
        return os.path.join(self.parent.sessionDirectory, file_name)

    def set_beam_lines(self, items):
        """Load the Beam Line combo with items"""
        self.clear_beam_lines()
        self.ui.beamLineComboBox.addItems(items)
        self.ui.beamLineComboBox.setCurrentIndex(
            self.ui.beamLineComboBox.count() - 1)

    def show_warning_box(self, message):
        QtGui.QMessageBox.warning(self, 'RadTrack', message)

    def update_sources_from_tabs(self):
        """Called from RbGlobal when the tab state changes. Resync the
        bunch source and beam line source combo items."""
        self.bunch_source_manager.update_sources_from_tabs()
        self.beam_line_source_manager.update_sources_from_tabs()

    def update_widget_state(self):
        """Set the enabled status on widgets based on current selections"""
        has_beam_line_source = self.beam_line_source_manager.has_selection()
        self.ui.beamLineLabel.setEnabled(has_beam_line_source)
        self.ui.beamLineComboBox.setEnabled(has_beam_line_source)
        show_momentum = self.bunch_source_manager.is_momentum_required()
        self.ui.momentumLabel.setVisible(show_momentum)
        self.ui.momentumLineEdit.setVisible(show_momentum)
        enable_button = self.bunch_source_manager.has_selection() \
           and self.beam_line_source_manager.has_selection()
        if show_momentum and self.ui.momentumLineEdit.text() == '':
            enable_button = False
        self.ui.simulateButton.setEnabled(enable_button)

    def validate_momentum(self):
        """Ensure the momentum value is valid"""
        if self.bunch_source_manager.is_momentum_required():
            try:
                momentum = float(self.ui.momentumLineEdit.text())
            except ValueError:
                try:
                    momentum = convertUnitsStringToNumber(
                        self.ui.momentumLineEdit.text(), 'MeV')
                except ValueError:
                    self.show_warning_box('Unable to parse momentum')
                    self.ui.momentumLineEdit.setFocus()
                    return None
        else:
            bunchTab = self.bunch_source_manager.get_tab_widget()
            if not hasattr(bunchTab, 'myBunch'):
                bunchTab.generateBunch()

            try:
                momentum = convertUnitsNumber(
                    bunchTab.myBunch.getDesignMomentumEV(), 'eV', 'MeV')
            except ValueError:
                self.show_warning_box(
                    'Invalid momentum value on Bunch Tab')
                return None
        return momentum

    def _abort_simulation(self):
        self.process.kill()

    def _add_menu_actions(self, menu, file_name, tab_type, name):
        """Adds the context menu actions for the specified tab_type"""
        for tab_name in self.get_tab_names_for_type(tab_type):
            menu.addAction(
                'Open in {} tab'.format(tab_name),
                lambda: self._load_tab(tab_name, file_name))
        menu.addAction(
            'Open in new {} tab'.format(name),
            lambda: self._new_tab(tab_type, file_name))

    def _add_result_file(self, text, file_name):
        """Adds the file entry to the simulation results list"""
        if not os.path.isfile(file_name):
            trace('missing result file: {}', file_name)
            return
        results = self.ui.simulationResultsListWidget
        icon = results.style().standardIcon(QtGui.QStyle.SP_FileIcon)
        item = QtGui.QListWidgetItem(icon, text)
        item.setData(QtCore.Qt.UserRole, file_name)
        results.addItem(item)

    def _add_result_files(self):
        """Adds output files from lattice elements and elegant template"""
        loader = self.beam_line_source_manager.get_lattice_element_loader()

        for element in loader.elementDictionary.values():
            if element.isBeamline():
                continue
            for output_parameter in element.outputFileParameters:
                i = element.parameterNames.index(output_parameter)
                if element.data[i]:
                    self._add_result_file(
                        '{}: {}'.format(element.name, type(element).__name__),
                        self._autocomplete_file_name(element.data[i]))

        matches = re.findall(r'\%s\.\w+', self.ELEGANT_TEMPLATE)
        for match in matches:
            file_name = self._autocomplete_file_name(match)
            if os.path.isfile(file_name):
                text = self._sdds_description(file_name)
                if not text:
                    text = os.path.basename(file_name)
                self._add_result_file(text, file_name)

    def _autocomplete_file_name(self, file_name):
        """Removes leading/trailing quotes and autocompletes %s.xxx files"""
        file_name = re.sub(r'\'|"', '', file_name)
        file_name = re.sub(r'\%s', self.ELEGANT_BASE_NAME, file_name)
        if not os.path.isfile(file_name):
            file_name = self.session_file(file_name=file_name)
        return file_name

    def _enable_parameters(self, is_enabled):
        """Enable or disable all the parameter fields"""
        for w in (self.ui.bunchSourceLabel,
                  self.ui.bunchSourceComboBox,
                  self.ui.beamLineSourceLabel,
                  self.ui.beamLineSourceComboBox,
                  self.ui.beamLineLabel,
                  self.ui.beamLineComboBox,
                  self.ui.momentumLabel,
                  self.ui.momentumLineEdit,
                  self.ui.simulateButton):
            w.setEnabled(is_enabled)

    def _enable_status_and_results(self):
        """Enable the simulation status and results"""
        self.ui.simulationStatusTextEdit.clear()
        self.status_mode = 'summary'
        self.summary_html = ''
        self.ui.simulationResultsListWidget.clear()
        for w in (self.ui.simulationStatusLabel,
                  self.ui.simulationStatusTextEdit,
                  self.ui.simulationResultsLabel,
                  self.ui.simulationResultsListWidget):
            w.setEnabled(True)
        self._enable_parameters(False)

    def _is_bunch_file(self, file_name):
        if re.search('\.csv$', file_name, re.IGNORECASE):
            return True
        if not self._is_sdds_file(file_name):
            return False
        """Scans the SDDS header for the 6D field names"""
        search_columns = ['x', 'xp', 'y', 'yp', 't', 'p']
        for line in self._read_sdds_header(file_name):
            match = re.search(r'^\&column\s.*?name\=(\w+)', line)
            if match:
                name = match.group(1).lower()
                if name in search_columns:
                    search_columns.remove(name)
        if len(search_columns):
            return False
        return True

    def _is_error_text(self, text):
        return re.search(r'^warn|^error|wrong units', text, re.IGNORECASE)

    def _is_sdds_file(self, file_name):
        """Returns True if the file has the SDDS header"""
        with open(file_name, 'r') as input_file:
            if re.search(r'^SDDS', input_file.readline()):
                return True
        return False

    def _load_tab(self, tab_name, file_name):
        """Load a parent tab with data from the specified file"""
        target = self.get_tab_by_name(tab_name)
        target.importFile(file_name)
        self.parent.tabWidget.setCurrentWidget(target)

    def _new_tab(self, tab_type, file_name):
        """Create a new parent tab and load the data from the specified file"""
        self.parent.newTab(tab_type)
        getRealWidget(self.parent.tabWidget.currentWidget()).importFile(file_name)

    def _process_finished(self, code, status):
        """Callback when simulation process has finished"""
        self._enable_parameters(True)
        self.ui.abortButton.setEnabled(False)
        self.ui.progressBar.setVisible(False)
        self.ui.progressBar.setMaximum(100)
        self.output_file.close()
        self.error_file.close()
        self.append_status('')

        # always add the bunch source and beam line source files
        # so they can be opened in the editor tabs to verify them
        if not self.bunch_source_manager.is_tab_choice():
            file_name = self.bunch_source_manager.get_file_name()
            self._add_result_file(os.path.basename(file_name), file_name)
        if not self.beam_line_source_manager.is_tab_choice():
            file_name = self.beam_line_source_manager.get_file_name()
            self._add_result_file(os.path.basename(file_name), file_name)

        if status == 0:
            if code == 0:
                self.append_status('Simulation completed successfully')
                self._add_result_files()
            else:
                self.append_status('Simulation failed with errors')
        else:
            self.append_status('Simulation was terminated')

    def _process_started(self):
        """Callback when simulation process has started"""
        self.ui.abortButton.setEnabled(True)
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setMaximum(0)

    def _process_stderr(self):
        """Callback with simulation stderr text"""
        out = str(self.process.readAllStandardError())
        for line in out.split("\n"):
            self.append_status(line)
        self.error_file.write(out)

    def _process_stdout(self):
        """Callback with simulation stdout text"""
        out = str(self.process.readAllStandardOutput())
        for line in out.split("\n"):
            if self._is_error_text(line):
                self.append_status(line)
        self.output_file.write(out)

    def _read_sdds_header(self, file_name):
        """Returns the header lines from a sdds file."""
        # doesn't use sdds module, avoids reading in entire file
        lines = []
        with open(file_name, 'r') as input_file:
            line = input_file.readline()
            while line != '':
                if re.search(r'^\&data ', line):
                    break
                lines.append(line)
                if len(lines) > 300:
                    break
                line = input_file.readline()
        return lines

    def _results_context_menu(self, position):
        """Show the context menu for a result item."""
        results = self.ui.simulationResultsListWidget
        if results.currentItem():
            file_name = results.currentItem().data(
                QtCore.Qt.UserRole).toString()
            menu = QtGui.QMenu()
            if re.search(r'\.lte$', file_name, re.IGNORECASE):
                self._add_menu_actions(
                    menu, file_name, RbBunchTransport, 'Bunch Transport')
            elif self._is_sdds_file(file_name):
                self._add_menu_actions(
                    menu, file_name, RbDcp, 'Data Visualization')
            if self._is_bunch_file(file_name):
                self._add_menu_actions(menu, file_name, BunchTab, 'Bunch')
            menu.exec_(results.mapToGlobal(position))

    def _run_simulation(self):
        """Generate the input files and start the Elegant process."""
        momentum = self.validate_momentum()
        if not momentum:
            return
        if not os.getenv('RPN_DEFNS', None):
            os.environ['RPN_DEFNS'] = resource.filename('defns.rpn')
        self.error_file = open(
            self.session_file(file_name=self.ERROR_FILE_NAME), 'w')
        self.output_file = open(
            self.session_file(file_name=self.OUTPUT_FILE_NAME), 'w')
        self._enable_status_and_results()
        # The replace() command escapes backslashes
        # since Elegant interprets \x as a special character.
        elegant_input_file = self._write_simulation_input_files(momentum).replace('\\', '\\\\')
        self.append_status('Running simulation ...\n')
        self.process.start('elegant', [elegant_input_file])

    def _sdds_description(self, file_name):
        """Return the sdds file description if present"""
        for line in self._read_sdds_header(file_name):
            match = re.search(r'^\&description .*?text="(.*?)"', line)
            if match:
                description = match.group(1)
                description = re.sub(r'\-\-input.*', '', description)
                description = re.sub(r'(\\|\/).*', '', description)
                return description
        return None

    def _setup_widgets(self):
        """Setup initial widget state"""
        self.ui.simulateButton.setIcon(
            self.ui.simulateButton.style().standardIcon(
                QtGui.QStyle.SP_MediaPlay))
        self.ui.simulateButton.clicked.connect(self._run_simulation)
        self.ui.abortButton.setIcon(
            self.ui.abortButton.style().standardIcon(
                QtGui.QStyle.SP_MediaStop))
        self.ui.abortButton.clicked.connect(self._abort_simulation)
        self.ui.momentumLineEdit.textChanged.connect(self.update_widget_state)
        self.ui.abortButton.setEnabled(False)
        self.ui.progressBar.setVisible(False)
        self.ui.simulationStatusTextEdit.customContextMenuRequested.connect(
            self._status_context_menu)
        self.ui.simulationResultsListWidget.customContextMenuRequested.connect(
            self._results_context_menu)
        self.bunch_source_manager = BunchSourceManager(
            self, self.ui.bunchSourceComboBox)
        self.beam_line_source_manager = BeamLineSourceManager(
            self, self.ui.beamLineSourceComboBox)

    def _show_full_status(self):
        """Show the full process stdout and stderr text"""
        self.status_mode = 'full'
        status = self.ui.simulationStatusTextEdit
        status.clear()
        text = ''
        for name in (self.OUTPUT_FILE_NAME, self.ERROR_FILE_NAME):
            with open(self.session_file(file_name=name), 'r') as input_file:
                text += input_file.read()
            text += '\n\n'
        status.moveCursor(QtGui.QTextCursor.End)
        status.insertPlainText(text)
        scroll_bar = status.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def _show_summary_status(self):
        """Show the summary status text"""
        self.status_mode = 'summary'
        self.ui.simulationStatusTextEdit.clear()
        self.ui.simulationStatusTextEdit.insertHtml(self.summary_html)

    def _status_context_menu(self, position):
        """Show the context menu for the status panel."""
        status = self.ui.simulationStatusTextEdit
        if status.isEnabled() and self.ui.simulateButton.isEnabled():
            menu = QtGui.QMenu()
            full = menu.addAction('Full Output', self._show_full_status)
            summary = menu.addAction(
                'Summary Output', self._show_summary_status)
            selected = full if self.status_mode == 'full' else summary
            selected.setCheckable(True)
            selected.setChecked(True)
            menu.exec_(status.mapToGlobal(position))

    def _write_simulation_input_files(self, momentum):
        """Generates and writes simulation input files"""
        self.append_status('Writing Elegant simulation file ...')
        elegant_file_name = self.session_file(suffix='ele')
        with open(elegant_file_name, 'w') as output_file:
            output_file.write(self.ELEGANT_TEMPLATE.format(
                latticeFileName=self.beam_line_source_manager \
                    .get_lattice_file_name(),
                beamlineName=self.ui.beamLineComboBox.currentText(),
                momentum=str(momentum),
                bunchFileName=self.bunch_source_manager.get_bunch_file_name()
            ))
        return elegant_file_name


class ComboManager():
    """Superclass for the BunchSourceManager and BeamLineSourceManager"""
    SELECT_FILE_CHOICE = 'Use another file ...'

    def __init__(self, rbele, combo, name, tab_type):
        self.rbele = rbele
        self.combo = combo
        self.tab_type = tab_type
        self.unselected_choice = 'Select {} source ...'.format(name)
        self.new_tab_choice = 'New {} ...'.format(name)
        self.combo.addItem(self.unselected_choice)
        self.combo.addItem(self.new_tab_choice)
        self.combo.addItem(self.SELECT_FILE_CHOICE)

    def get_file_name(self):
        """Returns the filename associated with a file item."""
        return self.combo.itemData(self.combo.currentIndex()).toString()

    def get_tab_widget(self):
        """Returns the parent tab widget by text name or None"""
        return self.rbele.get_tab_by_name(self.combo.currentText())

    def get_tab_items(self):
        """Returns the selection items which correspond to app tabs."""
        items = []
        for i in range(
                self.combo.findText(self.unselected_choice) + 1,
                self.combo.findText(self.new_tab_choice)):
            items.append(self.combo.itemText(i))
        return items

    def has_selection(self):
        return self.combo.currentIndex() > 0

    def is_new_tab_choice(self):
        """Opens a new tab for the combo tab_type. Returns True if selected"""
        if self.combo.currentText() == self.new_tab_choice:
            self.combo.setCurrentIndex(0)
            self.rbele.parent.newTab(self.tab_type)
            return True
        return False

    def is_select_file_choice(self, file_type):
        """If SELECT_FILE_CHOICE is selected, open the file chooser.
        Show the file dialog to select a file. Adds the new file to
        the list of choices."""
        if self.combo.currentText() != self.SELECT_FILE_CHOICE:
            return False
        file_name = QtGui.QFileDialog.getOpenFileName(
            self.rbele, 'Open', self.rbele.parent.lastUsedDirectory, file_type)
        if file_name == '':
            self.combo.setCurrentIndex(0)
        else:
            self.rbele.parent.lastUsedDirectory = os.path.dirname(file_name)
            # Check if file has already been selected
            index = self.combo.findData(file_name)
            if index > 0:
                self.combo.setCurrentIndex(index)
            else:
                index = self.combo.findText(self.SELECT_FILE_CHOICE)
                self.combo.setCurrentIndex(0)
                self.combo.insertItem(
                    index,
                    self.combo.style().standardIcon(QtGui.QStyle.SP_FileIcon),
                    os.path.basename(file_name), file_name)
                self.combo.setCurrentIndex(index)
        return True

    def is_tab_choice(self):
        """Returns True if a tab exists for the combo text"""
        return self.get_tab_widget() != None

    def update_sources_from_tabs(self):
        """Update the tab names within the combo values. May add or
        delete items from the list."""
        tab_names = self.rbele.get_tab_names_for_type(self.tab_type)
        delete_tabs = []
        for text in self.get_tab_items():
            if text in tab_names:
                tab_names.remove(text)
            else:
                delete_tabs.append(text)

        for name in delete_tabs:
            index = self.combo.findText(name)
            trace('deleting "{}" at {}', name, index)
            if index == self.combo.currentIndex():
                self.combo.setCurrentIndex(0)
            self.combo.removeItem(index)

        for name in tab_names:
            index = self.combo.findText(self.new_tab_choice)
            trace('inserting "{}" at {}', name, index)
            self.combo.insertItem(index, name)


class BunchSourceManager(ComboManager):
    """Manages the state and interaction with the Bunch Source ComboBox"""

    def __init__(self, rbele, combo):
        ComboManager.__init__(self, rbele, combo, 'beam bunch', BunchTab)
        self.combo.currentIndexChanged.connect(self._bunch_source_changed)

    def get_bunch_file_name(self):
        """Returns the file name of the beam bunch"""
        if self.is_tab_choice():
            self.rbele.append_status('Generating beam bunch file ...')
            bunch_file_name = self.rbele.session_file(suffix='sdds')
            self.get_tab_widget().saveToSDDS(bunch_file_name)
        else:
            bunch_file_name = self.get_file_name()
            # convert CSV files to SDDS
            if re.search('\.csv$', bunch_file_name, re.IGNORECASE):
                loader = BunchTab(parent=self.rbele.parent)
                loader.readFromCSV(bunch_file_name)
                bunch_file_name = self.rbele.session_file(suffix='sdds')
                loader.saveToSDDS(bunch_file_name)
        return bunch_file_name

    def is_momentum_required(self):
        return self.has_selection() and not self.is_tab_choice()

    def _bunch_source_changed(self):
        """Load bunch file if selected"""
        if self.is_select_file_choice('SDDS files (*.sdds);;CSV files (*.csv)'):
            return
        if self.is_new_tab_choice():
            return
        if self.is_tab_choice() and not self.rbele.validate_momentum():
            self.combo.setCurrentIndex(0)
            return
        self.rbele.update_widget_state()


class BeamLineSourceManager(ComboManager):
    """Manages the state and interaction with the Beam Line Source ComboBox"""

    def __init__(self, rbele, combo):
        ComboManager.__init__(
            self, rbele, combo, 'beam line', RbBunchTransport)
        self.loaderCache = {}
        self.combo.currentIndexChanged.connect(self._beam_line_source_changed)

    def get_lattice_file_name(self):
        """For tab items, generate the lattice file. For file items,
        return the file name"""
        if self.is_tab_choice():
            self.rbele.append_status('Generating beam lattice file ...')
            lattice_file_name = self.rbele.session_file(suffix='lte')
            self.get_tab_widget().exportToFile(lattice_file_name)
        else:
            lattice_file_name = self.get_file_name()
        return lattice_file_name

    def get_lattice_element_loader(self):
        """Returns the RbBunchTransport instance with the lattice elements"""
        loader = None
        if self.is_tab_choice():
            loader = self.get_tab_widget()
        elif self.has_selection():
            fileName = self.get_file_name()
            if fileName not in self.loaderCache:
                loader = RbBunchTransport(parent=self.rbele.parent)
                loader.importFile(fileName)
                self.loaderCache[fileName] = loader
            loader = self.loaderCache[fileName]
        return loader

    def _beam_line_source_changed(self):
        """Load beam line file and loads beam info into beamLineComboBox"""
        self.rbele.clear_beam_lines()
        if self.is_select_file_choice('*.lte'):
            return
        if self.is_new_tab_choice():
            return
        loader = self.get_lattice_element_loader()
        if loader:
            self._validate_and_load_beam_lines(loader)
        self.rbele.update_widget_state()

    def _validate_and_load_beam_lines(self, loader):
        """Extract the beam lines from the loader. Show an error if there
        are no lines available."""
        beam_lines = []
        for element in loader.elementDictionary.values():
            if element.isBeamline() and not element.name.startswith('-'):
                beam_lines.append(element.name)

        if len(beam_lines) == 0:
            self.rbele.show_warning_box(
                'Beam Line Source contains no beam lines')
            if self.is_tab_choice():
                self.combo.setCurrentIndex(0)
            else:
                fileName = self.get_file_name()
                del self.loaderCache[fileName]
                index = self.combo.currentIndex()
                self.combo.setCurrentIndex(0)
                self.combo.removeItem(index)
            return
        self.rbele.set_beam_lines(beam_lines)
