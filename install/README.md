###

Each subdirectory is used to build a single application in its own container.
The code has been tested with Docker, but we can add a Vagrant version if so
desired.

Once Docker is installed (see below), run this command:

```
# sh <subdirectory>/docker-build.sh
```

For example, to build elegant:

```
sh elegant/docker-build.sh
```

This will create an Docker image called radiasoft/<directory>, e.g. radiasoft/elegant.

To run the image, you become root:

```
# sh <subdirectory>/docker-run.sh
```

This will create a new container if one doesn't exist. Otherwise, it will
create a new container.

For example, to run elegant:

```
sh elegant/docker-run.sh
```

When you exit the shell, it will stop the container. You can restart the
container (and pick up where you left off) by re-executing `run.sh`.

### Install Docker

On a CentOS, you install docker this way:

```
sh install-centos-docker.sh
```

This will download the latest docker and start the docker daemon.

#### Windows build

* Install Anaconda 2.x
* conda install pip
* pip install cx_freeze
* install elegant
* install sdds
* install MikTeX
```

#### Doc

Need to make a docs directory. Using
[Google style guide](https://google-styleguide.googlecode.com/svn/trunk/pyguide.html)
and [example](http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html)

[See why Sphinx Napoleon](http://sphinxcontrib-napoleon.readthedocs.org/en/latest/) is
better way to generate API docs.

Install sphinx:

```bash
pip install sphinx sphinxcontrib-napoleon
mkdir docs
sphinx-quickstart
# docs is subdirectory, use source & build
```

* Add `'sphinxcontrib.napoleon'` to `extensions = []` to `source/conf.py`
* Add these lines to `source/conf.py`:
```python
napoleon_include_special_with_doc = True
napoleon_include_private_with_doc = True
```
* Add `modules` (output of napoleon) to `source/index.rst` after `toctree`:

```rst
.. toctree::
   :maxdepth: 2
   modules
```

This part should be in a bash script which is called by `travis.yml`. Whole thing
probably should be automated in a project setup (TODO(nagler): look around for this)

```bash
sphinx-apidoc -f -o docs/source radtrack
cd docs
make html
```

Some rules:

* `__init__` methods should not be documented. Use class level docstring. Napoleon is
hardwired to not include `__init__`.
* Use docstrings for attributes in __init__ like this:
```python
self.param1 = arg1
"""some description of param1"""
```
* Use `#:` for class and module attribute doc:
```python
#: some docstring for the attr
the_attr = 33
```

#### Linux Build

[Build PyQt4 into your virtualenv](http://www.expobrain.net/2013/01/23/build-pyqt4-into-your-virtualenv/)


```bash
# yum install libpng-devel freetype-devel qt-devel
: browse to http://www.riverbankcomputing.com/software/sip/download
: in your virtual env
$ cd ~/tmp
$ tar xzf sip*tar.gz
$ rm sip*tar.gz
$ cd sip-*
$ python configure.py --incdir=${VIRTUAL_ENV}/include
$ make install
$ cd ..
$ make
$ rm -rf sip*[0-9]

: Qt
$ http://download.qt.io/official_releases/qt
$ http://download.qt.io/official_releases/qt/4.8/4.8.6/qt-everywhere-opensource-src-4.8.6.tar.gz
$ tar xzf qt-everywhere-opensource-src-4.8.6.tar.gz
$ rm qt-everywhere-opensource-src-4.8.6.tar.gz
$ cd qt-everywhere-opensource-src-4.8.6
$ ./configure -opensource -confirm-license -prefix "$VIRTUAL_ENV" -prefix-install -nomake 'tests examples demos docs translations' -no-multimedia -no-webkit -no-javascript-jit -no-phonon -no-xmlpatterns -system-sqlite -no-script -no-svg -no-scripttools -no-qt3support
$ gmake
$ gmake install
$ cd ..

: browse to http://www.riverbankcomputing.com/software/pyqt/download
$ tar xzf PyQt-x11*tar.gz
$ rm PyQt-x11*tar.gz
$ cd PyQt-x11-*
$ python configure.py -g -q /usr/bin/qmake-qt4
$ make
$ make install

```
