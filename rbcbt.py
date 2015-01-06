import os.path
from collections import OrderedDict
from PySide import QtGui, QtCore

from RadTrack.beamlines.cbt import Ui_tree, genDialog, advDialog
from RbUtility import displayWithUnitsNumber, \
                      convertUnitsNumber, \
                      roundSigFig


class RbCbt(QtGui.QWidget):
    def __init__(self, particle_laser, parent = None):
        QtGui.QWidget.__init__(self)
        #determine type of window (particle/laser) beam transport
        if particle_laser == 'particle':
            importName = 'RbElegantElements'
        elif particle_laser == 'laser':
            importName = 'RbOpticalElements'
        else:
            raise Exception('Unrecognized particle_laser argument: ' + particle_laser)

        module = __import__('RadTrack.beamlines.' + importName, fromlist='.')
        self.beamlineType = module.beamlineType
        self.classDictionary = module.classDictionary
        self.acceptsFileTypes = [module.fileExtension]
        self.nameMangler = module.nameMangler
        self.importer = module.fileImporter
        self.exporter = module.fileExporter

        self.argument = particle_laser
        self.resolution = self.classDictionary.values()[0]().getResolution()
        self.defaultBeamline = ''
        #set layout
        self.ui = Ui_tree(self, particle_laser)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.ui.horizontalLayoutWidget)
        self.verticalLayout.addWidget(self.ui.treeWidget)
        self.verticalLayout.addWidget(self.ui.horizontalLayoutWidget_3)
        self.verticalLayout.addWidget(self.ui.horizontalLayoutWidget_2)
        #undo/redo 
        self.undoStack = QtGui.QUndoStack()
        #connections
        self.ui.workingBeamline.lengthChange.connect(self.postListDrop)
        self.ui.workingBeamline.itemDoubleClicked.connect(self.editElement)
        self.ui.workingBeamline.itemPressed.connect(self.listClick)
        self.adv = advDialog(self)
        for button in self.ui.buttons + self.adv.buttons:
            button.clicked.connect(self.createNewElement)
            button.setToolTip(self.classDictionary[self.nameMangler(button.text())].elementDescription)
        if len(self.ui.advancedNames) > 0:
            self.ui.advanced.clicked.connect(self.adv.show)
        self.ui.clearBeamlineButton.clicked.connect(self.newBeam)
        self.ui.saveBeamlineButton.clicked.connect(self.addBeam)
        self.ui.treeWidget.itemSelectionChanged.connect(self.treeClick)
        self.ui.treeWidget.itemDoubleClicked.connect(self.editElement)
        self.ui.graphicsView.itemDoubleClicked.connect(self.editElement)
        self.ui.graphicsView.wheelZoom.connect(self.zoomPreview)
        self.ui.graphicsView.dragDone.connect(self.drawLengthScale)
        self.ui.graphicsView.scene().selectionChanged.connect(self.picClick)
        self.ui.graphicsView.horizontalScrollBar().valueChanged.connect(self.drawLengthScale)
        self.ui.graphicsView.verticalScrollBar().valueChanged.connect(self.drawLengthScale)
        self.ui.contextMenuClicked.connect(self.createContextMenu)

        #### Keyboard shortcuts
        # Copy element in tree widget
        QtGui.QShortcut(QtGui.QKeySequence.Copy, self).activated.connect(lambda : self.copyElement(self.ui.treeWidget.currentItem()))

        # Zooming the preview window
        QtGui.QShortcut(QtGui.QKeySequence.ZoomIn, self).activated.connect(lambda : self.zoomPreview(1))
        QtGui.QShortcut(QtGui.QKeySequence.ZoomOut, self).activated.connect(lambda : self.zoomPreview(-1))
        
        #text
        self.beamlineTreeLabel = self.ui.translateUTF8('Beamlines')
        self.beamlineListLabelDefault = self.ui.translateUTF8('Working Beamline: ')

        #user interaction state
        if parent == None:
            self.parent = self
            self.parent.lastUsedDirectory = os.path.expanduser('~')
        else:
            self.parent = parent
        self.elementDictionary = OrderedDict()
        self.workingBeamlineName = ''
        self.preListSave = []
        self.preListNameSave = self.workingBeamlineName
        self.preListLabelSave = self.ui.label.text()
        self.zoomScale = 1

        # Graphical length legend for preview
        self.lengthLegend = []

        # More columns for treeWidget
        self.ui.treeWidget.setColumnCount(5)
        self.ui.treeWidget.headerItem().setText(2, "Length")
        self.ui.treeWidget.headerItem().setText(3, "Bend")
        self.ui.treeWidget.headerItem().setText(4, "Element Count")

    def undo(self):
        self.undoStack.undo()

    def redo(self):
        self.undoStack.redo()

    def hasChanged(self):
        return not self.undoStack.isClean()

    def postListDrop(self):
        self.fixWorkingBeamline()
        self.postListSave = self.listItems()
        if self.preListSave == self.postListSave:
            return
        self.postListNameSave = self.workingBeamlineName
        self.postListLabelSave = self.ui.label.text()
        undoAction = commandundoAdd2Beam(self)
        self.undoStack.push(undoAction)
        self.preListSave = self.postListSave
        self.preListNameSave = self.postListNameSave
        self.preListLabelSave = self.postListLabelSave
    
    def treeClick(self):
        # Draw element currently selected
        self.elementPreview()
        # Allow workingBeamline list to accept drops from treeWidget
        self.ui.workingBeamline.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        # Deselect everything in the list and preview
        for item in self.ui.workingBeamline.selectedItems() + \
                self.ui.graphicsView.scene().selectedItems():
            item.setSelected(False)


    def listClick(self):
        # Draw current working beamline
        self.workingBeamlinePreview()
        # Allow workingBeamline elements to be moved around without copying
        self.ui.workingBeamline.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        # Deselect everything in the tree and preview
        for item in self.ui.treeWidget.selectedItems() + \
                self.ui.graphicsView.scene().selectedItems():
            item.setSelected(False)
        self.ui.treeWidget.setCurrentItem(None)

    def picClick(self):
        # Deselect everything in the tree and preview
        for item in self.ui.treeWidget.selectedItems() + \
                self.ui.workingBeamline.selectedItems():
            item.setSelected(False)


    # Context menus
    def createContextMenu(self, name, location, globalPos):
        element = self.elementDictionary.get(name)

        # In the below functions, lambda: causes the function itself
        # to be passed to addAction, rather than the result of the
        # function
        mouseMenu = QtGui.QMenu(self)
        display = False

        if location == 'picture' and element is not None:
            # When a user opens a context menu on the picture of an element,
            # there's no indication of the name of the element.  The 
            # commands above the separator put the name of the element at
            # the top of the context menu.
            menuTitle = QtGui.QAction(element.name, mouseMenu)
            menuTitle.setEnabled(False)
            mouseMenu.addAction(menuTitle)
            mouseMenu.addSeparator()
            display = True
 
        if location in ['tree', 'picture'] and element is not None:
            mouseMenu.addAction(self.ui.translateUTF8('Edit'),
                    lambda: self.editElement(element.name))
            mouseMenu.addAction(self.ui.translateUTF8('New copy'),
                    lambda: self.copyElement(element.name))
            mouseMenu.addAction(self.ui.translateUTF8('Delete'),
                    lambda: self.deleteElement(element.name))
            if element.isBeamline():
                mouseMenu.addSeparator()
                mouseMenu.addAction(self.ui.translateUTF8('Set as default'),
                    lambda: setattr(self, 'defaultBeamline', element.name))
            display = True

        if location == 'picture' and len(self.ui.graphicsView.scene().items()) > 0:
            # Add option for saving entire beamline preview as an image file
            mouseMenu.addSeparator()
            mouseMenu.addAction(self.ui.translateUTF8('Save preview image...'), \
                    self.savePreviewImage)
            mouseMenu.addAction(self.ui.translateUTF8('Reset zoom'), self.drawElement)
            display = True

        if location == 'list' and element is not None:
            # user right/cmd-clicked in the workingBeamline list
            if not element.isBeamline():
                mouseMenu.addAction(self.ui.translateUTF8('Edit'),
                        lambda: self.editElement(element.name))

            mouseMenu.addAction(self.ui.translateUTF8('Add another'), self.listCopy)
            mouseMenu.addAction(self.ui.translateUTF8('Add multiple copies ...'), self.listMultipleCopy)
            display = True

            if element.isBeamline():
                mouseMenu.addAction(self.ui.translateUTF8('Reverse'), self.convertToReversed)

            mouseMenu.addAction(self.ui.translateUTF8('Remove'), self.removeFromWorkingBeamline)

        if display:
            mouseMenu.exec_(globalPos)


    def removeFromWorkingBeamline(self):
        undoAction = commandRemoveFromBeam(self)
        self.undoStack.push(undoAction)

    def editElement(self, name):
        try:
            selectedElement = self.elementDictionary[name]
        except KeyError: # Element name not found
            return

        if selectedElement.isBeamline():
            # restore selected beamline to Working Beamline list for further editing
            self.workingBeamlineName = selectedElement.name
            self.ui.label.setText(self.workingBeamlineName)
            self.ui.workingBeamline.clear()
            self.ui.workingBeamline.addItems([element.name for element in selectedElement.data])
            self.postListDrop()

        else: # Selected item is an element of a beamline (drift, quad, etc.)
            dialog = genDialog(selectedElement)
            if dialog.exec_():
                data = dialog.info + dialog.more
                newElement = type(selectedElement)([datum[1].text() for datum in data])
                undoAction = commandEditElement(self, selectedElement, newElement)
                self.undoStack.push(undoAction)
                self.elementPreview()

    def copyElement(self, name):
        # name could be text string or QTreeWidgetItem
        if name is None:
            return
        try:
            name = name.text(0)
        except AttributeError:
            pass

        originalElement = self.elementDictionary[name]
        newElement = type(originalElement)([originalElement.name] + originalElement.data[:])

        copyLabel = '_Copy'
        copyLabelLocation = newElement.name.rfind(copyLabel)
        if copyLabelLocation == -1:
            newElement.name = newElement.name + copyLabel
        else:
            newElement.name = newElement.name[:copyLabelLocation] + copyLabel
        undoAction = commandLoadElements(self, [newElement])
        self.undoStack.push(undoAction)


    def listMultipleCopy(self):
        copies, ok = QtGui.QInputDialog.getInt(self, \
                "Add multiple copies", \
                "Number of additional copies of " \
                + self.ui.workingBeamline.currentItem().text() + ":", \
                1,1)
        if ok:
            for i in range(copies):
                self.listCopy(False)
            self.postListDrop()

    def listCopy(self, postList = True):
        item = self.ui.workingBeamline.currentItem()
        row = self.ui.workingBeamline.row(item)
        self.ui.workingBeamline.insertItem(row, item.text())
        if postList:
            self.postListDrop()


    def rewriteBeamlineTree(self):
        # Update element list
        for group in self.topLevelTreeItems():
            for item in itemsInGroup(group):
                populateTreeItem(item, self.elementDictionary[item.text(0)])
        self.fitColumns()

        # Update Working Beamline
        self.fixWorkingBeamline()


    def fitColumns(self):
        for i in range(self.ui.treeWidget.columnCount()):
            if i != 1: # don't fit Description Column
                self.ui.treeWidget.resizeColumnToContents(i)


    def createNewElement(self):
        typeName = self.sender().text()
        elementType = self.classDictionary[self.nameMangler(typeName)]
        dialog = genDialog(elementType())
        if dialog.exec_():
            data = [datum[1].text() for datum in dialog.info + dialog.more]
            element = elementType(data)
            undoAction = commandLoadElements(self, [element])
            self.undoStack.push(undoAction)


    def uniqueName(self, name):
        # Element name cannot match a type name
        lowerTypes = [elementType.lower() for elementType in self.classDictionary]
        while name.lower() in lowerTypes:
            name = name + 'X'

        # Element name cannot match another element's name
        counter = 0
        baseName = name
        lowerNames = [elementName.lower() for elementName in self.elementDictionary]
        while name.lower() in lowerNames:
            counter += 1
            name = baseName + str(counter)

        return name

    def addBeam(self):
        beamline = self.beamlineType()
        if self.workingBeamlineName != '':
            beamline.name = self.workingBeamlineName

        for name in self.listItems():
            beamline.addElement(self.elementDictionary[name])              

        dialog = genDialog(beamline)
        if dialog.exec_():
            beamline.name = dialog.info[0][1].text()
            if self.workingBeamlineName != '':
                oldBeam = self.elementDictionary[self.workingBeamlineName]
                undoAction = commandEditElement(self, oldBeam, beamline)
                self.undoStack.push(undoAction)
            else:
                undoAction = commandLoadElements(self, [beamline], 'addBeam')
                self.undoStack.push(undoAction)



    def findElementInTreeByName(self, name):
        for group in self.topLevelTreeItems():
            for item in itemsInGroup(group):
                if item.text(0) == name:
                    return item


    def deleteElement(self, name):
        undoAction = commandDeleteElement(self, name)
        self.undoStack.push(undoAction)

    def newBeam(self):
        self.workingBeamlineName = ''
        self.ui.label.setText(self.beamlineListLabelDefault)
        self.ui.workingBeamline.clear()
        self.postListDrop()

    def fixWorkingBeamline(self):
        beamline = self.elementDictionary.get(self.workingBeamlineName)

        # Beamlines are constructed only from previously existing elements.
        # Beamlines cannot contain themselves.
        items = [name for name in self.listItems() if name in self.elementDictionary \
                and not self.elementDictionary[name].contains(beamline)]
        self.ui.workingBeamline.clear()
        self.ui.workingBeamline.addItems(items)

    def elementPreview(self):
        item = self.ui.treeWidget.currentItem()
        if item is not None:
            try:
                self.drawElement(self.elementDictionary[item.text(0)])
            except KeyError:
                self.ui.graphicsView.scene().clear()
        else:
            self.ui.graphicsView.scene().clear()

    def workingBeamlinePreview(self):
        bl = self.beamlineType()
        for name in self.listItems():
            bl.addElement(self.elementDictionary[name])
        self.drawElement(bl)

    def drawElement(self, element = None):
        if element is None:
            element = self.lastDrawnElement
        else:
            self.lastDrawnElement = element

        scene = self.ui.graphicsView.scene()
        scene.clear()
        element.picture(scene)
        sceneRect = scene.itemsBoundingRect()
        scene.setSceneRect(sceneRect)

        sx = sceneRect.width()
        sy = sceneRect.height()

        if sx == 0 or sy == 0:
            return

        viewSize = self.ui.graphicsView.size()
        vx = viewSize.width()
        vy = viewSize.height()

        scale = min([vx/sx, vy/sy, 1.0])

        self.ui.graphicsView.resetTransform()
        self.ui.graphicsView.scale(scale, scale)
        self.zoomScale = scale

        self.drawLengthScale()

    def visibleSceneRect(self):
        viewportRect= QtCore.QRect(0,0,self.ui.graphicsView.viewport().width(),
                                       self.ui.graphicsView.viewport().height())
        return self.ui.graphicsView.mapToScene(viewportRect).boundingRect()

    def drawLengthScale(self):
        if self.ui.graphicsView.scene() is None or len(self.ui.graphicsView.scene().items()) == 0:
            return
        self.removeLengthScale()
        vis = self.visibleSceneRect()

        # Determine a reasonable length to display
        length = 1.0 # meter
        widthFraction = 0.25 # maximum length of legend w.r.t. preview window
        while length*self.resolution < float(vis.width())*widthFraction:
            length = length*10.0

        while length*self.resolution > float(vis.width())*widthFraction:
            length = length/10.0

        textItem = QtGui.QGraphicsTextItem(displayWithUnitsNumber(length, 'm'))

        pixLength = int(length*self.resolution)
        if pixLength < 1:
            return

        # line showing length given by textItem
        try:
            rightEnd = QtCore.QPoint(vis.right()-vis.width()/10,
                                     vis.bottom()-vis.height()/10)
        except OverflowError:
            self.zoomPreview(1)
            return
        leftEnd = rightEnd - QtCore.QPoint(pixLength,0)
        self.lengthLegend.append(QtGui.QGraphicsLineItem(leftEnd.x(),
                                                         leftEnd.y(),
                                                         rightEnd.x(),
                                                         rightEnd.y()))
        endHeight = int(20.0/self.zoomScale) # constant-height despite zooming
        if endHeight <= 0:
            self.zoomPreview(-1)
            return
        # left upright bracket
        self.lengthLegend.append(QtGui.QGraphicsLineItem(leftEnd.x(),
                                                         leftEnd.y()+endHeight,
                                                         leftEnd.x(),
                                                         leftEnd.y()-endHeight))
        # right upright bracket
        self.lengthLegend.append(QtGui.QGraphicsLineItem(rightEnd.x(),
                                                         rightEnd.y()+endHeight,
                                                         rightEnd.x(),
                                                         rightEnd.y()-endHeight))
        # Scale textItem so it always appears the same size
        textItem.translate(rightEnd.x(),
                           rightEnd.y() - 
                           textItem.boundingRect().height()/(2*self.zoomScale))
        textItem.scale(1.0/self.zoomScale,
                       1.0/self.zoomScale)
        self.lengthLegend.append(textItem)

        for item in self.lengthLegend:
            self.ui.graphicsView.scene().addItem(item)

    def removeLengthScale(self):
        for item in self.lengthLegend:
            if item in self.ui.graphicsView.scene().items():
                self.ui.graphicsView.scene().removeItem(item)
        self.lengthLegend = []

    def zoomPreview(self, wheelClicks):
        scale = 1.2**wheelClicks
        self.zoomScale = self.zoomScale*scale
        self.ui.graphicsView.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.ui.graphicsView.scale(scale, scale)
        self.ui.graphicsView.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self.drawLengthScale()

    def savePreviewImage(self):
        imageSuffixes = ['.png', '.jpg', '.bmp', '.ppm', '.tiff', '.xbm', '.xpm']
        fileName, fileExtension = QtGui.QFileDialog.getSaveFileName(self, 'Save As',
                self.parent.lastUsedDirectory, ';;'.join(['*' + suffix for suffix in imageSuffixes]))
        if fileName == '':
            return
        fileExtension = fileExtension.lstrip("*")
        if not fileName.endswith(fileExtension):
            fileName = fileName + fileExtension
        self.parent.lastUsedDirectory = os.path.dirname(fileName)

        self.removeLengthScale()
        view = self.ui.graphicsView

        try:
            # reduce image size if either dimension is larger than maxImageDimension
            maxImageDimension = 2**14 - 1
            sceneSize = max([view.scene().itemsBoundingRect().width(),
                             view.scene().itemsBoundingRect().height()])*self.zoomScale
            scale = min([1.0, maxImageDimension/sceneSize])
            self.zoomScale = self.zoomScale*scale
            view.setTransformationAnchor(QtGui.QGraphicsView.AnchorViewCenter)
            view.scale(scale, scale)
            view.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)

            progress = QtGui.QProgressDialog('Creating Image ...', 'Cancel', 0, 6, self)
            progress.setMinimumDuration(0)
            progress.setValue(0)
            image = QtGui.QImage((view.scene().itemsBoundingRect().size()*self.zoomScale).toSize(),
                    QtGui.QImage.Format_ARGB32_Premultiplied)
            if progress.wasCanceled():
                return
            progress.setValue(1)
            progress.setLabelText('Filling Background ...')
            if fileExtension in ['.png', '.tiff', '.xpm']:
                image.fill(QtGui.QColor('transparent'))
            else:
                image.fill(QtGui.QColor('white'))
            if progress.wasCanceled():
                return

            progress.setValue(2)
            progress.setLabelText('Creating Painter ...')
            painter = QtGui.QPainter(image)
            if progress.wasCanceled():
                return

            progress.setValue(3)
            progress.setLabelText('Rendering Image ...')
            view.scene().render(painter)
            if progress.wasCanceled():
                return

            progress.setValue(4)
            progress.setLabelText('Saving Image ...')
            if not image.save(fileName):
                print "Image (" + fileName + ") was not saved."
                progress.reset()
                return

            progress.setLabelText('Deleting Painter ...')
            progress.setValue(5)

        finally:
            del painter
            progress.setValue(6)
            self.drawLengthScale()

    def convertToReversed(self):
        undoAction = commandReverse(self)
        self.undoStack.push(undoAction)

    def topLevelTreeItems(self):
        return [self.ui.treeWidget.topLevelItem(i) for i in range(self.ui.treeWidget.topLevelItemCount())]

    def listItems(self):
        return [self.ui.workingBeamline.item(i).text() for i in range(self.ui.workingBeamline.count())]

    def importFile(self, fileName):
        newElements, defaultBeamline = self.importer(fileName)
        if newElements is not None:
            undoAction = commandLoadElements(self, newElements.values())
            self.undoStack.push(undoAction)
        if defaultBeamline is not None:
            self.defaultBeamline = defaultBeamline

    def exportToFile(self, outputFileName = None):
        if not outputFileName:
            outputFileName, _ = QtGui.QFileDialog.getSaveFileName(self,
                'Export Charged Beam Transport',
                self.parent.lastUsedDirectory,
                '*.' + self.acceptsFileTypes[0])
        else:
            # Exporting a single tab doesn't count towards hasChanged()
            # Only saving to a project file provides this function with a name
            self.undoStack.setClean()

        self.exporter(outputFileName, self.elementDictionary, self.defaultBeamline)

        
