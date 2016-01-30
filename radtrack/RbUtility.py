from __future__ import print_function, division
import math
import string
import numpy as np
from matplotlib.path import Path

# How to use:
#
# convertUnitsNumber(5, "km", "m") returns 5000
# convertUnitsString("5 km", "m") returns "5000 m"
# convertUnitsNumberToString(5, "km", "m") returns "5000 m"
# convertUnitsStringToNumber("5 km", "m") returns 5000
# displayWithUnitsNumber(5000, "m") returns "5 km"
# displayWithUnitsString("5000 m") returns "5 km"
#
# The above functions should be used instead of __parseUnits
# or the __unitConversion dictionary
#
# __parseUnits("km") returns 1000


def __parseUnits(unit):
    # Attempt parsing of compound unit (e.g., 'm/s^2')
    convertValue = 1.0
    currentUnit = ''
    multiply = True

    for char in (unit + '*'): # add extra '*' to process last unit
        if char in ['/', '*']:
            if '^' in currentUnit:
                currentUnit, exponent = currentUnit.split('^')
                exponent = float(exponent)
            else:
                exponent = 1.0
            exponent = exponent if multiply else -exponent
            convertValue = convertValue*(__unitConversion[currentUnit]**exponent)
            multiply = (char == '*')
            currentUnit = ''
        else:
            currentUnit = currentUnit + char

    return convertValue

def separateNumberUnit(inputString):
    # How this works: after stripping all whitespace, the functions looks for
    # the largest continuous block of characters starting from the left that
    # can be converted to a float.  The rest (if any) are assumed to specify
    # the units.
    parse = removeWhitespace(inputString)

    for numLength in range(len(parse),-1,-1):
        try:
            number = float(parse[:numLength])
            unit = parse[numLength:]
            if unit.startswith('/'):
                unit = '1' + unit
                number = float(parse[:(numLength-1)])
        except ValueError:
            continue
        else:
            break

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
        return number*__parseUnits(oldUnit)/__parseUnits(newUnit)
    except (ValueError, KeyError):
        raise ValueError('Cannot convert "' + oldUnit + '" to "' + newUnit + '".')

def convertUnitsString(inputString, newUnit):
    number, unit = separateNumberUnit(inputString)
    return convertUnitsNumberToString(number, unit, newUnit)

def convertUnitsNumberToString(number, oldUnit, newUnit):
    return (str(convertUnitsNumber(number, oldUnit, newUnit)) + ' ' + removeWhitespace(newUnit)).strip()

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
    if value < 0:
        return '-' + displayWithUnitsNumber(-value, currentUnit)

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
__unitConversion = dict()
__unitConversion[''] = 1 # unitless unit
__unitConversion['1'] = 1 # for inverse units (1/s = Hz)
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
            __unitConversion[prefix + unit] = multiplier
            row.append(prefix + unit)
        if prefix == last:
            break

        multiplier = multiplier/1000

    if addRow:
        addToUnitTable(row)

def addToUnitConversion(unit, value, otherUnit):
    __unitConversion[unit] = value*__unitConversion[otherUnit]

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
addToUnitConversion('deg', math.pi/180, 'rad')

#temporal frequency -> Hz
addMetricUnit('Hz')
addToUnitConversion('1/s', 1, 'Hz')

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

#electrical resistance -> Ohm
addMetricUnit('Ohm')

#electrical potential -> V
addMetricUnit('V')

#mks mass -> g
addMetricUnit('g', 'k')


# Round number x to sig significant figures
def roundSigFig(x, sig):
    try:
        # find a, b such that x = a*10^b (1 <= a < 10)
        b = math.floor(math.log10(abs(x)))
        a = x/(10**b)
        return round(a, sig-1)*(10**b)
    except ValueError:
        return 0


rpnOp = dict()
# Basic Math
rpnOp['+'] = lambda stack : stack.pop(-2) + stack.pop(-1)
rpnOp['-'] = lambda stack : stack.pop(-2) - stack.pop(-1)
rpnOp['*'] = lambda stack : stack.pop(-2) * stack.pop(-1)
rpnOp['mult'] = rpnOp['*']
rpnOp['/'] = lambda stack : stack.pop(-2) / stack.pop(-1)
rpnOp['sqr'] = lambda stack : stack.pop(-1)**2
rpnOp['sqrt'] = lambda stack : math.sqrt(stack.pop(-1))
rpnOp['pow'] = lambda stack : stack.pop(-2)**stack.pop(-1)
rpnOp['chs'] = lambda stack : -stack.pop(-1)
rpnOp['abs'] = lambda stack : abs(stack.pop(-1))
rpnOp['mod'] = lambda stack : stack.pop(-2) % stack.pop(-1)
rpnOp['rec'] = lambda stack : 1/stack.pop(-1)
rpnOp['max2'] = lambda stack : max(stack.pop(-2), stack.pop(-1))
rpnOp['min2'] = lambda stack : min(stack.pop(-2), stack.pop(-1))
rpnOp['sign'] = lambda stack : stack.pop(-1) if stack[-1] == 0 else (1 if stack.pop(-1) > 0 else -1)

