#### Windows build

Put all files in `\Program Files (x86)`.

* Install Anaconda 2.x
* conda install pip
* pip install cx_freeze
* install elegant
* install sdds
* install MikTeX

Then run as user `Win` (or whatever your user name is)

```bat
cd "c:\Program Files (x86)"
python c:\Users\Win\src\radiasoft\radtrack\install\radtrack_pkg_win32.py zip-all
del /s/q/f c:\Users\Win\src\radiasoft\foss-mirror\radtrack_pkg
move radtrack_pkg c:\Users\Win\src\radiasoft\foss-mirror\radtrack_pkg
cd c:\Users\Win\src\radiasoft\radtrack
python install\cx_freeze_win32.py bdist_msi
```
