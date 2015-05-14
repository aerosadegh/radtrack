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
git clone https://github.com/radiasoft/pykern.git
cd pykern
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

#### Running tests

You can run the tests with either `py.test` or `python setup.py test` in the main
directory. To run an individual test, go to the directory and run `py.test <file>`.

One trick that's useful when debugging is:

```
py.test --capture=no some_test.py
```

This will allow you to watch `stdout` and `stderr` in real-time as the test runs.
Normally, `py.test` captures output and only writes it if there is a failure.

#### Installing Alpha on Mac

Currently only Mac OS X (Darwin) install:

```
curl -s -L https://raw.githubusercontent.com/radiasoft/radtrack-installer/master/darwin.sh | bash
```
