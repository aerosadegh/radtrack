# -*- coding: utf-8 -*-
"""Provides groups of parameters for components of RadTrack.

You can refer to the documentation in `radtrack.util.parameters_generated`,
but you import this module to get all the values.

Example:
    You import this module and instantiate::

        import radtrack.util.parameters as params

        p = params.SomeGroup()
        do something with p.some_value

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""

#TODO(robnagler): test file dates and regenerate if not there before importing
import os.path
try:
    from radtrack.util.parameters_generated import *
except ImportError:
    import radtrack.util.gen_parameters
    radtrack.util.gen_parameters.parse_and_write(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'parameters.xlsx'
        )
    )
    from radtrack.util.parameters_generated import *
