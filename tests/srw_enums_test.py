# -*- coding: utf-8 -*-
"""pytest for `radtrack.srw_enums`

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import pytest

from radtrack import srw_enums


def test_density_method():
    """Verify a couple of values exist"""
    d = srw_enums.DensityComputation
    assert d(1) == d.NEAR_FIELD, \
        'DensityMethod.NEAR_FIELD should be 1'
    assert d(2) == d.FAR_FIELD, \
        'DensityMethod.FAR_FIELD eq enum iself'
    assert d(2) == 'FAR_FIELD', \
        'DensityMethod.FAR_FIELD has name FAR_FIELD'
    assert d(2) == 2, \
        'DensityMethod.FAR_FIELD == 2'
    assert d(2) != 1, \
        'DensityMethod.FAR_FIELD != 1'
    assert d(2) > 1, \
        'DensityMethod.FAR_FIELD > 1'
    assert d(2) >= d(1), \
        'DensityMethod.FAR_FIELD >= 1'
    assert d(1) < 'FAR_FIELD', \
        'DensityMethod.FAR_FIELD > 1'
    assert d(1) <= d(2), \
        'DensityMethod.FAR_FIELD >= 1'
    with pytest.raises(KeyError) as e:
        if d(2) != 'no match':
            pass
    with pytest.raises(ValueError) as e:
        if d(2) != 31456:
            pass
    assert d.from_anything('NEAR_FIELD').value == 1, \
        'from_anything(NEAR_FIELD) should return an enum with value 0'
    assert d.from_anything(2) == d.FAR_FIELD, \
        'from_anything(1) should return FAR_FIELD'
