import os
import os.path
import sys

exe_dir = os.path.dirname(os.path.abspath(__file__))
our_paths = [
    r'Anaconda',
    r'Anaconda\Scripts',
    r'APS\Elegant',
    r'APS\Elegant\MinGW',
    r'APS\SDDS ToolKit',
    r'tex\miktex\bin']
new_path = [os.path.join(exe_dir, d) for d in our_paths]

our_exes = [
    'anaconda.bat',
    'elegant.exe',
    'python.exe',
    'SDDS1.dll',
    'sddsplot.exe',
     'tex.exe']
for p in os.getenv('PATH').split(os.pathsep):
    if not any([os.path.exists(os.path.join(p, e)) for e in our_exes]):
        new_path.append(p)

os.environ['PATH'] = os.pathsep.join(new_path)

import RbGlobal
RbGlobal.main(sys.argv)
