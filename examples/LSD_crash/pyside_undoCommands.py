from PySide.QtGui import QUndoCommand, QTreeWidgetItem

# QUndoCommand for creating a new THING and adding it's name to the 
# QTreeWidget
class LoadThings(QUndoCommand):
    def __init__(self, widget, thing):
        super(LoadThings, self).__init__()
        self.widget = widget

        self.createdThing = thing
        self.item = QTreeWidgetItem()
        self.item.setText(0, thing.name)

        typeName = type(thing).__name__
        for i in range(self.widget.ui.treeWidget.topLevelItemCount()):
            group = self.widget.ui.treeWidget.topLevelItem(i)
            if group.text(0) == typeName:
                self.group = group
                break
        else: # group not found
            self.group = QTreeWidgetItem()
            self.group.setText(0, typeName)

    def redo(self):
        if self.widget.ui.treeWidget.indexOfTopLevelItem(self.group) == -1:
            self.widget.ui.treeWidget.addTopLevelItem(self.group)
        self.group.addChild(self.item)
        self.group.setExpanded(True)
        self.widget.ui.treeWidget.setCurrentItem(self.item)

    def undo(self):
        self.group.takeChild(self.group.childCount()-1)
        if self.group.childCount() == 0:
            parentIndex = self.widget.ui.treeWidget.indexOfTopLevelItem(self.group)
            self.widget.ui.treeWidget.takeTopLevelItem(parentIndex)
            

# QUndoCommand for adding a THING's name to the QListWidget
class Add2List(QUndoCommand):
    def __init__(self, widget):
        super(Add2List, self).__init__()
        self.widget = widget
        self.previousList = self.widget.preListSave[:]
        self.nextList = self.widget.postListSave[:]

    def undo(self):
        self.widget.ui.listw.clear()
        self.widget.ui.listw.addItems(self.previousList)

    def redo(self):
        self.widget.ui.listw.clear()
        self.widget.ui.listw.addItems(self.nextList)
