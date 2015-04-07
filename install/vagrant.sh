#!/bin/bash
if [ Darwin != "$(uname)" ]; then
    echo 'Unsupported system. We only support Mac OS X at this time.' 1>&2
    exit 1
fi

echo 'Installing RadTrack...'
set -e
err_trap() {
    local e=$?
    if [ 0 != "$e" ]; then
        trap - EXIT ERR
        echo "INSTALLATION FAILED: Please contact support@radtrack.net" 1>&3
    fi
    exit $e
}
trap err_trap EXIT ERR
shopt -s nullglob

# Separate directory
vm_dir="$(echo ~/RadTrack/.vm)"
if [ ! -d  "$vm_dir" ]; then
    mkdir -p "$vm_dir"
fi
cd $vm_dir

with_log() {
    {
        echo "$(date) $@"
        "$@"
    } >> vagrant.log 2>&1
}
with_log="$(type with_log | tail +2)"

# install 
boot_volume=
get_boot_volume() {
    if [ -n "$_boot_volume" ]; then
        return
    fi
    for f in /Volumes/*; do
        if diskutil info "$f" 2>&1 | egrep -s -q 'Mount Point: +/$'; then
            boot_volume="$f"
            return
        fi
    done
    echo 'Unable to find boot volume for install' 1>&2
    exit 1
}
first_sudo=true
install_pkg() {
    local pkg="$1"
    local dmg="$pkg.dmg"
    local url="https://depot.radiasoft.org/foss/$dmg"
    get_boot_volume
    echo "Downloading $pkg... (speed depends on Internet connection)"
    # Needed for XQuartz which mounts dmg at XQuartz-<version>
    vol="$(echo /Volumes/$pkg*)"
    if [ -n "$vol" ]; then
        with_log hdiutil unmount "$vol"
    fi
    rm -f "$dmg"
    with_log curl -L -O -s "$url" 
    with_log hdiutil mount "$dmg"
    vol="$(echo /Volumes/$pkg*)"
    echo "Installing $pkg... (may take a minute or two)"
    if $first_sudo; then
        echo 'Please enter your Mac login password when prompted.'
        first_sudo=false
    fi
    with_log sudo installer -package "$(echo $vol/*.pkg)" -target "$boot_volume"
    with_log hdiutil unmount "$vol"
    rm -f "$dmg"
}
echo 'Checking for 3rd party packages to install...'
if [ ! -d /Applications/Utilities/XQuartz.app ]; then
    install_pkg XQuartz
fi
if [ -z "$(type -p VBoxManage)" ]; then
    install_pkg VirtualBox
fi
if [ -z "$(type -p vagrant)" ]; then
    install_pkg Vagrant
fi

# Vagrant destroy
echo 'Destroying old virtual machine...'
with_log perl -w <<'EOF'
use strict;
foreach my $line (`vagrant global-status --prune 2>&1`) {
    next
        unless $line =~ m{default +virtualbox +\w+ +(/.+)}
        && -d $1;
    chdir($1) || die("$1: unable to go to directory\n");
    next
        unless open(IN, 'Vagrantfile')
        && <IN> =~ m{vm.box.*biviosoftware/radtrack};
    system('vagrant destroy --force');
    system('rm -rf .vagrant Vagrantfile');
}
EOF

# Vagrant install
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
if vagrant box list 2>&1 | grep -s -q biviosoftware/radtrack; then
    echo 'Checking virtual machine update... (may take an hour if out of date)'
    with_log vagrant box update
else
    echo 'Downloading virtual machine... (may take an hour)'
    with_log vagrant box add https://atlas.hashicorp.com/biviosoftware/boxes/radtrack
fi
echo 'Starting virtual machine... (may take several minutes)'
with_log vagrant up

# radtrack command
rm -f radtrack
cat > radtrack <<EOF
#!/bin/sh
echo 'Starting radtrack... (may take a few seconds)'
cd $vm_dir
$with_log
if ! vagrant status 2>&1 | grep -s -q default.*running; then
    echo 'Starting virtual machine... (may take a minute)'
    with_log vagrant up
fi
with_log exec vagrant ssh -c 'radtrack --beta-test'
EOF
chmod +x radtrack
source_bashrc=false
if [ -z "$(bash -l -c 'type -t radtrack')" ]; then
    source_bashrc=true
    echo 'radtrack() { ~/RadTrack/.vm/radtrack; }' >> ~/.bashrc
fi
if $source_bashrc; then
    echo 'Before you start radtrack, you will need to:'
    echo '. ~/.bashrc'
fi
echo 'To run radtrack:'
echo 'radtrack'

