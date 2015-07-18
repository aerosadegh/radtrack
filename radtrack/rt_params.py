# -*- coding: utf-8 -*-
u"""Parameter declaration parser

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import __builtin__
import collections
import copy
import importlib
import re
import UserDict

import enum
import yaml

from pykern.pkdebug import pkdc, pkdp
from pykern import pkcompat
from pykern import pkio
from pykern import pkresource
from pykern import pkyaml

_cache = {}

class Declaration(UserDict.DictMixin):
    """Describe a parameter and its children (if any)

    Attributes:
        children (ordered): OrderedDict of subparameters
        label (str): displayed to the user (default: generated from name)
        name (str): programmatic name
        py_type (type): how to render value (None implies has children)
        required (list or dict): components need this parameter (may be inherited)
        units (str): expected units (default: None)
    """
    def __init__(self, decl, qualifier=None):
        #TODO(robnagler) more type checking: especially required and children
        self.name = decl['name']
        self.qualified_name = qualifier + '.' + self.name if qualifier else self.name
        self.label = self._label(decl)
        self.py_type = self._py_type(decl)
        self.units = self._units(decl)
        self.required = self._required(decl)
        self.children = self._children(decl)
        assert self.children or self.py_type, \
            '{}: declaration must be one type or the other'

    def __repr__(self):
        return 'Declaration("{}")'.format(self.name)

    def __getitem__(self, key):
        if not (self.children and key in self.children):
            raise KeyError(key)
        return self.children[key]

    def keys(self):
        if not self.children:
            return []
        return self.children.keys()

    def _children(self, decl):
        if 'children' not in decl:
            return None
        res = collections.OrderedDict()
        for c in decl['children']:
            if pkcompat.isinstance_str(c):
                d = c
                n = c
            else:
                d = Declaration(c, self.qualified_name)
                n = d.name
            assert n not in res, \
                '{}: duplicate key in {}'.format(n, self.name)
            res[n] = d
        return res

    def _label(self, decl):
        if 'label' in decl:
            return decl['label']
        res = self.name
        res = re.sub(r'(^|_)([a-z])', lambda x: x.group(1) + x.group(2).upper(), res)
        res = re.sub(r'_', ' ', res)
        res = re.sub(r'\bLen\b', 'Length', res)
        res = re.sub(r'\bNum\b', 'Number of', res)
        res = re.sub(r'\bCoord\b', 'Coordinate', res)
        res = re.sub(r'\bAvg\b', 'Average', res)
        return res

    def _py_type(self, decl):
        """Parse py_type to Python type instance"""
        if 'py_type' not in decl:
            return None
        t = decl['py_type']
        try:
            t = getattr(__builtin__, t)
            if isinstance(t, type):
                return t
        except AttributeError:
            pass
        s = re.search(r'^(\w+)\.(\w+)$', decl['py_type'])
        assert s, \
            '{py_type}: py_type for {name} not found'.format(*decl)
        m = importlib.import_module('radtrack.' + s.group(1))
        t = getattr(m, s.group(2))
        assert isinstance(t, type), \
            '{py_type}: py_type for {name} not a type'.format(*decl)
        return t

    def _required(self, decl):
        return decl['required']

    def _units(self, decl):
        return decl['units'] if 'units' in decl else None


class Default(UserDict.DictMixin):

    def __init__(self, value, decl, component, parent_type=None, qualifier=None):
        self.decl = decl
        self.qualified_name = qualifier + '.' + decl.qualified_name if qualifier else decl.qualified_name
        if decl.py_type and not decl.children:
            self.value = _parse_value(value, decl.py_type)
        elif parent_type:
            self.value = _parse_value(decl.name, parent_type)
        self.children = self._children(value, decl, component)

    def iter_leaves(self):
        if not self.children:
            yield self
        else:
            for c in self.children.values():
                for l in c.iter_leaves():
                    yield l

    def iter_leaves(self):
        if not self.children:
            yield self
        else:
            for c in self.children.values():
                for l in c.iter_leaves():
                    yield l

    def iter_nodes(self):
        yield self
        if not self.children:
            return
        for c in self.children.values():
            for l in c.iter_nodes():
                yield l

    def __repr__(self):
        return 'Default("{}")'.format(self.decl.qualified_name)

    def __getitem__(self, key):
        if not (self.children and key in self.children):
            raise KeyError('{}: no key in {}'.format(key, self))
        return self.children[key]

    def keys(self):
        if not self.children:
            return []
        return self.children.keys()

    def _children(self, values, decl, component):
        if not decl.children:
            return None
        res = collections.OrderedDict()
        for child_decl in decl.values():
            if component not in child_decl.required:
                continue
            d = Default(
                values[child_decl.name], child_decl, component, decl.py_type, self.qualified_name)
            res[child_decl.name] = d
        return res


def declarations(file_prefix):
    """Parsed parameter declarations from ``<file_prefix>_declarations.yml``

    Args:
        file_prefix (str): which file to parse

    Returns:
        OrderedDict: mapping of declarations
    """
    return _get(file_prefix, 'declarations', _parse_declarations)


def defaults(file_prefix, decl):
    """Parsed parameter defaults from ``<file_prefix>_defaults.yml``

    Args:
        file_prefix (str): which file to parse

    Returns:
        dict: mapping of default values
    """
    return _get(file_prefix, 'defaults', lambda v, fp: _parse_defaults(v, fp, decl))


def init_params(defaults):
    """Create a tree of default params excluding headings and computed params

    Args:
        defaults (dict): used for initializations

    Returns:
        dict: nested dictionary of params
    """
    res = collections.OrderedDict()
    for k, v in defaults.items():
        res[k] = init_params(v.children) if v.children else v.value
    return res


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
        values = pkyaml.load_resource('{}_{}'.format(file_prefix, which))
        _cache[which] = how(values, file_prefix)
    return _cache[which]


def _parse_declarations(values, file_prefix):
    """Recurse the parsed YAML declarations; convert values and types

    Order preserving so can use for layout.

    Args:
        values (list): raw YAML as a list
        file_prefix (str): which file to parse
    """
    root = Declaration({
        'name': '',
        'children': values,
        'required': None,
    })
    _parse_declarations_link(root, root)
    return root


def _parse_declarations_link(decl, root):
    for k, v in decl.items():
        if not isinstance(v, Declaration):
            decl.children[k] = root[k]
        else:
            _parse_declarations_link(v, root)


def _parse_defaults(values, file_prefix, decl):
    """Recurse the parsed YAML defaults; convert values by declarations

    Args:
        values (list): raw YAML as a list
        file_prefix (str): which file to parse
    Returns:
        dict: parsed YAML
    """
    # Need to parse
    return Default(values, decl, file_prefix)


def _parse_value(v, t):
    if hasattr(t, 'from_anything'):
        return t.from_anything(v)
    return t(v)
