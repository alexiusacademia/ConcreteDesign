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

        layoutLeftPane.setSpacing(10)
        layoutInputs        = QtGui.QGridLayout()
        layoutRightPane     = QtGui.QVBoxLayout()

        # Create labels
        lblTitle            = QtGui.QLabel("<center><h2>DESIGN OF RECTANGULAR CONCRETE BEAM</h2></center>")
        lblInputs           = QtGui.QLabel("<br><b>Inputs</b>")
        lblFactoredMoment   = QtGui.QLabel("Factored Moment (kN-m)")
        lblBeamWidth        = QtGui.QLabel("Beam Width (mm)")
        lblBeamHeight       = QtGui.QLabel("Beam Height (mm)")

        # Create line edits
        self.leFactoredMoment    = QtGui.QLineEdit()
        self.leFactoredMoment.setToolTip('Enter factored loading')
        self.leBeamWidth         = QtGui.QLineEdit()
        self.leBeamHeight        = QtGui.QLineEdit()

        # Create buttons
        btnCalculate        = QtGui.QPushButton("Calculate")
        btnCalculate.setShortcut("Ctrl+R")
        btnCalculate.setFixedWidth(100)
        btnCalculate.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))     # Set the cursor
        btnCalculate.clicked.connect(self.calculate)                            # Invoke the calculate function

        # Create the log/output window
        self.browserOutput       = QtGui.QTextBrowser()
        self.browserOutput.setMinimumWidth(400)
        self.browserOutput.setMaximumWidth(1000)
        self.browserOutput.setMinimumHeight(400)

        # Add widgets to layout
        layout.addWidget(lblTitle)
        layout.addLayout(layoutArea)

        layoutLeftPane.addWidget(lblInputs)
        layoutLeftPane.addLayout(layoutInputs)
        layoutLeftPane.addSpacing(10)
        layoutLeftPane.addWidget(btnCalculate)
        layoutLeftPane.addSpacing(10)
        layoutLeftPane.addStretch()

        layoutArea.addSpacing(10)
        layoutArea.addLayout(layoutLeftPane)
        layoutArea.addSpacing(5)
        layoutArea.addSpacing(5)
        layoutArea.addLayout(layoutRightPane)
        layoutArea.addSpacing(10)

        layoutInputs.addWidget(lblFactoredMoment, 0, 0)
        layoutInputs.addWidget(self.leFactoredMoment, 0, 1)
        layoutInputs.addWidget(lblBeamWidth, 1, 0)
        layoutInputs.addWidget(self.leBeamWidth, 1, 1)
        layoutInputs.addWidget(lblBeamHeight, 2, 0)
        layoutInputs.addWidget(self.leBeamHeight, 2, 1)

        layoutRightPane.addWidget(self.browserOutput)
        layoutRightPane.addSpacing(10)

    def calculate(self):
        print("Start calculate...")
        rect        = RectangularBeam.RectangularBeam()

        # Get values from settings
        fpc         = float(self.parentWindow.setting.value('concreteCompressiveStress'))
        fy          = float(self.parentWindow.setting.value('steelYieldStrength'))
        cc          = float(self.parentWindow.setting.value('concreteCover'))

        # Set the material properties
        rect.setConcreteCompressiveStress(fpc)
        rect.setSteelYieldStrength(fy)

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
            float(self.leBeamHeight.text())
            rect.setBeamHeight(float(self.leBeamHeight.text()))
        except:
            raise ValueError
        rect.setConcreteCover(cc)

        rect.calculateSteelArea()               # Calculate steel area

        # Generate output
        output      = self.browserOutput
        output.append("<h2>Rectangular Beam Concrete Design</h2>")
        output.append("<b>Parameters:</b>")
        output.append("f'c\t: %0.2f %s" % (fpc,"Mpa"))
        output.append("fy\t: %0.2f %s" % (fy,"Mpa"))
        output.append("d'\t: %0.2f %s" % (cc, "mm"))

        output.append("<b>Inputs:</b>")
        output.append("Mu\t= %0.2f %s" % (rect.getMuMax()/1000000,"kN-m"))
        output.append("B\t= %0.2f %s" % (float(self.leBeamWidth.text()),"mm"))
        output.append("H\t= %0.2f %s" % (float(self.leBeamHeight.text()),"mm"))

        output.append("<b>Start of Calculation:</b>")
        output.append("rho min\t= %0.6f" % rect.Pmin)
        output.append("B1 \t= %0.3f" % rect.B1)
        output.append("rho bal\t= %0.6f" % rect.Pbal)
        output.append("rho max\t= %0.6f" % rect.Pmax)
        output.append("w \t= %0.4f" % rect.w)
        output.append("Ru \t= %0.3f %s" % (rect.Ru, "MPa"))
        output.append("MuMax\t= %0.2f %s" % (rect.MuMax/1000000, "kN-m"))
        computation = ""
        if rect.MuMax > rect.Mu:
            output.append("MuMax > Mu")
            output.append("Design for singly supported beam.")
            computation = rect.singlyReinforced()
        else:
            output.append("MuMax < Mu")
            output.append("Design for doubly supported beam.")
            computation = rect.doublyReinforced()
        output.append(computation)
        output.append("<b>End of calculation</b>")


if __name__ == '__main__':
    app = QtGui.QApplication([])
    m = RectRCBeam()
    app.exec_()