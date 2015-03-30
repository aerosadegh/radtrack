#!/bin/sh
version=$(perl -e 'print((`vboxmanage --version` =~ /([\d\.]+)/)[0])')
test "$version" || {
    echo 'virtual box not installed' 1>&2
    exit 1
}
vagrant destroy
rm -f package.box
rm -f Vagrantfile
set -e
vagrant init hansode/fedora-21-server-x86_64
vagrant up
vagrant ssh -c "sudo sh /vagrant/guest-update.sh $version"
vagrant reload
vagrant ssh -c 'sudo sh /vagrant/install-vagrant.sh'
vagrant halt
vagrant package --output package.box
vagrant box add biviosoftware/radtrack package.box
echo 'Go to https://atlas.hashicorp.com/biviosoftware/boxes/radtrack/versions/new'
echo 'Use github version in log'
echo 'provider: virtualbox'
echo 'Upload "package.box" from this directory'
