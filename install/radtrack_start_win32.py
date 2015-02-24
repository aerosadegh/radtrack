import os
import os.path
import subprocess
import sys

import radtrack_pkg_win32

d = sys.argv[0]
if not len(d):
    d = sys.executable
os.chdir(os.path.dirname(os.path.abspath(d)))
if radtrack_pkg_win32.unzip_all():
    subprocess.check_call([r'Anaconda\pythonw.exe', 'radtrack_win32.py'])
