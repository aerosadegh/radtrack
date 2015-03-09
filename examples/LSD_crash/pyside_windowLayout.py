from PySide import QtCore, QtGui

# A tree from which a user selects things to put into the list widget
class dtreeWidget(QtGui.QTreeWidget):
    def __init__(self, parent = None):
        super(dtreeWidget, self).__init__(parent)
        self.setDragEnabled(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.setColumnCount(1)

# A widget containing a user-created list
class dlistWidget(QtGui.QListWidget):
    lengthChange = QtCore.Signal()
    contextMenuClicked = QtCore.Signal(QtCore.QPoint)

    def __init__(self, parent = None):
        super(dlistWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def dropEvent(self, event):
        super(dlistWidget, self).dropEvent(event)
        self.lengthChange.emit()

    def contextMenuEvent(self, event):
        item = self.itemAt(self.viewport().mapFromGlobal(event.globalPos()))
        if item is not None:
            self.contextMenuClicked.emit(event.globalPos())


# Main GUI specification
class Ui_tree(QtCore.QObject):
    contextMenuClicked = QtCore.Signal(QtCore.QPoint)

    def __init__(self, parent, elementClass):
        super(Ui_tree, self).__init__()
        # Element buttons
        self.ButtonsWidget = QtGui.QWidget(parent)
        self.Buttons = QtGui.QHBoxLayout(self.ButtonsWidget)

        self.addButton = QtGui.QPushButton(self.ButtonsWidget)
        self.addButton.setText(elementClass.__name__)
        self.Buttons.addWidget(self.addButton)

        self.testButton = QtGui.QPushButton(self.ButtonsWidget)
        self.testButton.setText('TEST')
        self.Buttons.addWidget(self.testButton)

        # Element list
        self.treeWidget = dtreeWidget(parent)
        # Beamline creation list
        self.listw = dlistWidget(parent)

        # Total layout
        parent.verticalLayout = QtGui.QVBoxLayout(parent)
        parent.verticalLayout.addWidget(self.ButtonsWidget)
        parent.verticalLayout.addWidget(self.treeWidget)
        parent.verticalLayout.addWidget(self.listw)

        # Signal connections
        self.listw.contextMenuClicked.connect(self.contextMenu)

        QtCore.QMetaObject.connectSlotsByName(parent)

    def contextMenu(self, globalPosition):
        self.contextMenuClicked.emit(globalPosition)

# A dialog box which creates a new THING with an input box
# for the name
class genDialog(QtGui.QDialog):
    def __init__(self, oldElement):
        super(genDialog, self).__init__()

        #create buttons
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setOrientation(QtCore.Qt.Vertical)
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        #create layouts
        flayout = QtGui.QFormLayout()

        # Get name from oldElement
        self.info = QtGui.QLabel('Name'), QtGui.QLineEdit(oldElement.name)
        flayout.addRow(self.info[0],self.info[1])

        #set main layout
        mainlayout = QtGui.QGridLayout(self)
        mainlayout.addLayout(flayout,0,0)
        mainlayout.addWidget(buttonBox,0,1)
        
        #connections
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.setWindowTitle(oldElement.__class__.__name__)
