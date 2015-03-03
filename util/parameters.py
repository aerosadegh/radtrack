# -*- coding: utf-8 -*-
""" Generates parameter configuration

    :copyright: Copyright (c) 2015 RadiaSoft LLC.  All Rights Reserved.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import print_function
from future.utils import viewitems
import re

import argh
import openpyxl

HEADINGS = ['name', 'py_type', 'default', 'units', 'is_primary', 'description']
SHEET_DESCRIPTION = 'desc'
SHEET_ROWS = 'rows'
VALID_TYPES = dict([(t, getattr(__builtins__, t)) for t in ['int', 'str', 'float', 'bool']])
NUMERIC_TYPES = [int, float]
VALID_UNITS = ['m', 'um', 'in']

def generate(file_xlsx):
    params = parse(file_xlsx)
    with open('params.py', 'w') as cfg:
        cfg.write('''"""Configuration generated from {}
"""
'''.format(file_xlsx))
        for sheet, sheet_v in viewitems(params):
            cfg.write('''
class {}:
    """{}"""

'''.format(sheet, sheet_v[SHEET_DESCRIPTION]))
            for param, param_v in viewitems(sheet_v[SHEET_ROWS]):
                v = param_v['default']
                if v is not None:
                    t = param_v['py_type']
                    if t != bool:
                        if t == str:
                            v = 'u' + repr(v)
                        else:
                            v = '{}({})'.format(t.__name__, v)
                cfg.write(u'''    {} = {}
'''.format(param, v))


def parse(file_xlsx):
    """Read file_xlsx and produce an internal tree of sheets and params"""
    wb = openpyxl.load_workbook(file_xlsx)
    res = {}

    def assert_id(name, names, prefix, which):
        assert name, prefix + 'missing ' + which
        assert name not in names, prefix + 'duplicate ' + which
        assert re.search(r'^[a-z][a-z0-9_]*$', name, flags=re.IGNORECASE), \
            prefix + which + ' is invalid python identifer'

    for sheet in wb:
        assert_id(sheet.title, res, str(sheet.title) + ': ', 'sheet name')
        sheet_rows = {}
        res[sheet.title] = {SHEET_ROWS: sheet_rows, SHEET_DESCRIPTION: ''}
        i = -1
        for row in sheet.rows:
            i += 1
            if i == 0:
                res[sheet.title][SHEET_DESCRIPTION] = row[0].value
                continue
            if i == 1:
                for c, h in zip(row, HEADINGS):
                    assert c.value == h, \
                        'mismatched heading: {} != {}'.format(c.value, h)
                continue
            n = row[0].value
            # unicode desc
            # name with space: real desc
            assert_id(
                n, sheet_rows,
                '{}[{}] "{}": '.format(sheet.title, i, n), 'parameter name')
            assert len(row) == len(HEADINGS)
            r = sheet_rows[n] = dict(zip(HEADINGS, map(lambda r: r.value, row)))
            t = r['py_type'] = VALID_TYPES[r['py_type']]
            if r['default'] is not None:
                r['default'] = t(r['default'])
            else:
                assert t != bool, '{}: must have a default value for "bool"'
            u = r['units']
            if u is None:
                assert t not in NUMERIC_TYPES, \
                    '{}: must provide units for "{}"'.format(n, t)
            else:
                assert u in VALID_UNITS, '{}: has unknown units "{}"'.format(n, u)
                assert t in NUMERIC_TYPES, \
                    '{}: units not acceptable for "{}"'.format(n, t)

        assert i > 2, '{}: too few rows'.format(sheet.title)
    return res


if __name__ == '__main__':
    argh.dispatch_commands([parse, generate])
