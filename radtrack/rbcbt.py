from __future__ import absolute_import, division, print_function, unicode_literals
import os, shutil
from collections import OrderedDict
import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui, QtCore

from radtrack.ui.cbt import Ui_tree, genDialog, advDialog
from radtrack.RbUtility import displayWithUnitsNumber, \
                      convertUnitsNumber, \
                      roundSigFig


class RbCbt(QtGui.QWidget):
    def __init__(self, module, parent = None):
        QtGui.QWidget.__init__(self)
        
        #customize for simulation type
        self.beamlineType = module.beamlineType
        self.classDictionary = module.classDictionary
        self.acceptsFileTypes = [module.fileExtension]
        self.importer = module.fileImporter
        self.exporter = module.fileExporter

        self.defaultBeamline = ''

        #set layout
        self.ui = Ui_tree(self, module)

        #undo/redo 
        self.undoStack = QtGui.QUndoStack()

        #connections
        self.ui.workingBeamline.lengthChange.connect(self.callAfterWorkingBeamlineChanges)
        self.ui.workingBeamline.itemDoubleClicked.connect(self.editElement)
        self.ui.workingBeamline.itemPressed.connect(self.listClick)
        self.adv = advDialog(self)
        for button in self.ui.buttons + self.adv.buttons:
            button.clicked.connect(self.createNewElement)
            button.setToolTip(self.classDictionary[button.text()].elementDescription)
        if len(self.ui.advancedNames) > 0:
            self.ui.advanced.clicked.connect(self.adv.show)
        self.ui.clearBeamlineButton.clicked.connect(self.newBeam)
        self.ui.saveBeamlineButton.clicked.connect(self.addBeam)
        self.ui.treeWidget.itemSelectionChanged.connect(self.treeClick)
        self.ui.treeWidget.itemClicked.connect(self.treeClick)
        self.ui.treeWidget.itemDoubleClicked.connect(self.treeItemDoubleClicked)
        self.ui.treeWidget.itemEntered.connect(self.elementTreeHovered)
        self.ui.treeWidget.itemExited.connect(self.elementTreeExit)
        self.ui.graphicsView.itemDoubleClicked.connect(self.editElement)
        self.ui.graphicsView.wheelZoom.connect(self.zoomPreview)
        self.ui.graphicsView.dragDone.connect(self.drawLengthScale)
        self.ui.graphicsView.horizontalScrollBar().valueChanged.connect(self.drawLengthScale)
        self.ui.graphicsView.verticalScrollBar().valueChanged.connect(self.drawLengthScale)
        self.ui.graphicsView.itemDropped.connect(self.droppedOnGraphicsWindow)
        self.ui.contextMenuClicked.connect(self.createContextMenu)

        #### Keyboard shortcuts ####
        # Copy element in tree widget
        QtGui.QShortcut(QtGui.QKeySequence.Copy, self).activated.connect(lambda : self.copyElement(self.ui.treeWidget.currentItem()))

        # Zooming the preview window
        QtGui.QShortcut(QtGui.QKeySequence.ZoomIn, self).activated.connect(lambda : self.zoomPreview(1))
        QtGui.QShortcut(QtGui.QKeySequence.ZoomOut, self).activated.connect(lambda : self.zoomPreview(-1))
        
        #text
        self.addToBeamClickText = self.ui.translateUTF8('Add to current beam line')
        self.beamlineTreeLabel = self.ui.translateUTF8('Beamlines')
        self.beamlineListLabelDefault = self.ui.translateUTF8('New Beamline: ')
        self.ui.label.setText(self.beamlineListLabelDefault)
        self.emptyWorkingBeamlineCheck()

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
        self.drawPreviewEnabled = True

        # Graphical length legend for preview
        self.lengthLegend = []

    def undo(self):
        self.undoStack.undo()

    def redo(self):
        self.undoStack.redo()

    def addToEndOfWorkingBeamLine(self, elementName, copies = None):
        if not copies:
            copies, ok = self.getNumberOfCopies(elementName)
        else:
            ok = True

        if ok:
            for i in range(copies):
                self.ui.workingBeamline.addItem(elementName)
            self.callAfterWorkingBeamlineChanges()
        
    def addReversedToEndOfWorkingBeamLine(self, elementName, copies = None):
        bl = self.elementDictionary[elementName]
        blr = bl.reverse()
        self.elementDictionary[blr.name] = blr
        self.addToEndOfWorkingBeamLine(blr.name, copies)

    def emptyWorkingBeamlineCheck(self):
        isEmpty = self.ui.workingBeamline.count() == 0
        self.ui.clearBeamlineButton.setDisabled(isEmpty)
        self.ui.saveBeamlineButton.setDisabled(isEmpty)

    def droppedOnGraphicsWindow(self):
        if self.ui.treeWidget.currentItem():
            self.ui.workingBeamline.addItem(self.ui.treeWidget.currentItem().text(0))
            self.callAfterWorkingBeamlineChanges()

    def callAfterWorkingBeamlineChanges(self):
        self.fixWorkingBeamline()
        self.postListSave = self.workingBeamlineElementNames()
        if self.preListSave == self.postListSave:
            self.emptyWorkingBeamlineCheck()
            return
        self.postListNameSave = self.workingBeamlineName
        self.postListLabelSave = self.ui.label.text()
        undoAction = commandundoAdd2Beam(self)
        self.undoStack.push(undoAction)
        self.preListSave = self.postListSave
        self.preListNameSave = self.postListNameSave
        self.preListLabelSave = self.postListLabelSave
    
    def treeClick(self, item = None, column = None):
        # Draw element currently selected
        if item and item.text(column) == self.addToBeamClickText:
            self.addToEndOfWorkingBeamLine(item.text(0), 1)
        else:
            self.elementPreview()
        # Allow workingBeamline list and beamline preview to accept drops from treeWidget
        self.ui.workingBeamline.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.ui.graphicsView.setAcceptDrops(True)

    def treeItemDoubleClicked(self, item, column):
        if item and item.text(column) != self.addToBeamClickText:
            self.editElement(item.text(0))

    def elementTreeHovered(self, item, column):
        if item.text(column) == self.addToBeamClickText:
            self.ui.treeWidget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        else:
            self.elementTreeExit()

    def elementTreeExit(self):
        self.ui.treeWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def listClick(self):
        # Draw current working beamline
        self.workingBeamlinePreview()
        # Allow workingBeamline elements to be moved around without copying
        self.ui.workingBeamline.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        # Don't allow drags to beamline preview
        self.ui.graphicsView.setAcceptDrops(False)

    def createContextMenu(self, name, location, globalPos):
        element = self.elementDictionary.get(name)

        mouseMenu = QtGui.QMenu(self)

        if element:
            if location == 'picture':
                menuTitle = QtGui.QAction(element.toolTip(), mouseMenu)
                menuTitle.setEnabled(False)
                mouseMenu.addAction(menuTitle)
                mouseMenu.addSeparator()

            mouseMenu.addAction(self.ui.translateUTF8('Edit ...'), lambda: self.editElement(element.name))
            mouseMenu.addAction(self.ui.translateUTF8('New copy'), lambda: self.copyElement(element.name))
            mouseMenu.addAction(self.ui.translateUTF8('Delete element'), lambda: self.deleteElement(element.name))
            mouseMenu.addSeparator()

            if location == 'tree':
                mouseMenu.addAction(self.addToBeamClickText,
                        lambda: self.addToEndOfWorkingBeamLine(element.name, 1))
                mouseMenu.addAction('Add multiple copies ...',
                        lambda: self.addToEndOfWorkingBeamLine(element.name))
                mouseMenu.addAction('Add reversed',
                        lambda: self.addReversedToEndOfWorkingBeamLine(element.name, 1))
                mouseMenu.addAction('Add multiple reversed ..',
                        lambda: self.addReversedToEndOfWorkingBeamLine(element.name))

            if location == 'list':
                if element.isBeamline():
                    mouseMenu.addAction(self.ui.translateUTF8('Reverse'), self.convertToReversed)

                mouseMenu.addAction(self.ui.translateUTF8('Add another'), self.listCopy)
                mouseMenu.addAction(self.ui.translateUTF8('Add multiple copies ...'), self.listMultipleCopy)

                mouseMenu.addAction(self.ui.translateUTF8('Remove from beam line'), self.removeFromWorkingBeamline)

        if location == 'picture' and not self.ui.graphicsView.scene().zeroSized():
            mouseMenu.addSeparator()
            mouseMenu.addAction(self.ui.translateUTF8('Save preview image...'), \
                    self.savePreviewImage)
            mouseMenu.addAction(self.ui.translateUTF8('Reset zoom'), self.drawElement)
            mouseMenu.addAction(self.ui.translateUTF8('Turn ' + ('off' if self.drawPreviewEnabled else 'on') + \
                    ' graphical preview'), self.toggleDrawPreview)

        if mouseMenu.actions():
            mouseMenu.exec_(globalPos)

    def toggleDrawPreview(self):
        self.drawPreviewEnabled = not self.drawPreviewEnabled
        self.drawElement()
        
    def removeFromWorkingBeamline(self):
        undoAction = commandRemoveFromBeam(self)
        self.undoStack.push(undoAction)

    def editElement(self, name):
        try:
            selectedElement = self.elementDictionary[name]
        except KeyError: # Element name not found
            return

        if selectedElement.isBeamline():
            self.setWorkingBeamline(selectedElement)
            self.callAfterWorkingBeamlineChanges()
        else:
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

    def getNumberOfCopies(self, elementName):
        return QtGui.QInputDialog.getInt(self, \
                "Add multiple copies", \
                "Number of copies of " \
                + elementName + " to add:", \
                1,1)

    def listMultipleCopy(self):
        copies, ok = self.getNumberOfCopies(self.ui.workingBeamline.currentItem().text())
        if ok:
            for i in range(copies):
                self.listCopy(False)
            self.callAfterWorkingBeamlineChanges()

    def listCopy(self, postList = True):
        item = self.ui.workingBeamline.currentItem()
        row = self.ui.workingBeamline.row(item)
        self.ui.workingBeamline.insertItem(row, item.text())
        if postList:
            self.callAfterWorkingBeamlineChanges()

    def rewriteBeamlineTree(self):
        # Update element list
        for group in self.topLevelTreeItems():
            for item in itemsInGroup(group):
                populateTreeItem(self.addToBeamClickText, item, self.elementDictionary[item.text(0)])
        self.fitColumns()

        # Update Working Beamline
        self.fixWorkingBeamline()

    def fitColumns(self):
        for i in range(self.ui.treeWidget.columnCount()):
            if i != 1: # don't fit Description Column
                self.ui.treeWidget.resizeColumnToContents(i)

    def createNewElement(self):
        typeName = self.sender().text()
        elementType = self.classDictionary[typeName]
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
        if self.workingBeamlineName:
            beamline.name = self.workingBeamlineName

        for name in self.workingBeamlineElementNames():
            beamline.addElement(self.elementDictionary[name])              

        dialog = genDialog(beamline)
        if dialog.exec_():
            beamline.name = dialog.info[0][1].text()
            if self.workingBeamlineName:
                oldBeam = self.elementDictionary[self.workingBeamlineName]
                undoAction = commandEditElement(self, oldBeam, beamline)
            else:
                undoAction = commandLoadElements(self, [beamline])
            self.setWorkingBeamline()
            self.callAfterWorkingBeamlineChanges()
            self.undoStack.push(undoAction)
        self.emptyWorkingBeamlineCheck()

    def findElementInTreeByName(self, name):
        for group in self.topLevelTreeItems():
            for item in itemsInGroup(group):
                if item.text(0) == name:
                    return item

    def deleteElement(self, name):
        undoAction = commandDeleteElement(self, name)
        self.undoStack.push(undoAction)

    def newBeam(self):
        self.setWorkingBeamline()
        self.callAfterWorkingBeamlineChanges()

    def setWorkingBeamline(self, beamline = None):
        self.workingBeamlineName = beamline.name if (beamline and beamline.name in self.elementDictionary) else ''
        self.ui.label.setText(('Editing element: ' + self.workingBeamlineName) if self.workingBeamlineName else \
                self.beamlineListLabelDefault)
        self.ui.workingBeamline.clear()
        if beamline:
            self.ui.workingBeamline.addItems([element.name for element in beamline.data])
        self.emptyWorkingBeamlineCheck()
        self.workingBeamlinePreview()

    def fixWorkingBeamline(self):
        beamline = self.elementDictionary.get(self.workingBeamlineName)

        # Beamlines are constructed only from previously existing elements.
        # Beamlines cannot contain themselves.
        items = [name for name in self.workingBeamlineElementNames() if name in self.elementDictionary \
                and not self.elementDictionary[name].contains(beamline)]
        self.ui.workingBeamline.clear()
        self.ui.workingBeamline.addItems(items)

    def elementPreview(self):
        try:
            item = self.ui.treeWidget.currentItem()
            self.drawElement(self.elementDictionary[item.text(0)])
        except (AttributeError, KeyError):
            self.ui.graphicsView.scene().clear()

    def workingBeamlinePreview(self):
        bl = self.beamlineType()
        for name in self.workingBeamlineElementNames():
            bl.addElement(self.elementDictionary[name])
        self.drawElement(bl)

    def drawElement(self, element = None):
        scene = self.ui.graphicsView.scene()
        scene.clear()

        if not self.drawPreviewEnabled:
            return

        drawMessage = QtGui.QProgressDialog('Drawing beam line ...', 'Cancel', 0, 5, self.parent)
        drawMessage.setMinimumDuration(100)
        drawMessage.setValue(0)
        if element:
            self.lastDrawnElement = element
        else:
            element = self.lastDrawnElement

        element.picture(scene)
        sceneRect = scene.itemsBoundingRect()
        scene.setSceneRect(sceneRect)

        drawMessage.setValue(1)

        sx = sceneRect.width()
        sy = sceneRect.height()

        if sx == 0 or sy == 0:
            drawMessage.setValue(drawMessage.maximum())
            return

        viewSize = self.ui.graphicsView.size()
        vx = viewSize.width()
        vy = viewSize.height()

        scale = min([vx/sx, vy/sy, 1.0])

        drawMessage.setValue(2)
        self.ui.graphicsView.resetTransform()
        drawMessage.setValue(3)
        self.ui.graphicsView.scale(scale, scale)
        drawMessage.setValue(4)
        self.zoomScale = scale

        self.drawLengthScale()
        drawMessage.setValue(drawMessage.maximum())

    def visibleSceneRect(self):
        viewportRect = QtCore.QRect(0,0,self.ui.graphicsView.viewport().width(),
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
        resolution = self.classDictionary.values()[0]().getResolution()

        while length*resolution < float(vis.width())*widthFraction:
            length = length*10.0

        while length*resolution > float(vis.width())*widthFraction:
            length = length/10.0

        textItem = QtGui.QGraphicsTextItem(displayWithUnitsNumber(length, 'm'))

        pixLength = int(length*resolution)
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
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save As',
                self.parent.lastUsedDirectory, ';;'.join(['*' + suffix for suffix in imageSuffixes]))
        if fileName == '':
            return
        fileExtension = os.path.splitext(fileName)[1]
        self.parent.lastUsedDirectory = os.path.dirname(fileName)

        view = self.ui.graphicsView
        questionBox = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'RadTrack', 'Render entire beamline or just the viewable portion?')
        responses = [questionBox.addButton(text , QtGui.QMessageBox.ActionRole) for text in ['Entire Beamline', 'Viewable Portion']]
        questionBox.exec_()

        if questionBox.clickedButton() == responses[0]:
            boundingRectangle = view.scene().itemsBoundingRect()
        else:
            boundingRectangle = self.visibleSceneRect()

        # reduce image size if either dimension is larger than maxImageDimension
        maxImageDimension = 2**14 - 1
        sceneSize = max([boundingRectangle.width(),
                         boundingRectangle.height()])*self.zoomScale
        scale = min([1.0, maxImageDimension/sceneSize])
        self.zoomScale = self.zoomScale*scale
        view.setTransformationAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        view.scale(scale, scale)
        view.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)

        try:
            progress = QtGui.QProgressDialog('Creating Image ...', 'Cancel', 0, 6, self)
            progress.setMinimumDuration(0)
            progress.setValue(0)
            image = QtGui.QImage((boundingRectangle.size()*self.zoomScale).toSize(),
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
            view.scene().render(painter, QtCore.QRectF(), boundingRectangle)
            if progress.wasCanceled():
                return

            progress.setValue(4)
            progress.setLabelText('Saving Image ...')
            if not image.save(fileName):
                QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                 'RadTrack', "Image (" + fileName + ") was not saved.").exec_()
                progress.reset()
                return

        finally:
            progress.setLabelText('Deleting Painter ...')
            progress.setValue(5)
            try:
                del painter
            except:
                pass
            progress.setValue(6)
            self.drawLengthScale()

    def convertToReversed(self):
        beamlineName = self.ui.workingBeamline.currentItem().text()
        reversedBeamline = self.elementDictionary[beamlineName].reverse()
        self.elementDictionary[reversedBeamline.name] = reversedBeamline
        self.ui.workingBeamline.currentItem().setText(reversedBeamline.name)
        self.callAfterWorkingBeamlineChanges()

    def topLevelTreeItems(self):
        return [self.ui.treeWidget.topLevelItem(i) for i in range(self.ui.treeWidget.topLevelItemCount())]

    def workingBeamlineElementNames(self):
        return [self.ui.workingBeamline.item(i).text() for i in range(self.ui.workingBeamline.count())]

    def importFile(self, fileName):
        ignoreMissingImportFiles = False
        try:
            importedData = self.importer(fileName)
        except IOError as e:
            QtGui.QMessageBox(QMessageBox.Warning, 'RadTrack', e.message).exec_()
            return

        if importedData:
            newElements, defaultBeamline = importedData

            if newElements:
                undoAction = commandLoadElements(self, newElements.values())
                self.undoStack.push(undoAction)

            if defaultBeamline:
                self.defaultBeamline = defaultBeamline

            # Copy files referenced by the elements into the current working directory
            for element in [e for e in newElements.values() if not e.isBeamline()]:
                for parameter in element.inputFileParameters:
                    index = element.parameterNames.index(parameter)
                    if element.data[index]:
                        path = os.path.join(os.path.dirname(fileName), element.data[index])
                        try:
                            shutil.copy2(path, self.parent.sessionDirectory)
                        except IOError:
                            if not ignoreMissingImportFiles:
                                box = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                                        'Missing File Reference',
                                                        'The file "' + path.replace('\\', '/') + '" specified by element "' + \
                                                        element.name + '" cannot be found.\n\n' +\
                                                        'Do you wish to ignore future warnings of this type?',
                                                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, self)
                                box.exec_()
                                if box.standardButton(box.clickedButton()) == QtGui.QMessageBox.Yes:
                                    ignoreMissingImportFiles = True

    def exportToFile(self, outputFileName = None):
        if not outputFileName:
            outputFileName = QtGui.QFileDialog.getSaveFileName(self,
                'Export Charged Beam Transport',
                self.parent.lastUsedDirectory,
                '*.' + self.acceptsFileTypes[0])
                
        if not outputFileName:
            return # User cancelled

        self.exporter(outputFileName, self.elementDictionary, self.defaultBeamline)

    def closeEvent(self, event):
        # Large pictures seem to crash python on exiting RadTrack,
        # so clear the picture before exiting.
        self.ui.graphicsView.scene().clear()
        QtGui.QWidget.closeEvent(self, event)


        
