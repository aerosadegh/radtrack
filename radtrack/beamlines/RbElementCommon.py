# -*- coding: utf-8 -*-
"""
Created on  Sun Aug 25 22:57:26 2013

Copyright (c) 2013 RadiaBeam Technologies. All Rights Reserved
Generated by dataParse_v4.py2013-09-18 11:05:51
by Steven Wu, Mark Harrison
"""

from __future__ import print_function, division, unicode_literals, absolute_import
import string
import PyQt4.QtGui as pygui
import PyQt4.QtCore as pycore
from math import sin, cos, tan, pi, sqrt

def cot(angle):
    return 1/tan(angle)

from radtrack.util.unitConversion import convertUnitsStringToNumber
from radtrack.util.RbMath import rpn


# Creates a QTransform object that rotates and places a QGraphicsItem
# into its proper place
#
# For placing a QPoint/QPointF, use newPoint = placement(pos,angle).map(oldPoint)
def placement(pos, angle):
    return pygui.QTransform().translate(pos.x(), pos.y()).rotateRadians(angle)

def sanitizeName(name):
    # Strip out invalid characters
    validCharacters = string.ascii_letters + string.digits + '~@$%^&-_+={}[]|/?<>.:'
    name = ''.join([char for char in name if char in validCharacters])

    if not name.startswith(tuple(string.ascii_letters)):
        name = 'X' + name

    return name


def drawPath(element, x, y, pen, transform, scene):
    for i in range(len(x)-1):
        segmentStart = transform.map(pycore.QPointF(x[i], y[i]))
        segmentEnd   = transform.map(pycore.QPointF(x[i+1], y[i+1]))
        segment = pygui.QGraphicsLineItem(
                    pycore.QLineF(segmentStart, segmentEnd))
        segment.setPen(pen)
        segment.setToolTip(element.toolTip())
        scene.addItem(segment)


# Common properties to all elements (particle beamlines and laser beamlines)
class elementCommon(object):
    _pixPerMeter = 200

    inputFileParameters = []
    outputFileParameters = []

    def __init__(self, inputData = None):
        if inputData is None:
            # one more [''] for the name
            inputData = ['' for item in [''] + self.parameterNames]

        inputName = inputData[0]
        self.data = inputData[1:]
        self.setName(inputName if inputName else type(self).__name__[0])

    def toolTip(self):
        return self.name + ' (' + type(self).__name__ + ')'

    def isBeamline(self):
        return False

    def getName(self):
        return self._name

    def setName(self, newName):
        self._name = sanitizeName(newName)

    name = property(getName, setName)

    def getResolution(self):
        return elementCommon._pixPerMeter

    def reverse(self):
        # reversing a single element does nothing
        return self

    def displayLine(self):
        sentence = [(param, datum) for (param, datum) in \
                zip(self.parameterNames, self.data) if datum]

        #add "=" in within phrases, then add ', ' between those groups
        return ', '.join(['='.join(phrase) for phrase in sentence])

    def contains(self, searchElement):
        return False

    def getNumberOfElements(self):
        return 1

    # returns the value of an element's parameter by searching for name
    def getParameter(self, pName):
        index = self.parameterNames.index(pName)
        val = self.data[index]
        try:
            return convertUnitsStringToNumber(val, self.units[index])
        except ValueError:
            return rpn(val)

    def getLength(self):
        return self.findParameter(['L', 'XMAX', 'Length'])

    def getAngle(self):
        return self.findParameter(['ANGLE', 'KICK', 'HKICK'])

    def getDisplacement(self):
        position, _ = self.newPosition(pycore.QPointF(0, 0), 0)
        return sqrt(position.x()**2 + position.y()**2)

    def getPeriods(self):
        return self.findParameter(['PERIODS', 'POLES'])

    def getRadius(self):
        return self.findParameter(['R', 'SIZE_X', 'XSIZE', 'RX', 'X_MAX'])

    def findParameter(self, labelList):
        for label in labelList:
            if label in self.parameterNames:
                try:
                    return self.getParameter(label)
                except ValueError:
                    return 0
        else:
            return 0

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        if self.name != other.name:
            return False
        return self.data == other.data

    def __ne__(self, other):
        return not self == other

