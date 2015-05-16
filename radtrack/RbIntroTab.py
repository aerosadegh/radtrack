from PyQt4 import QtGui, QtCore
from radtrack.ui.rbintro import Ui_Widget

class RbIntroTab(QtGui.QWidget):
    defaultTitle = 'Start here'
    acceptsFileTypes = ['start']

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        categoryLayout = dict()
        categoryLayout['beams'] = self.ui.beamsVerticalLayout
        categoryLayout['beam lines'] = self.ui.beamLinesVerticalLayout
        categoryLayout['simulations'] = self.ui.simulationsVerticalLayout
        categoryLayout['tools'] = self.ui.toolsVerticalLayout

        self.parent = parent
        for tabType in self.parent.availableTabTypes:
            button = QtGui.QPushButton(self.parent.tr(tabType.task), \
                                       self.parent)
            button.clicked.connect(lambda ignore, tabType = tabType : \
                                       self.parent.newTab(tabType))
            categoryLayout[tabType.category].addWidget(button)

        for layout in categoryLayout.values():
            layout.addStretch()

        self.container = self

    def exportToFile(self, fileName = None):
        with open(fileName, 'w'):
            pass
