#---------------------------------------------------#
#   RectangularBeam.py                              #
#   class for design of rectangular beam concrete   #
#                                                   #
#   This class is for the design of a rectangular   #
#   reinforced concrete beam based on NSCP          #
#   (National Structural Code of the Philippines)   #
#---------------------------------------------------#

import math

# Constants
PHI     = 0.90          # Reduction factor

class RectangularBeam:
    def __init__(self):
        # Initializers
        self.beamWidth                  = 0.0
        self.beamHeight                 = 0.0
        self.concreteCover              = 40
        self.steelTension               = 0
        self.steelCompression           = 0
        self.factoredMoment             = 0

    #-------------------#
    #       Setters     #
    #-------------------#
    def setBeamWidth(self, beamWidth):
        self.beamWidth      = beamWidth

    def setBeamHeight(self, beamHeight):
        self.beamHeight     = beamHeight

    def setSteelYieldStrength(self, yieldStrength):
        self.steelYieldStrength = yieldStrength

    def setConcreteCompressiveStress(self, compressiveStress):
        self.concreteCompressiveStress  = compressiveStress

    def setConcreteCover(self, concreteCover):
        self.concreteCover              = concreteCover

    def setFactoredMoment(self, factoredMoment):
        self.factoredMoment             = factoredMoment

    def setFactoredShear(self, factoredShear):
        self.factoredShear              = factoredShear

    def setConcreteWeightFactor(self, concreteWeightFactor):
        self.concreteWeightFactor       = concreteWeightFactor

    def setBeamReductionFactor(self, beamReductionFactor):
        self.beamReductionFactor        = beamReductionFactor

    #-------------------#
    #       Getters     #
    #-------------------#
    def getMuMax(self):
        return self.MuMax
    def getSteelCompression(self):
        return self.steelCompression
    def getSteelTension(self):
        return self.steelTension

    #-------------------#
    #       Methods     #
    #-------------------#
    def calculateSteelArea(self):
        # Set some short variables
        self.fy                     = self.steelYieldStrength
        self.fpc                    = self.concreteCompressiveStress
        b                           = self.beamWidth
        H                           = self.beamHeight
        self.Mu                     = self.factoredMoment * 1000000             # Convert to N-mm2

        # Print inputs
        print("------------------------")
        print("START OF CONCRETE DESIGN")
        print("------------------------")
        print("\nINPUTS:\n")
        print("\tfy\t= ", self.fy, " MPa")
        print("\tf'c\t= ", self.fpc, " MPa")
        print("\tb\t= ", b, " mm")
        print("\tH\t= ", H, " mm")
        print("\tMu\t= ", self.factoredMoment, " kN-m")
        print("\n---------------------")
        print("START OF CALCULATIONS")
        print("---------------------")

        # Solve for Pmin (rho minimum)
        self.Pmin           = 1.4 / self.fy
        print("rho min\t= ", round(self.Pmin, 6))

        # Solve for B1
        if self.fpc <= 30:
            self.B1         = 0.85
        else:
            self.B1         = 0.85 - (0.008 * (self.fpc - 30))
        print("B1 = ", round(self.B1, 3))

        # Solve for PBal (rho balance)
        self.Pbal           = (0.85 * self.fpc * self.B1 * 600) / (self.fy * (self.fy + 600))
        print("rho bal\t= ", round(self.Pbal, 6))

        # Solve for Mu max to determine if double reinforcement is required
        self.Pmax           = 0.75 * self.Pbal              # Get the rho max
        self.w              = self.Pmax * self.fy / self.fpc
        self.Ru             = self.fpc * self.w * (1 - (0.59 * self.w))
        self.MuMax          = PHI * self.Ru * b * (H ** 2)
        print("rho max = 0.75Pbal \t= ", round(self.Pmax, 6))
        print("w = Pmax * fy / f'c \t= ", round(self.w, 3))
        print("Ru = f'c * w * (1 - 0.59w) \t= ", round(self.Ru, 3), "MPa")
        print("MuMax = ", PHI, "* Ru * b * H^2\t= ", round(self.MuMax/1000000, 2), "kN-m")

        # Test for MuMax against Actual Mu
        if self.MuMax > self.Mu:
            # Design as singly reinforced concrete
            print("MuMax > Mu")
            print("Design as singly reinforced concrete.")
            self.singlyReinforced()
        else:
            # Design as doubly reinforced concrete
            print("MuMax < Mu")
            print("Design as doubly reinforced concrete.")
            self.doublyReinforced()

    def singlyReinforced(self):
        print("\n---------------------------------")
        print("START OF SINGLY REINFORCED DESIGN")
        print("---------------------------------")
        Ru              = self.factoredMoment * 1000000 / (PHI * self.beamWidth * self.beamHeight**2)
        P               = 0.85 * self.fpc / self.fy * (1 - (1 - (2 * Ru / (0.85 * self.fpc)))**0.5)         # rho
        As              = P * self.beamWidth * self.beamHeight
        print("Ru\t= ", round(Ru, 3), "MPa")
        print("rho\t= ", round(P, 6))
        print("As\t= ", round(As, 2), "sq.mm")
        self.steelTension   = As

        strOutput = "Ru\t= %0.3f %s \n" % (Ru, "MPa")
        strOutput += "rho\t= %0.6f \n" % P
        strOutput += "As\t= %0.2f sq.mm." % As

        return strOutput

    def doublyReinforced(self):
        print("\n---------------------------------")
        print("START OF DOUBLY REINFORCED DESIGN")
        print("---------------------------------")
        Mu1             = self.MuMax
        As1             = self.Pmax * self.beamWidth * self.beamHeight
        Mu2             = self.factoredMoment * 1000000 - Mu1
        As2             = Mu2 / (PHI * self.fy * (self.beamHeight - self.concreteCover))        # Compression Steel
        As              = As1 + As2                                                             # Tension steel
        print("Mu1\t= ", round(Mu1, 2), "N-mm2")
        print("As1\t= ", round(As1, 2), "sq.mm")
        print("Mu2\t= ", round(Mu2, 2), "N-mm2")
        print("As2\t= ", round(As2, 2), "sq.mm. (Compression steel)")
        print("As = As1 + As2 \t= ", round(As, 2), "sq.mm. (Tension steel)")
        self.steelTension       = As
        self.steelCompression   = As2

        strOutput = "Mu1\t= %0.3f %s \n" % (Mu1/1000000, "kN-m")
        strOutput += "As1\t= %0.2f sq.mm. \n" % As1
        strOutput += "Mu2\t= %0.3f kN-m\n" % (Mu2/1000000)
        strOutput += "As2\t= %0.2f sq.mm. (Compression steel) \n" % As2
        strOutput += "As = As1 + As2\t= %0.2f sq.mm. (Tension steel)" % As

        return strOutput

    def calculateShearReinforcement(self, base, depth, barDiam, legs):
        """
        :param factoredShear:
        :param base:
        :param depth:
        :param barDiam:
        :param legs:
        :return:
        """

        fpc                 = self.concreteCompressiveStress
        fy                  = self.steelYieldStrength
        Y                   = self.concreteWeightFactor
        phi                 = self.beamReductionFactor
        strOutput           = ''

        strOutput += 'Calculate shear strength provided by concrete:\n'
        strOutput += ''

        """ Area of stirrup """
        self.Av     = math.pi / 4 * math.pow(barDiam, 2) * legs

        self.Vu             = self.factoredShear * 1000                          # Factored shear force, Vu
        self.Vc             = 0.17 * Y * math.sqrt(fpc) * base * depth      # Concrete shear strength, Vc
        strOutput += 'Vc\t= ' + str(round((self.Vc/1000),2)) + ' kN\n'

        # Test if shear reinforcement is required
        if self.Vu > (phi * self.Vc):
            # Stirrups are necessary
            self.Vn         = self.Vu / phi
            self.Vs         = self.Vn - self.Vc

            strOutput += 'phi\t= ' + str(phi) + '\n'
            strOutput += 'Vu > ' + str(phi) + 'Vc\n'
            strOutput += 'Av\t= ' + str(round(self.Av, 2)) + '\n'

            if self.Vs <= (0.66 * math.sqrt(fpc) * base * depth):

                A           = 0.33 * math.sqrt(fpc) * base * depth

                # Calculate spacing of stirrups
                self.S      = self.Av * fy * depth / self.Vs
                strOutput += 'Spacing\t= Av . fy . d / Vs\n'
                strOutput += 'Spacing\t= ' + str(round(self.S, 2)) + '\n'

                # Calculate maximum spacing
                if self.Vs <= A:
                    if (depth/2) > 600:
                        self.maxSpacing = 600
                    else:
                        self.maxSpacing = depth/2
                else:
                    if (depth/4) > 300:
                        self.maxSpacing = 300
                    else:
                        self.maxSpacing = depth/4
                strOutput += 'Smax\t= ' + str(round(self.maxSpacing, 2)) + ' mm\n'

                if self.S > self.maxSpacing:
                    self.S = self.maxSpacing

                strOutput += 'Adopt Spacing = ' + str(math.floor(self.S))


            else:
                # Adjust the size of the beam
                print("Beam section needs to be adjusted.")
                return 'Beam section needs to be adjusted!'

        else:
            if self.Vu > (0.5 * phi * self.Vc):
                # Minimum area of stirrup
                strOutput += 'Vu > 1/2 . phi . Vc\n'
                strOutput += '\tProvide minimum reinforcement based on Av(min)'
                s1  = self.Av * fy / (0.062 * math.sqrt(fpc) * base)
                s2  = self.Av * fy / (0.35 * base)
                s3  = depth/2

                if s1 < s2:
                    if s1 < s3:
                        self.S = s1
                    else:
                        self.S = s3
                else:
                    if s2 < s3:
                        self.S = s2
                    else:
                        self.S = s3

                strOutput += 'Use spacing\t= ' + str(math.floor(self.S)) + ' mm'
            else:
                return "Stirrups are not required."

        return strOutput