# -*- coding: utf-8 -*-
"""pytest for `radtrack.genesis.rbGenLatFile`

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""

import os
import os.path
import re

import pytest

import numpy as np
from radtrack.genesis import lattice_file

def test_conformance():
    """Read the file and make sure it is formated correctly"""
    fn = 'lattice_file_test.out'
    if os.path.exists(fn):
        os.remove(fn)
    unit_length = 3.1415
    elems = {
        'QF': [
            np.array([1.1, 1.2, 1.3]),
            np.array([2.1, 2.2, 2.3]),
        ],
        'AW': [
            np.array([3.1, 3.2, 3.3]),
            np.array([4.1, 4.2, 4.3]),
            np.array([5.1, 5.2, 5.3]),
        ],
    }
    lattice_file.write(fn, elems, unit_length)
    with open(fn) as f:
        res = f.read()
    def a(p, flags=re.MULTILINE):
        assert re.search(p, res, flags=flags), p + ': no match' 
    a(r'--\nQF    1\.1    1\.2    1\.3    \n')
    a(r'  \nAW    5\.1    5\.2    5\.3    \n$', flags=0)
    a(r'QF +1.1 .*\nQF +2.1 .*\n(?:#.*\n)+AW +3.1 .*\nAW +4.1 .*\nAW +5.1 ')
