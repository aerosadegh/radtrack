#!/bin/sh
if [ "x$(id -u)" != x0 ]; then
    echo 'Must be run as root' 1>&2
    exit 1
fi
rpm -U http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
yum -y install docker-io
chkconfig --add docker
service docker start
