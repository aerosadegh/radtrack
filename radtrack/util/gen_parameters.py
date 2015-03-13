# -*- coding: utf-8 -*-
"""Generates parameter configuration for RadTrack from a spreadsheet.

Translates ``radtrack/util/parameters.xlsx`` to ``radtrack/util/parameters.py``,
which is a collection of classes holding state.

How to import generated class::

    import radtrack.util.parameters as params

:copyright: Copyright (c) 2015 RadiaBeam Technologies LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""

from __future__ import print_function
from future.utils import viewitems
import __builtin__
import keyword
import os.path
import re
import sys

import openpyxl

#: Order of the headings on each sheet of parameters.xlsx.
HEADINGS = [
    'py_name', 'display_name', 'py_type', 'default', 'units', 'is_primary', 'description']

#: Which types are valid
VALID_TYPES = [bool, float, int, str];

#: Map valid types from their names to classes
NAME_TO_TYPE = dict([(t.__name__, t) for t in VALID_TYPES])

#: The types which must have units associated with them. Other types do not have units.
TYPES_WITH_UNITS = [int, float]

#TODO(robnagler): these should be objects
#: Names of units.
VALID_UNITS = ['in', 'm', 'um']

#: File extension for output file name
OUT_FILENAME_SUFFIX = '_generated.py'

#: Converts units unicode properly independent of Python version
NAME_TO_UNITS = dict(zip(VALID_UNITS, VALID_UNITS))

#: Names needed in the parameters.py namespace
RESERVED_WORDS = ['attrs', 'META']

def parse_and_write(parameters_xlsx, parameters_py=None):
    """Parse parameters_xlsx and generate parameters_py

    Args:
        parameters_xlsx (str): Excel file to parse. Must match `HEADINGS`.
        parameters_py (str): name of the python file (used for testing)


    Returns:
        str: absolute path for parameters_py

    (parameters_py is used for testing.)
    """
    parsed = _parse(parameters_xlsx)
    out_filename = parameters_py
    if out_filename is None:
        out_filename = os.path.splitext(parameters_xlsx)[0] + OUT_FILENAME_SUFFIX
    if not os.path.isabs(out_filename):
        out_filename = os.path.abspath(out_filename)
    with open(out_filename, 'w') as out:
        _write_header(parameters_xlsx, out)
        _write_meta(parsed, out)
        _write_classes(parsed, parameters_xlsx, out)
    return out_filename


def _parse(parameters_xlsx):
    """Read parameters_xlsx and produce an internal tree of sheets and params"""
    err_prefix = parameters_xlsx
    all_ids = []
    try:
        wb = openpyxl.load_workbook(parameters_xlsx)
        res = {}
        err_prefix_file = err_prefix
        for raw_sheet in wb:
            err_prefix = '{}, sheet {}'.format(err_prefix_file, raw_sheet.title)
            err_prefix_sheet = err_prefix
            st = _parse_id(raw_sheet.title, res, 'sheet title', all_ids)
            res[st] = sheet = {
                'py_name': st,
                'attrs': {},
            }
            for row_num, raw_row in enumerate(raw_sheet.rows, start=1):
                err_prefix = '{}, row {}'.format(err_prefix_sheet, row_num)
                row = map(lambda r: r.value, raw_row)
                if row_num == 1:
                    sheet['description'] = _parse_description(row[0])
                elif row_num == 2:
                    _parse_headings(row)
                else:
                    r = _parse_param(row, sheet, all_ids)
                    sheet['attrs'][r['py_name']] = r
            assert row_num > 2, 'too few rows'
        return res
    except Exception as e:
        raise type(e), type(e)('{}: {}'.format(err_prefix, e)), sys.exc_info()[2]


def _parse_description(value):
    """Verify sheet description is defined and not too short"""
    min_len = 10
    assert value is not None and len(value) >= min_len, \
        '{}: description must be at least {} chars, but is only {}'.format(
            value, min_len, len(value))
    return value


def _parse_headings(row):
    """Do the headings match for this sheet?"""
    for cell, h in zip(row, HEADINGS):
        assert cell == h, \
            'mismatched heading: expected {}, but got {}'.format(h, cell)


def _parse_id(name, names, which, all_ids):
    """Verify sheet or parameter name is a valid identifier and not a duplicate"""
    # Ensure it's ascii
    def _msg(fmt):
        return fmt.format(which)
    name = name.encode('ascii')
    assert name, _msg('missing {}')
    assert name not in names, _msg('duplicate {}')
    assert re.search(r'^[a-z][a-z0-9_]*$', name, flags=re.IGNORECASE), \
        _msg('{} is invalid Python identifer')
    assert not keyword.iskeyword(name), _msg('{} is a Python keyword')
    assert not hasattr(__builtin__, name), _msg('{} is a Python builtin')
    assert name not in all_ids, _msg('{} matches another identifier')
    # Note this includes "description", which is also defined for sheets
    assert name not in HEADINGS, _msg('{} matches a heading label')
    assert name not in RESERVED_WORDS, _msg('{} matches a reserved word')
    all_ids.append(name)
    return name


def _parse_param(row, sheet, all_ids):
    """Parse a parameter row, validating type, default, and py_name"""
    assert len(row) == len(HEADINGS), \
        'incorrect number of columns ({})'.format(len(row))
    row = dict(zip(HEADINGS, row))
    row['py_name'] = _parse_id(row['py_name'], sheet['attrs'], 'parameter name', all_ids)
    row['py_type'] = _parse_param_type(row)
    row['default'] = _parse_param_default(row)
    row['units'] = _parse_param_units(row)
    row['display_name'] = _parse_param_display_name(row)
    row['description'] = _parse_description(row['description'])
    row['is_primary'] = _parse_param_is_primary(row)
    return row


def _parse_param_default(row):
    """Verify parameter default matches type"""
    if row['default'] is None:
        return None
    # Might be unicode so just return the value
    if row['py_type'] == str:
        return row['default']
    return row['py_type'](row['default'])


def _parse_param_display_name(row):
    """Verify there is a display_name else copy py_name"""
    v = row['display_name']
    if v is None or len(v) == 0:
        return row['py_name']
    return v


def _parse_param_is_primary(row):
    """Verify is_primary is a boolean"""
    return bool(row['is_primary'])

def _parse_param_type(row):
    """Is type in the known list?"""
    assert row['py_type'] in NAME_TO_TYPE, \
        '{}: invalid py_type'.format(row['py_type'])
    return NAME_TO_TYPE[row['py_type']]


def _parse_param_units(row):
    t = row['py_type']
    u = row['units']
    if u is None:
        assert t not in TYPES_WITH_UNITS, \
            'must provide units for type "{}"'.format(t)
        return None
    assert u in VALID_UNITS, 'unknown units "{}"'.format(u)
    assert t in TYPES_WITH_UNITS, \
        'units "{}" not acceptable for type "{}"'.format(u, t)
    return NAME_TO_UNITS[u]


def _value_as_str(value):
    """Return a valid python string for value

    Args:
        value (object): value to convert

    Returns:
        str or unicode: python code for value
    """
    if value is None:
        return repr(value)
    t = type(value)
    if t == bool:
        return repr(value)
    if t == type:
        return value.__name__
    if t == str or t == unicode:
        return repr(value)
    return '{}({})'.format(t.__name__, repr(value))


def _write_classes(parsed, parameters_xlsx, out):
    """Write the classes for each sheet"""
    for sheet, attrs in _viewitems_sorted(parsed):
        _write_class(sheet, attrs, out)

def _write_class(name, attrs, out):
    """Write the class header then params"""
    template = '''

class {}(object):
    """{}
    """

    def __init__(
        self,
'''
    out.write(template.format(name, attrs['description']))
    for param, param_attrs in _viewitems_sorted(attrs['attrs']):
        _write_class_init_arg(param, param_attrs, out)
    template = '''
    ):
'''
    out.write(template)
    for param, param_attrs in _viewitems_sorted(attrs['attrs']):
        _write_class_init_attr(param, param_attrs, out)

def _write_class_init_arg(name, attrs, out):
    """Ouptut a single arg initialized with its default value"""
    d = _value_as_str(attrs['default'])
    out.write('        {}={},\n'.format(name, d))


def _write_class_init_attr(name, attrs, out):
    """Ouptut a single assignment to self from an arg"""
    out.write(
        '        #: {}\n        self.{} = {},\n'.format(
            attrs['description'], name, name),
    )


def _write_header(parameters_xlsx, out):
    """Output module docstring"""
    template = '''# -*- coding: utf-8 -*-
"""See `radtrack.util.parameters` DO NOT IMPORT THIS MODULE.

