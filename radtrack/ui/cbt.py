# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cbt.ui'
#
# Created: Fri Sep 06 16:32:19 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class dtreeWidget(QtGui.QTreeWidget):
    itemDoubleClicked = QtCore.pyqtSignal(str)
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
        self.lastIndex = QtCore.QPersistentModelIndex()
        self.viewport().installEventFilter(self)

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.pos())
        if item is not None:
            self.itemDoubleClicked.emit(item.text(0))

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item is not None:
            self.contextMenuClicked.emit(item.text(0), "tree", event.globalPos())

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
        self.setFlow(QtGui.QListView.LeftToRight)
        self.setMaximumSize(QtCore.QSize(16777215, 60))
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)

    def dropEvent(self, event):
        super(dlistWidget, self).dropEvent(event)
        self.lengthChange.emit()

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(self.viewport().mapFromGlobal(event.globalPos()))
        if item is not None:
            self.itemDoubleClicked.emit(item.text())

    def contextMenuEvent(self, event):
        item = self.itemAt(self.viewport().mapFromGlobal(event.globalPos()))
        if item is not None:
            self.contextMenuClicked.emit(item.text(), "list", event.globalPos())

# Needed so QGraphicsScene can accept drops
class beamGraphicsScene(QtGui.QGraphicsScene):
    def __init__(self):
        super(beamGraphicsScene, self).__init__()

    def dragMoveEvent(self, event):
        event.accept()

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

class Ui_tree(QtCore.QObject):
    contextMenuClicked = QtCore.pyqtSignal(str,str,QtCore.QPoint)

    def __init__(self, tree, module):
        super(Ui_tree, self).__init__()

        self.names = sorted(module.classDictionary.keys())
        self.advancedNames = sorted(module.advancedNames)
        self.nameMangler = module.nameMangler
        self.fileType = module.fileExtension.lstrip('.').upper()

        self.treeObjectName = "tree"
        tree.setObjectName(self.treeObjectName)
        tree.resize(856, 490)
        self.treeWidget = dtreeWidget(tree)
        self.horizontalLayoutWidget = QtGui.QWidget(tree)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 831, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttons = []
        for name in [n for n in self.names if n not in self.advancedNames]:
            self.buttons.append(QtGui.QPushButton(self.horizontalLayoutWidget))
            self.buttons[-1].setObjectName(name)
            self.horizontalLayout.addWidget(self.buttons[-1])
        if len(self.advancedNames) > 0:
            self.advanced = QtGui.QPushButton(self.horizontalLayoutWidget)
            self.advanced.setObjectName("advanced")
            self.advanced.setToolTip("More elements")
            self.horizontalLayout.addWidget(self.advanced)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(tree)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 310, 831, 171))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.graphicsView = beamGraphicsWindow(self.horizontalLayoutWidget_2)
        self.graphicsView.setRenderHints(QtGui.QPainter.Antialiasing | 
                QtGui.QPainter.SmoothPixmapTransform | 
                QtGui.QPainter.TextAntialiasing)
        self.horizontalLayout_2.addWidget(self.graphicsView)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(tree)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 270, 831, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtGui.QLabel(self.horizontalLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.workingBeamline = dlistWidget()
        self.horizontalLayout_3.addWidget(self.workingBeamline)
        self.saveBeamlineButton = QtGui.QPushButton()
        self.saveBeamlineButton.setObjectName("saveBeamlineButton")
        self.horizontalLayout_3.addWidget(self.saveBeamlineButton)
        self.clearBeamlineButton = QtGui.QPushButton()
        self.clearBeamlineButton.setObjectName("clearBeamlineButton")
        self.horizontalLayout_3.addWidget(self.clearBeamlineButton)

        self.retranslateUi(tree)
        QtCore.QMetaObject.connectSlotsByName(tree)

        # Signal connections
        self.treeWidget.contextMenuClicked.connect(self.contextMenu)
        self.graphicsView.contextMenuClicked.connect(self.contextMenu)
        self.workingBeamline.contextMenuClicked.connect(self.contextMenu)

    def retranslateUi(self, tree):
        tree.setWindowTitle(self.translateUTF8("Form"))
        self.treeWidget.headerItem().setText(0, self.translateUTF8("Element"))
        self.treeWidget.headerItem().setText(1, self.translateUTF8("Description"))
        for button in self.buttons:
            button.setText(self.translateUTF8(str(button.objectName())))
        if len(self.advancedNames) > 0:
            self.advanced.setText(self.translateUTF8("ADVANCED"))
        self.clearBeamlineButton.setText(self.translateUTF8("Clear\nBeamline"))
        self.saveBeamlineButton.setText(self.translateUTF8("Save\nBeamline"))
        self.label.setText(self.translateUTF8("Working Beamline: "))

    def translateUTF8(self, string):
        return QtGui.QApplication.translate(self.treeObjectName, \
                string, \
                None, \
                QtGui.QApplication.UnicodeUTF8)

    def contextMenu(self, name, location, globalPosition):
        self.contextMenuClicked.emit(name, location, globalPosition)

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
                location[row][1].setToolTip(oldElement.parameterDescription[i] + \
                        (' (unit: ' + oldElement.units[i] + ')' if oldElement.units[i].strip() != '' else ''))
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
        mainlayout.addLayout(flayout,0,0)
        mainlayout.addWidget(buttonBox,0,1)
        mainlayout.addWidget(moreButton,1,1)
        mainlayout.addWidget(scrollArea, 1,0)
        
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
        nameMangler = parent.nameMangler
        columns = 6
        for k, name in enumerate(parent.ui.advancedNames):
            row = k // columns
            col = k % columns
            button = QtGui.QPushButton(name)
            button.setToolTip(encyclopedia[nameMangler(name)].elementDescription)
            grid.addWidget(button, row, col)
            self.buttons.append(button)
        self.setLayout(grid)
