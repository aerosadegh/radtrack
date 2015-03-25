# -*- coding: utf-8 -*-
"""Manage external resources

This module manages resources


:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""

import errno
import os.path
import pkg_resources
import re

def filename(relative_filename):
    """Return the filename to the resource

    Args:
        relative_filename (str): file name relative to package_data directory.

    Returns:
        str: absolute path of the resource file
    """
    pkg = re.match(r'^\w+', __name__).group(0)
    fn = os.path.join('package_data', relative_filename)
    res = pkg_resources.resource_filename(pkg, fn)
    if not os.path.isfile(res):
        raise IOError((errno.ENOENT, 'resource does not exist', res))
    return res
