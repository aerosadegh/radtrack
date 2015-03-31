#!/bin/sh
if [ Darwin != "$(uname)" ]; then
    echo 'Unsupported system. We only support Mac OS X at this time' 1>&2
    exit 1
fi

echo 'Installing RadTrack...'

yes_or_no() {
    local response
    read -r -p "$1? [y/N] " response
    case $response in
        [yY][eE][sS]|[yY])
            true
            ;;
        *)
            false
            ;;
    esac
}

if [ -f Vagrantfile -o -d .vagrant ]; then
    if [ -f .vagrant/machines/default/virtualbox/index_uuid ]; then
        if yes_or_no 'Destroy existing VM'; then
            vagrant destroy
        else
            echo 'Destroy vm first or create a new directory' 1>&2
            exit 1
        fi
    fi
    rm -rf Vagrantfile .vagrant
fi

rm -f radtrack

if [ ! -z "$(ls -A)" ]; then
    echo 'Current directory is not empty. Please create a new directory,'
    echo 'or clear this one. Then you can rerun this command' 1>&2
    exit 1
fi

set -e
if [ ! -d ~/RadTrack ]; then
    mkdir ~/RadTrack
fi
boot_volume=
get_boot_volume() {
    if [ ! -z "$_boot_volume" ]; then
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
install_pkg() {
    local vol="$1"
    local url="$2"
    local dmg="$(basename $url)"
    get_boot_volume
    echo "Downloading and installing $vol..."
    vol="/Volumes/$vol"
    curl -L -O "$url"
    hdiutil mount "$dmg" &> /dev/null
    sudo installer -package "$(echo $vol/*.pkg)" -target "$boot_volume"
    hdiutil unmount "$vol"
    rm -f "$dmg"
}
if [ -z "$(type -p VBoxManage)" ]; then
    echo 'Downloading and installing Vagrant...'
    install_pkg VirtualBox http://download.virtualbox.org/virtualbox/4.3.26/VirtualBox-4.3.26-98988-OSX.dmg 
fi
if [ -z "$(type -p vagrant)" ]; then
    install_pkg Vagrant https://dl.bintray.com/mitchellh/vagrant/vagrant_1.7.2.dmg
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
