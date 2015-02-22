#!/usr/bin/env python
import glob
import os
import os.path
import shutil
import sys

exe_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(exe_dir)
os.chdir(root_dir)
build_dir = 'build_win32'
try:
    shutil.rmtree(build_dir)
except:
    pass
install_src_dir = 'install'
cx_freeze_py = 'cx_freeze_win32.py'
shutil.copytree('.', build_dir, ignore=shutil.ignore_patterns(build_dir, '.git', install_src_dir))
shutil.copy2(os.path.join(install_src_dir, cx_freeze_py), build_dir)

aps_build_dir = 'APS'
tex_exe = 'tex.exe'
exe_to_dst = {
    'sddsplot.exe': aps_build_dir,
    'elegant.exe': aps_build_dir,
    tex_exe: 'tex',
}
aps_build_dir = os.path.join(build_dir, aps_build_dir)
os.mkdir(aps_build_dir)

for exe, dst in exe_to_dst.iteritems():
    for p in os.getenv('PATH').split(os.pathsep):
        abs_exe = os.path.abspath(os.path.join(p, exe))
        if os.path.exists(abs_exe):
            src = os.path.dirname(abs_exe)
            dst = os.path.join(build_dir, dst)
            if exe == tex_exe:
                src = os.path.join(src, '..\..')
            else:
                dst = os.path.join(dst, os.path.basename(src))
            print src + ' ' + dst
            shutil.copytree(src, dst)
            break
os.chdir(build_dir)
# call python cx_freeze_py bdist_msi
