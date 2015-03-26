# -*- coding: utf-8 -*-
"""Creates a lattice file for Genesis

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""

import os
import copy
import jinja2


def write(filename, elems, unit_length):
    """Write the lattice file in Genesis format.

    Args:
        filename (str): output; will be removed, if exists
        elems (dict): QF (Quads) and AW (Undulators) specification
        unit_length (float): usually the undulator period
    """
    params = copy.copy(elems)
    params['unit_length'] = unit_length
    if os.path.lexists(filename):
        os.remove(filename)
    # Note: trailing whitespace
    template = '''? VERSION = 1.0
? UNITLENGTH = {{ unit_length }}
#
# Quads:
# QF    dB/dx       L        space
#--------------------------------------
{% for quad_array in QF %}
QF    {{ quad_array|fmt_array }}
{% endfor %}
#
# Undulators:
# AW    AW0       L        space
#--------------------------------------
{% for und_array in AW %}
AW    {{ und_array|fmt_array }}
{% endfor %}
'''
    je = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    je.filters['fmt_array'] = lambda a: ''.join(str(v) + '    ' for v in a)
    jt = je.from_string(template)
    with open(filename, 'w') as f:
        f.write(jt.render(params))
