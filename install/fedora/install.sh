#!/bin/sh
set -e
umask 022
cfg=/cfg
chmod -R a+rX /cfg

if /sbin/lsmod | grep -i -s -q vbox; then
    dd if=/dev/zero of=/swap bs=1M count=1024
    mkswap /swap
    chmod 600 /swap
    swapon /swap
    echo '/swap none swap sw 0 0' >> /etc/fstab
    perl -pi -e 's{^(X11Forwarding) no}{$1 yes}' /etc/ssh/sshd_config
    systemctl restart sshd.service
fi

yum --quiet --assumeyes install $(cat /cfg/yum-install.list)
curl -s -L https://raw.githubusercontent.com/radiasoft/foss-mirror/master/install-as-root.sh | bash

sh /cfg/install-root.sh

exec_user=vagrant
id -u $exec_user &>/dev/null || useradd --create-home $exec_user
su --login $exec_user --command="sh /cfg/install-exec-user.sh"