# -*- coding: utf-8 -*-
u"""Types for SRW parameters.

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import enum
import yaml

from pykern import pkio
from pykern import pkresource
from pykern import pkyaml


#: Dictionary of display names
DISPLAY_NAMES = pkyaml.load_file(pkresource.filename('srw_enums.yml'))


class Enum(enum.Enum):
    """Wraps :class:`enum.Enum` with helper routines"""

    def __init__(self, *args):
        super(Enum, self).__init__(*args)
        self.display_name = DISPLAY_NAMES[self.__class__.__name__][self.name]

    def has_name(self, name):
        """Compares `name` with `self.name`

        Args:
            name (str): string name to compare

        Returns:
            bool: True if self has `name`

        """
        return self.name == name

    @classmethod
    def from_anything(cls, value):
        """Convert value (str, int, obj) to instance of `cls`

        Args:
            value (object): may be str, int, or obj
        Returns:
            enum.Enum: returns instance
        """
        if isinstance(value, cls):
            return value
        if isinstance(value, int):
            return cls(value)
        return cls[value]


@enum.unique
class DensityMethod(Enum):
    NEAR_FIELD = 0
    FAR_FIELD = 1


@enum.unique
class Flux(Enum):
    TOTAL = 0
    PER_UNIT_SURFACE = 1


@enum.unique
class SimComplexity(Enum):
    MULTI_PARTICLE = 0
    SINGLE_PARTICLE = 1


@enum.unique
class SimKind(Enum):
    E = 0
    X = 1
    Y = 2
    X_AND_Y = 3
    E_AND_X = 4
    E_AND_Y = 5
    E_AND_X_AND_Y = 6


@enum.unique
class UndulatorOrientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