# xPic classes are for drawing a beamline preview
class alphaPic:
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        length = self.getLength()*self.getResolution()
        if length == 0:
            length = .5*self.getResolution()
        height = length
        alphaAngle = 40.71*pi/180

        exitAngle = angle + (pi - 2*alphaAngle)

        alphBox = [pycore.QPointF(-.5*length, 0),
                   pycore.QPointF(-.5*length, -height),
                   pycore.QPointF( .5*length, -height),
                   pycore.QPointF( .5*length, 0)]
        transform = pygui.QTransform().rotateRadians((pi/2)-alphaAngle)*placement(pos,angle)


        item = pygui.QGraphicsPolygonItem(pygui.QPolygonF(alphBox))
        item.setToolTip(self.toolTip())
        item.setTransform(transform)
        item.setBrush(pygui.QBrush(pycore.Qt.red))
        scene.addItem(item)

        sample = 200
        tRange = [float(i)/sample for i in range(sample)]
        x = [7.5*height*t*(t-.5)*(t-1) for t in tRange]
        x.append(0)
        y = [.9*height*4*t*(t-1) for t in tRange]
        y.append(0)
        pen = pygui.QPen(pycore.Qt.blue)
        drawPath(self, x, y, pen, transform, scene)

        return pos, exitAngle

    def newPosition(self, pos, angle):
        alphaAngle = 40.71*pi/180
        exitAngle = angle + (pi - 2*alphaAngle)
        return pos, exitAngle


class bendPic:
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        xSize = self.getLength()*self.getResolution()
        if xSize == 0:
            xSize = .1*self.getResolution()
        bendAngle = self.getAngle()

        entranceEdgeAngle = self.findParameter(['E1'])
        exitEdgeAngle = self.findParameter(['E2'])

        if type(self).__name__ == 'RBEN':
            entranceEdgeAngle += bendAngle/2
            exitEdgeAngle += bendAngle/2

        trapezoidAngle1 = (pi/2)-(0.5*bendAngle - entranceEdgeAngle)
        trapezoidAngle2 = (pi/2)-(0.5*bendAngle - exitEdgeAngle)
        ySize    = 0.75*self.getResolution()
        ySize = min([ySize, abs(2*xSize/(cot(trapezoidAngle1)+cot(trapezoidAngle2)))])
        xSlant1  = ySize / (2*tan(trapezoidAngle1))
        xSlant2  = ySize / (2*tan(trapezoidAngle2))

        trapezoid = [pycore.QPointF(-xSlant1,         -ySize/2),
                     pycore.QPointF( xSize + xSlant2, -ySize/2),
                     pycore.QPointF( xSize - xSlant2,  ySize/2),
                     pycore.QPointF( xSlant1,          ySize/2)]

        transform = pygui.QTransform().rotateRadians(.5*bendAngle)*placement(pos,angle)

        pic = pygui.QGraphicsPolygonItem(pygui.QPolygonF(trapezoid))
        pic.setTransform(transform)
        pic.setBrush(pygui.QBrush(pycore.Qt.blue))
        pic.setToolTip(self.toolTip())
        scene.addItem(pic)

        exitPoint = transform.map(pycore.QPointF(xSize, 0))
        angleNew = angle + bendAngle
        return exitPoint, angleNew

    def newPosition(self, pos, angle):
        xSize = self.getLength()
        bendAngle = self.getAngle()

        transform = pygui.QTransform().rotateRadians(.5*bendAngle)*placement(pos,angle)

        exitPoint = transform.map(pycore.QPointF(xSize, 0))
        angleNew = angle + bendAngle
        return exitPoint, angleNew



class driftPic:
    def getNumberOfElements(self):
        return 0

    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        length = self.getLength() * self.getResolution()
        exitPoint = placement(pos,angle).map(pycore.QPointF(length, 0))

        pen = pygui.QPen()
        pen.setBrush(self.beamColor)
        pen.setWidth(self.beamWidth*self.getResolution())
        pen.setCapStyle(pycore.Qt.FlatCap)

        line = pygui.QGraphicsLineItem(pycore.QLineF(pos, exitPoint))
        line.setToolTip(self.toolTip())
        line.setPen(pen)

        line.setZValue(-1) # place underneath all other elements
        scene.addItem(line)
        return exitPoint, angle

    def newPosition(self, pos, angle):
        length = self.getLength()
        exitPoint = placement(pos,angle).map(pycore.QPointF(length, 0))

        return exitPoint, angle