def populateTreeItem(item, element):
    item.setText(0, element.name)
    item.setText(1, element.displayLine())
    item.setText(2, displayWithUnitsNumber(roundSigFig(element.getLength()), 'm'))
    item.setText(3, str(roundSigFig(convertUnitsNumber(element.getAngle(), 'rad', 'deg')))+' deg')
    item.setText(4, str(element.getNumberOfElements()) if element.isBeamline() else '')

def itemsInGroup(group):
    return [group.child(i) for i in range(group.childCount())]




# Undo Commands
class commandEditElement(QtGui.QUndoCommand):
    def __init__(self, widget, currentElement, newElement):
        QtGui.QUndoCommand.__init__(self)
        self.widget = widget
        self.activeElement = currentElement
        self.oldElement = type(self.activeElement)([self.activeElement.name] + self.activeElement.data[:])
        self.newElement = newElement

    def redo(self):
        if self.newElement is not None:
            self.replaceActive(self.newElement)
       
    def undo(self):
        if self.newElement is not None:
            self.replaceActive(self.oldElement)
            
    def replaceActive(self, source):
        oldName = self.activeElement.name
        self.activeElement.name = source.name
        self.activeElement.data = source.data

        del self.widget.elementDictionary[oldName]
        self.widget.elementDictionary[self.activeElement.name] = self.activeElement

        treeItem = self.widget.findElementInTreeByName(oldName)
        populateTreeItem(treeItem, source)

        for i, name in enumerate(self.widget.listItems()):
            if name == oldName:
                self.widget.ui.workingBeamline.item(i).setText(source.name)

        self.widget.rewriteBeamlineTree()
        self.widget.elementPreview()


