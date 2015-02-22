#!/usr/bin/env python
from cx_Freeze import setup, Executable
import glob
import os
import os.path

include_files = []
for pkg in ['APS', 'tex']:
    for root, dirnames, filenames in os.walk(pkg):
        for filename in filenames:
            include_files.append(os.path.join(root, filename))

includes = ['atexit']
buildOptions = dict(
    packages = [], excludes = [], includes=includes, include_files=include_files)

base = 'Win32GUI'

executables = [
    Executable('radtrack-windows.py', base=base, shortcutName='RadTrack', shortcutDir='DesktopFolder')
]

setup(
    name='RadTrack',
    version = '1.0',
    description = 'RadTrack is an open source framework for working with codes that model particle dynamics and electromagnetic radiation',
    options = dict(build_exe = buildOptions),
    executables = executables)