DO NOT EDIT THIS FILE. It is automatically generated from {}.
"""
'''
    out.write(template.format(parameters_xlsx))


def _write_meta(parsed, out):
    """Output ``_init_meta()`` which creates a collection of namedtuples"""
    template = '''
from collections import namedtuple

def _n(name, attrs):
    """Create namedtuple instance from dict"""
    return namedtuple('_class_' + name, sorted(attrs.keys()))(**attrs)

#: Meta data for all the classes and parameters as namedtuples.
META = '''
    out.write(template)
    indent_inc = ''.ljust(4)

    def write_attrs(name, attrs, indent, terminator):
        out.write("_n('{}', {{\n".format(name))
        indent += indent_inc
        for k, v in _viewitems_sorted(attrs):
            out.write("{}'{}': ".format(indent, k))
            if type(v) == dict:
                write_attrs(k, v, indent, ',')
            else:
                out.write(_value_as_str(v))
                out.write(',\n')
        out.write('{}}}){}\n'.format(indent[:-len(indent_inc)], terminator))

    write_attrs('META', parsed, '', '')

def _viewitems_sorted(items):
    """Call viewitems and sort the result by the key

    Args:
        items (dict): to iterate and sort

    Returns:
        list of tuples: what to iterate over
    """
    return sorted(list(viewitems(items)), key=lambda x: str.lower(x[0]))
