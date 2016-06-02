from PyQt4 import QtGui, QtCore
from radtrack.ui.RbRawDataDialogBox import Ui_Dialog

class RbRawDataDialogBox(QtGui.QDialog):
    def __init__(self, parent, fileName):
        super(RbRawDataDialogBox, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        with open(fileName) as f:
            for line in f:
                self.ui.textBrowser.append(line)
        cursor = self.ui.textBrowser.textCursor()
        cursor.setPosition(0);
        self.ui.textBrowser.setTextCursor(cursor)
        self.ui.label.setText(fileName)
