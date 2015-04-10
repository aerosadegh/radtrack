from math import pi, sqrt, asin, sin, acos, cos, log10, floor
import string

# How to use:
#
# convertUnitsNumber(5, "km", "m") returns 5000
# convertUnitsString("5 km", "m") returns "5000 m"
# convertUnitsNumberToString(5, "km", "m") returns "5000 m"
# convertUnitsStringToNumber("5 km", "m") returns 5000
# displayWithUnitsNumber(5000, "m") returns "5 km"
# displayWithUnitsString("5000 m") returns "5 km"
#
# Leaving the new unit argument blank in the
# convertUnits*() functions converts to the
# unit which has unitConversion[unit] = 1
# (usually corresponding to the SI base unit)
#
# The above functions should be used instead of parseUnits
# or the unitConversion dictionary
#
# parseUnits("5 km") returns "5000"


def parseUnits(inputString):
    try:
        number, unit = separateNumberUnit(inputString)
        if unit == '':
            # no unit specified, return original string to not
            # lose precision in converting to and from float
            return inputString
    except ValueError:
        return inputString # number is not a number

    # Attempt parsing of compound unit (e.g., 'm/s^2')
    convertValue = 1.0
    currentUnit = ''
    multiply = True
    try:
        for char in (unit + '*'): # add extra '*' to process last unit
            if char in ['/', '*']:
                if '^' in currentUnit:
                    currentUnit, exponent = currentUnit.split('^')
                    exponent = float(exponent)
                else:
                    exponent = 1.0
                exponent = exponent if multiply else -exponent
                convertValue = convertValue*(unitConversion[currentUnit]**exponent)
                multiply = (char == '*')
                currentUnit = ''
            else:
                currentUnit = currentUnit + char
    except KeyError:
        return inputString # unit is not valid

    return str(number*convertValue)

def separateNumberUnit(inputString):
    # How this works: after stripping all whitespace, the functions looks for
    # the largest continuous block of characters starting from the left that
    # can be converted to a float.  The rest (if any) are assumed to specify
    # the units.
    parse = removeWhitespace(inputString)

    for numLength in range(len(parse),-1,-1):
        try:
            number = float(parse[:numLength])
        except ValueError:
            pass
        else:
            break
    unit = parse[numLength:]

    try:
        return number, unit
    except UnboundLocalError:
        return float(inputString), ''


def convertUnitsNumber(number, oldUnit, newUnit):
    oldUnit = removeWhitespace(oldUnit)
    newUnit = removeWhitespace(newUnit)

    if '' in [oldUnit, newUnit] and '%' not in [oldUnit, newUnit]:
        return number # values without units don't get converted

    try:
        return number*float(parseUnits('1' + oldUnit))/float(parseUnits('1' + newUnit))
    except ValueError: # float(...) failed
        raise ValueError('Cannot convert "' + oldUnit + '" to "' + newUnit + '".')

def convertUnitsString(inputString, newUnit):
    number, unit = separateNumberUnit(inputString)
    return convertUnitsNumberToString(number, unit, newUnit)

def convertUnitsNumberToString(number, oldUnit, newUnit):
    return str(convertUnitsNumber(number, oldUnit, newUnit)) + ' ' + removeWhitespace(newUnit)

def convertUnitsStringToNumber(inputString, newUnit):
    value, unit = separateNumberUnit(inputString)
    return convertUnitsNumber(value, unit, newUnit)

# This function converts a value to units that result in the
# smallest number larger than one.
def displayWithUnitsNumber(value, currentUnit):
    if currentUnit is None:
        return str(value)
    if value == 0:
        return str(value) + ' ' + currentUnit

    # Separate compound units
    # 'ft/sec' -> 'ft' '/sec'
    restUnit = ''
    for symbol in ['/', '*']:
        i = currentUnit.find(symbol)
        if i > -1:
            currentUnit, restUnit = currentUnit[:i], currentUnit[i:] + restUnit

    # Convert only first part of compound unit
    if '^' in currentUnit:
        baseUnit, exponent = currentUnit.split('^')
    else:
        baseUnit, exponent = currentUnit, None
    extra = '' if exponent is None else ('^' + exponent)
    try:
        group = unitTable[baseUnit]
        if '-' in extra: # negative exponent
            group = reversed(group)
        for unit in [u + extra for u in group]:
            newValue = convertUnitsNumber(value, currentUnit, unit)
            if newValue >= 1:
                break
        return str(newValue) + ' ' + unit + restUnit
    except KeyError:
        return str(value) + ' ' + currentUnit

