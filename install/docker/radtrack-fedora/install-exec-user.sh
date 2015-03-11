#!/bin/sh
set -e
cat >> /root/.bashrc <<EOF
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi
export PS1='\$ '
EOF
