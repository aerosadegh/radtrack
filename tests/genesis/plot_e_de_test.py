# -*- coding: utf-8 -*-
"""pytest for `radtrack/use_cases/genesis/lcls`

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""

import os
import os.path
import subprocess

import pytest

import numpy as np
import radtrack
# import use_cases.genesis.lcls.plot_e_de

from pykern import pkunit

def test_run_lcls():
    """Run Genesis on an LCLS input file"""

    with pkunit.save_chdir_work():
        print ' about to call GENESIS'
        subprocess.call(["cp", "../../../use_cases/genesis/lcls/lcls.in", "."])
        subprocess.call(["genesis", "-i", "lcls.in"])
        print ' GENESIS subprocess has returned'

        out_file_exists = os.path.exists("./lcls.out.h5")
        assert out_file_exists == True

def test_read():
    """Read the file"""
    file_name = "../../../use_cases/genesis/lcls/lcls.out.h5"
    if os.path.exists(file_name):
        print ' file exists!'
#        os.remove(file_name)