def displayWithUnitsString(inputString):
    value, unit = separateNumberUnit(inputString)
    return displayWithUnitsNumber(value, unit)

# Unit Conversions
unitConversion = dict()
unitConversion[''] = 1
unitTable = dict()
prefixes = ['P', 'T', 'G', 'M', 'k', '', 'm', 'u', 'n', 'p', 'f', 'a']
firstMultiplier = 1.0e15 # value of first unit prefix in prefixes
def addMetricUnit(unit, first = prefixes[0], last = prefixes[-1], addRow = True):
    multiplier = firstMultiplier
    row = []
    add = False
    for prefix in prefixes:
        if prefix == first:
            add = True
        if add:
            unitConversion[prefix + unit] = multiplier
            row.append(prefix + unit)
        if prefix == last:
            break

        multiplier = multiplier/1000

    if addRow:
        addToUnitTable(row)

def addToUnitConversion(unit, value, otherUnit):
    unitConversion[unit] = value*unitConversion[otherUnit]

def addToUnitTable(row):
    for unit in row:
        unitTable[unit] = row

#percent -> fraction
addToUnitConversion('%', .01, '')
addToUnitTable(['%'])

#length units -> meters
addMetricUnit('m', 'k', 'f', False)
addToUnitConversion('cm', .01, 'm')
addToUnitConversion('micron', 1, 'um')
addToUnitConversion('ang', .1, 'nm')
addToUnitConversion('in', 2.54, 'cm')
addToUnitConversion('mil', .001, 'in')
addToUnitConversion('thou', 1, 'mil')
addToUnitConversion('ft', 12, 'in')
addToUnitConversion('yd', 3, 'ft')
addToUnitConversion('mi', 5280, 'ft')
addToUnitTable(['km', 'm', 'cm', 'mm', 'um', 'nm', 'pm', 'fm'])
addToUnitTable(['mi', 'yd', 'ft', 'in', 'mil'])

#angle units -> rad
addMetricUnit('rad', '')
addToUnitConversion('deg', pi/180, 'rad')

#temporal frequency -> Hz
addMetricUnit('Hz')

#time -> seconds
addMetricUnit('s', '', 'f', False)
addMetricUnit('sec', '', 'f', False)
addToUnitConversion('min', 60, 'sec')
addToUnitConversion('hr', 60, 'min')
addToUnitTable(['hr', 'min', 's', 'ms', 'us', 'ns', 'ps', 'fs'])

#energy units -> eV
addMetricUnit('eV')

#charge units -> C
addMetricUnit('C')

#magnet units -> T
addMetricUnit('T')
addToUnitConversion('G', .0001, 'T')
addToUnitConversion('mG', .001, 'G')

#current -> A
addMetricUnit('A')

#energy -> J
addMetricUnit('J')

#power -> W
addMetricUnit('W')


# Round number x to sig significant figures
def roundSigFig(x, sig):
    try:
        # find a, b such that x = a*10^b (1 <= a < 10)
        b = floor(log10(abs(x)))
        a = x/(10**b)
        return round(a, sig-1)*(10**b)
    except ValueError:
        return 0


