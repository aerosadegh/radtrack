# -*- coding: utf-8 -*-
"""Invokes RbGlobal.main()

:copyright: Copyright (c) 2015 RadiaBeam Technologies LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""

def main():
    """Invoke RbGlobal with sys.argv"""
    import sys
    import radtrack.RbGlobal
    radtrack.RbGlobal.main(sys.argv)
