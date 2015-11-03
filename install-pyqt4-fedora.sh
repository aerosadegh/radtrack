#!/bin/bash
set -e
if [[ $(pyenv version) =~ ^system ]]; then
    echo 'please activate a pyenv' 1>&2
    exit 1
fi
qt=
qmake=

bin_dir=$(dirname "$(pyenv which python)")
for qt in "$bin_dir" /usr/local/qt-4.* /opt/local /usr/lib64/qt4; do
    qmake=$qt/bin/qmake
    if [[ -x $qmake ]]; then
        break
    fi
done
if [[ ! $qmake ]]; then
    echo 'qmake not found. Need for PyQt4.' 1>&2
    exit 1
fi

set -e
build_qt_pkg() {
    local tgz=$1.tar.gz
    shift
    # Put tmp local to user
    local tmp=~/tmp/build_qt_pkg
    trap "cd; rm -rf '$tmp'" EXIT
    rm -rf "$tmp"
    mkdir -p "$tmp"
    cd "$tmp"
    curl -s -S -L -O https://depot.radiasoft.org/foss/"$tgz"
    tar xzf "$tgz"
    rm -f "$tgz"
    cd *
    # Need to see if static is required
    python configure.py "$@"
    make
    # You will see this, which apparently doesn't matter:
    # install: cannot create regular file
    #   ‘/usr/lib64/qt4/plugins/designer/libpyqt4.so’: Permission denied
    # make[1]: [install_target] Error 1 (ignored)
    make install
}

need_install() {
    local p=$1
    if python -c "import $p" 2>/dev/null; then
        return 1
    fi
    return 0
}

if need_install sip 1; then
    build_qt_pkg sip --incdir="$(dirname "$bin_dir")/include"
fi

if need_install PyQt4; then
    build_qt_pkg PyQt4 --confirm-license -q "$qmake"
fi
