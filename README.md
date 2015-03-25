### RadTrack

RadTrack is an open source framework for working with codes that model particle dynamics and electromagnetic radiation.

#### Setting Up Development

This script should set up a development environment. It's written in Unix
terms, but should be translatable to Windows:

```bash
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
```