# Constants
rpnOp['pi'] = lambda stack : math.pi
rpnOp['log_10'] = lambda stack : math.log(10)
rpnOp['HUGE'] = lambda stack : math.exp(100)

# Physics Constants
rpnOp['mev'] = lambda stack : 0.51099906 # electron mass in MeV
rpnOp['c_mks'] = lambda stack : 299792458 # speed of light in mks
rpnOp['c_cgs'] = lambda stack : rpnOp['c_mks'](stack)*100 # speed of light in cm/s
rpnOp['e_cgs'] = lambda stack : 4.80325e-10 # elementary charge is cgs
rpnOp['e_mks'] = lambda stack : 1.60217733e-19 # elementary charge in mks
rpnOp['me_cgs'] = lambda stack : 9.1093897e-28 # mass of electron in cgs
rpnOp['me_mks'] = lambda stack : rpnOp['me_cgs'](stack)/1000 # mass of electron in mks
rpnOp['re_cgs'] = lambda stack : 2.81794092e-13
rpnOp['re_mks'] = lambda stack : rpnOp['re_cgs'](stack)/100
rpnOp['kb_cgs'] = lambda stack : 1.380658e-16
rpnOp['kb_mks'] = lambda stack : rpnOp['kb_cgs'](stack)/1e7
rpnOp['hbar_mks'] = lambda stack : 1.0545887e-34
rpnOp['hbar_MeVs'] = lambda stack : 6.582173e-22
rpnOp['mp_mks'] = lambda stack : 1.6726485e-27 # mass of proton in mks
rpnOp['mu_o'] = lambda stack : 4*math.pi*1e-7 # vacuum permeability
rpnOp['eps_o'] = lambda stack : 1/((rpnOp['c_mks'](stack)**2) * rpnOp['mu_o'](stack)) # vacuum permittivity
### Alpha Magnet
rpnOp['Kas'] = lambda stack : 191.655e-2
rpnOp['Kaq'] = lambda stack : 75.0499e-2

### Relativistic Functions
rpnOp['beta.p'] = lambda stack : stack[-1]/math.sqrt(1 + (stack.pop(-1)**2))
rpnOp['gamma.p'] = lambda stack : math.sqrt(1 + (stack.pop(-1)**2))
rpnOp['gamma.beta'] = lambda stack : 1/math.sqrt((stack.pop(-1)**2) - 1)
rpnOp['p.beta'] = lambda stack : stack[-1]/math.sqrt(1 - (stack.pop(-1)**2))
rpnOp['p.gamma'] = lambda stack : math.sqrt((stack.pop(-1)**2) - 1)

# Trigonometry
rpnOp['dasin'] = lambda stack : (180.0/math.pi)*math.asin(stack.pop(-1))
rpnOp['asin'] = lambda stack : math.asin(stack.pop(-1))
rpnOp['sin'] = lambda stack : math.sin(stack.pop(-1))
rpnOp['dsin'] = lambda stack : math.sin((math.pi/180)*stack.pop(-1))
rpnOp['dacos'] = lambda stack : (180.0/math.pi)*math.acos(stack.pop(-1))
rpnOp['acos'] = lambda stack : math.acos(stack.pop(-1))
rpnOp['cos'] = lambda stack : math.cos(stack.pop(-1))
rpnOp['dcos'] = lambda stack : math.cos((math.pi/180)*stack.pop(-1))
rpnOp['datan'] = lambda stack : (180.0/math.pi)*math.atan(stack.pop(-1))
rpnOp['atan'] = lambda stack : math.atan(stack.pop(-1))
rpnOp['tan'] = lambda stack : math.tan(stack.pop(-1))
rpnOp['dtan'] = lambda stack : math.tan((math.pi/180)*stack.pop(-1))
rpnOp['rtod'] = lambda stack : stack.pop(-1)*180/math.pi
rpnOp['dtor'] = lambda stack : stack.pop(-1)*math.pi/180
rpnOp['hypot'] = lambda stack : math.hypot(stack.pop(-2), stack.pop(-1))
# Usage: [x1 y1 x2 y2 dist2]
rpnOp['dist2'] = lambda stack : math.hypot(stack.pop(-4) - stack.pop(-2), stack.pop(-2) - stack.pop(-1))
rpnOp['knee'] = lambda stack : (math.atan(stack.pop(-1)) + (math.pi/2))/math.pi
rpnOp['Tn'] = lambda stack : math.cos(math.acos(stack.pop(-2))*stack.pop(-1))

