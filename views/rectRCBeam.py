import sys
import os.path as osp
from PyQt4 import QtGui
from PyQt4 import QtCore
from models import RectangularBeam

class RectRCBeam(QtGui.QMdiSubWindow):
    def __init__(self, parent):
        super(RectRCBeam, self).__init__(parent)
        self.parentWindow   = parent

        icon_path   = osp.join(osp.dirname(sys.modules[__name__].__file__), 'beamsection.png')
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowTitle('Rectangular')
        self.createUI()
        self.leFactoredMoment.setFocus()
        self.show()

    def createUI(self):
        # Create layout managers
        layout              = self.layout()         # Get the default layout
        layoutArea          = QtGui.QHBoxLayout()
        layoutLeftPane      = QtGui.QVBoxLayout()
        layoutSplitter      = QtGui.QSplitter(QtCore.Qt.Horizontal)

        layoutLeftPane.setSpacing(10)
        layoutInputs        = QtGui.QGridLayout()
        layoutRightPane     = QtGui.QVBoxLayout()

        # Create labels
        lblTitle            = QtGui.QLabel("<center><h2>DESIGN OF RECTANGULAR CONCRETE BEAM</h2></center>")
        lblTitle.setFixedHeight(30)
        lblInputs           = QtGui.QLabel("<br><center><h3>Inputs</h3></center>")
        lblFactoredMoment   = QtGui.QLabel("Factored Moment (kN-m)")
        lblBeamWidth        = QtGui.QLabel("Beam Width (mm)")
        lblBeamHeight       = QtGui.QLabel("Beam Effective Depth (mm)")
        lblFactoredShear    = QtGui.QLabel("Factored Shear Force (kN)")

        # Create line edits
        self.leFactoredMoment    = QtGui.QLineEdit()
        self.leFactoredMoment.returnPressed.connect(self.calculate)
        self.leFactoredMoment.setToolTip('Enter factored loading')
        self.leBeamWidth         = QtGui.QLineEdit()
        self.leBeamWidth.returnPressed.connect(self.calculate)
        self.leBeamWidth.setToolTip('Base with of the beam.')
        self.leBeamEffectiveDepth= QtGui.QLineEdit()
        self.leBeamEffectiveDepth.returnPressed.connect(self.calculate)
        self.leBeamEffectiveDepth.setToolTip('Distance from outer compression face\n '
                                             'of concrete to centroid of tension steel.')
        self.leFactoredShear    = QtGui.QLineEdit()
        self.leFactoredShear.returnPressed.connect(self.calculate)
        self.leFactoredShear.setToolTip("Factored shear force, Vu")

        # Create buttons
        btnCalculate        = QtGui.QPushButton("Calculate")
        btnCalculate.setShortcut("Ctrl+R")
        btnCalculate.setFixedWidth(100)
        btnCalculate.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))     # Set the cursor
        btnCalculate.clicked.connect(self.calculate)                            # Invoke the calculate function

        # Create the log/output window
        self.browserOutput       = QtGui.QTextBrowser()
        self.browserOutput.setMinimumWidth(400)
        self.browserOutput.setMinimumHeight(400)

        # Create frames
        frameLeftPane           = QtGui.QFrame()
        frameLeftPane.setMaximumWidth(300)
        frameLeftPane.setLayout(layoutLeftPane)
        frameRightPane          = QtGui.QFrame()
        frameRightPane.setLayout(layoutRightPane)

        # Add widgets to layout
        layout.addWidget(lblTitle)
        layout.addWidget(layoutSplitter)

        layoutLeftPane.addWidget(lblInputs)
        layoutLeftPane.addLayout(layoutInputs)
        layoutLeftPane.addSpacing(10)
        layoutLeftPane.addWidget(btnCalculate)
        layoutLeftPane.addSpacing(10)
        layoutLeftPane.addStretch()

        layoutInputs.addWidget(lblFactoredMoment, 0, 0)
        layoutInputs.addWidget(self.leFactoredMoment, 0, 1)
        layoutInputs.addWidget(lblBeamWidth, 1, 0)
        layoutInputs.addWidget(self.leBeamWidth, 1, 1)
        layoutInputs.addWidget(lblBeamHeight, 2, 0)
        layoutInputs.addWidget(self.leBeamEffectiveDepth, 2, 1)
        layoutInputs.addWidget(lblFactoredShear, 3, 0)
        layoutInputs.addWidget(self.leFactoredShear, 3, 1)

        layoutRightPane.addWidget(self.browserOutput)
        layoutRightPane.addSpacing(10)

        layoutSplitter.addWidget(frameLeftPane)
        layoutSplitter.addWidget(frameRightPane)

    def calculate(self):
        print("Start calculate...")
        # Replace empty inputs with zero
        if self.leFactoredMoment.text() == '':
            self.leFactoredMoment.setText('0')
        if self.leBeamWidth.text() == '':
            self.leBeamWidth.setText('0')
        if self.leBeamEffectiveDepth.text() == '':
            self.leBeamEffectiveDepth.setText('0')
        if self.leFactoredShear.text() == '':
            self.leFactoredShear.setText('0')

        rect        = RectangularBeam.RectangularBeam()

        # Get values from settings
        fpc         = float(self.parentWindow.setting.value('concreteCompressiveStress'))
        fy          = float(self.parentWindow.setting.value('steelYieldStrength'))
        cc          = float(self.parentWindow.setting.value('concreteCover'))
        mainBarDiam = float(self.parentWindow.setting.value('beamMainBar'))
        stirrupDiam = float(self.parentWindow.setting.value('beamStirrup'))
        phi         = float(self.parentWindow.setting.value('beamReductionFactor'))
        stirrupLegs = int(self.parentWindow.setting.value('stirrupLegs'))
        concreteWeightFactor    = float(self.parentWindow.setting.value('concreteWeightFactor'))

        # Set the material properties
        rect.setConcreteCompressiveStress(fpc)
        rect.setSteelYieldStrength(fy)
        rect.setConcreteWeightFactor(concreteWeightFactor)
        rect.setBeamReductionFactor(phi)

        # Get the values from inputs
        try:
            float(self.leFactoredMoment.text())
            rect.setFactoredMoment(float(self.leFactoredMoment.text()))
        except:
            raise ValueError
        try:
            float(self.leBeamWidth.text())
            rect.setBeamWidth(float(self.leBeamWidth.text()))
        except:
            raise ValueError
        try:
            float(self.leBeamEffectiveDepth.text())
            rect.setBeamHeight(float(self.leBeamEffectiveDepth.text()))
        except:
            raise ValueError
        try:
            float(self.leFactoredShear.text())
            rect.setFactoredShear(float(self.leFactoredShear.text()))
        except:
            raise ValueError
        rect.setConcreteCover(cc)

        rect.calculateSteelArea()               # Calculate steel area
        shearDesign   = rect.calculateShearReinforcement(float(self.leBeamWidth.text()),
                                                         float(self.leBeamEffectiveDepth.text()), stirrupDiam, stirrupLegs)
        # Generate output
        self.browserOutput.clear()
        output      = self.browserOutput
        output.append("<h2>Rectangular Beam Concrete Design</h2>")
        output.append("<b>Parameters:</b>")
        output.append("f'c\t: %0.2f %s" % (fpc,"Mpa"))
        output.append("fy\t: %0.2f %s" % (fy,"Mpa"))
        output.append("d'\t: %0.2f %s" % (cc, "mm"))

        output.append("<b>Inputs:</b>")
        output.append("Mu\t= %s kN-m" % (self.leFactoredMoment.text()))
        output.append("b\t= %0.2f %s" % (float(self.leBeamWidth.text()),"mm"))
        output.append("d\t= %0.2f %s" % (float(self.leBeamEffectiveDepth.text()), "mm"))
        output.append("Vu\t= %0.2f kN")

        output.append("<b>Start of Calculation:</b>")
        output.append("<big><u>Design for flexure:</u></big>")
        output.append("rho min\t= %0.6f" % rect.Pmin)
        output.append("B1 \t= %0.3f" % rect.B1)
        output.append("rho bal\t= %0.6f" % rect.Pbal)
        output.append("rho max\t= %0.6f" % rect.Pmax)
        output.append("w \t= %0.4f" % rect.w)
        output.append("Ru \t= %0.3f %s" % (rect.Ru, "MPa"))
        output.append("MuMax\t= %0.2f %s" % (rect.MuMax/1000000, "kN-m"))
        flexureDesign = ""
        if rect.MuMax > rect.Mu:
            output.append("MuMax > Mu")
            output.append("Design for singly reinforced beam.")
            flexureDesign = rect.singlyReinforced()
        else:
            output.append("MuMax < Mu")
            output.append("Design for doubly reinforced beam.")
            flexureDesign = rect.doublyReinforced()
        output.append(flexureDesign)

        output.append("<big><u>Design for shear</u></big>")
        output.append(shearDesign)
        output.append("<b>End of calculation</b>")

if __name__ == '__main__':
    app = QtGui.QApplication([])
    m = RectRCBeam()
    app.exec_()