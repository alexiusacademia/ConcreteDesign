from PyQt4 import QtGui

class SpreadsheetTemplate(QtGui.QFrame):
    def __init__(self, parent):
        super(SpreadsheetTemplate, self).__init__(parent)
        print(self.windowTitle())
        # Position the window at the bottom
        y = parent.height()#-self.height()
        print(parent.height())
        self.move(0, y)
        self.createUI()

    def createUI(self):
        # Create table
        table       = QtGui.QTableWidget()
        table.setRowCount(1)
        table.setColumnCount(5)

        # Create layout
        layout      = QtGui.QVBoxLayout()
        self.setLayout(layout)

        # Add widget to layout
        layout.addWidget(table)

    # Override closeEvent
    def closeEvent(self, *args, **kwargs):
        self.hide()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    s   = SpreadsheetTemplate()
    app.exec_()