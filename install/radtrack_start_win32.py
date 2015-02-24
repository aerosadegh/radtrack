import os
import os.path
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(sys.executable)))
subprocess.check_call([r'Anaconda\pythonw.exe', 'radtrack_win32.py'])
