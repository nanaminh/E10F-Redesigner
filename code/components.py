# ------------------------------------------------------
# Imports
# ------------------------------------------------------

import math

# ------------------------------------------------------
# Class/components definitions
# ------------------------------------------------------

# Simple class for the Panel component of the redesign
class Panel:
    def __init__ (self, width, height, material):
        self.width = width
        self.height = height
        self.material = material

        self.neutralAxis = height/2
        self.momentOfInertia = 1/12*width*math.pow(height, 3)
        self.area = width*height

# Create a class for the LBracket, containing all of its properties
class Stringer:
    def __init__ (self, width, thickness, material):
        self.width = width
        self.thickness = thickness
        self.material = material

        smallestRectangleMoment = 1/12*math.pow((width-thickness), 4)
        biggestRectangleMoment = 1/12*math.pow(width, 4)

        self.area = (2*width-thickness)*thickness
        self.neutralAxis = 1/self.area*(thickness/2*(math.pow(width, 2) + width*thickness - math.pow(thickness, 2)))
        self.momentOfInertia = biggestRectangleMoment - smallestRectangleMoment - math.pow((self.neutralAxis-thickness/2), 2)*(width-thickness)*thickness - math.pow((width/2-self.neutralAxis), 2)*(width-thickness)*thickness

class Design:
    def __init__ (self, panel, stringer, amountOfStringers, length):
        self.panel = panel
        self.stringer = stringer
        self.amountOfStringers = amountOfStringers
        self.length = length

        self.area = self.GetTotalArea()

    def GetTotalArea (self):
        return self.panel.area + self.amountOfStringers*self.stringer.area
    
    # Returns a boolean regarding whether the design is sufficient or not
    def IsSufficient (self, ultimateLoad, limitLoad, kC, c, minRivetSpacing):

        def IsPanelBucklingOkay ():
            sigmaCritical = kC * self.panel.material.eModulus * math.pow((self.panel.height/fStringerPitch), 2)

            if(sigmaCritical > fLimitStress):
                return True
            else:
                return None

        def IsColumnBucklingOkay ():
            fCriticalLoad = c * math.pow(math.pi, 2) * self.stringer.material.eModulus * self.stringer.momentOfInertia / math.pow(self.length, 2)
            
            if fCriticalLoad * self.amountOfStringers > ultimateLoad:
                return True
            else:
                return None

        def IsInterRivetBucklingOkay ():
            fTauInterRivet = 0.9 * kC * self.panel.material.eModulus * math.pow((self.panel.height/minRivetSpacing), 2)

            if fTauInterRivet < fUltimateStress and fTauInterRivet > fLimitStress:
                return True
            else:
                return None

        # Create some constants which the various check functions need
        fUltimateStress = ultimateLoad/self.area
        fLimitStress = limitLoad/self.area
        fStringerPitch = self.panel.width/(self.amountOfStringers-1)

        if IsPanelBucklingOkay() == True and IsColumnBucklingOkay() == True and IsInterRivetBucklingOkay() == True:
            return True

        else:
            return None

class Material:
    def __init__ (self, name, sigmaUltimate, eModulus, density):
        self.name = name
        self.sigmaUltimate = sigmaUltimate
        self.eModulus = eModulus
        self.density = density

    def ToString (self):
        return "Material name: " + self.name + "\nSigma Ultimate: " + str(self.sigmaUltimate) + "\nE Modulus: " + str(self.eModulus) + "\nDensity: " + str(self.density)