from radtrack.RbFEL import RbFEL

def test_fel():

    a = RbFEL()
    a.ui.charge.setText('300 pC')
    a.ui.slicemit.setText('1 mm*mrad')
    a.ui.ebeamenergy.setText('600 MeV')
    a.ui.energyspread.setText('0.01%')
    a.ui.bunchlen.setText('1.5 ps')
    a.ui.reprate.setText('150 kHz')
    a.ui.ufield.setText('0.9 T')
    a.ui.beta.setText('1.0 m')
    a.ui.radiatedwavelength.setText('13.5 nm')

    expectedAveragePower = '39.783 W'
    expectedSaturationLength = '12.024 m'
    expectedUndulatorPeriod = '1.7702 cm'

    assert a.ui.averagepower.text() == expectedAveragePower
    assert a.ui.uperiod.text() == expectedUndulatorPeriod
    assert a.ui.saturation.text() == expectedSaturationLength
