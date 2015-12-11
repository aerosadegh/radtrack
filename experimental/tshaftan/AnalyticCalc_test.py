# -*- coding: utf-8 -*-
u"""PyTest for :mod:`radiasoft.AnalyticCalc`

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import os
import pytest

from pykern.pkdebug import pkdc, pkdp
from pykern import pkunit

from radtrack.srw.AnalyticCalc import IDWaveLengthPhotonEnergy

def test_IDWaveLengthPhotonEnergy():
    (Kx, Ky, lam_r, e_ph) = IDWaveLengthPhotonEnergy(
        lam_u=0.1, Bx=1, By=2, Gam=6000)
    _assert(18.68, Kx)


def _assert(expect, actual, expected_error=0.001):
    assert expected_error > abs(expect/actual - 1)
