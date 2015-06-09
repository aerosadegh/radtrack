# -*- coding: utf-8 -*-
u"""Types for SRW parameters

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
#: Dictionary of display names

import enum

from radtrack import rt_enum

@enum.unique
class DensityMethod(rt_enum.Enum):
    NEAR_FIELD = 1
    FAR_FIELD = 2


@enum.unique
class Flux(rt_enum.Enum):
    TOTAL = 1
    PER_UNIT_SURFACE = 2


@enum.unique
class SimComplexity(rt_enum.Enum):
    MULTI_PARTICLE = 0
    SINGLE_PARTICLE = 1


@enum.unique
class SimKind(rt_enum.Enum):
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