class particleDrift(driftPic):
    beamColor = pycore.Qt.gray
    beamWidth = .1 # meters


class aperturePic(driftPic):
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        length = self.getLength() * self.getResolution()
        if length == 0:
            length = .01*self.getResolution()

        opening = self.getRadius()*self.getResolution()
        if opening == 0:
            opening = .1*self.getResolution()

        height = opening*2

        lower = [pycore.QPointF(0,      -opening),
                 pycore.QPointF(0,      -height),
                 pycore.QPointF(length, -height),
                 pycore.QPointF(length, -opening)]

        itemLower = pygui.QGraphicsPolygonItem(pygui.QPolygonF(lower))
        itemUpper = pygui.QGraphicsPolygonItem(pygui.QPolygonF(lower))

        # Create upper part from lower part
        upperTransform = pygui.QTransform().translate(length,0).rotate(180)

        # Place entire aperture
        itemLower.setTransform(placement(pos, angle))
        itemUpper.setTransform(upperTransform*placement(pos, angle))

        #brushes fill the item with designated color&pattern
        for item in [itemLower, itemUpper]:
            item.setBrush(pygui.QBrush(pycore.Qt.black))
            item.setToolTip(self.toolTip())
            scene.addItem(item)

        # draw line for drift
        return driftPic.picture(self, scene, pos, angle)

def curvedSurface(sign, height, position):
    totalAngle = pi/4
    drawRadius = height/totalAngle
    samples = 20
    drawAngles = [-totalAngle/2 + i*totalAngle/samples for i in range(samples+1)]
    surface = []
    for drawAngle in drawAngles:
        surface.append(pycore.QPointF(
            sign*drawRadius*(1-cos(drawAngle))+position,
            drawRadius*sin(drawAngle)))

    return surface, 2*drawRadius*(1-cos(totalAngle/2))


class reflectiveGratingPic:
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        ySize = self.getRadius()*self.getResolution()
        if ySize == 0:
            ySize = .1*self.getResolution()
        _, xSize = curvedSurface(0, ySize, 0)
        rotationAngle = self.findParameter(['THETA'])
        samples = 20
        gratingShape = []
        for i in range(samples):
            i = float(i)
            if i%2 == 0:
                x = 0
                y = ySize*(1 - 2*(i/samples))
            else:
                x = -xSize/3
                y = ySize*(1 - 2*((i-1)/samples))
            gratingShape.append(pycore.QPointF(x, y))
        gratingShape.append(pycore.QPointF(xSize, -ySize))
        gratingShape.append(pycore.QPointF(xSize, ySize))

        item = pygui.QGraphicsPolygonItem(pygui.QPolygonF(gratingShape))
        item.setTransform(placement(pos, angle+rotationAngle))
        item.setBrush(pycore.Qt.gray)
        item.setToolTip(self.toolTip())
        scene.addItem(item)

        return pos, angle-(pi-rotationAngle*2)


    def newPosition(self, pos, angle):
        rotationAngle = self.findParameter(['THETA'])
        return pos, angle-(pi-rotationAngle*2)


class gratingPic:
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        ySize = self.getRadius()*self.getResolution()
        if ySize == 0:
            ySize = .1*self.getResolution()
        xSize = ySize/5
        boxes = 10
        boxHeight = ySize/(boxes)
        boxWidth = xSize
        for i in range(boxes):
            i = float(i)
            boxShape = []
            y = -ySize*(1-2*i/boxes)
            boxShape.append(pycore.QPointF(-boxWidth, y))
            boxShape.append(pycore.QPointF(-boxWidth, y+boxHeight))
            boxShape.append(pycore.QPointF(0, y+boxHeight))
            boxShape.append(pycore.QPointF(0, y))
            item = pygui.QGraphicsPolygonItem(pygui.QPolygonF(boxShape))
            item.setTransform(placement(pos, angle))
            item.setBrush(pycore.Qt.black)
            item.setToolTip(self.toolTip())
            scene.addItem(item)

        return pos, angle


    def newPosition(self, pos, angle):
        return pos, angle



