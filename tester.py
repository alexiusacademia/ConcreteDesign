import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from views import materialProperties
from views import rectRCBeam
from views import geometrySetting
from views import settingsLoadingFactors
from views import spreadsheet
from models import Footing

class MainApp(QtGui.QMainWindow):

    SPREADSHEET_COUNTER = 0

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.mdi        = QtGui.QMdiArea()
        self.setCentralWidget(self.mdi)
        statusBar       = self.statusBar()
        self.createMenus()
        self.createToolbars()
        # Create preferences/setting
        self.createSettings()

    def createSettings(self):
        self.setting     = QtCore.QSettings("ASA", "Reinforced Concrete Design")
        try:
            float(self.setting.value('concreteCompressiveStress'))
            float(self.setting.value('steelYieldStrength'))
            float(self.setting.value('concreteWeight'))
        except:
            self.setting.setValue('concreteCompressiveStress', 20.7)
            self.setting.setValue('steelYieldStrength', 276.0)
            self.setting.setValue('concreteWeight', 23.4)
        try:
            int(self.setting.value('concreteCover'))
        except:
            # Pass a default value
            self.setting.setValue('concreteCover', 40)
        try:
            int(self.setting.value('beamMainBar'))
        except:
            self.setting.setValue('beamMainBar', 12)
        try:
            int(self.setting.value('beamStirrup'))
        except:
            self.setting.setValue('beamStirrup', 10)
        try:
            float(self.setting.value('deadloadFactor'))
            float(self.setting.value('liveloadFactor'))
        except:
            self.setting.setValue('deadloadFactor', 1.4)
            self.setting.setValue('liveloadFactor', 1.7)
        try:
            float(self.setting.value('concreteWeightFactor'))
        except:
            self.setting.setValue('concreteWeightFactor', 1.0)
        try:
            float(self.setting.value('beamReductionFactor'))
        except:
            self.setting.setValue('beamReductionFactor', 0.75)
        try:
            int(self.setting.value('stirrupLegs'))
        except:
            self.setting.setValue('stirrupLegs', 2)


    def createMenus(self):
        # Create menubar
        menuBar                     = self.menuBar()

        # Create menus
        mnuFile                     = menuBar.addMenu("File")
        mnuSpreadsheet              = menuBar.addMenu("Spreadsheet")
        mnuSettings                 = menuBar.addMenu("Settings")
        mnuHelp                     = menuBar.addMenu("Help")

        # Create Actions
        actionExit                  = mnuFile.addAction("Exit")
        actionExit.setShortcut("Ctrl+X")

        actionSpreadsheetRectangularBeam           = mnuSpreadsheet.addAction("Rectangular Beam")
        actionSpreadsheetRectangularBeam.setShortcut("Ctrl+B")

        actionSettingMaterial       = mnuSettings.addAction("Material Properties")
        actionSettingMaterial.setShortcut("Ctrl+M")

        actionSettingGeometry       = mnuSettings.addAction("Geometry Settings")
        actionSettingGeometry.setShortcut("Ctrl+G")

        actionSettingLoadingFactor  = mnuSettings.addAction("Loading Factor Settings")
        actionSettingLoadingFactor.setShortcut("Ctrl+L")

        actionAbout                 = mnuHelp.addAction("About")

        # Add actions to the menus
        mnuFile.addAction(actionExit)

        # Add triggers to the actions
        mnuFile.triggered[QtGui.QAction].connect(self.menuActions)
        mnuSpreadsheet.triggered[QtGui.QAction].connect(self.menuActions)
        mnuSettings.triggered[QtGui.QAction].connect(self.menuActions)
        mnuHelp.triggered[QtGui.QAction].connect(self.menuActions)

    def createToolbars(self):
        # Create toolbar group
        toolBarSS           = QtGui.QToolBar('')
        toolBarSS.setToolTip('Spreadsheet')
        toolBarSS.setMovable(False)
        self.addToolBar(toolBarSS)

        toolBarSetting      = QtGui.QToolBar('')
        toolBarSetting.setToolTip('Settings')
        toolBarSetting.setMovable(False)
        self.addToolBar(toolBarSetting)


        # Create action
        actionRectangular   = QtGui.QAction(QtGui.QIcon("views/beamsection.png"), "Rectangular Beam", self)

        actionMaterial      = QtGui.QAction(QtGui.QIcon("views/materialproperties.png"), "Material Properties", self)
        actionGeometry      = QtGui.QAction(QtGui.QIcon("views/geometrysetting.png"), "Geometry Settings", self)
        actionLoadingFactor = QtGui.QAction(QtGui.QIcon("views/loadingfactorsetting.png"), "Loading Factor Settings", self)

        # Add the action to the toolbars
        toolBarSS.addWidget(QtGui.QLabel("Solvers"))
        toolBarSS.addAction(actionRectangular)
        toolBarSS.addSeparator()

        toolBarSetting.addWidget(QtGui.QLabel("Settings"))
        toolBarSetting.addAction(actionMaterial)
        toolBarSetting.addAction(actionGeometry)
        toolBarSetting.addAction(actionLoadingFactor)
        toolBarSetting.addSeparator()

        # Actions
        toolBarSS.actionTriggered[QtGui.QAction].connect(self.menuActions)
        toolBarSetting.actionTriggered[QtGui.QAction].connect(self.menuActions)

    def menuActions(self, q):
        cmd = q.text()

        if cmd == 'Exit':
            self.setStatusTip("Exit the application.")
            sys.exit()
        elif cmd == 'Rectangular Beam':
            self.setStatusTip("Open a spreadsheet/solver.")
            print('Opening solver/spreadsheet...')
            self.startSpreadsheetRectangularBeam()
        elif cmd == 'Material Properties':
            print("Setting the materials properties.")
            materialProperties.MaterialSettings(self)
        elif cmd == 'Geometry Settings':
            print("Geometry setting..")
            geometrySetting.GeometrySetting(self)
        elif cmd == "Loading Factor Settings":
            print("Loading factor setting...")
            settingsLoadingFactors.LoadingFactors(self)
        elif cmd == "About":
            print("Show about dialog.")


    def startSpreadsheetRectangularBeam(self):
        sub = rectRCBeam.RectRCBeam(self)
        self.mdi.addSubWindow(sub)
        sub.show()

    def showSpreadsheet(self):
        # Create spreadsheet
        self.spreadsheet1     = spreadsheet.SpreadsheetTemplate(self)
        self.mdi.addSubWindow(self.spreadsheet1)
        self.spreadsheet1.show()

    def hideSpreadsheet(self, spreadsheet):
        spreadsheet.hide()

    def closeEvent(self, event):
        result = QtGui.QMessageBox.question(self,
                      "Confirm Exit...",
                      "Are you sure you want to exit ?",
                      QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
        event.ignore()

        if result == QtGui.QMessageBox.Yes:
            event.accept()

app = QtGui.QApplication(sys.argv)
main = MainApp()
main.show()
main.showMaximized()
main.setWindowTitle('Reinforced Concrete Design')

app.exec_()