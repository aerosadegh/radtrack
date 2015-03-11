# -*- coding: utf-8 -*-
""" pytest for `radtrack.util.gen_parameters`

    :copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
    :license: Apache, see license.md for more details.
"""

import glob
import os
import os.path

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
    out_py = gen_parameters.parse_and_write('conformance/metadata1.xlsx', 'conformance/metadata1_out.py')
    with open(out_py, 'r') as f:
        pass
