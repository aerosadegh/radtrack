#!/bin/sh
umask 022
rpm --quiet --install https://raw.githubusercontent.com/radiasoft/foss-mirror/master/elegant-26.0.2-1.rhel.6.5.openmpi.x86_64.rpm
rpm --quiet --install https://raw.githubusercontent.com/radiasoft/foss-mirror/master/openmpi-1.8.4-1.x86_64.rpm
yum --quiet --assumeyes install gcc
