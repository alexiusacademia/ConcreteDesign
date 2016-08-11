import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from views import materialProperties
from views import rectRCBeam
from views import geometrySetting

class MainApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.mdi        = QtGui.QMdiArea()
        self.setCentralWidget(self.mdi)
        statusBar       = self.statusBar()
        self.createMenus()

        # Create preferences/setting
        self.createSettings()

    def createSettings(self):
        self.setting     = QtCore.QSettings("ASA", "Reinforced Concrete Design")
        try:
            print(self.setting.value('concreteCompressiveStress'))
        except:
            self.setting.setValue('concreteCompressiveStress', 20.7)
            self.setting.setValue('steelYieldStrength', 276.0)
        try:
            int(self.setting.value('concreteCover'))
            print(self.setting.value('concreteCover'))
        except:
            # Pass a default value
            self.setting.setValue('concreteCover', 40)

    def createMenus(self):
        # Create menubar
        menuBar             = self.menuBar()

        # Create menus
        mnuFile             = menuBar.addMenu("File")
        mnuSpreadsheet      = menuBar.addMenu("Spreadsheet")
        mnuSettings         = menuBar.addMenu("Settings")

        # Create Actions
        actionExit          = mnuFile.addAction("Exit")
        actionExit.setShortcut("Ctrl+X")

        actionSpreadsheet   = mnuSpreadsheet.addAction("Spreadsheet")
        actionSpreadsheet.setShortcut("Ctrl+H")

        actionSettingMaterial   = mnuSettings.addAction("Material Properties")
        actionSettingMaterial.setShortcut("Ctrl+M")

        actionSettingGeometry   = mnuSettings.addAction("Geometry Settings")
        actionSettingGeometry.setShortcut("Ctrl+G")

        # Add actions to the menus
        mnuFile.addAction(actionExit)

        # Add triggers to the actions
        mnuFile.triggered[QtGui.QAction].connect(self.menuActions)
        mnuSpreadsheet.triggered[QtGui.QAction].connect(self.menuActions)
        mnuSettings.triggered[QtGui.QAction].connect(self.menuActions)

    def menuActions(self, q):
        cmd = q.text()

        if cmd == 'Exit':
            self.setStatusTip("Exit the application.")
            print('App is exiting...')
            sys.exit()
        elif cmd == 'Spreadsheet':
            self.setStatusTip("Open a spreadsheet/solver.")
            print('Opening solver/spreadsheet...')
            self.startSpreadsheet()
        elif cmd == 'Material Properties':
            print("Setting the materials properties.")
            materialProperties.MaterialSettings(self)
        elif cmd == 'Geometry Settings':
            print("Geometry setting..")
            geometrySetting.GeometrySetting(self)


    def startSpreadsheet(self):
        sub = rectRCBeam.RectRCBeam(self)
        self.mdi.addSubWindow(sub)
        sub.show()

app = QtGui.QApplication(sys.argv)
main = MainApp()
main.show()
main.showMaximized()
main.setWindowTitle('Reinforced Concrete Design')
app.exec_()