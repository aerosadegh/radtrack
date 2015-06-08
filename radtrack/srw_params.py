# -*- coding: utf-8 -*-
u"""Parameter declaration parser

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import __builtin__
import collections
import importlib
import re

import enum
import yaml

from pykern.pkdebug import pkdi
from pykern import pkcompat
from pykern import pkio
from pykern import pkresource
from pykern import pkyaml

_map = {}


def declarations():
    """Parsed declarations from ``srw_declarations.yml``

    Returns:
        dict: mapping of declarations
    """
    return _get('declarations', _parse_declarations)


def defaults():
    """Parsed defaults from ``srw_defaults.yml``

    Returns:
        dict: mapping of default values
    """
    return _get('defaults', _parse_defaults)


def _get(which, how):
    global _map
    if which not in _map:
        y = pkyaml.load_file(pkresource.filename('srw_{}.yml'.format(which)))
        _map[which] = how(y)
    return _map[which]


def _parse_declarations(fields, is_top=True):
    res = collections.OrderedDict()
    for f in fields:
        if len(f) == 1:
            k = f.keys()[0]
            f = _parse_declarations(f[k], False)
            assert not 'label' in f, \
                '{}.parameter name may not be "label"'.format(k)
            f['label'] = k
        else:
            for x in ('display_as_checkbox', 'rt_old', 'units'):
                if x not in f:
                    f[x] = None
            f['py_type'] = _parse_type(f)
        assert not re.search(r'^\d+$', f['label']), \
            '{label}: label must not be an integer'.format(*f)
        res[f['label']] = f
    return res


def _parse_defaults(values, d=None, res=None):
    # Need to parse
    if not d:
        d = declarations()
    for k, v in values.items():
        sub_d = d[k]
        if not isinstance(v, dict):
            values[k] = _parse_value(sub_d['py_type'], v)
            continue
        if not 'py_type' in sub_d:
            _parse_defaults(v, sub_d)
            continue
        # Enum selector is strange, because there is a value
        t = sub_d['py_type']
        assert isinstance(t, enum.EnumMeta), \
            '{}: unable to parse value for {}'.format(d['py_type'], d['label'])
        for k2, v2 in v.items():
            v[k2] = _parse_defaults(v2, d)
        v2['_value'] = _parse_value(t, k2)
    return values


def _parse_value(t, v):
    if hasattr(t, 'from_anything'):
        return t.from_anything(v)
    return t(v)


def _parse_type(f):
    """Parse py_type to Python type instance"""
    try:
        t = getattr(__builtin__, f['py_type'])
        if isinstance(t, type):
            return t
    except AttributeError:
        pass
    s = re.search(r'^(\w+)\.(\w+)$', f['py_type'])
    assert s, \
        '{py_type}: py_type for {label} not found'.format(*f)
    m = importlib.import_module('radtrack.' + s.group(1))
    t = getattr(m, s.group(2))
    assert isinstance(t, type), \
        '{py_type}: py_type for {label} not a type'.format(*f)
    return t