def populateTreeItem(addToBeamClickText, item, element):
    item.setText(0, element.name)
    item.setText(1, element.displayLine())
    item.setText(2, displayWithUnitsNumber(roundSigFig(element.getLength(), 4), 'm'))
    item.setText(3, str(roundSigFig(convertUnitsNumber(element.getAngle(), 'rad', 'deg'), 4))+' deg')
    item.setText(4, str(element.getNumberOfElements()) if element.isBeamline() else '')
    item.setText(5, addToBeamClickText)
    item.setForeground(5, QtCore.Qt.red)
    font = item.font(5)
    font.setBold(True)
    font.setUnderline(True)
    item.setFont(5, font)

def itemsInGroup(group):
    return [group.child(i) for i in range(group.childCount())]




# Undo Commands
class commandEditElement(QtGui.QUndoCommand):
    def __init__(self, widget, currentElement, newElement):
        QtGui.QUndoCommand.__init__(self)
        self.widget = widget
        self.activeElement = currentElement
        self.oldElement = type(self.activeElement)([self.activeElement.name] + self.activeElement.data[:])

        # Make sure newElement doesn't have the same name as another existing element unless
        # it is the name of the currentElement (editing in place).
        if newElement.name in self.widget.elementDictionary and \
                self.widget.elementDictionary[newElement.name] != currentElement:
            newElement.name = self.widget.uniqueName(newElement.name)
        self.newElement = newElement

    def redo(self):
        self.replaceActive(self.newElement)
        if self.newElement.isBeamline():
            self.widget.setWorkingBeamline()
       
    def undo(self):
        self.replaceActive(self.oldElement)
        if self.oldElement.isBeamline():
            self.widget.setWorkingBeamline(self.newElement)
            
    def replaceActive(self, source):
        oldName = self.activeElement.name

        # Slot in data to element in elementDictionary
        self.activeElement.name = source.name
        self.activeElement.data = source.data

        # Change key in elementDictionary while preserving insertion order
        newDict = OrderedDict()
        for key, value in zip(self.widget.elementDictionary, self.widget.elementDictionary.values()):
            if key == oldName:
                newDict[self.activeElement.name] = self.activeElement
            else:
                newDict[key] = value
        self.widget.elementDictionary = newDict

        # Propagate name changes to tree and working beamline
        treeItem = self.widget.findElementInTreeByName(oldName)
        populateTreeItem(self.widget.addToBeamClickText, treeItem, source)
        for i, name in enumerate(self.widget.workingBeamlineElementNames()):
            if name == oldName:
                self.widget.ui.workingBeamline.item(i).setText(source.name)
        self.widget.rewriteBeamlineTree()
        self.widget.elementPreview()
        self.widget.emptyWorkingBeamlineCheck()


