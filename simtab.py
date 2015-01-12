import sys
from PyQt4 import QtGui, QtCore
from RadTrack.interactions.simulationpanel import Ui_Form

class simtab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.programs.setDragEnabled(True)
        self.ui.graphicsView.setAcceptDrops(True)

        rect = QtCore.QRectF(0,0,2000,1080)
        
        background = QtGui.QGraphicsRectItem(rect)
        whitebrush = QtGui.QBrush(QtCore.Qt.white)
        background.setBrush(whitebrush)
        background.setAcceptDrops(True)

        self.scene = customscene(self)
        self.scene.addItem(background)
        self.scene.signal.connect(self.addbox)

        self.ui.graphicsView.setScene(self.scene)
        


    def addbox(self, pos):
        a = self.scene.itemAt(pos)
        if int(a.pos().x()) == 0 and int(a.pos().y()) == 0:
               
            item = myitem()
            item.text = self.ui.programs.currentItem().text()
            item.setPos(pos)
            item.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
            self.scene.addItem(item)

        else:
            item = myitem()
            item.text = self.ui.programs.currentItem().text()
            item.setPos(a.pos().x()+150,a.pos().y())
            line = QtGui.QGraphicsLineItem()
            pen = QtGui.QPen(QtCore.Qt.blue)
            line.setPen(pen)
            item.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
            
            l = QtCore.QLineF(a.pos().x()+100,a.pos().y()+25,item.pos().x(),item.pos().y()+25)
            line.setLine(l)
            self.scene.addItem(line)
            self.scene.addItem(item)




class customscene(QtGui.QGraphicsScene):
    signal = QtCore.Signal(QtCore.QPointF)

    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self)

    def dragEnterEvent(self, event):
        super(customscene, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(customscene, self).dragMoveEvent(event)

    def dropEvent(self, event):
        super(customscene, self).dropEvent(event)
        self.signal.emit(event.scenePos())

class myitem(QtGui.QGraphicsItem):

    def __init__(self, parent=None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self.limit = QtCore.QRectF(0,0,100,50)
        self.setAcceptDrops(True)
        self.text = ''
        
    def boundingRect(self):
        return self.limit

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.red)
        painter.drawRect(self.limit)
        painter.drawText(self.limit, QtCore.Qt.AlignCenter, self.text)

    def dropEvent(self, event):
        super(myitem, self).dropEvent(event)

    def dragEnterEvent(self, event):
        super(myitem, self).dragEnterEvent(event)
        
    def dragMoveEvent(self, event):
        super(myitem, self).dragMoveEvent(event)




'''def main():

    app = QtGui.QApplication(sys.argv)
    myapp = simtab()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()'''