# Hyperbolic Trig
rpnOp['cosh'] = lambda stack : math.cosh(stack.pop(-1))
rpnOp['acosh'] = lambda stack : math.acosh(stack.pop(-1))
rpnOp['sinh'] = lambda stack : math.sinh(stack.pop(-1))
rpnOp['asinh'] = lambda stack : math.asinh(stack.pop(-1))
rpnOp['tanh'] = lambda stack : math.tanh(stack.pop(-1))
rpnOp['atanh'] = lambda stack : math.atanh(stack.pop(-1))

# Powers and Logs
rpnOp['10x'] = lambda stack : 10**stack.pop(-1)
rpnOp['log'] = lambda stack : math.log10(stack.pop(-1))
rpnOp['ln'] = lambda stack : math.log(stack.pop(-1))

# Stack manipulation
rpnOp['='] = lambda stack : stack[-1]
rpnOp['over'] = lambda stack : stack[-2]
rpnOp['swap'] = lambda stack : stack.pop(-2)

def minmaxN(stack, wantMax):
    N = stack.pop(-1)
    lst = []
    for loop in range(int(N)):
        lst.append(stack.pop())
    return max(lst) if wantMax else min(lst)
rpnOp['maxN'] = lambda stack : minmaxN(stack, True)
rpnOp['minN'] = lambda stack : minmaxN(stack, False)

# Booleans
rpnOp['true'] = lambda stack : True
rpnOp['false'] = lambda stack : False
rpnOp['=='] = lambda stack : stack.pop(-2) == stack.pop(-1)
rpnOp['test'] = lambda stack : 'true' if stack.pop(-1) else 'false'

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
        while (line[lineEdit] not in string.whitespace or insideQuote(line, lineEdit)) and lineEdit > lineBegin:
            lineEdit -= 1 # backup up until whitespace is found
        if lineEdit == lineBegin:
            # whitespace not found, skip ahead to next whitespace or end of line
            while (line[lineEdit] not in string.whitespace or insideQuote(line, lineEdit)) and lineEdit < len(line):
                lineEdit += 1
            if lineEdit == len(line):
                return line
        line = line[:lineEdit] + newLine + indent + line[lineEdit:].strip()
        lineBegin = lineEdit + len(newLine)

    return line

def insideQuote(line, position):
    quoted = False
    for index in range(position + 1):
        if line[index] == '"' and not characterEscaped(line, index):
            quoted = not quoted
    return quoted


def stripComments(line, commentCharacter):
    for i in range(len(line)):
        if line[i] == commentCharacter and not insideQuote(line, i) and not characterEscaped(line, i):
            return line[:i].strip()
    return line.strip()

def characterEscaped(line, position):
    return position > 0 \
            and line[position - 1] == '\\' \
            and not characterEscaped(line, position - 1)

def removeWhitespace(string):
    return ''.join(string.split())


# Generic Exception class for file read errors
class FileParseException(Exception):
    def __init__(self, message):
        self.message = message

# Returns the data-holding widget inside layout widgets (QScrollArea, etc.)
def getRealWidget(widget):
    try:
        return getRealWidget(widget.widget())
    except Exception:
        return widget

__fileTypeDescription = dict()
__fileTypeDescription['*'] = 'All files'
__fileTypeDescription['lte'] = 'Elegant lattice file'
__fileTypeDescription['sdds'] = 'Self-Describing Data Set'
__fileTypeDescription['save'] = None
__fileTypeDescription['start'] = None
__fileTypeDescription['csv'] = 'Comma-separated value file'
__fileTypeDescription['rad'] = 'Laser beam line file'
__fileTypeDescription['out'] = 'Output file'
__fileTypeDescription['bun'] = 'Beam bunch file'
__fileTypeDescription['twi'] = 'Twiss parameter file'
__fileTypeDescription['sig'] = 'Sigma matrix file'
__fileTypeDescription['cen'] = 'Centroid output file'
__fileTypeDescription['dat'] = 'Data file'
__fileTypeDescription['txt'] = 'Text file'
__fileTypeDescription['fin'] = 'Elegant final properties file'
__fileTypeDescription['fel'] = 'FEL Calculator file'
__fileTypeDescription['lat'] = 'Genesis lattice file'
__fileTypeDescription['png'] = 'PNG Image'
__fileTypeDescription['jpg'] = 'JPG Image'
__fileTypeDescription['bmp'] = 'BMP Image'
__fileTypeDescription['ppm'] = 'PPM Image'
__fileTypeDescription['tiff'] = 'TIFF Image'
__fileTypeDescription['xbm'] = 'XBM Image'
__fileTypeDescription['xpm'] = 'XPM Image'
__fileTypeDescription['h5'] = 'Hierarchial Data Format'

def fileTypeDescription(ext):
    try:
        return __fileTypeDescription[ext] + ' (*.' + ext + ')'
    except TypeError:
        return None

