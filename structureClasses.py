# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 08:34:32 2016

@author: Alex
"""

from structureInputs import getInputs, water_density
from sympy import *
from decimal import Decimal as d
import math
from scipy.optimize import fsolve

class drilledShaft(object):
    def __init__(self, name):
        self.name = name
    def gatherInputs(self):
        inputDict = getInputs()
        self.nBlows = inputDict['nBlows']
        self.factoredShear = inputDict['factoredShear']
        self.factoredMoment = inputDict['factoredMoment']
        self.factoredTorsion = inputDict['factoredTorsion']
        self.sfOT = inputDict['sfOT']
        self.sfTor = inputDict['sfTor']
        self.shaftDiameter = inputDict['shaftDiameter']
        self.soilDensity = inputDict['soilDensity']
        self.offset = inputDict['offset']
        self.soilType = inputDict['soilType']
        self.waterLevel = inputDict['waterLevel']
        if self.soilType == "sand":
            self.soilAOF = inputDict['soilAOF']
            self.soilSS = 0
        if self.soilType == "clay":
            self.soilSS = inputDict['soilSS']
#    def addShaftEmb(self):
#        shaftConditions = [self.shaftEmbSTor, self.shaftEmbSandOT, self.shaftEmbClayOT]
#        shaftEmb = max(shaftConditions)
#        self.shaftEmb = shaftEmb
    def getFactoredShear(self):
        return self.factoredShear
    def getFactoredMoment(self):
        return self.factoredMoment
    def getFactoredTorsion(self):
        return self.factoredTorsion
    def getSoilType(self):
        return self.soilType
    def getSfOT(self):
        return self.sfOT
    def getShaftDiameter(self):
        return self.shaftDiameter
    def getShaftEmb(self):
        return self.shaftEmb
    def getSoilDensity(self):
        return self.soilDensity
    def getSoilAOF(self):
        return self.soilAOF
    def getSoilSS(self):
        return self.soilSS
    def getOffset(self):
        return self.offset
    def Kp(self):
        """Rankine's passive lateral earth pressure"""
        Kp = math.tan(math.radians(45 + (self.soilAOF / 2.0))) ** 2
        Kp = round(Kp, 1)
        if Kp < 1:
            return 1
        return Kp
    def bromsSandShort(self, debug = False):
        """short free-head pile in cohensionless soil using Brom's method.
        inputs (from class instance):
            factoredShear in kip
            factoredMoment in kip-ft
        results:
            shaft minimum embedment (shaftEmb) rounded up to whole number in ft"""
        L = Symbol('L')
        y = lambda L: (((self.soilDensity * self.shaftDiameter * L ** 3 *
                self.Kp()) / 2) - (self.factoredShear * 1000) *
                (self.offset + L) - (self.factoredMoment * 1000))
        L_exact = nsolve(y(L), 1)
#        print "shaftEmb =", shaftEmb
        L_ceil = math.ceil(L_exact)
        if debug == True:
            print "Soil Density =", self.soilDensity
            print "Shaft Diameter =", self.shaftDiameter
            print "Kp =", self.Kp()
            print "Offset =", self.offset
            print "Factored Moment (kip-lb) =", self.factoredMoment
            print "Factored Shear (kip) =", self.factoredShear
            print "L_exact (ft) =", L_exact
            print "L_ceil (ft) =", L_ceil
        self.shaftEmbSandOT = L_ceil
        return self.shaftEmbSandOT
    def bromsCandLong(self, debug = False):
        """short free-head pile in cohesive soil using Regular Broms method for
        shaftEmb > 3 * shaftDiameter.
        inputs (from class instance):
            factoredShear in kip
            factoredMoment in kip
        results:
            shaft minimum embedment (shaftEmb) rounded up to whole number in ft"""
        soilSS = self.soilSS
        factoredShear = self.factoredShear
        factoredMoment = self.factoredMoment
        if soilSS == 0:
            soilSS = 0.01 #set to minimum value to prevent use of zero
        fClay = (factoredShear / (9.0 * soilSS * self.shaftDiameter))
        eClay = ((factoredMoment / float(factoredShear)) + #moment and shear in kip-ft and kip
                self.offset)
        mMaxTemp = factoredShear * (eClay + (1.5 * self.shaftDiameter) + (0.5 * fClay))
        g = math.sqrt((mMaxTemp / (2.25 * soilSS * self.shaftDiameter)))
        L_exact = (1.5 * self.shaftDiameter + fClay + g)
        L_ceil = math.ceil(L_exact)
        if debug == True:
            print "fClay =", fClay
            print "eClay =", eClay
            print "Mmaxtemp =", mMaxTemp
            print "g =", g
            print "L(exact) =", L_exact
            print "L(ceil) =", L_ceil
        self.shaftEmbClayOT = L_ceil
        return self.shaftEmbClayOT

        """Modified Broms method for cohesive soils and short piles is broken. DO NOT USE!!!"""

