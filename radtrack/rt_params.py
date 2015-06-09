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

from pykern.pkdebug import pkdc, pkdi, pkdp
from pykern import pkcompat
from pykern import pkio
from pykern import pkresource
from pykern import pkyaml

_cache = {}


def declarations(file_prefix):
    """Parsed parameter declarations from ``<file_prefix>_declarations.yml``

    Args:
        file_prefix (str): which file to parse

    Returns:
        OrderedDict: mapping of declarations
    """
    return _get(file_prefix, 'declarations', _parse_declarations)


def defaults(file_prefix):
    """Parsed parameter defaults from ``<file_prefix>_defaults.yml``

    Args:
        file_prefix (str): which file to parse

    Returns:
        dict: mapping of default values
    """
    return _get(file_prefix, 'defaults', _parse_defaults)


def init_params(defaults, declarations):
    """Create a tree of default params excluding headings and computed params

    Args:
        defaults (dict): used for initializations
        declarations (dict): relevant expected declarations

    Returns:
        dict: nested dictionary of params
    """
    res = {}
    for k in defaults:
        res2 = {}
        res[k] = res2
        df = defaults[k]
        d = declarations[k]
        if d['is_selector_for_params']:
            for k2 in df:
                res2[k2] = init_params(df[k2], declarations)
        else:
            for d in declarations[k].values():
                if not isinstance(d, dict) \
                    or d['is_computed_param'] or d['display_as_heading']:
                    continue
                res2[d['label']] = df[d['label']]
    return res


def iter_display_declarations(declarations):
    """Iterate over primary params and headings

    Args:
        declarations (OrderedDict): what to iterate

    Yields:
        declaration (dict): values of `declarations`
    """
    for d in declarations.values():
        if isinstance(d, dict) and not d['is_computed_param']:
            yield d


def iter_primary_param_declarations(declarations):
    """Iterate over primary params and not headings

    Args:
        declarations (OrderedDict): what to iterate

    Yields:
        declaration (dict): values of `declarations`
    """
    for d in declarations.values():
        if isinstance(d, dict) and not d['is_computed_param'] and not d['display_as_heading']:
            yield d


def _get(file_prefix, which, how):
    """Get from cache or parse and validate YAML file.

    Args:
        file_prefix (str): which file to parse
        which (str): "declarations" or "defaults"
        how (callable): parser

    Returns:
        dict: parsed YAML file; declarations are an OrderedDict;
              defaults are a regular dict.
    """
    global _cache
    if which not in _cache:
        y = pkyaml.load_resource('{}_{}'.format(file_prefix, which))
        _cache[which] = how(y, file_prefix=file_prefix)
    return _cache[which]


def _parse_declarations(values, file_prefix=None):
    """Recurse the parsed YAML declarations; convert values and types

    Order preserving so can use for layout.

    Args:
        values (list): raw YAML as a list
        file_prefix (str): which file to parse
    """
    res = collections.OrderedDict()
    for v in values:
        if len(v) == 1:
            k = v.keys()[0]
            v = _parse_declarations(v[k], False)
            assert not 'label' in v, \
                '{}.parameter name may not be "label"'.format(k)
            v['label'] = k
            #TODO(robnagler) need to solve collisions problem
            v['is_selector_for_params'] = False
        else:
            for x in (
                'display_as_checkbox',
                'display_as_heading',
                'is_computed_param',
                'is_selector_for_params',
                'units',
            ):
                if x not in v:
                    v[x] = None if x == 'units' else False
            v['py_type'] = _parse_type(v)
        res[v['label']] = v
    return res


def _parse_defaults(values, d=None, file_prefix=None):
    """Recurse the parsed YAML defaults; convert values by declarations

    Args:
        values (list): raw YAML as a list
        file_prefix (str): which file to parse
    Returns:
        dict: parsed YAML
    """
    # Need to parse
    if not d:
        d = declarations(file_prefix)
    res = {}
    for k, v in values.items():
        sub_d = d[k]
        if not isinstance(v, dict):
            res[k] = _parse_value(v, sub_d['py_type'])
            continue
        if not sub_d['is_selector_for_params']:
            res[k] = _parse_defaults(v, sub_d)
            continue
        # Selector is strange, because there is a value
        t = sub_d['py_type']
        assert isinstance(t, enum.EnumMeta), \
            '{}: unable to parse value for {}'.format(d['py_type'], d['label'])
        res[k] = {}
        for k2, v2 in v.items():
            res[k][k2] = _parse_defaults(v2, d)
    return res


def _parse_value(v, t):
    if hasattr(t, 'from_anything'):
        return t.from_anything(v)
    return t(v)


def _parse_type(v):
    """Parse py_type to Python type instance"""
    try:
        t = getattr(__builtin__, v['py_type'])
        if isinstance(t, type):
            return t
    except AttributeError:
        pass
    s = re.search(r'^(\w+)\.(\w+)$', v['py_type'])
    assert s, \
        '{py_type}: py_type for {label} not found'.format(*v)
    m = importlib.import_module('radtrack.' + s.group(1))
    t = getattr(m, s.group(2))
    assert isinstance(t, type), \
        '{py_type}: py_type for {label} not a type'.format(*v)
    return t
