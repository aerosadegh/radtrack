import sys, random
from PyQt4 import QtGui

from pyqt_undoCommands import Add2List, LoadThings
from pyqt_windowLayout import Ui_tree, genDialog

class THING(object):
    def __init__(self):
        self.name = str(random.randint(0,1000000))

class mainWindow(QtGui.QWidget):
    def __init__(self):
        super(mainWindow, self).__init__()

        # Save current condition of list so it can be restored
        # with self.undoStack.undo()
        self.preListSave = []

        #set layout
        self.ui = Ui_tree(self, THING)

        #undo/redo 
        self.undoStack = QtGui.QUndoStack()

        #connections
        self.ui.listw.lengthChange.connect(self.postListDrop)
        self.ui.addButton.clicked.connect(self.createNewThing)
        self.ui.testButton.clicked.connect(self.test)
        self.ui.contextMenuClicked.connect(self.listCopy)

        # Undo/Redo keyboard shortcuts
        QtGui.QShortcut(QtGui.QKeySequence.Undo, self).activated.connect(self.undo)
        QtGui.QShortcut(QtGui.QKeySequence.Redo, self).activated.connect(self.redo)

    def undo(self):
        self.undoStack.undo()

    def redo(self):
        self.undoStack.redo()

    # Creates an action to return the list to a previous state
    # after a drag/drop or other action that changes the list
    def postListDrop(self):
        self.postListSave = self.listItems()
        undoAction = Add2List(self)
        self.undoStack.push(undoAction)
        self.preListSave = self.postListSave
    
    # Copies an item in the list widget next to the original
    def listCopy(self):
        if self.ui.listw.count() == 0:
            return
        item = self.ui.listw.currentItem()
        if item is not None:
            row = self.ui.listw.row(item)
            self.ui.listw.insertItem(row, item.text())
            self.postListDrop()

    # Opens and closes a dialog box used to create a new element
    def createNewThing(self):
        thing = THING()
        dialog = genDialog(thing)
        dialog.show()
        dialog.accept()
        thing.name = dialog.info[1].text()
        undoAction = LoadThings(self, thing)
        self.undoStack.push(undoAction)

    # Returns a list of strings from the contents of the list widget
    def listItems(self):
        return [self.ui.listw.item(i).text() for i in range(self.ui.listw.count())]


    # Run through all commands randomly and automatically
    functions = []
    functions.append(undo)
    functions.append(redo)
    functions.append(listCopy)
    functions.append(createNewThing)
    def test(self):
        while True:
            number = random.randint(0, len(self.functions)-1)
            print self.functions[number]
            if self.ui.listw.count() > 0:
                self.ui.listw.setCurrentItem(self.ui.listw.item(random.randint(0,self.ui.listw.count()-1)))
            self.functions[number](self)


def run():
    app = QtGui.QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
