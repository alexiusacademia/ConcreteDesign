import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import os.path as osp

class MaterialSettings(QtGui.QDialog):
    def __init__(self, parent):
        super(MaterialSettings, self).__init__(parent)
        self.parentWindow = parent
        self.createUI()
        icon_path   = osp.join(osp.dirname(sys.modules[__name__].__file__), 'materialproperties.png')
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.show()

    def createUI(self):
        self.setWindowTitle("Material Properties Setting")

        # Create layout managers
        layout                      = QtGui.QVBoxLayout()
        layoutFPC                   = QtGui.QHBoxLayout()
        layoutFy                    = QtGui.QHBoxLayout()
        layoutConcreteWeightType    = QtGui.QHBoxLayout()
        layoutConcreteWeight        = QtGui.QHBoxLayout()
        layoutBeamReductionFactor   = QtGui.QHBoxLayout()
        layoutButtons               = QtGui.QHBoxLayout()

        # Create labels
        lblTitle                = QtGui.QLabel("<h3><b>Material Properties</b></h3>")
        lblFPC                  = QtGui.QLabel("f'c (MPa)")
        lblFy                   = QtGui.QLabel("fy (MPa)")
        lblConcreteWeightType   = QtGui.QLabel("Concrete weight type")
        lblConcreteWeight       = QtGui.QLabel("Concrete Weight (kN/cu.m.)")
        lblBeamReductionFactor  = QtGui.QLabel("Beam reduction factor")

        # Create line edits
        self.leFPC                  = QtGui.QLineEdit()
        self.leFPC.setAlignment(QtCore.Qt.AlignHCenter)
        self.leFPC.setText(str(self.parentWindow.setting.value('concreteCompressiveStress')))

        self.leFy                   = QtGui.QLineEdit()
        self.leFy.setAlignment(QtCore.Qt.AlignHCenter)
        self.leFy.setText(str(self.parentWindow.setting.value('steelYieldStrength')))

        self.leConcreteWeight       = QtGui.QLineEdit()
        self.leConcreteWeight.setAlignment(QtCore.Qt.AlignHCenter)
        self.leConcreteWeight.setText(str(self.parentWindow.setting.value('concreteWeight')))

        self.cbConcreteWeightType   = QtGui.QComboBox()
        self.cbConcreteWeightType.addItems(['Lightweight', 'Sand-lighweight', 'Normal weight'])
        self.cbConcreteWeightType.setCurrentIndex(self.getConcreteWeightType(self.parentWindow.setting.value('concreteWeightFactor')))

        self.leBeamReductionFactor  = QtGui.QLineEdit()
        self.leBeamReductionFactor.setAlignment(QtCore.Qt.AlignHCenter)
        self.leBeamReductionFactor.setText(str(self.parentWindow.setting.value('beamReductionFactor')))
        self.leBeamReductionFactor.setToolTip('NSCP 2001: 0.85\nNSCP 2010: 0.75')

        #  Create push buttons
        btnApply        = QtGui.QPushButton("Apply")
        btnApply.clicked.connect(self.applySettings)
        btnCancel       = QtGui.QPushButton("Cancel")
        btnCancel.clicked.connect(self.cancel)

        # Add widgets to layouts
        layout.addWidget(lblTitle)
        layout.addLayout(layoutFPC)
        layout.addLayout(layoutFy)
        layout.addLayout(layoutConcreteWeightType)
        layout.addLayout(layoutConcreteWeight)
        layout.addLayout(layoutBeamReductionFactor)
        layout.addSpacing(10)
        layout.addLayout(layoutButtons)

        layoutFPC.addWidget(lblFPC)
        layoutFPC.addStretch()
        layoutFPC.addWidget(self.leFPC)

        layoutFy.addWidget(lblFy)
        layoutFy.addStretch()
        layoutFy.addWidget(self.leFy)

        layoutConcreteWeightType.addWidget(lblConcreteWeightType)
        layoutConcreteWeightType.addStretch()
        layoutConcreteWeightType.addWidget(self.cbConcreteWeightType)

        layoutConcreteWeight.addWidget(lblConcreteWeight)
        layoutConcreteWeight.addStretch()
        layoutConcreteWeight.addWidget(self.leConcreteWeight)

        layoutBeamReductionFactor.addWidget(lblBeamReductionFactor)
        layoutBeamReductionFactor.addStretch()
        layoutBeamReductionFactor.addWidget(self.leBeamReductionFactor)

        layoutButtons.addStretch()
        layoutButtons.addWidget(btnApply)
        layoutButtons.addWidget(btnCancel)

        self.setLayout(layout)

    def getConcreteWeightFactor(self):
        type    = self.cbConcreteWeightType.currentText()
        if type == 'Lightweight':
            return 0.75
        elif type == 'Sand-lighweight':
            return 0.85
        else:
            return 1.0

    def getConcreteWeightType(self, weightFactor):
        wf  = float(weightFactor)
        if wf == 0.75:
            return 0
        elif wf == 0.85:
            return 1
        else:
            return 2

    def applySettings(self):
        print("Applying settings...")
        # Get values from the inputs
        try:
            self.parentWindow.setting.setValue('concreteCompressiveStress', float(self.leFPC.text()))
            self.parentWindow.setting.setValue('steelYieldStrength', float(self.leFy.text()))
            self.parentWindow.setting.setValue('concreteWeight', float(self.leConcreteWeight.text()))
            self.parentWindow.setting.setValue('concreteWeightFactor', self.getConcreteWeightFactor())
            self.parentWindow.setting.setValue('beamReductionFactor', self.leBeamReductionFactor.text())
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