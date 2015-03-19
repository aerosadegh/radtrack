#!/bin/sh
set -e
umask 022
cfg=/cfg
chmod -R a+rX /cfg

/sbin/lsmod | grep -i -s -q vbox
if [ $? == 0 -a ! -f /swap ]; then
    dd if=/dev/zero of=/swap bs=1M count=1024
    mkswap /swap
    chmod 600 /swap
    swapon /swap
    echo '/swap none swap sw 0 0' >> /etc/fstab
fi

yum --quiet --assumeyes install $(cat /cfg/yum-install.list)
curl -s -L https://raw.githubusercontent.com/radiasoft/foss-mirror/master/install-as-root.sh | bash

sh /cfg/install-root.sh

exec_user=vagrant
id -u $exec_user &>/dev/null || useradd --create-home $exec_user
su --login $exec_user --command="sh /cfg/install-exec-user.sh"
