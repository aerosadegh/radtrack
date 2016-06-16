from PyQt4 import QtCore, QtGui
from math import sqrt
from radtrack.util.stringTools import wordwrap

class dtreeWidget(QtGui.QTreeWidget):
    contextMenuClicked = QtCore.pyqtSignal(str,str,QtCore.QPoint)
    itemExited = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(dtreeWidget, self).__init__(parent)
        self.setGeometry(QtCore.QRect(9, 90, 831, 181))
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.setColumnCount(2)
        self.setObjectName("treeWidget")
        self.setMouseTracking(True)
        self.lastIndex = QtCore.QPersistentModelIndex()
        self.viewport().installEventFilter(self) # see def eventFilter(...) below

        self.headerItem().setText(0, "Element")
        self.headerItem().setText(1, "Description")
        self.headerItem().setText(2, "Length")
        self.headerItem().setText(3, "Start-End Distance")
        self.headerItem().setText(4, "Bend")
        self.headerItem().setText(5, "Element Count")
        self.headerItem().setText(6, "")
        self.headerItem().setText(7, "")

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item is not None:
            self.contextMenuClicked.emit(item.text(0), "tree", event.globalPos())

    # Don't process right-clicks on element items as normal clicks
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            super(dtreeWidget, self).mouseReleaseEvent(event)

    # Emit signal when the mouse cursor leaves a QTreeWidgetItem.
    # This is needed to change the cursor from a pointing hand back to an arrow
    # when hovering over a blank area of the QTreeWidget after hovering over the
    # add-to-beamline text link.
    # Inspired by:
    # http://stackoverflow.com/questions/20064975/how-to-catch-mouse-over-event-of-qtablewidget-item-in-pyqt
    def eventFilter(self, widget, event):
        if widget is self.viewport():
            index = self.lastIndex
            if event.type() == QtCore.QEvent.MouseMove:
                index = self.indexAt(event.pos())
            elif event.type() == QtCore.QEvent.Leave:
                index = QtCore.QModelIndex()
            if index != self.lastIndex:
                self.itemExited.emit()
                self.lastIndex = index
        return QtGui.QTreeWidget.eventFilter(self, widget, event)

class dlistWidget(QtGui.QListWidget):
    lengthChange = QtCore.pyqtSignal()
    itemDoubleClicked = QtCore.pyqtSignal(str)
    contextMenuClicked = QtCore.pyqtSignal(str,str,QtCore.QPoint)

    def __init__(self, parent=None):
        super(dlistWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setFlow(QtGui.QListView.LeftToRight)
        self.setMaximumSize(QtCore.QSize(16777215, 60))
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)

    def dropEvent(self, event):
        super(dlistWidget, self).dropEvent(event)
        self.lengthChange.emit()

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.pos())
        if item is not None:
            self.itemDoubleClicked.emit(item.text())

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item is not None:
            self.contextMenuClicked.emit(item.text(), "list", event.globalPos())

# Needed so QGraphicsScene can accept drops
class beamGraphicsScene(QtGui.QGraphicsScene):
    def __init__(self):
        super(beamGraphicsScene, self).__init__()

    def dragMoveEvent(self, event):
        event.accept()

    def zeroSized(self):
        return self.width() == 0 or self.height() == 0