class commandLoadElements(QtGui.QUndoCommand):
    def __init__(self, widget, elements, origin = ''):
        QtGui.QUndoCommand.__init__(self)
        self.widget = widget
        self.createdBeam = (origin == 'addBeam')

        self.createdElements = elements
        self.items = []
        self.createGroups = []
        self.groups = []
        self.groupPositions = []
        newGroups = []
        newGroupPosition = len(self.widget.topLevelTreeItems())
        itemCreateProgress = QtGui.QProgressDialog('Creating items ...',
                None, # Don't show a cancel button
                0,
                len(self.createdElements)-1)
        itemCreateProgress.setMinimumDuration(0)
        itemCreateProgress.setValue(0)
        for i, element in enumerate(self.createdElements):
            self.items.append(QtGui.QTreeWidgetItem())
            if element.name.startswith('-'):
                self.createGroups.append(False)
                self.groups.append(None)
                self.groupPositions.append(None)
                newGroups.append(None)
                continue
            populateTreeItem(self.items[-1], element)

            if element.isBeamline():
                typeName = self.widget.beamlineTreeLabel
            else:
                typeName = type(element).__name__
            if typeName in newGroups:
                index = newGroups.index(typeName)
                self.createGroups.append(False)
                self.groups.append(self.groups[index])
                self.groupPositions.append(self.groupPositions[index])
            else:
                for groupPosition, group in enumerate(self.widget.topLevelTreeItems()):
                    if group.text(0) == typeName:
                        self.createGroups.append(False)
                        self.groups.append(group)
                        self.groupPositions.append(groupPosition)
                        break
                else: # group not found
                    self.createGroups.append(True)
                    self.groups.append(QtGui.QTreeWidgetItem())
                    self.groups[-1].setText(0, typeName)
                    if element.isBeamline():
                        self.groupPositions.append(0)
                    else:
                        self.groupPositions.append(newGroupPosition)
                        newGroupPosition += 1
            newGroups.append(typeName)
            itemCreateProgress.setValue(i)

    def redo(self):
        treeAddProgress = QtGui.QProgressDialog('Adding to element tree ...',
                None, # Don't show a cancel button
                0,
                len(self.createdElements)-1)
        treeAddProgress.setMinimumDuration(0)
        treeAddProgress.setValue(0)
        for i, element in enumerate(self.createdElements):
            element.name = self.widget.uniqueName(element.name)
            self.widget.elementDictionary[element.name] = element
            self.items[i].setText(0, element.name)
            if element.name.startswith('-'): # reversed beamline
                continue
            if self.createGroups[i]:
                self.widget.ui.treeWidget.insertTopLevelItem(self.groupPositions[i], self.groups[i])
            self.groups[i].addChild(self.items[i])
            self.groups[i].setExpanded(True)
            treeAddProgress.setValue(i)
        self.widget.fitColumns()
        if len(self.createdElements) > 0:
            self.widget.ui.treeWidget.setCurrentItem(self.items[i])
        self.widget.elementPreview()
        if self.createdBeam:
            self.widget.ui.workingBeamline.clear()
            self.widget.workingBeamlineName = ''
            self.widget.ui.label.setText(self.widget.beamlineListLabelDefault)

    def undo(self):
        for i in range(len(self.createdElements)-1,-1,-1):
            # Delete elements from dictionary
            del self.widget.elementDictionary[self.createdElements[i].name]
            if self.createdElements[i].name.startswith('-'): # reversed beamline
                continue
            # Remove elements from tree
            index = self.items[i].parent().indexOfChild(self.items[i])
            self.items[i].parent().takeChild(index)
            # Delete group if adding element created a new group
            if self.createGroups[i]:
                self.widget.ui.treeWidget.takeTopLevelItem(self.groupPositions[i])
        if self.createdBeam:
            for element in self.createdElements[0].data:
                self.widget.ui.workingBeamline.addItem(element.name)
            self.widget.workingBeamlinePreview()
        else:
            self.widget.elementPreview()
            
