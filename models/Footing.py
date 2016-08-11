#---------------------------------------------------#
#   Footing.py                                      #
#   class for design of rectangular beam concrete   #
#                                                   #
#   This class is for the design of a rectangular   #
#   reinforced concrete beam based on NSCP          #
#   (National Structural Code of the Philippines)   #
#---------------------------------------------------#

class Footing:
    def  __init__(self):
        print("Initializing variables...")
        self.soilUnitWeight = 0

    #---------------#
    #   Setters     #
    #---------------#
    def setSteelYieldStrength(self, yieldStrength):
        self.steelYieldStrength         = yieldStrength

    def setConcreteCompressiveStress(self, compressiveStress):
        self.concreteCompressiveStress  = compressiveStress

    def setSoilUnitWeight(self, soilUnitWeight):
        self.soilUnitWeight             = soilUnitWeight            # gs

    def setConcreteUnitWeight(self, concreteUnitWeight):
        self.concreteUnitWeight         = concreteUnitWeight        # gc

    def setSoilBearingCapacity(self, soilBearingCapacity):
        self.soilBearingCapacity        = soilBearingCapacity       # ga

    def setFootingDepth(self, footingDepth):
        self.footingDepth               = footingDepth              # H

    def setAxialDeadload(self, axialDeadload):
        self.axialDeadload              = axialDeadload             # PDL

    def seAxialLiveload(self, axialLiveload):
        self.axialLiveLoad              = axialLiveload             # PLL

    def setMomentDeadload(self, momentDeadload):
        self.momentDeadload             = momentDeadload            # MDL

    def setMomentLiveload(self, momentLiveload):
        self.momentLiveload             = momentLiveload            # MLL

    def setColumnWidth(self, columnWidth):
        self.columnWidth                = columnWidth               # c2

    def setColumnLength(self, columnLength):
        self.columnLength               = columnLength              # c1

    def setFootingWidth(self, footingWidth):
        self.footingWidth               = footingWidth              # b

    def setFootingEffectiveDepth(self, footingEffectiveDepth):
        self.footingEffectiveDepth      = footingEffectiveDepth     # d

    def setBarDiameter(self, barDiameter):
        self.barDiameter                = barDiameter               # Bar diam