class beamGraphicsWindow(QtGui.QGraphicsView):
    itemDoubleClicked = QtCore.pyqtSignal(str)
    wheelZoom = QtCore.pyqtSignal(int)
    contextMenuClicked = QtCore.pyqtSignal(str,str,QtCore.QPoint)
    dragDone = QtCore.pyqtSignal()
    itemDropped = QtCore.pyqtSignal()

    def __init__(self, layoutWidget):
        super(beamGraphicsWindow, self).__init__(layoutWidget)
        self.setObjectName("graphicsView")
        self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.setScene(beamGraphicsScene())
        self.setAcceptDrops(True)

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(self.viewport()\
                .mapFromGlobal(event.globalPos()))
        if item is not None:
            self.itemDoubleClicked.emit(item.toolTip().split()[0])

    def mouseMoveEvent(self, event):
        super(beamGraphicsWindow, self).mouseMoveEvent(event)
        self.dragDone.emit()

    def wheelEvent(self, event):
        self.wheelZoom.emit(event.delta()/120.0)

    def contextMenuEvent(self, event):
        item = self.itemAt(self.viewport().mapFromGlobal(event.globalPos()))
        if item is not None:
            self.contextMenuClicked.emit(item.toolTip().split()[0], "picture", event.globalPos())
        else:
            self.contextMenuClicked.emit(None, "picture", event.globalPos())

    def dropEvent(self, event):
        super(beamGraphicsWindow, self).dropEvent(event)
        self.itemDropped.emit()

class genDialog(QtGui.QDialog):
    def __init__(self, oldElement):
        super(genDialog, self).__init__()
        #info stash
        self.info = []
        self.more = []

        #create buttons
        moreButton = QtGui.QPushButton('More')
        moreButton.setCheckable(True)
        moreButton.setAutoDefault(False)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setOrientation(QtCore.Qt.Vertical)
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        #create extendable zone
        extension = QtGui.QWidget()
        scrollArea = QtGui.QScrollArea()
        #create layouts
        flayout = QtGui.QFormLayout()
        extlayout = QtGui.QFormLayout()

        # Get name from oldElement
        self.info.append([QtGui.QLabel('Name'), QtGui.QLineEdit(oldElement.name)])
        self.info[0][1].selectAll()
        self.info[0][1].setToolTip('Identifying name of element.')
        flayout.addRow(self.info[0][0],self.info[0][1])

        # Attempting to create fields
        try:
            for i in range(len(oldElement.parameterNames)):
                try:
                    data = oldElement.data[i]
                except IndexError:
                    data = ''

                if i<5:
                    location = self.info
                    row = i+1
                    layout = flayout
                else:
                    location = self.more
                    row = i-5
                    layout = extlayout

                location.append([QtGui.QLabel(oldElement.parameterNames[i]), QtGui.QLineEdit(data)])
                location[row][1].setToolTip(wordwrap(oldElement.parameterDescription[i] + \
                        (' (unit: ' + oldElement.units[i] + ')' if oldElement.units[i].strip() else ''), 60))
                layout.addRow(location[row][0],location[row][1])
        except AttributeError:
            # Beamlines don't have parameterNames attribute,
            # skip rest of dialog creation
            pass

        if len(self.more)==0:
            moreButton.setEnabled(False)

        #set extension widget layout
        extension.setLayout(extlayout)
        #set widget inside scroll area
        scrollArea.setWidget(extension)
        #set main layout
        mainlayout = QtGui.QGridLayout(self)
        mainlayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        if not oldElement.isBeamline():
            mainlayout.addWidget(QtGui.QLabel('Blank cells will have default values.\n'), 0, 0)
        mainlayout.addLayout(flayout,1,0)
        mainlayout.addWidget(buttonBox,1,1)
        mainlayout.addWidget(moreButton,2,1)
        mainlayout.addWidget(scrollArea, 2,0)
        
        #connections
        moreButton.toggled.connect(scrollArea.setVisible)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.setWindowTitle(oldElement.__class__.__name__)
        scrollArea.hide()


class advDialog(QtGui.QDialog):
    def __init__(self, parent):
        super(advDialog, self).__init__(parent)
        self.buttons = []
        grid = QtGui.QGridLayout()
        encyclopedia = parent.classDictionary

        # Choose grid dimensions to be closest to a square
        columns = int(round(sqrt(len(parent.advancedNames))))
        for k, name in enumerate(sorted(parent.advancedNames)):
            row = k // columns
            col = k % columns
            button = QtGui.QPushButton(name)
            button.setToolTip(wordwrap(encyclopedia[name].elementDescription, 60))
            grid.addWidget(button, row, col)
            self.buttons.append(button)
        self.setLayout(grid)
