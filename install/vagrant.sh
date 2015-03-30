#!/bin/sh
if [ -f Vagrantfile -o -d .vagrant ]; then
    echo 'remove Vagrantfile and .vagrant in this directory' 1>&2
    if [ -f .vagrant/machines/default/virtualbox/index_uuid ]; then
        echo 'Destroy vm first:' 1>&2
        echo "vagrant destroy $(cat .vagrant/machines/default/virtualbox/index_uuid)" 1>&2
    fi
    exit 1
fi
if [ ! -z "$(ls -A)" ]; then
    echo 'Current directory must be empty. Create a new directory and rerun this command' 1>&2
    exit 1
fi
set -e
if [ ! -d ~/RadTrack ]; then
    mkdir ~/RadTrack
fi
cat > Vagrantfile <<'EOF'
# -*- mode: ruby -*-
# vi: set ft=ruby :
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "biviosoftware/radtrack"
  config.vm.hostname = "radtrack"
  config.ssh.forward_x11 = true
  config.vm.synced_folder ENV["HOME"] + "/RadTrack", "/home/vagrant/RadTrack"
end
EOF
cat > radtrack <<EOF
#!/bin/sh
echo 'Starting radtrack... (may take a few seconds)'
vagrant ssh -c radtrack
EOF
chmod +x radtrack
if vagrant box list | grep -s -q biviosoftware/radtrack; then
    vagrant box update
fi
vagrant up
echo 'To start radtrack, run:'
echo './radtrack'
