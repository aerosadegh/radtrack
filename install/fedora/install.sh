#!/bin/sh
set -e
umask 022
cfg=/cfg
chmod -R a+rX /cfg

yum --quiet --assumeyes install $(cat /cfg/yum-install.list)
curl -s -L https://depot.radiasoft.org/foss/install-as-root.sh | bash

sh /cfg/install-root.sh

exec_user=vagrant
id -u $exec_user &>/dev/null || useradd --create-home $exec_user
su --login $exec_user --command="sh /cfg/install-exec-user.sh"
