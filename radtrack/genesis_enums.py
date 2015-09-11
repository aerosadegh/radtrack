# -*- coding: utf-8 -*-
u"""Types for Genesis parameters

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
#: Dictionary of display names

import enum

from radtrack import rt_enum

@enum.unique
class UndulatorType(rt_enum.Enum):
    PLANAR = 0
    HELICAL = 1


@enum.unique
class TaperType(rt_enum.Enum):
    NONE = 0
    LINEAR = 1
    QUADRATIC = 2


@enum.unique
class ErrorType(rt_enum.Enum):
    GAUSSIAN_MINMIZE = -2
    UNIFORM_MINIMIZE = -1
    NONE = 0
    UNIFORM = 1
    GAUSSIAN = 2


@enum.unique
class EnergyProfile(rt_enum.Enum):
    UNIFORM = 1
    GAUSSIAN = 0


@enum.unique
class GenerateGaus(rt_enum.Enum):
    JOINTPROBABILITY = 0
    INVERTEDERROR = 1

@enum.unique
class Boundary(rt_enum.Enum):
    DIRECHLET = 0
    NEUMANN = 1

@enum.unique
class SCCalc(rt_enum.Enum):
    ONCE = 0
    FOUR = 1

@enum.unique
class CellStart(rt_enum.Enum):
    FULL = 0
    HALF = 2
    
@enum.unique
class ShotnoiseAlgorithm(rt_enum.Enum):
    FAWLEY = 0
    PENNMAN = 1
    
@enum.unique
class ScanVar(rt_enum.Enum):
    GAMMA0 = 1
    DELGAM = 2
    CURPEAK = 3
    XLAMDS = 4
    AW0 = 5
    ISEED = 6
    PXBEAM = 7
    PYBEAM = 8
    XBEAM = 9
    YBEAM = 10
    RXBEAM = 11
    RYBEAM = 12
    XLAMD = 13
    DELAW = 14
    ALPHAX = 15
    ALPHAY = 16
    EMITX = 17
    EMITY = 18
    PRAD0 = 19
    ZRAYL = 20
    ZWAIST = 21
    AWD = 22
    BEAMFILE = 23
    BEAMOPT = 24
    BEAMGAM = 25
    
@enum.unique
class FFspectrum(rt_enum.Enum):
    NEAR_FIELD = 0
    FAR_FIELD = -1
    TOTAL = 1
