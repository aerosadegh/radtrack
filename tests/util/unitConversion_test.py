from radtrack.util.unitConversion import convertUnitsString, \
                                         convertUnitsStringToNumber, \
                                         convertUnitsNumberToString, \
                                         convertUnitsNumber
from radtrack.util.RbMath import roundSigFig
from math import pi
import pytest

def test_unit_conversion():
    # Simple test
    a = '12 in'
    ac = convertUnitsString(a, 'km')
    b = '1 ft'
    bc = convertUnitsString(b, 'km')
    assert ac == bc

    # Compound test
    a = '60 mi/hr'
    ac = roundSigFig(convertUnitsStringToNumber(a, 'm/s'), 10)
    b = '88 ft/sec'
    bc = roundSigFig(convertUnitsStringToNumber(b, 'm/s'), 10)
    assert ac == bc

    # Invalid test
    a = '4 score'
    with pytest.raises(ValueError):
        convertUnitsString(a, 'years')

    # Higher dimension test
    a = 16.7 # km^2, 
    ac = convertUnitsNumberToString(a, 'km^2', 'mi^2')
    b = '6.44790604766 mi^2'
    bc = convertUnitsString(b, 'mi^2')
    assert ac == bc

    # Angle test
    a = 3 # radians
    ac = roundSigFig(convertUnitsNumber(a, 'rad', 'deg'), 10)
    b = 3*180/pi # 3 rad in degrees
    bc = roundSigFig(b, 10)
    assert ac == bc

    # Compound units
    a = "9.8 m/s^2"
    ac = roundSigFig(convertUnitsStringToNumber(a, "ft/ms^2"), 6)
    b = 3.21522e-5 # ft / (ms^2)
    assert ac == b

    # Inverse units
    a = "10 1/s"
    ac = convertUnitsString(a, 'Hz')
    b = "10.0 Hz"
    assert ac == b

    a = "1 1/ns"
    ac = convertUnitsString(a, 'GHz')
    b = "1.0 GHz"
    assert ac == b