class commandRemoveFromBeam(QtGui.QUndoCommand):
    def __init__(self, widget):
        QtGui.QUndoCommand.__init__(self)
        self.widget = widget
        self.row = self.widget.ui.workingBeamline.currentRow()
        self.text = self.widget.ui.workingBeamline.currentItem().text()
        
    def redo(self):
        self.widget.ui.workingBeamline.takeItem(self.row)
        self.widget.workingBeamlinePreview()       
        
    def undo(self):
        self.widget.ui.workingBeamline.insertItem(self.row, self.text)
        self.widget.workingBeamlinePreview()
        
        
class commandundoAdd2Beam(QtGui.QUndoCommand):
    def __init__(self, widget):
        QtGui.QUndoCommand.__init__(self)
        self.widget = widget

        self.previousList = self.widget.preListSave[:]
        self.previousListName = self.widget.preListNameSave
        self.previousListLabel = self.widget.preListLabelSave

        self.nextList = self.widget.postListSave[:]
        self.nextListName = self.widget.postListNameSave
        self.nextListLabel = self.widget.postListLabelSave

    def undo(self):
        self.widget.ui.workingBeamline.clear()
        for name in self.previousList:
            self.widget.ui.workingBeamline.addItem(name)
        self.widget.workingBeamlineName = self.previousListName
        self.widget.ui.label.setText(self.previousListLabel)
        self.widget.workingBeamlinePreview()

    def redo(self):
        self.widget.ui.workingBeamline.clear()
        for name in self.nextList:
            self.widget.ui.workingBeamline.addItem(name)
        self.widget.workingBeamlineName = self.nextListName
        self.widget.ui.label.setText(self.nextListLabel)
        self.widget.workingBeamlinePreview()


