#---------------------------------------------------#
#   Footing.py                                      #
#   class for design of rectangular beam concrete   #
#                                                   #
#   This class is for the design of a rectangular   #
#   reinforced concrete beam based on NSCP          #
#   (National Structural Code of the Philippines)   #
#---------------------------------------------------#

import math

class Footing:
    def  __init__(self):
        print("Initializing variables...")
        try:
            print(self.footingClearConcreteCover)
        except:
            self.footingClearConcreteCover = 75

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
        """ Depth down to bottom of footing. """
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
        self.footingWidth               = footingWidth              # b in meters
    def setFootingEffectiveDepth(self, footingEffectiveDepth):
        self.footingEffectiveDepth      = footingEffectiveDepth     # d
    def setBarDiameter(self, barDiameter):
        self.barDiameter                = barDiameter               # Bar diam
    def setDeadloadFactor(self, deadloadFactor):
        self.deadloadFactor             = deadloadFactor
    def setLiveloadFactor(self, liveloadFactor):
        self.liveloadFactor             = liveloadFactor

    #-------------------#
    #       Methods     #
    #-------------------#
    def calculate(self):
        #---------------------------------------#
        #   Solve for required footing length   #
        #---------------------------------------#
        """ P - Unfactored axial loading """
        self.P          = self.axialDeadload + self.axialLiveLoad
        """ M - Unfactored moment in kN-m"""
        self.M          = self.momentDeadload + self.momentLiveload
        """ e - eccentricity """
        self.e          = self.M / self.P
        """ hc - total thickness of footing in meters """
        self.hc         = (self.footingEffectiveDepth +
                           1.5 * self.barDiameter + self.footingClearConcreteCover)/1000
        """ hs - height of overburden soil """
        self.hs         = self.footingDepth - self.hc
        """ qe - effective allowable pressure in kPa """
        self.qe         = self.soilBearingCapacity - self.concreteUnitWeight*self.hc - self.soilUnitWeight*self.hs

        A                   = self.qe
        B                   = self.P / self.footingWidth * -1
        C                   = 6 * self.e * self.P / self.footingWidth * -1
        L                   = (-1 * B + math.sqrt(math.pow(B, 2) - 4 * A * C))/(2 * A)
        self.footingLength  = math.ceil(L)          # Length of footing in meters
        q2                  = self.P / (self.footingWidth * self.footingLength) \
                              - (6 * self.P * self.e) / \
                                (self.footingWidth * pow(self.footingLength, 2))

        self.Pu             = self.deadloadFactor * self.axialDeadload + \
                              self.liveloadFactor * self.axialLiveLoad          # Factored axial
        self.Mu             = self.deadloadFactor * self.momentDeadload + \
                              self.liveloadFactor * self.momentLiveload         # Factored moment
        #self.eu             =