class lensPic:
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        height = self.getRadius()*self.getResolution()
        if height == 0:
            height = .2*self.getResolution()

        previousSurface = None
        position = 0
        for radius in self.radii():
            if radius > 0:
                sign = 1
            elif radius < 0:
                sign = -1
            else:
                sign = 0

            surface, advance = curvedSurface(sign, height, position)
            position += advance

            if previousSurface is not None:
                item = pygui.QGraphicsPolygonItem(pygui.QPolygonF(previousSurface + surface))
                item.setTransform(placement(pos, angle))
                item.setBrush(pygui.QColor(pycore.Qt.blue).lighter())
                item.setToolTip(self.toolTip())
                scene.addItem(item)

            previousSurface = surface
            previousSurface.reverse()

        exitPoint = placement(pos, angle).map(pycore.QPointF(position-advance, 0))

        return exitPoint, angle

    def newPosition(self, pos, angle):
        return pos, angle


class magnetPic:
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        length = self.getLength()*self.getResolution()
        height = 0.5*self.getResolution()

        exitPoint = placement(pos, angle).map(pycore.QPointF(length, 0))

        quad = [pycore.QPointF(0,      -0.5*height),
                pycore.QPointF(0,       0.5*height),
                pycore.QPointF(length,  0.5*height),
                pycore.QPointF(length, -0.5*height)]
        item = pygui.QGraphicsPolygonItem(pygui.QPolygonF(quad))

        item.setToolTip(self.toolTip())
        item.setTransform(placement(pos,angle))
        if hasattr(self.color, 'setStart'):
            self.color.setStart(pycore.QPointF(0,0))
            self.color.setFinalStop(pycore.QPointF(length,0))
        item.setBrush(pygui.QBrush(self.color))

        scene.addItem(item)

        return exitPoint, angle

    def newPosition(self, pos, angle):
        length = self.getLength()
        exitPoint = placement(pos, angle).map(pycore.QPointF(length, 0))
        return exitPoint, angle


class mirrorPic:
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        rotationAngle = self.findParameter(['THETA'])
        focalLength = self.findParameter(['F'])
        height = self.getRadius()*self.getResolution()
        if height == 0:
            height = .1*self.getResolution()

        if focalLength > 0:
            sign = -1
        elif focalLength < 0:
            sign = 1
        else:
            sign = 0

        frontSurface, advance = curvedSurface(sign, height, 0)
        backSurface, _ = curvedSurface(sign, height, advance)
        backSurface.reverse()

        item = pygui.QGraphicsPolygonItem(pygui.QPolygonF(frontSurface + backSurface))
        item.setTransform(placement(pos, angle+rotationAngle))
        item.setBrush(pygui.QColor(pycore.Qt.blue).lighter())
        item.setToolTip(self.toolTip())
        scene.addItem(item)

        return pos, angle-(pi-rotationAngle*2)

    def newPosition(self, pos, angle):
        rotationAngle = self.findParameter(['THETA'])
        return pos, angle-(pi-rotationAngle*2)


class recircPic:
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        radius = .3*self.getResolution()
        initAngle = .2
        finalAngle = pi - initAngle

        steps = 100
        tRange = [float(t)/steps for t in range(steps+1)]
        thetas = [initAngle + t*(finalAngle-initAngle) for t in tRange]

        x = [radius*cos(theta) for theta in thetas]
        y = [radius*sin(theta) for theta in thetas]
        pen = pygui.QPen(pycore.Qt.green)
        pen.setWidth(radius/10)
        pen.setCapStyle(pycore.Qt.RoundCap)
        drawPath(self, x, y, pen, placement(pos, angle), scene)

        y = [-yi for yi in y]
        drawPath(self, x, y, pen, placement(pos, angle), scene)

        d = .3*radius*sqrt(2)/2
        arrowHead = [pycore.QPointF(radius  ,  0),
                     pycore.QPointF(radius-d, d),
                     pycore.QPointF(radius+d, d)]
        head1 = pygui.QGraphicsPolygonItem(pygui.QPolygonF(arrowHead))
        head1.setBrush(pycore.Qt.green)
        head1.setPen(pen)
        head1.setTransform(placement(pycore.QPointF(0,0), min(thetas))*placement(pos, angle))
        head1.setToolTip(self.toolTip())
        scene.addItem(head1)

        head2 = pygui.QGraphicsPolygonItem(pygui.QPolygonF(arrowHead))
        head2.setBrush(pycore.Qt.green)
        head2.setPen(pen)
        head2.setTransform(placement(pycore.QPointF(0,0), pi+min(thetas))*placement(pos, angle))
        head2.setToolTip(self.toolTip())
        scene.addItem(head2)

        return pos, angle

    def newPosition(self, pos, angle):
        return pos, angle