#     def bromsCandShort(self):
#         """short free-head pile in cohesive soil using Modified Broms method for
#         shaftEmb < 3 * shaftDiameter.
#         inputs:
#             factoredShear in kip
#             factoredMoment in kip-ft
#         results:
#             shaft minimum embedment (shaftEmb) rounded up to whole number in ft."""
#
#         soilSS = float(self.soilSS)
#         shaftDia = float(self.shaftDiameter)
#         fM = float(self.factoredMoment)
#         fS = float(self.factoredShear)
#         oS = float(self.offset)
#         if soilSS == 0:
#             soilSS = 0.1 #set a minimum level for analysis to prevent use of zero
#         soilSlope = 8.0 * (soilSS / (3.0 * shaftDia))
#         print 'Soil Slope =', soilSlope
#         eClay = ((fM / fS) + oS)
#         print 'eClay =', eClay
#
#         N = Symbol('N')
#         M = Symbol('M')
#
#         nForce = lambda M, N: ((soilSlope * ((2.0 * M) + N)) + (2.0 * soilSS)) * (N * (shaftDia / 2.0))
#         mForce = lambda M: ((2.0 * soilSS) + (M * soilSlope)) * (M * (shaftDia / 2.0))
#         mArm = lambda M: eClay + (M / 3.0) * ((((2.0 * ((M * soilSlope) + soilSS)) + soilSS)) / ((M * soilSlope) + (2.0 * soilSS)))
#         nArm = lambda M, N: (eClay + M + ((N / 3.0) * (((2.0 * ((N * soilSlope) + (M * soilSlope) + soilSS)) +
#                             ((M * soilSlope) + soilSS)) / ((soilSlope * ((2.0 * M) + N)) + (2.0 * soilSS)))))
#
#         givenN = lambda M, N: fS + nForce(M, N) - ((nForce(M, N) * nArm(M, N)) / mArm(M))
#         givenM = lambda M, N: mForce(M) * mArm(M) - nForce(M, N) * nArm(M, N)


    def resistTorSand(self, debug = False):
        """calculate the shaft embedment required to resist torsion in cohesionless \
        soil in ft and applies sfTOR to the output.

        NOTE: loadTransfRatio and cohesionFactor are based upon concrete and soil interaction. \
        This torsion model is not meant to be used with permanent casings on the drilled shaft."""
        if self.nBlows < 15 or self.nBlows > 5:
            loadTransfRatio = 1.5 * (self.nBlows / 15)
        elif self.nBlows < 5:
            loadTransfRatio = 0
        else:
            loadTransfRatio = 1.5
        coefFriction = float(math.tan(math.radians(self.soilAOF)))
        if self.waterLevel == "above":
            concDensity = float(150 - water_density)   #only applicable for submerged conditions
        else:
            concDensity = float(150)
        L = Symbol('L')
        shaftDia = self.shaftDiameter
        soilDensity = self.soilDensity
        factoredTorsion = float(self.factoredTorsion * 1000)
        y = lambda L: (factoredTorsion - (pi * shaftDia * L * soilDensity *
                      (L / 2.0) * loadTransfRatio * (shaftDia / 2.0)) +
                      (pi * ((shaftDia / 2) ** 2) * L * concDensity *
                      (shaftDia / 3.0) * coefFriction))
        L_exact = nsolve(y(L), 3)
        L_ceil = math.ceil(L_exact)
        if debug == True:
            print "Load Transfer Ratio (wFDOT) =", loadTransfRatio
            print "Coefficient of Friction =", coefFriction
            print "Concrete Density (pcf) =", concDensity
            print "L(exact) =", L_exact
            print "L(ceil) =", L_ceil
            print "y = ", float(y(L_exact)), "<-- should = 0"
            print "Factored Torsion (lb-ft) =", factoredTorsion
        self.shaftEmbSTor = L_ceil
        return self.shaftEmbSTor

    def __str__(self):
        return self.name


###############################################################################
"""Testing and other stuff"""

struct1 = drilledShaft('one')
#struct1.gatherInputs()
struct1.soilDensity = 112
struct1.nBlows = 15
struct1.shaftDiameter = 3.50
struct1.soilAOF = 30
struct1.soilSS = 2.0
struct1.factoredShear = 150
struct1.factoredMoment = 277.7
struct1.factoredTorsion = 5
struct1.offset = 0
struct1.waterLevel = "below"
struct1.bromsSandShort(debug = True)
# struct1.bromsCandShort()
struct1.bromsCandLong(debug = True)
struct1.resistTorSand(debug = True)
#
#struct1.addShaftEmb()
#print struct1.getShaftEmb()
