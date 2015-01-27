#!/bin/sh
chmod -R a+rX /cfg
groupadd --gid 500 vagrant
useradd vagrant --uid 500 --gid vagrant --create-home
cd /root
sh /cfg/install.sh