def fileTypeList(exts):
    return ';;'.join([fileTypeDescription(ext.strip('.')) for ext in ['*'] + exts if fileTypeDescription(ext)])

from PyQt4.QtGui import QFileDialog
import os
def getSaveFileName(widget, exts = None):
    if exts:
        if isinstance(exts, (str, unicode)):
            exts = [exts]
    else:
        exts = widget.acceptsFileTypes

    dialog = QFileDialog(widget, 'Save File', widget.parent.lastUsedDirectory, fileTypeList(exts))
    dialog.setDefaultSuffix(exts[0])
    dialog.filterSelected.connect(lambda filter : dialog.setDefaultSuffix(filter.split('*')[1].strip(')').strip('.')))
    dialog.setAcceptMode(QFileDialog.AcceptSave)
    if dialog.exec_():
        fileName = dialog.selectedFiles()[0]
        if os.path.isdir(fileName):
            return None
        else:
            widget.parent.lastUsedDirectory = os.path.dirname(fileName)
            return fileName



"""
Generalized algorithm for plotting contour and/or scatter plots.
  self.plotFlag is queried to determine what's done.

Adapted from open source method: scatter_contour.py
https://github.com/astroML/astroML/blob/master/astroML/plotting/scatter_contour.py

Parameters
----------
plotFlag : style of plot (scatter, contour, line, etc.)
plotType : axis scaling (linear, log-log, or semi-log)
x, y     : x and y data for the contour plot
ax       : the axes on which to plot
divs     : desired number of divisions along each axis
levels   : integer or array (optional, default=10)
         number of contour levels, or array of contour levels
"""
def scatConPlot(plotFlag, plotType, x, y, ax, divs=10, levels=10):
    if plotFlag in ['contour', 'combo']:
        threshold = 8 if plotFlag == 'combo' else 1

        # generate the 2D histogram, allowing the algorithm to use
        #   all data points, automatically calculating the 2D extent
        myHist, edges = np.histogramdd([x,y], divs)
        xbins, ybins = edges[0], edges[1]

        # specify contour levels, allowing user to input simple integer
        levels = np.asarray(levels)
        # if user specified an integer, then populate levels reasonably
        if levels.size == 1:
            levels = np.linspace(threshold, myHist.max(), levels)

        # define the 'extent' of the contoured area, using the
        #   the horizontal and vertical arrays generaed by histogram2d()
        extent = [xbins[0], xbins[-1], ybins[0], ybins[-1]]
        i_min = np.argmin(levels)

        # draw a zero-width line, which defines the outer polygon,
        #   in order to reduce the number of points drawn
        outline = ax.contour(myHist.T, levels[i_min:i_min+1],linewidths=0,extent=extent)

        # generate the contoured image, filled or not
        #   use myHist.T, rather than full myHist, to limit extent of the contoured region
        #   i.e. only the high-density regions are contoured
        #   the return value is potentially useful to the calling method
        ax.contourf(myHist, levels, extent=extent)

    # logic for finding particles in low-density regions
    if plotFlag == 'combo':
        # create new 2D array that will hold a subset of the particles
        #   i.e. only those in the low-density regions
        lowDensityArray = np.hstack([x[:, None], y[:, None]])

        # extract only those particles outside the high-density region
        if len(outline.allsegs[0]) > 0:
            outer_poly = outline.allsegs[0][0]
            points_inside = Path(outer_poly).contains_points(lowDensityArray)
            Xplot = lowDensityArray[~points_inside]
        else:
            Xplot = lowDensityArray

    if plotFlag.startswith('scatter') or plotFlag.endswith('line'):
        Xplot = np.hstack([x[:, None], y[:, None]])

    if plotFlag in ['combo', 'scatter', 'scatter-line']:

        # Terrible hack to get around the "fact" that scatter plots
        # to not get correct axis limits either axis is log scale.
        # ax.plot(...) seems to work, so draw a plot and then delete
        # it, leaving the plot with a correct axes view.

        toRemove, = ax.plot(Xplot[:,0], Xplot[:,1], c='w')
        ax.scatter(Xplot[:,0], Xplot[:,1], marker='.', c='k')
        ax.lines.remove(toRemove)

    if plotFlag.endswith('line'):
        ax.plot(Xplot[:,0], Xplot[:,1], c='k')

    if plotFlag in ['line', 'scatter', 'scatter-line']:
        if plotType in ['log-log', 'semi-logx']:
            ax.set_xscale('log', nonposx='mask')

        if plotType in ['log-log', 'semi-logy']:
            ax.set_yscale('log', nonposy='mask')

        if plotType in ['linear', 'semi-logy']:
            ax.set_xscale('linear')

        if plotType in ['linear', 'semi-logx']:
            ax.set_yscale('linear')
