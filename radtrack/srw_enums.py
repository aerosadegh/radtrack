# -*- coding: utf-8 -*-
u"""Types for SRW parameters

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
#: Dictionary of display names

import enum

from radtrack import rt_enum

@enum.unique
class DensityComputation(rt_enum.Enum):
    NEAR_FIELD = 1
    FAR_FIELD = 2


@enum.unique
class FluxCalculation(rt_enum.Enum):
    TOTAL = 1
    PER_UNIT_SURFACE = 2


@enum.unique
class SimulationComplexity(rt_enum.Enum):
    MULTI_PARTICLE = 0
    SINGLE_PARTICLE = 1


@enum.unique
class SimulationKind(rt_enum.Enum):
    E = 0
    X = 1
    Y = 2
    X_AND_Y = 3
    E_AND_X = 4
    E_AND_Y = 5
    E_AND_X_AND_Y = 6


@enum.unique
class UndulatorOrientation(rt_enum.Enum):
    HORIZONTAL = 0
    VERTICAL = 1

@enum.unique
class SRCalculationMethod(rt_enum.Enum):
    MANUAL = 0
    AUTO_UNDULATOR = 1
    AUTO_WIGGLER = 2

@enum.unique
class Polarization(rt_enum.Enum):
    LINEAR_HORIZONTAL = 0
    LINEAR_VERTICAL = 1
    LINEAR_45_DEGREES = 2
    LINEAR_135_DEGREES = 3
    CIRCULAR_RIGHT = 4
    CIRCULAR_LEFT = 5
    TOTAL = 6

@enum.unique
class Intensity(rt_enum.Enum):
    SINGLE_ELECTRON_INTENSITY = 0
    SINGLE_ELECTRON_FLUX = 1
    REAL_PART_OF_ELECTRON_E_FIELD = 2
    IMAGINARY_PART_OF_ELECTRON_E_FIELD = 3