class solenoidPic:
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        length = self.getLength()*self.getResolution()
        if length == 0:
            length = .3*self.getResolution()
        height = length

        exitPoint = placement(pos, angle).map(pycore.QPointF(length, 0))

        solenoidBox = [pycore.QPointF(0,       height/2),
                       pycore.QPointF(0,      -height/2),
                       pycore.QPointF(length, -height/2),
                       pycore.QPointF(length,  height/2)]

        item = pygui.QGraphicsPolygonItem(pygui.QPolygonF(solenoidBox))
        item.setToolTip(self.toolTip())
        item.setTransform(placement(pos,angle))
        item.setBrush(pygui.QBrush(pygui.QColor(pycore.Qt.blue).lighter()))
        scene.addItem(item)

        # Draw helix to represent solenoid magnet
        loops = 8
        steps = 100*loops
        ratio = .5 # loop width as a fraction of length
        fraction = [float(i)/steps for i in range(steps)]
        x = [length*(1.0/(1+2*ratio))*(t + ratio*(1-cos((loops+.5)*(2*pi)*t))) for t in fraction]
        y = [.4*height*sin((loops+.5)*(2*pi)*t) for t in fraction]

        pen = pygui.QPen(pycore.Qt.black)
        drawPath(self, x, y, pen, placement(pos, angle), scene)

        return exitPoint, angle

    def newPosition(self, pos, angle):
        length = self.getLength()
        exitPoint = placement(pos, angle).map(pycore.QPointF(length, 0))
        return exitPoint, angle


class undulatorPic:
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        length  = self.getLength()*self.getResolution()
        periods = int(self.getPeriods())
        if periods == 0:
            periods = int(5*self.getLength())
        longBoxSize = length/(2*periods)
        tranBoxSize = 0.25*self.getResolution()

        exitPoint = placement(pos, angle).map(pycore.QPointF(length, 0))

        for j in range(2*periods):
            # Draw lower half of undulator
            if j % 2 == 1:
                boxLower = [pycore.QPointF(    j*longBoxSize,  0.25*tranBoxSize),
                            pycore.QPointF(    j*longBoxSize,       tranBoxSize),
                            pycore.QPointF((j+1)*longBoxSize,       tranBoxSize),
                            pycore.QPointF((j+1)*longBoxSize,  0.25*tranBoxSize)]
            else:
                boxLower = [pycore.QPointF(    j*longBoxSize,  0.5*tranBoxSize),
                            pycore.QPointF(    j*longBoxSize,      tranBoxSize),
                            pycore.QPointF((j+1)*longBoxSize,      tranBoxSize),
                            pycore.QPointF((j+1)*longBoxSize,  0.5*tranBoxSize)]

            itemLower = pygui.QGraphicsPolygonItem(pygui.QPolygonF(boxLower))
            itemUpper = pygui.QGraphicsPolygonItem(pygui.QPolygonF(boxLower))

            # Create upper part of undulator from lower part
            upperTransform = pygui.QTransform()
            upperTransform.translate(length,0)
            upperTransform.rotate(180)

            #Place entire undulator
            itemLower.setTransform(placement(pos, angle))
            itemUpper.setTransform(upperTransform*placement(pos, angle))

            #brushes fill the item with designated color&pattern
            itemLower.setBrush(pygui.QBrush(pycore.Qt.gray))
            itemUpper.setBrush(pygui.QBrush(pycore.Qt.gray))
            itemLower.setToolTip(self.toolTip())
            itemUpper.setToolTip(self.toolTip())
            scene.addItem(itemLower)
            scene.addItem(itemUpper)

        sample = 4 # points to draw per undulator period
        points = periods*sample
        tRange = [float(i)/points for i in range(points+1)]
        x = [t*length for t in tRange]
        y = [-0.1*tranBoxSize*sin(t*periods*2*pi) for t in tRange]
        pen = pygui.QPen(pycore.Qt.red)
        drawPath(self, x, y, pen, placement(pos, angle), scene)

        if type(self).__name__ == 'LSRMDLTR':
            pen = pygui.QPen()
            pen.setBrush(pygui.QColor(pycore.Qt.red).lighter())
            pen.setWidth(10)

            laser = pygui.QGraphicsLineItem(0,-tranBoxSize/2, length/2,0)
            laser.setTransform(placement(pos, angle))
            laser.setToolTip(self.toolTip())
            laser.setPen(pen)
            scene.addItem(laser)

        return exitPoint, angle

    def newPosition(self, pos, angle):
        length  = self.getLength()
        exitPoint = placement(pos, angle).map(pycore.QPointF(length, 0))
        return exitPoint, angle


