### RadTrack

RadTrack is an open source framework for working with codes that model particle dynamics and electromagnetic radiation.

#### Setting Up Development

This script should set up a development environment. It's written in Unix
terms, but should be translatable to Windows:

```bash
# Assumes running in virtualenv an PyQt4 is installed
pip install numpy
cd
mkdir src
cd src
mkdir biviosoftware
cd biviosoftware
git clone https://github.com/biviosoftware/pybivio
cd pybivio
python setup.py develop
cd ../..
mkdir radiasoft
cd radiasoft
git clone https://github.com/radiasoft/radtrack
cd radtrack
python setup.py develop
rm -f radtrack/dcp/sdds*
cp install/fedora/sdds* $(python -c 'from distutils.sysconfig import get_python_lib as x; print x()')
```

#### Installing Alpha on Mac

Currently only Mac OS X (Darwin) install:

```
curl -s -L https://raw.githubusercontent.com/radiasoft/radtrack-installer/master/darwin.sh | bash
```
