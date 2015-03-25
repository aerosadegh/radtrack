# -*- coding: utf-8 -*-
"""Fix sdds imports

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""
try:
    import sdds
    import sddsdatamodule as sddsdata
except ImportError:
    import radtrack.dcp.sdds as sdds
    import radtrack.dcp.sddsdata as sddsdata
