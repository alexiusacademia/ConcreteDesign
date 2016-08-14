import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import os.path as osp

class GeometrySetting(QtGui.QDialog):
    def __init__(self, parent):
        super(GeometrySetting, self).__init__(parent)
        self.parentWindow = parent
        self.createUI()
        icon_path   = osp.join(osp.dirname(sys.modules[__name__].__file__), 'geometrysetting.png')
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.show()

    def createUI(self):
        self.setWindowTitle("Geometry Setting")

        # Create layout managers
        layout              = QtGui.QVBoxLayout()
        layoutCC            = QtGui.QHBoxLayout()       # Layout for concrete cover entry
        layoutBeamMainBar   = QtGui.QHBoxLayout()
        layoutBeamStirrup   = QtGui.QHBoxLayout()
        layoutStirrupLegs   = QtGui.QHBoxLayout()
        layoutButtons       = QtGui.QHBoxLayout()

        # Create labels
        lblTitle            = QtGui.QLabel("<h3><b>Geometry Properties</b></h3>")
        lblCC               = QtGui.QLabel("Concrete Cover (mm)")
        lblBeamMainBar      = QtGui.QLabel("Beam main bar dia. (mm)")
        lblBeamStirrup      = QtGui.QLabel("Beam stirrup dia. (mm)")
        lblStirrupLegs      = QtGui.QLabel("Number of stirrup legs")

        # Create line edits
        self.leCC               = QtGui.QLineEdit()
        self.leCC.setAlignment(QtCore.Qt.AlignHCenter)
        self.leCC.setText(str(self.parentWindow.setting.value('concreteCover')))
        self.leBeamMainBar      = QtGui.QLineEdit()
        self.leBeamMainBar.setAlignment(QtCore.Qt.AlignHCenter)
        self.leBeamMainBar.setText(str(self.parentWindow.setting.value('beamMainBar')))
        self.leBeamStirrup      = QtGui.QLineEdit()
        self.leBeamStirrup.setAlignment(QtCore.Qt.AlignHCenter)
        self.leBeamStirrup.setText(str(self.parentWindow.setting.value('beamStirrup')))
        self.leStirrupLegs      = QtGui.QLineEdit()
        self.leStirrupLegs.setAlignment(QtCore.Qt.AlignHCenter)
        self.leStirrupLegs.setText(str(self.parentWindow.setting.value('stirrupLegs')))

        #  Create push buttons
        btnApply            = QtGui.QPushButton("Apply")
        btnApply.clicked.connect(self.applySettings)
        btnCancel           = QtGui.QPushButton("Cancel")
        btnCancel.clicked.connect(self.cancel)

        # Add widgets to layouts
        layout.addWidget(lblTitle)
        layout.addLayout(layoutCC)
        layout.addLayout(layoutBeamMainBar)
        layout.addLayout(layoutBeamStirrup)
        layout.addLayout(layoutStirrupLegs)
        layout.addLayout(layoutButtons)

        layoutCC.addWidget(lblCC)
        layoutCC.addStretch()
        layoutCC.addWidget(self.leCC)

        layoutBeamMainBar.addWidget(lblBeamMainBar)
        layoutBeamMainBar.addStretch()
        layoutBeamMainBar.addWidget(self.leBeamMainBar)

        layoutBeamStirrup.addWidget(lblBeamStirrup)
        layoutBeamStirrup.addStretch()
        layoutBeamStirrup.addWidget(self.leBeamStirrup)

        layoutStirrupLegs.addWidget(lblStirrupLegs)
        layoutStirrupLegs.addStretch()
        layoutStirrupLegs.addWidget(self.leStirrupLegs)

        layoutButtons.addStretch()
        layoutButtons.addWidget(btnApply)
        layoutButtons.addWidget(btnCancel)

        self.setLayout(layout)

    def applySettings(self):
        print("Applying settings...")

        # Get values from the inputs
        try:
            self.parentWindow.setting.setValue('concreteCover', float(self.leCC.text()))
            self.parentWindow.setting.setValue('beamMainBar', float(self.leBeamMainBar.text()))
            self.parentWindow.setting.setValue('beamStirrup', float(self.leBeamStirrup.text()))
            self.parentWindow.setting.setValue('stirrupLegs', int(self.leStirrupLegs.text()))
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