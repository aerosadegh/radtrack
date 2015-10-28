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
from pykern import pkcompat

#: look up display names
_display_name_cache = {}


class Enum(enum.Enum):
    """Wraps :class:`enum.Enum` with helper methods and attrs

    Attributes:
        display_name (str): human readable name
    """

    def __init__(self, *args):
        super(Enum, self).__init__(*args)
        #TODO(robnagler) Assert all values of an enum are exactly the same type
        assert isinstance(self.value, (int,float)), \
            '{}: must in instance of int or float'.format(self.value)
        self.display_name = _display_name(self)

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
        if isinstance(value, (int,float)):
            return cls(value)
        if pkcompat.isinstance_str(value):
            return cls[value.upper()]
        raise AssertionError('{}: is not an instance of {}'.format(value, cls))

    def __cmp__(self, anything):
        """Compares `anything` with `self`

        Args:
            anything (object): name, enum, value etc. to compare

        Returns:
            int: -1, 0, 1 or NotImplemented if types don't compare

        """
        if anything is None:
            return 1
        a = self.__class__.from_anything(anything).value
        if isinstance(anything, int):
            return self.value.__cmp__(a)
        # Since our values are constants, we can use simple compares
        if self.value < a:
            return -1
        return 0 if self.value == a else 1

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0


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
