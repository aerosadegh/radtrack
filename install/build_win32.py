#!/usr/bin/env python
import glob
import os
import os.path
import shutil
import subprocess
import sys

exe_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(exe_dir)
os.chdir(root_dir)
build_dir = 'build_win32'
try:
    shutil.rmtree(build_dir)
except:
    pass
assert not os.path.exists(build_dir), build_dir + ': unable to delete'
install_src_dir = 'install'
cx_freeze_py = 'cx_freeze_win32.py'
shutil.copytree('.', build_dir, ignore=shutil.ignore_patterns(build_dir, '.git', install_src_dir))
for f in glob.glob(os.path.join(install_src_dir, '*_win32.py')):
    shutil.copy2(f, build_dir)

os.chdir(build_dir)
sp = subprocess.Popen(['python', cx_freeze_py, 'bdist_msi'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
out = sp.stdout.read()
rc = sp.wait()
if rc != 0:
    sys.stderr.write(out)
    sys.stderr.write('Build failed\n')
    sys.exit(rc)
