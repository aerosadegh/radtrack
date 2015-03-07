print 'FEL Calculations Test ...'
try:
    from RbFEL import RbFEL

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

    expectedAveragePower = '39.79 W'
    expectedSaturationLength = '12.02 m'
    expectedUndulatorPeriod = '1.77 cm'
    failed = False
    if a.ui.averagepower.text() != expectedAveragePower:
        print 'Average Power Calculated:', a.ui.averagepower.text(), 'Expected:', expectedAveragePower
        failed = True
    if a.ui.uperiod.text() != expectedUndulatorPeriod:
        print 'Undulator Period Calculated:', a.ui.uperiod.text(), 'Expected:', expectedUndulatorPeriod
        failed = True
    if a.ui.saturation.text() != expectedSaturationLength:
        print 'Saturation Length Calculated:', a.ui.saturation.text(), 'Expected:', expectedSaturationLength
        failed = True
    if failed:
        raise Exception()
except Exception as e:
    print e
    raise
print 'Passed.'