class watchPic:
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        flagSizePix = self.flagSize*self.getResolution()

        flag = [pycore.QPointF(0, 0),
                pycore.QPointF(0, -4*flagSizePix),
                pycore.QPointF(flagSizePix, -3.5*flagSizePix),
                pycore.QPointF(0, -3*flagSizePix),
                pycore.QPointF(0, 0)]

        flagItem = pygui.QGraphicsPolygonItem(pygui.QPolygonF(flag))
        flagItem.setTransform(placement(pos, angle))
        flagItem.setBrush(pygui.QBrush(pycore.Qt.green))
        flagItem.setToolTip(self.toolTip())

        scene.addItem(flagItem)

        return pos, angle

    def newPosition(self, pos, angle):
        return pos, angle

class zeroLengthPic:
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        size = self.getResolution()/2
        start = pycore.QPointF(0, size)
        end = pycore.QPointF(0, -size)
        screen = pygui.QGraphicsLineItem(pycore.QLineF(start, end))
        pen = pygui.QPen(pycore.Qt.red)
        pen.setBrush(pycore.Qt.black)
        pen.setWidth(10)
        pen.setCapStyle(pycore.Qt.FlatCap)

        screen.setTransform(placement(pos, angle))
        screen.setPen(pen)
        screen.setToolTip(self.toolTip())

        scene.addItem(screen)

        return pos, angle

    def newPosition(self, pos, angle):
        return pos, angle


class rfPic(zeroLengthPic):
    def picture(self, scene, pos = pycore.QPointF(0,0), angle = 0):
        length = self.getLength()*self.getResolution()
        if length < 1:
            return zeroLengthPic.picture(self, scene, pos, angle)
        cavityHeight = 0.3*self.getResolution()
        exitPoint = placement(pos,angle).map(pycore.QPointF(length, 0))

        cavityWidth = cavityHeight/2
        numberCavities = max([int((length/cavityWidth)+.5), 1])
        cavityWidth = length/numberCavities

        color = pygui.QBrush(pygui.QColor(255, 196, 29)) # ~ copper color
        for i in range(numberCavities):
            ellipse = pygui.QGraphicsEllipseItem()
            ellipse.setRect(pycore.QRectF(i*cavityWidth,-cavityHeight/2, cavityWidth,cavityHeight))
            ellipse.setTransform(placement(pos, angle))
            ellipse.setBrush(color)
            ellipse.setToolTip(self.toolTip())
            scene.addItem(ellipse)
        rectangle = pygui.QGraphicsRectItem(0, -cavityHeight/6, length, cavityHeight/3)
        rectangle.setTransform(placement(pos, angle))
        rectangle.setBrush(color)
        rectangle.setToolTip(self.toolTip())
        scene.addItem(rectangle)

        return exitPoint, angle

    def newPosition(self, pos, angle):
        length = self.getLength()
        exitPoint = placement(pos,angle).map(pycore.QPointF(length, 0))
        return exitPoint, angle
