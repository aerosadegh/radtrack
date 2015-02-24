from __future__ import print_function
import datetime
import glob
import os
import os.path
import shutil
import sys
import time
import traceback
import win32com.shell.shell as shell
import win32event
import zipfile

import argh

AS_ADMIN = 'as_admin'
SRC_DIR = 'radtrack_pkg'
DST_DIRS = ['APS', 'Anaconda', 'tex']
SUFFIX = '.zip'
UNINSTALL_SENTINEL = 'uninstalled'

def uninstall_check():
    """Remove old install directories, because cx_freeze does not have an
    uninstaller script
    """
    if os.path.exists(UNINSTALL_SENTINEL):
        return
    print('Cleaning up previous installation')
    for d in DST_DIRS:
        if os.path.exists(d):
            print('Removing: ' + d)
            shutil.rmtree(d)
    with open(UNINSTALL_SENTINEL) as f:
        f.write(str(datetime.datetime.now()))

def unzip_all():
    """Unzip all the files in DIR and remove zip files (re-entrant)"""
    zip_names = glob.glob(os.path.join(SRC_DIR, '*' + SUFFIX))
    is_running_as_admin = sys.argv[-1] == AS_ADMIN
    if not zip_names:
        return not is_running_as_admin
    if not is_running_as_admin:
        script = sys.argv[0]
        if script:
            script = os.path.abspath(script)
        params = '"' + '" "'.join([script] + sys.argv[1:] + [AS_ADMIN]) + '"'
        p = shell.ShellExecuteEx(
            lpVerb='runas',
            lpFile=sys.executable,
            nShow=5,
            lpParameters=params)
        win32event.WaitForSingleObject(p['hProcess'], -1)
        return True

    # There should be a stdout here
    print('Post install: unzipping support packages')
    try:
        uninstall_check()
        for zip_name in zip_names:
            print(zip_name)
            with zipfile.ZipFile(zip_name, 'r') as z:
                for m in z.infolist():
                    if os.path.exists(m.filename):
                        os.remove(m.filename)
                    z.extract(m)
            os.remove(zip_name)
        os.rmdir(SRC_DIR)
    except:
        traceback.print_exc()
    finally:
        time.sleep(5)
    return False

def zip_all():
    """Create zip files for APS, Anaconda, tex in SRC_DIR"""
    shutil.rmtree(SRC_DIR, ignore_errors=True)
    os.mkdir(SRC_DIR)
    for d in DST_DIRS:
        zip_index = 1
        def next_file():
            for root, dirs, files in os.walk(d):
                for f in files:
                    yield os.path.join(root, f)
        nf = next_file()
        def create_zip(zip_name):
            # Ignore the unlikely empty zip file case
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
                print(zip_name)
                size = 0
                for file_count in range(1000):
                    try:
                        n = nf.next()
                        z.write(n)
                        # zip members have unix-style slashes
                        n = n.replace('\\', '/')
                        size += z.getinfo(n).compress_size
                        # Keep well under 100MB to avoid hitting github limit
                        if size > 50000000:
                            break
                    except StopIteration:
                        return False
            return True

        while True:
            zip_name = '{}{:0>4}{}'.format(d, zip_index, SUFFIX)
            zip_index += 1
            if not create_zip(os.path.join(SRC_DIR, zip_name)):
                break


if __name__ == '__main__':
    argh.dispatch_commands([zip_all, unzip_all])