class commandLoadElements(QtGui.QUndoCommand):
    def __init__(self, widget, elements):
        QtGui.QUndoCommand.__init__(self)
        self.widget = widget

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
            populateTreeItem(self.widget.addToBeamClickText, self.items[-1], element)

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
        treeAddProgress.setMinimumDuration(500)
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
        self.widget.emptyWorkingBeamlineCheck()
        
    def undo(self):
        self.widget.ui.workingBeamline.insertItem(self.row, self.text)
        self.widget.emptyWorkingBeamlineCheck()
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
        self.widget.ui.workingBeamline.addItems(self.previousList)
        self.widget.workingBeamlineName = self.previousListName
        self.widget.ui.label.setText(self.previousListLabel)
        self.widget.emptyWorkingBeamlineCheck()
        self.widget.workingBeamlinePreview()

    def redo(self):
        self.widget.ui.workingBeamline.clear()
        self.widget.ui.workingBeamline.addItems(self.nextList)
        self.widget.workingBeamlineName = self.nextListName
        self.widget.ui.label.setText(self.nextListLabel)
        self.widget.emptyWorkingBeamlineCheck()
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
        self.oldWorkingBeamline = self.widget.workingBeamlineElementNames()
        self.oldElementDictionary = OrderedDict()
        for element in self.widget.elementDictionary.values():
            self.oldElementDictionary[element.name] = element
            if element.isBeamline() and not element.name.startswith('-'):
                self.oldBeamlines.append(element)
                self.oldBeamlineData.append(element.data[:])

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
        self.widget.rewriteBeamlineTree() # calls self.widget.fixWorkingBeamline()
        self.widget.ui.graphicsView.scene().clear()
        self.widget.emptyWorkingBeamlineCheck()

    def undo(self):
        # Restore to dictionary
        self.widget.elementDictionary = self.oldElementDictionary

        # Restore to tree
        if self.widget.ui.treeWidget.indexOfTopLevelItem(self.parent) == -1:
            self.widget.ui.treeWidget.insertTopLevelItem(self.parentIndex, self.parent)
        self.parent.insertChild(self.childIndex, self.treeItem)

        # Restore to beamlines
        for i in range(len(self.oldBeamlines)):
            self.oldBeamlines[i].data = self.oldBeamlineData[i][:]

        # Restore to list
        self.widget.ui.workingBeamline.clear()
        self.widget.ui.workingBeamline.addItems(self.oldWorkingBeamline)

        self.widget.rewriteBeamlineTree()
        self.widget.ui.treeWidget.setCurrentItem(self.treeItem)
        self.widget.emptyWorkingBeamlineCheck()
        self.widget.elementPreview()
