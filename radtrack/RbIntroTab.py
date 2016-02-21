from PyQt4 import QtGui
from collections import OrderedDict
from radtrack.ui.rbintro import Ui_Widget

class RbIntroTab(QtGui.QWidget):
    defaultTitle = 'Start here'
    acceptsFileTypes = ['start']

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_Widget()
        self.ui.setupUi(self)


        categoryLayout = OrderedDict()
        categoryLayout['beams'] = self.ui.beamsVerticalLayout
        categoryLayout['beam lines'] = self.ui.beamLinesVerticalLayout
        categoryLayout['simulations'] = self.ui.simulationsVerticalLayout
        categoryLayout['tools'] = self.ui.toolsVerticalLayout

        self.parent = parent

        # Create button for every available tab type in RbGlobal
        for tabType in self.parent.availableTabTypes:
            if tabType == type(self):
                continue
            button = QtGui.QPushButton(self.parent.tr(tabType.task), \
                                       self.parent)
            button.clicked.connect(lambda ignore, tabType = tabType : \
                                       self.parent.newTab(tabType))
            categoryLayout[tabType.category].addWidget(button)

        # Set tab order of buttons (start in top-left, go down,
        # then to top of next column)
        lastWidget = None
        for layout in categoryLayout.values():
            layout.addStretch()
            for index in range(layout.count()):
                widget = layout.itemAt(index).widget()
                if type(widget) == QtGui.QPushButton:
                    if lastWidget:
                        self.setTabOrder(lastWidget, widget)
                    lastWidget = widget

    def exportToFile(self, fileName):
        with open(fileName, 'w'):
            pass

    def importFile(self, fileName):
        pass
