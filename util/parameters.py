# -*- coding: utf-8 -*-
""" Generates parameter configuration
    
    :copyright: Copyright (c) 2015 RadiaSoft LLC.  All Rights Reserved.
    :license: MIT, see LICENSE for more details.
"""

import re

import argh
import openpyxl

def parse(file_xlsx):
    """Read file_xlsx and produce an internal tree of sheets and params"""
    wb = openpyxl.load_workbook(file_xlsx)
    res = {}
    headings = ['parameter', 'py_type', 'units', 'is_primary', 'description']
    valid_types = ['int', 'str', 'float', 'bool']
    valid_units = ['m', 'in', '', 'secs']

    def assert_id(name, names, prefix, which):
        assert name, prefix + 'missing ' + which
        assert name not in names, prefix + 'duplicate ' + which
        assert re.search(r'^[a-z][a-z0-9_]*$', name, flags=re.IGNORECASE), \
            prefix + which + ' is invalid python identifer'

    for sheet in wb:
        assert_id(sheet.title, res, str(sheet.title) + ': ', 'sheet name')
        sheet_res = res[sheet.title] = {}
        first = True
        i = -1
        for row in sheet.rows:
            i += 1
            if i == 0:
                for c, h in zip(row, headings):
                    assert c.value == h, 'mismatched heading: {} != {}'.format(c.value, h)
                first = False
                continue
            n = row[0].value
            assert_id(n, sheet_res, '{}[{}] "{}": '.format(sheet.title, i, n), 'parameter name')
            assert len(row) == len(headings)
            sheet_res[n] = dict(zip(headings, map(lambda r: r.value, row)))
            
    return str(res)

if __name__ == '__main__':
    argh.dispatch_commands([parse])
