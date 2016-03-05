from pykern.pkdebug import pkdc
from PyQt4 import QtGui, QtCore
import os

def add_result_file(listWidget, text, file_name):
    """Adds the file entry to the simulation results list"""
    if not os.path.isfile(file_name):
        pkdc('missing result file: {}', file_name)
        return
    icon = listWidget.style().standardIcon(QtGui.QStyle.SP_FileIcon)
    item = QtGui.QListWidgetItem(icon, text)
    item.setData(QtCore.Qt.UserRole, file_name)
    listWidget.addItem(item)

def results_context_menu(listWidget, globalGUI, position):
    """Show the context menu for a result item."""
    if listWidget.currentItem():
        file_name = listWidget.currentItem().data(
            QtCore.Qt.UserRole).toString()
        menu = QtGui.QMenu()
        ext = os.path.splitext(file_name)[1].strip('.')
        for tabType in globalGUI.availableTabTypes:
            if ext in tabType.acceptsFileTypes:
                _add_menu_actions(globalGUI, menu, file_name, tabType, tabType.defaultTitle)
        menu.exec_(listWidget.mapToGlobal(position))

def _add_menu_actions(globalGUI, menu, file_name, tab_type, name):
    """Adds the context menu actions for the specified tab_type"""
    for tab_name in get_tab_names_for_type(globalGUI, tab_type):
        menu.addAction(
            'Open in {} tab'.format(tab_name),
            lambda: _load_tab(globalGUI, tab_name, file_name))
    menu.addAction(
        'Open in new {} tab'.format(name),
        lambda: _new_tab(globalGUI, tab_type, file_name))

def _load_tab(globalGUI, tab_name, file_name):
    """Load a globalGUI tab with data from the specified file"""
    target = get_tab_by_name(globalGUI, tab_name)
    target.importFile(file_name)
    globalGUI.tabWidget.setCurrentWidget(target)


def _new_tab(globalGUI, tab_type, file_name):
    """Create a new globalGUI tab and load the data from the specified file"""
    globalGUI.newTab(tab_type)
    globalGUI.tabWidget.currentWidget().importFile(file_name)


def get_tab_names_for_type(globalGUI, tab_type):
    """Returns a list of app tab names with the specified type"""
    tab_names = []
    for i in range(globalGUI.tabWidget.count()):
        name = globalGUI.tabWidget.tabText(i)
        if type(get_tab_by_name(globalGUI, name)) == tab_type:
            tab_names.append(name)
    return tab_names


def get_tab_by_name(globalGUI, tab_name):
    """Returns an app tab widget by text value"""
    tab = globalGUI.tabWidget
    for i in range(tab.count()):
        if tab.tabText(i) == tab_name:
            return tab.widget(i)
    return None
