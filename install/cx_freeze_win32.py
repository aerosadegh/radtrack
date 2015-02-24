#!/usr/bin/env python
import glob
import os
import os.path

import cx_Freeze
import msilib

# Using the same upgrade code enforces uninstalling previous version
UPGRADE_CODE = '{4F4F1C8E-BB7E-11E4-8C00-080027D2CC95}'

include_files = list(glob.glob('*.py'))
include_files.extend(list(glob.glob(r'install\*win32.py')))
include_files.append(('RadTrack', 'RadTrack'))
tex_exe = 'tex.exe'
exe_to_dst = {
    'sddsplot.exe': r'APS\SDDS Plot',
    'elegant.exe': r'APS\Elegant',
    tex_exe: 'tex',
    'python.exe': 'Anaconda',
}
for exe, dst in exe_to_dst.iteritems():
    for p in os.getenv('PATH').split(os.pathsep):
        abs_exe = os.path.abspath(os.path.join(p, exe))
        if os.path.exists(abs_exe):
            src = os.path.dirname(abs_exe)
            if exe == tex_exe:
                src = os.path.dirname(os.path.dirname(src))
            include_files.append((src, dst))
            break

build_exe_options = dict(
    packages = [], excludes = [], includes=[], include_files=include_files,
    silent=True
)
bdist_msi_options = dict(
    upgrade_code=UPGRADE_CODE)

base = 'Win32GUI'

executables = [
    cx_Freeze.Executable(r'install\radtrack_start_win32.py', base=base, shortcutName='RadTrack', shortcutDir='DesktopFolder')
]

class local_bdist_msi(cx_Freeze.bdist_msi):
    """Override add_config so can set the "start in" directory for the
    shortcut. See cx_Freeze.windist
    """
    def add_config(self, fullname):
        # Hardwired b/c there is only one Executable() above
        index = 0
        baseName = os.path.basename(
            self.distribution.executables[index].targetName)
        # http://stackoverflow.com/questions/24195311/how-to-set-shortcut-working-directory-in-cx-freeze-msi-bundle
        msilib.add_data(
            self.db, 'Shortcut',
            [('S_APP_%s' % index, 'DesktopFolder',
              'QWeb', 'TARGETDIR',
              '[TARGETDIR]%s' % baseName,
              None, None, None,
              None, None, None, 'TARGETDIR')])
        cx_Freeze.bdist_msi.add_config(self, fullname)

cx_Freeze.setup(
    # cmdclass={'bdist_msi': local_bdist_msi},
    name='RadTrack',
    version = '1.0',
    description = 'RadTrack is an open source framework for working with codes that model particle dynamics and electromagnetic radiation',
    options = dict(
        build_exe = build_exe_options,
        bdist_msi= bdist_msi_options
    ),
    executables = executables)