class commandReverse(QtGui.QUndoCommand):
    def __init__(self, widget):
        QtGui.QUndoCommand.__init__(self)
        self.widget = widget
        self.item = self.widget.ui.workingBeamline.currentItem()
        elementName = self.item.text()
        element = self.widget.elementDictionary[elementName]
        self.reversedElement = element.reverse()
        self.isNewElement = self.reversedElement.name not in self.widget.elementDictionary

    def redo(self):
        if self.isNewElement:
            self.widget.elementDictionary[self.reversedElement.name] = self.reversedElement
        self.item.setText(self.reversedElement.name)
        self.widget.workingBeamlinePreview()

    def undo(self):
        if self.isNewElement:
            del self.widget.elementDictionary[self.reversedElement.name]
        self.item.setText(self.reversedElement.reverse().name)
        self.widget.workingBeamlinePreview()


class commandDeleteElement(QtGui.QUndoCommand):
    def __init__(self, widget, name):
        QtGui.QUndoCommand.__init__(self)
        self.widget = widget
        self.element = self.widget.elementDictionary[name]
        self.treeItem = self.widget.findElementInTreeByName(self.element.name)
        self.parent = self.treeItem.parent()
        self.childIndex = self.parent.indexOfChild(self.treeItem)
        self.parentIndex = self.widget.ui.treeWidget.indexOfTopLevelItem(self.parent)
        self.oldBeamlines = []
        self.oldBeamlineData = []
        self.oldWorkingBeamline = self.widget.listItems()
        for beamline in self.widget.elementDictionary.values():
            if beamline.isBeamline() and not beamline.name.startswith('-'):
                self.oldBeamlines.append(beamline)
                self.oldBeamlineData.append(beamline.data[:])

    def redo(self):
        # Delete from dictionary
        del self.widget.elementDictionary[self.element.name]

        # Delete from tree
        self.parent.removeChild(self.treeItem)
        if self.parent.childCount() == 0:
            self.widget.ui.treeWidget.takeTopLevelItem(self.parentIndex)

        # Delete from beamlines
        for beamline in self.widget.elementDictionary.values():
            if beamline.isBeamline() and not beamline.name.startswith('-'):
                beamline.data = [element for element in beamline.data \
                        if element is not self.element]

        # Delete from list
        self.widget.rewriteBeamlineTree()
        self.widget.ui.graphicsView.scene().clear()

    def undo(self):
        # Restore to dictionary
        self.widget.elementDictionary[self.element.name] = self.element

        # Restore to tree
        if self.widget.ui.treeWidget.indexOfTopLevelItem(self.parent) == -1:
            self.widget.ui.treeWidget.insertTopLevelItem(self.parentIndex, self.parent)
        self.parent.insertChild(self.childIndex, self.treeItem)

        # Restore to beamlines
        for i in range(len(self.oldBeamlines)):
            self.oldBeamlines[i].data = self.oldBeamlineData[i][:]

        # Restore to list
        self.widget.ui.workingBeamline.clear()
        for name in self.oldWorkingBeamline:
            self.widget.ui.workingBeamline.addItem(name)

        self.widget.rewriteBeamlineTree()
        self.widget.ui.treeWidget.setCurrentItem(self.treeItem)
        self.widget.elementPreview()
