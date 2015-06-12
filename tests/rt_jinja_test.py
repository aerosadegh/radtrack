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
