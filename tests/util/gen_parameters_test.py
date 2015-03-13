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
    """Verify parser fails when spreadsheets are in error"""
    for xlsx in glob.glob('deviance/*.xlsx'):
        with pytest.raises(AssertionError):
            gen_parameters.parse_and_write(xlsx, 'deviance_out.py')


def test_conformance():
    """Read sample files, and verify the output is done correctly"""
    out_py = gen_parameters.parse_and_write('conformance/metadata1.xlsx', 'metadata1_out.py')
    m = _import(out_py)


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