rpnOp = dict()
rpnOp['+'] = lambda stack : stack.pop(-2)+stack.pop(-1)
rpnOp['-'] = lambda stack : stack.pop(-2)-stack.pop(-1)
rpnOp['*'] = lambda stack : stack.pop(-2)*stack.pop(-1)
rpnOp['/'] = lambda stack : stack.pop(-2)/stack.pop(-1)
rpnOp['='] = lambda stack : stack[-1]
rpnOp['sqr'] = lambda stack : stack.pop(-1)**2
rpnOp['sqrt'] = lambda stack : sqrt(stack.pop(-1))
rpnOp['pow'] = lambda stack : stack.pop(-2)**stack.pop(-1)
rpnOp['pi'] = lambda stack : pi
rpnOp['mev'] = lambda stack : 0.51099906 # electron mass in MeV
def betap(x):
    return x/sqrt(1+(x**2))
rpnOp['beta.p'] = lambda stack : betap(stack.pop(-1))
rpnOp['c_mks'] = lambda stack : 299792458 # speed of light in mks
rpnOp['dasin'] = lambda stack : (180.0/pi)*asin(stack.pop(-1))
rpnOp['asin'] = lambda stack : asin(stack.pop(-1))
rpnOp['sin'] = lambda stack : sin(stack.pop(-1))
rpnOp['dsin'] = lambda stack : sin((pi/180)*stack.pop(-1))
rpnOp['dacos'] = lambda stack : (180.0/pi)*acos(stack.pop(-1))
rpnOp['acos'] = lambda stack : acos(stack.pop(-1))
rpnOp['cos'] = lambda stack : cos(stack.pop(-1))
rpnOp['dcos'] = lambda stack : cos((pi/180)*stack.pop(-1))
rpnOp['datan'] = lambda stack : (180.0/pi)*atan(stack.pop(-1))
rpnOp['atan'] = lambda stack : atan(stack.pop(-1))
rpnOp['tan'] = lambda stack : tan(stack.pop(-1))
rpnOp['dtan'] = lambda stack : tan((pi/180)*stack.pop(-1))
def rpn(expression):
    valueStack = []
    for token in expression.strip('"').split():
        try:
            valueStack.append(float(token))
        except ValueError: # token is not a number
            try:
                valueStack.append(rpnOp[token](valueStack))
            except (KeyError, IndexError):
                # named function not defined in rpnOp or valueStack is empty
                raise ValueError('Token: "' + token + '" in "' + expression + '" is not a valid RPN expression.')
    if len(valueStack) == 1:
        return valueStack[0]
    else:
        raise ValueError('"' + expression + '" is not a valid RPN expression.')



# Divides a string into lines of maximum width 'lineWidth'. 'endLine' specifies
# a string to be appended to any wrapped lines if a continuation character is
# needed. The variable 'indenting' specifies a number of spaces to indent the
# wrapped lines.
def wordwrap(line, lineWidth, endLine = '', indenting = 0):
    if indenting > lineWidth/2:
        indenting = lineWidth/2
    line = line.replace('\n',' ') # get rid of any existing newlines
    lineBegin = 0 # location of last line break
    newLine = endLine + '\n'
    indent = ' '*indenting

    # word wrap: maximum line length is lineWidth
    while lineBegin + lineWidth < len(line):
        # location of editing cursor
        lineEdit = lineBegin + lineWidth - len(endLine)
        while line[lineEdit] not in string.whitespace and lineEdit > lineBegin:
            lineEdit += -1 # backup up until whitespace is found
        if lineEdit == lineBegin:
            # whitespace not found, skip ahead to next whitespace or end of line
            while line[lineEdit] not in string.whitespace and lineEdit < len(line):
                lineEdit += 1
            if lineEdit == len(line):
                return line
        line = line[:lineEdit] + newLine + indent + line[lineEdit:].strip()
        lineBegin = lineEdit + len(newLine)

    return line



def stripComments(line, commentCharacter):
    insideQuote = False
    for i in range(len(line)):
        if line[i] == commentCharacter and not insideQuote:
            return line[:i].strip()
        if line[i] == '"' and (i == 0 or line[i-1] != '\\'): # non-escaped quote
            insideQuote = not insideQuote
    return line.strip()


def removeWhitespace(string):
    return ''.join(string)


# Generic Exception class for file read errors
class FileParseException(Exception):
    def __init__(self, message):
        self.message = message
