# -*- coding: utf-8 -*-
"""pytest for `radtrack.util.resource`

:copyright: Copyright (c) 2015 RadiaBeam Technologies, LLC.  All Rights Reserved.
:license: Apache, see license.md for more details.
"""
import os.path

import pytest

import radtrack.util.resource as resource

def test_deviance():
    """Make sure we can't find a resource that doesn't exist"""
    with pytest.raises(IOError):
        resource.filename('not_found_resource')

def test_conformance():
    """Find resource we know about. Make sure it exists"""
    assert os.path.isfile(resource.filename('defns.rpn')), 'defns.rpn not found'
