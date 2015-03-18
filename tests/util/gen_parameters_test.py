# -*- coding: utf-8 -*-
"""pytest for `radtrack.util.gen_parameters`

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see license.md for more details.
"""

import glob
import importlib
import os
import os.path
import sys

import pytest

import radtrack.util.gen_parameters as gen_parameters

def setup_module():
    """chdir to where the test spreadsheets are"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


def test_deviance():
    """Verify parser fails when spreadsheet is in error.

    The files are in the deviance/ subdirectory. The name of the files
    explains the type of assertion expected.
    """
    for xlsx in glob.glob('deviance/*.xlsx'):
        with pytest.raises(AssertionError):
            gen_parameters.parse_and_write(xlsx, 'deviance_out.py')


def test_conformance():
    """Read sample files, and verify the generated python is correct

    The files are located in conformance/ subdirectory. All files
    should parse without exceptions.
    """
    out_py = gen_parameters.parse_and_write(
        'conformance/metadata1.xlsx', 'metadata1_out.py')
    m = _import(out_py)
    assert m.sect1().int_in == 1, 'default is not valid'
    assert m.sect1(int_in=3).int_in == 3, 'override of default invalid'
    assert type(m.sect2().arPrecF_1) == float
    assert m.sect2().arPrecF_1 == -1.3
    assert m.sect1().Is_Cap == True, \
        'validate type conversion and default'
    assert m.sect1(Is_Cap=0).Is_Cap == False, \
        '__setattr__ converts value'
    assert m.sect1(Is_Cap=None).Is_Cap is None, \
        '__setattr__ allows None'
    assert m.META.sect1.description == u'sect1 description'
    assert m.META.sect1.py_name == 'sect1'
    assert m.META.sect1.attrs.int_in.py_name == 'int_in'
    assert m.META.sect1.attrs.int_in.description == u'an integer measuring inches'
    assert m.META.sect1.attrs.int_in.display_name == 'int_in'
    assert m.META.sect1.attrs.int_in.is_primary == True, \
        'is_primary must be a bool and True'
    assert m.META.sect1.attrs.int_in.units == 'in'
    assert m.META.sect1.attrs.float_um.display_name == u'μMeter'


def _import(module_path):
    """Import a python file which is not coupled to a directory

    Args:

        module_path (str): filename of the form "dir/foo.py"

    Returns:

        module: the imported module instance
    """
    sys.path.insert(0, os.path.dirname(module_path))
    try:
        b = os.path.splitext(os.path.basename(module_path))[0]
        return importlib.import_module(b)
    finally:
        sys.path.pop(0)
