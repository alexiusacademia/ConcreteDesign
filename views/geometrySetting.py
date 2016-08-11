import sys
from PyQt4 import QtCore
from PyQt4 import QtGui

class GeometrySetting(QtGui.QDialog):
    def __init__(self, parent):
        super(GeometrySetting, self).__init__(parent)
        self.parentWindow = parent
        self.createUI()
        self.show()

    def createUI(self):
        self.setWindowTitle("Material Properties Setting")

        # Create layout managers
        layout          = QtGui.QVBoxLayout()
        layoutCC        = QtGui.QHBoxLayout()       # Layout for concrete cover entry
        layoutButtons   = QtGui.QHBoxLayout()

        # Create labels
        lblTitle        = QtGui.QLabel("<h3><b>Geometry Properties</b></h3>")
        lblCC           = QtGui.QLabel("Concrete Cover (mm)")

        # Create line edits
        self.leCC       = QtGui.QLineEdit()
        self.leCC.setAlignment(QtCore.Qt.AlignHCenter)
        self.leCC.setText(str(self.parentWindow.setting.value('concreteCover')))

        #  Create push buttons
        btnApply        = QtGui.QPushButton("Apply")
        btnApply.clicked.connect(self.applySettings)
        btnCancel       = QtGui.QPushButton("Cancel")
        btnCancel.clicked.connect(self.cancel)

        # Add widgets to layouts
        layout.addWidget(lblTitle)
        layout.addLayout(layoutCC)
        layout.addLayout(layoutButtons)

        layoutCC.addWidget(lblCC)
        layoutCC.addWidget(self.leCC)

        layoutButtons.addWidget(btnApply)
        layoutButtons.addWidget(btnCancel)

        self.setLayout(layout)

    def applySettings(self):
        print("Applying settings...")

        # Get values from the inputs
        try:
            self.parentWindow.setting.setValue('concreteCover', float(self.leCC.text()))
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