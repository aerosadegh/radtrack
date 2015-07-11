# -*- coding: utf-8 -*-
u"""Extension to :class:`enum.Enum`

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import enum
import yaml

from pykern import pkinspect
from pykern import pkio
from pykern import pkresource
from pykern import pkyaml

#: look up display names
_display_name_cache = {}


class Enum(enum.Enum):
    """Wraps :class:`enum.Enum` with helper methods and attrs

    Attributes:
        display_name (str): human readable name
    """

    def __init__(self, *args):
        super(Enum, self).__init__(*args)
        self.display_name = _display_name(self)

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
        return cls[value.upper()]

def _display_name(e):
    """Lookup display_name for enum

    Args:
        e (Enum): what to look up

    Returns:
        str: display name for `e`
    """
    f = pkinspect.module_basename(e)
    if f not in _display_name_cache:
        # Name collisions avoided because this is a radtrack namespace
        _display_name_cache[f] = pkyaml.load_resource(f)
    return _display_name_cache[f][e.__class__.__name__][e.name]
