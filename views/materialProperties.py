import sys
from PyQt4 import QtCore
from PyQt4 import QtGui

class MaterialSettings(QtGui.QDialog):
    def __init__(self, parent):
        super(MaterialSettings, self).__init__(parent)
        self.parentWindow = parent
        self.createUI()
        self.show()

    def createUI(self):
        self.setWindowTitle("Material Properties Setting")

        # Create layout managers
        layout          = QtGui.QVBoxLayout()
        layoutFPC       = QtGui.QHBoxLayout()
        layoutFy        = QtGui.QHBoxLayout()
        layoutButtons   = QtGui.QHBoxLayout()

        # Create labels
        lblTitle        = QtGui.QLabel("<h3><b>Material Properties</b></h3>")
        lblFPC          = QtGui.QLabel("f'c (MPa)")
        lblFy           = QtGui.QLabel("fy (MPa)")

        # Create line edits
        self.leFPC      = QtGui.QLineEdit()
        self.leFPC.setAlignment(QtCore.Qt.AlignHCenter)
        self.leFPC.setText(str(self.parentWindow.setting.value('concreteCompressiveStress')))
        self.leFy       = QtGui.QLineEdit()
        self.leFy.setAlignment(QtCore.Qt.AlignHCenter)
        self.leFy.setText(str(self.parentWindow.setting.value('steelYieldStrength')))

        #  Create push buttons
        btnApply        = QtGui.QPushButton("Apply")
        btnApply.clicked.connect(self.applySettings)
        btnCancel       = QtGui.QPushButton("Cancel")
        btnCancel.clicked.connect(self.cancel)

        # Add widgets to layouts
        layout.addWidget(lblTitle)
        layout.addLayout(layoutFPC)
        layout.addLayout(layoutFy)
        layout.addLayout(layoutButtons)

        layoutFPC.addWidget(lblFPC)
        layoutFPC.addWidget(self.leFPC)

        layoutFy.addWidget(lblFy)
        layoutFy.addWidget(self.leFy)

        layoutButtons.addWidget(btnApply)
        layoutButtons.addWidget(btnCancel)

        self.setLayout(layout)

    def applySettings(self):
        print("Applying settings...")

        # Get values from the inputs
        try:
            self.parentWindow.setting.setValue('concreteCompressiveStress', float(self.leFPC.text()))
            self.parentWindow.setting.setValue('steelYieldStrength', float(self.leFy.text()))
            msgBox  = QtGui.QMessageBox()
            msgBox.setWindowTitle('Success')
            msgBox.setText('Setting saved.')
            msgBox.setIcon(QtGui.QMessageBox.Information)
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.show()
            msgBox.exec_()
            self.close()
        except:
            # Display a message box
            msgBox  = QtGui.QMessageBox()
            msgBox.setWindowTitle("Input Error")
            msgBox.setText("Inputs must be numeric!\nPlease check your inputs.")
            msgBox.setIcon(QtGui.QMessageBox.Information)
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.show()
            raise ValueError

    def cancel(self):
        self.close()