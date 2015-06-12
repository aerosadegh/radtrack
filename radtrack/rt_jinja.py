# -*- coding: utf-8 -*-
u"""Simplify jinja templating.

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

from pykern.pkdebug import pkdc, pkdi, pkdp
import re

import jinja2


def render(template, params):
    """Parse template for $name and replace with special filter then render

    Since a common case is to render floating point numbers, we
    have a special pattern ``$var`` which is replaced with
    ``{{ var | rt_filter }}``, which maps to the appropriate float filter.

    If the template begins with a newline, leading newlines will be stripped
    from the amount of the first indent, e.g.::

        template = '''
            first line whitespace sets the mark to delete to
            this line will be left indented.
                this line will have four spaces
            another line
        '''

    A trailing newline will always be added.

    Args:
        template (str): what to render
        params (dict): variables to render

    Returns:
        str: rendered template with params.

    """
    template = _template(template)
    je = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    je.filters['rt_filter'] = _rt_filter
    jt = je.from_string(_template(template))
    return jt.render(params)


def _rt_filter(v):
    """Format floats as .3f or .3e depending on size"""
    if type(v) is not float:
        return v
    a = abs(v)
    f = 'e' if a >= 1000 or a < 0.001 else 'f'
    return ('{:.3' + f + '}').format(v)


def _template(t):
    """Parse template"""
    if t.startswith('\n'):
        t2 = t.lstrip()
        i = str(len(t) - len(t2) - 1)
        t = re.sub(
            r'^\s{1,' + i + '}',
            '',
            t2,
            flags=re.IGNORECASE + re.MULTILINE,
        )
    if not t.endswith('\n'):
        t += '\n'
    return re.sub(
        r'\$([a-z]\w*)',
        r'{{\1|rt_filter}}',
        t,
        flags=re.IGNORECASE,
    )
