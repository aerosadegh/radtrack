# -*- coding: utf-8 -*-
"""Invokes `radtrack.RbGlobal.call_main`

:copyright: Copyright (c) 2015 RadiaBeam Technologies LLC.  All Rights Reserved.
:license: Apache, see LICENSE for more details.
"""

def main():
    """Invoke `radtrack.RbGlobal.call_main` in beta test mode."""
    import radtrack.RbGlobal
    radtrack.RbGlobal.main(project_file=None, beta_test=True)

if __name__ == '__main__':
    main()
