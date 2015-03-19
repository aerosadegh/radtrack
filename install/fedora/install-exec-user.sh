#!/bin/sh
#### set -e
# /tmp may be small
export TEMP=/var/tmp
curl -s -L https://raw.githubusercontent.com/biviosoftware/home-env/master/install.sh | bash
(
    set +e
    . ~/.bashrc
    b_install_pyenv 2
    exit 0
)
cat > ~/.post.bashrc << 'EOF'
py2
EOF
. ~/.bashrc
curl -s -L https://raw.githubusercontent.com/radiasoft/foss-mirror/master/install-as-user.sh | bash
cd ~/src/biviosoftware
git clone -q https://github.com/biviosoftware/pybivio
cd pybivio
pip install -e .
mkdir -p ~/src/radiasoft
cd ~/src/radiasoft
git clone -q https://github.com/radiasoft/radtrack
cd radtrack
# Need to do this first, or scipy complains with:
#   ImportError: No module named numpy.distutils.core
pip install numpy
pip install -e .
