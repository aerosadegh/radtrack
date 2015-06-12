# -*- coding: utf-8 -*-
"""pytest for `radtrack.rt_jinja`

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import pytest


def test__template():
    """Verify template formats properly"""
    from radtrack.rt_jinja import _template
    assert 'a\n' == _template('a'), \
        '_template always appends a newine'
    assert 'a\n' == _template('a\n'), \
        '_template does not append an extra newine'
    assert 'a\n b\n' == _template('\n a\n  b'), \
        '_template strips leading spaces up to a point'
    assert '{{b|rt_filter}} $ c{{a|rt_filter}}\n' == _template('$b $ c$a'), \
        '_template replaces "$x" but not "$ x"'

def test_render():
    """Verify render"""
    from radtrack.rt_jinja import render
    p = dict(a=999.0, b=999.0, CdeF=6789, d=.001, e=.000999, f=1000.0)
    assert '999.000 999.0 6789 0.001 9.990e-04 1.000e+03\n' \
        == render('$a {{b}} $CdeF $d $e $f', p), \
        'render converts float magically'
