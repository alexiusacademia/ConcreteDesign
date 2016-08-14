import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import os.path as osp

class LoadingFactors(QtGui.QDialog):
    def __init__(self, parent):
        super(LoadingFactors, self).__init__(parent)
        self.parentWindow = parent
        self.createUI()
        icon_path   = osp.join(osp.dirname(sys.modules[__name__].__file__), 'loadingfactorsetting.png')
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.show()

    def createUI(self):
        self.setWindowTitle("Material Properties Setting")

        # Create layout managers
        layout          = QtGui.QVBoxLayout()
        layoutDeadLoad  = QtGui.QHBoxLayout()       # Layout for dead load factor
        layoutLiveLoad  = QtGui.QHBoxLayout()       # Layout for live load factor
        layoutButtons   = QtGui.QHBoxLayout()

        # Create labels
        lblTitle        = QtGui.QLabel("<h3><b>Loading Factors</b></h3>")
        lblDeadLoad     = QtGui.QLabel("Dead Load")
        lblLiveLoad     = QtGui.QLabel("Live Load")

        # Create line edits
        self.leDeadLoadFactor   = QtGui.QLineEdit()
        self.leDeadLoadFactor.setAlignment(QtCore.Qt.AlignHCenter)
        self.leDeadLoadFactor.setText(str(self.parentWindow.setting.value('deadloadFactor')))
        self.leLiveLoadFactor   = QtGui.QLineEdit()
        self.leLiveLoadFactor.setAlignment(QtCore.Qt.AlignHCenter)
        self.leLiveLoadFactor.setText(str(self.parentWindow.setting.value('liveloadFactor')))

        #  Create push buttons
        btnApply        = QtGui.QPushButton("Apply")
        btnApply.clicked.connect(self.applySettings)
        btnCancel       = QtGui.QPushButton("Cancel")
        btnCancel.clicked.connect(self.cancel)

        # Add widgets to layouts
        layout.addWidget(lblTitle)
        layout.addLayout(layoutDeadLoad)
        layout.addLayout(layoutLiveLoad)
        layout.addLayout(layoutButtons)

        layoutDeadLoad.addWidget(lblDeadLoad)
        layoutDeadLoad.addStretch()
        layoutDeadLoad.addWidget(self.leDeadLoadFactor)

        layoutLiveLoad.addWidget(lblLiveLoad)
        layoutLiveLoad.addStretch()
        layoutLiveLoad.addWidget(self.leLiveLoadFactor)

        layoutButtons.addWidget(btnApply)
        layoutButtons.addWidget(btnCancel)

        self.setLayout(layout)

    def applySettings(self):
        print("Applying settings...")

        # Get values from the inputs
        try:
            self.parentWindow.setting.setValue('deadloadFactor', float(self.leDeadLoadFactor.text()))
            self.parentWindow.setting.setValue('liveloadFactor', float(self.leLiveLoadFactor.text()))
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