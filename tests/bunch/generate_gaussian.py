from __future__ import absolute_import, division, print_function, unicode_literals
import radtrack.BunchTab

def generate_gaussian():
    inputDict = dict()
    inputDict['charge'] = 300e-12
    inputDict['slicemit'] = 1e-6
    inputDict['ebeamenergy'] = 600e6
    inputDict['energyspread'] = 0.0001
    inputDict['peakamp'] = 200
    inputDict['bunchlen'] = 1.5e-12
    inputDict['reprate'] = 150e3
    inputDict['ufield'] = 0.9
    inputDict['beta'] = 1.0
    inputDict['radiatedwavelength'] = 13.5e-9

    resultDict = calculate(inputDict)

    my_bunch = BunchTab(Null)

    expectedAveragePower = 39.783 # W
    expectedSaturationLength = 12.024 # m
    expectedUndulatorPeriod = 0.017702 # m

    assert roundSigFig(resultDict['averagePower'], 5) == expectedAveragePower
    assert roundSigFig(resultDict['undulatorPeriod'], 5) == expectedUndulatorPeriod
    assert roundSigFig(resultDict['saturationLength'], 5) == expectedSaturationLength
