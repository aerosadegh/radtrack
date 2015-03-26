print 'Unit Conversion Test ...'

from RbUtility import convertUnitsString, \
                      convertUnitsStringToNumber, \
                      convertUnitsNumberToString, \
                      convertUnitsNumber, \
                      roundSigFig
from math import pi

# Simple test
a = '12 in'
ac = convertUnitsString(a, 'km')
b = '1 ft'
bc = convertUnitsString(b, 'km')
if ac != bc:
    print a, ac
    print b, bc
    raise Exception

# Compound test
a = '60 mi/hr'
ac = roundSigFig(convertUnitsStringToNumber(a, 'm/s'), 10)
b = '88 ft/sec'
bc = roundSigFig(convertUnitsStringToNumber(b, 'm/s'), 10)
if ac != bc:
    print a, ac
    print b, bc
    raise Exception

# Invalid test
a = '4 score'
try:
    ac = convertUnitsString(a, 'years')
except ValueError:
    pass
else:
    print a, ac
    raise Exception

# Higher dimension test
a = 16.7 # km^2, 
ac = convertUnitsNumberToString(a, 'km^2', 'mi^2')
b = '6.44790604765 mi^2'
bc = convertUnitsString(b, 'mi^2')
if ac != bc:
    print a, ac
    print b, bc
    raise Exception

# Angle test
a = 3 # radians
ac = roundSigFig(convertUnitsNumber(a, 'rad', 'deg'), 10)
b = 3*180/pi # 3 rad in degrees
bc = roundSigFig(b, 10)
if ac != bc:
    print a, ac
    print b, bc
    raise Exception


# Compound units
a = "9.8 m/s^2"
ac = roundSigFig(convertUnitsStringToNumber(a, "ft/ms^2"), 6)
b = 3.21522e-5 # ft / (ms^2)

if ac != b:
    print a, ac
    print b
    raise Exception

print 'Passed.'
